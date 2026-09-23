#!/usr/bin/env python3
"""Background worker for the cockpit: Claude sign-ins and isolated extraction runs.

Runs as `ledger-worker.service`. It polls the jobs table in the workspace database,
starts `run_model.py` for queued extractions (at most 4 at once, 2 per user) with the
starting user's own token, checks each finished workbook outside the sandbox and imports
it as an immutable version. Connect jobs drive `claude setup-token` in a pseudo-terminal
so a user can sign in from the Settings page. Runner processes live in their own session,
so they survive a worker restart; a restarted worker reattaches to them by pid.

    python3 _dev/tools/cockpit/worker.py            # run forever
    python3 _dev/tools/cockpit/worker.py --once     # one pass (tests)
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pty
import re
import select
import shutil
import signal
import sqlite3
import struct
import subprocess
import sys
import tempfile
import termios
import threading
import time
import fcntl
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cockpit import data, runs, trace  # noqa: E402
from cockpit.workspace import _now  # noqa: E402

REPO = HERE.parents[2]
RUNNER = Path(os.environ.get("COCKPIT_RUNNER") or HERE.parent / "sandbox/run_model.py")
CHECKER = HERE.parent / "check_lean.py"
CLAUDE = os.environ.get("COCKPIT_CLAUDE_BIN") or shutil.which("claude") or "claude"
INSTRUCTION = REPO / "SEC_Deal_Ledger_Extraction_Instruction.md"
LINK_RE = re.compile(r"https://claude\.com/cai/oauth/authorize\S+")
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\x1b[()][A-Za-z0-9]|\x1b[=>]")
CLAUDE_ERROR_RE = re.compile(r"(OAuth error:.*?)(?:Press Enter|$)", re.S)
CONNECT_TIMEOUT = 10 * 60
TERMINAL = {"completed", "failed", "timed_out", "cancelled"}


def log(message: str) -> None:
    print(f"{_now()} {message}", flush=True)


def instruction_version(path: Path = INSTRUCTION) -> str | None:
    found = re.search(r"\bv(\d+\.\d+(?:\.\d+)?)\b", path.read_text(encoding="utf-8")[:600])
    return f"v{found.group(1)}" if found else None


def alive(pid: int | None, run_dir: str | None) -> bool:
    """True while `pid` is still this job's runner. After a reboot the pid may belong to something else."""
    if not pid:
        return False
    try:
        if Path(f"/proc/{pid}/stat").read_text().split(")")[-1].split()[0] == "Z":
            return False  # a zombie child counts as finished
        command = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
    except OSError:
        return False
    return bool(run_dir) and run_dir.encode() in command


class Worker:
    def __init__(self, repo: Path = REPO):
        self.cockpit = data.Cockpit(repo)
        self.workspace = self.cockpit.workspace
        self.repo = repo
        self.children: dict[str, subprocess.Popen] = {}
        self.signalled: set[str] = set()
        self.connects: dict[str, threading.Thread] = {}

    # ---- database helpers -------------------------------------------------------

    def connect(self) -> sqlite3.Connection:
        conn = self.workspace._connect(write=True)
        assert conn is not None
        return conn

    def update(self, job_id: str, **fields: Any) -> None:
        if not fields:
            return
        conn = self.connect()
        try:
            conn.execute(f"UPDATE jobs SET {', '.join(f'{key}=?' for key in fields)} WHERE id=?", (*fields.values(), job_id))
            conn.commit()
        finally:
            conn.close()

    def jobs(self, where: str, params: tuple = ()) -> list[sqlite3.Row]:
        conn = self.connect()
        try:
            return conn.execute(f"SELECT * FROM jobs WHERE {where} ORDER BY created_at, rowid", params).fetchall()
        finally:
            conn.close()

    def job(self, job_id: str) -> sqlite3.Row:
        return self.jobs("id=?", (job_id,))[0]

    # ---- main loop ----------------------------------------------------------------

    def recover(self) -> None:
        """After a restart: jobs cut off between steps are finished or failed."""
        for job in self.jobs("kind='extract' AND state IN ('preparing')"):
            self.fail(job, "worker_restart", "The worker restarted while preparing this run.")
        for job in self.jobs("kind='extract' AND state IN ('checking','importing')"):
            self.guarded(job, self.finish)
        for job in self.jobs("kind='connect_claude' AND (state IN ('waiting_for_code','completing') OR (state='queued' AND started_at IS NOT NULL))"):
            self.update(job["id"], state="failed", input=None, error="Interrupted by a server restart; connect again.", ended_at=_now())

    def guarded(self, job: sqlite3.Row, step) -> Any:
        """Run one job's step; an unexpected error fails that job instead of stopping every later job."""
        try:
            return step(job)
        except Exception as exc:  # noqa: BLE001
            log(f"extraction {job['id']}: {step.__name__} failed: {type(exc).__name__}: {exc}")
            current = self.job(job["id"])
            if current["state"] in TERMINAL:
                return False
            self.keep_receipts(current, Path(current["run_dir"]) if current["run_dir"] else None)
            self.fail(current, "worker_error", f"{type(exc).__name__}: {exc}"[:500])
            return False

    def tick(self) -> None:
        for job in self.jobs("kind='extract' AND state='running'"):
            child = self.children.get(job["id"])
            finished = child.poll() is not None if child else not alive(job["pid"], job["run_dir"])
            if job["cancel_requested"] and not finished and job["id"] not in self.signalled:
                try:
                    os.kill(job["pid"], signal.SIGTERM)
                except ProcessLookupError:
                    pass
                self.signalled.add(job["id"])
            if finished:
                self.children.pop(job["id"], None)
                self.guarded(job, self.finish)
        for job in self.jobs("kind='extract' AND state='queued' AND cancel_requested=1"):
            self.update(job["id"], state="cancelled", failure_reason="cancelled", ended_at=_now())
            self.activity(job, "extraction_failed", "Extraction cancelled before it started")
        running = self.jobs("kind='extract' AND state='running'")
        for job in self.jobs("kind='extract' AND state='queued' AND cancel_requested=0"):
            mine = sum(1 for other in running if other["actor"] == job["actor"])
            if len(running) >= runs.CAPS["total"] or mine >= runs.CAPS["per_user"]:
                continue
            if self.guarded(job, self.start):
                running = self.jobs("kind='extract' AND state='running'")
        for job in self.jobs("kind='connect_claude' AND state='queued' AND started_at IS NULL"):
            if job["cancel_requested"]:
                self.update(job["id"], state="cancelled", ended_at=_now())
                continue
            thread = threading.Thread(target=self.sign_in, args=(job["id"], job["actor"]), daemon=True)
            self.update(job["id"], started_at=_now())
            self.connects[job["id"]] = thread
            thread.start()

    # ---- extraction ---------------------------------------------------------------

    def start(self, job: sqlite3.Row) -> bool:
        params = json.loads(job["params"])
        token = runs.token_path(job["actor"])
        if not token.is_file():
            self.fail(job, "not_connected", "No Claude account is connected for this user.")
            return False
        try:
            _, filing, _ = self.cockpit.resolve(job["slug"])
        except data.DealNotFound:
            self.fail(job, "unknown_deal", "The deal's filing is not available.")
            return False
        run_dir = self.repo / "_dev/runs" / f"cockpit-{job['id']}"
        conn = self.connect()
        try:  # claim the job, so a second worker cannot start it too
            claimed = conn.execute("UPDATE jobs SET state='preparing', started_at=?, run_dir=? WHERE id=? AND state='queued' AND cancel_requested=0", (_now(), str(run_dir), job["id"])).rowcount
            conn.commit()
        finally:
            conn.close()
        if not claimed:
            return False
        prepare = subprocess.run([sys.executable, str(RUNNER), "prepare", "--provider", "opus", "--run-dir", str(run_dir),
                                  "--deal", job["slug"], "--filing", filing.name, "--model", params["model"],
                                  "--effort", params["effort"], "--timeout-minutes", str(params["timeout_minutes"])],
                                 cwd=self.repo, capture_output=True, text=True)
        if prepare.returncode != 0:
            self.fail(self.job(job["id"]), "prepare_failed", (prepare.stderr or prepare.stdout).strip()[-500:])
            return False
        environment = {**os.environ, "SEC_CLAUDE_OAUTH_TOKEN_FILE": str(token)}
        with (run_dir / "cockpit-worker.log").open("ab") as output:
            child = subprocess.Popen([sys.executable, str(RUNNER), "worker", "--provider", "opus", "--run-dir", str(run_dir)],
                                     cwd=self.repo, env=environment, stdin=subprocess.DEVNULL, stdout=output, stderr=output,
                                     start_new_session=True, close_fds=True)
        self.children[job["id"]] = child
        self.update(job["id"], state="running", pid=child.pid)
        log(f"started extraction {job['id']} for {job['slug']} by {job['actor']} (pid {child.pid})")
        return True

    def finish(self, job: sqlite3.Row) -> None:
        run_dir = Path(job["run_dir"]) if job["run_dir"] else None
        status_path = run_dir / "status.json" if run_dir else None
        status = json.loads(status_path.read_text()) if status_path and status_path.is_file() else {}
        if status.get("plan_usage"):
            self.plan_usage(job["actor"], status["plan_usage"])
        result = {key: status.get(key) for key in ("usage", "plan_usage", "continuations", "elapsed_seconds", "usage_limit_resets_at") if status.get(key) is not None}
        state = status.get("state")
        if state != "completed":
            reason = status.get("failure_reason") or ("worker_restart" if state in (None, "running") else state)
            if state in (None, "running"):
                error = "The run stopped without recording an outcome."
            else:
                error = status.get("error")
            final = "cancelled" if job["cancel_requested"] else state if state in ("timed_out", "cancelled") else "failed"
            reason = "cancelled" if final == "cancelled" else reason
            self.keep_receipts(job, run_dir)
            self.update(job["id"], state=final, failure_reason=reason, error=error, result=json.dumps(result), ended_at=_now())
            self.activity(job, "extraction_failed", self.describe(job, f"extraction {'cancelled' if final == 'cancelled' else 'failed'} ({reason})"))
            log(f"extraction {job['id']} ended: {final} / {reason}")
            return
        self.update(job["id"], state="checking")
        workbook = run_dir / "extraction" / f"{job['slug']}.xlsx"
        _, filing, _ = self.cockpit.resolve(job["slug"])
        check_path = run_dir / "check.json"
        check = subprocess.run([sys.executable, str(CHECKER), "--workbook", str(workbook), "--filing", str(filing), "--output", str(check_path)],
                               cwd=self.repo, capture_output=True, text=True)
        if check.returncode not in (0, 1) or not check_path.is_file():
            self.keep_receipts(job, run_dir)
            self.update(job["id"], state="failed", failure_reason="checker_error", error=(check.stderr or check.stdout).strip()[-500:], result=json.dumps(result), ended_at=_now())
            self.activity(job, "extraction_failed", self.describe(job, "extraction could not be checked"))
            return
        summary = json.loads(check_path.read_text()).get("summary") or {}
        checker = {"errors": summary.get("errors", 0), "warnings": summary.get("warnings", 0)}
        result["checker"] = checker
        self.update(job["id"], state="importing", result=json.dumps(result))
        version_id = self.import_version(job, run_dir, workbook, status, checker)
        self.activity(job, "extraction", self.describe(job, f"extraction finished: {checker['errors']} errors, {checker['warnings']} warnings"), version_id)
        shutil.rmtree(run_dir, ignore_errors=True)
        log(f"extraction {job['id']} imported as {version_id}")

    def describe(self, job: sqlite3.Row, what: str) -> str:
        params = json.loads(job["params"])
        return f"{params.get('engine', runs.ENGINE)} · {params.get('effort')} · {instruction_version() or 'instruction'} {what}"

    def import_version(self, job: sqlite3.Row, run_dir: Path, workbook: Path, status: dict[str, Any], checker: dict[str, int]) -> str:
        metadata = json.loads((run_dir / "metadata.json").read_text())
        digest = hashlib.sha256(workbook.read_bytes()).hexdigest()
        started = dt.datetime.fromisoformat(status.get("started_at") or job["started_at"])
        version_id = f"opus55-{metadata['effort']}-{started:%Y%m%d-%H%M}-{digest[:6]}"
        destination = self.repo / "_dev/cockpit/state/versions" / job["slug"] / version_id
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(workbook, destination / f"{job['slug']}.xlsx")
        for name in ("metadata.json", "command.json", "status.json", "validation.json", "provider-results.json", "prompt.txt", "check.json"):
            if (run_dir / name).is_file():
                shutil.copy2(run_dir / name, destination / name)
        version = instruction_version()
        name = runs.NAMES.get(job["actor"], job["actor"])
        label = f"{runs.ENGINE} · {metadata['effort']} · {version or 'instruction ' + metadata['instruction_sha256'][:7]} — {name}, {started:%-d %b %H:%M}"
        conn = self.connect()
        try:  # the version row and the job's completion land together; a retry after a crash replaces the row
            conn.execute("INSERT OR REPLACE INTO versions (slug, id, label, path, sha256, kind, engine, model, effort, instruction_version, instruction_sha256, filing_sha256, started_by, started_at, finished_at, receipts, checker) VALUES (?,?,?,?,?,'raw',?,?,?,?,?,?,?,?,?,?,?)",
                         (job["slug"], version_id, label, str((destination / f"{job['slug']}.xlsx").relative_to(self.repo)), digest, runs.ENGINE,
                          metadata["model"], metadata["effort"], version, metadata["instruction_sha256"], metadata["filing_sha256"], job["actor"],
                          status.get("started_at") or job["started_at"], status.get("ended_at") or _now(), str(destination.relative_to(self.repo)), json.dumps(checker)))
            conn.execute("UPDATE jobs SET state='completed', version_id=?, ended_at=? WHERE id=?", (version_id, _now(), job["id"]))
            conn.commit()
        finally:
            conn.close()
        return version_id

    def keep_receipts(self, job: sqlite3.Row, run_dir: Path | None) -> None:
        if not run_dir or not run_dir.is_dir():
            return
        destination = self.repo / "_dev/cockpit/state/jobs" / job["id"]
        destination.mkdir(parents=True, exist_ok=True)
        for name in ("metadata.json", "command.json", "status.json", "validation.json", "provider-results.json", "stderr.log", "cockpit-worker.log"):
            if (run_dir / name).is_file():
                shutil.copy2(run_dir / name, destination / name)
        shutil.rmtree(run_dir, ignore_errors=True)

    def fail(self, job: sqlite3.Row, reason: str, error: str) -> None:
        self.update(job["id"], state="failed", failure_reason=reason, error=error, ended_at=_now())
        self.activity(job, "extraction_failed", self.describe(job, f"extraction failed ({reason})"))
        log(f"extraction {job['id']} failed: {reason}")

    def activity(self, job: sqlite3.Row, kind: str, summary: str, version_id: str | None = None) -> None:
        conn = self.connect()
        try:
            trace._activity(conn, job["slug"], job["actor"], kind, summary=summary, version_id=version_id)
            conn.commit()
        finally:
            conn.close()

    def plan_usage(self, user: str, info: dict[str, Any]) -> None:
        conn = self.connect()
        try:
            conn.execute("INSERT INTO plan_usage VALUES (?, 'claude', ?, ?) ON CONFLICT(user, provider) DO UPDATE SET at=excluded.at, info=excluded.info", (user, _now(), json.dumps(info)))
            conn.commit()
        finally:
            conn.close()

    # ---- Claude sign-in -------------------------------------------------------------

    def sign_in(self, job_id: str, user: str) -> None:
        """Drive `claude setup-token`: publish its link, feed the pasted code, save the token."""
        home = Path(tempfile.mkdtemp(prefix="cockpit-signin-"))
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 50, 500, 0, 0))
        process = None
        try:
            process = subprocess.Popen([CLAUDE, "setup-token"], stdin=slave, stdout=slave, stderr=slave, cwd=home, start_new_session=True, close_fds=True,
                                       env={"HOME": str(home), "PATH": os.environ.get("PATH", ""), "TERM": "xterm-256color", "BROWSER": "/bin/false"})
            os.close(slave)
            slave = -1
            output = ""
            deadline = time.monotonic() + CONNECT_TIMEOUT

            def read(seconds: float) -> bool:
                nonlocal output
                ready, _, _ = select.select([master], [], [], seconds)
                if not ready:
                    return True
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    return False
                if not chunk:
                    return False
                output = ANSI_RE.sub("", output + chunk.decode("utf-8", "replace"))
                return True

            link = None
            while link is None:
                if time.monotonic() > deadline or self.job(job_id)["cancel_requested"]:
                    raise TimeoutError("cancelled" if self.job(job_id)["cancel_requested"] else "Claude did not offer a sign-in link.")
                if not read(0.5) and process.poll() is not None:
                    raise RuntimeError("Claude exited before offering a sign-in link.")
                found = LINK_RE.search(output)
                if found and "Paste" in output[found.end():]:
                    link = found.group(0)
            self.update(job_id, state="waiting_for_code", result=json.dumps({"link": link}))
            while True:
                job = self.job(job_id)
                if job["cancel_requested"]:
                    raise TimeoutError("cancelled")
                if job["input"]:
                    code = job["input"]
                    break
                if time.monotonic() > deadline:
                    raise TimeoutError("No code was entered within ten minutes.")
                read(1.0)
            self.update(job_id, state="completing", input=None)
            output_before = len(output)
            # Claude's input reads a multi-character write as a paste, so an Enter in the same
            # write never submits. Let the pasted code settle, then press Enter on its own.
            os.write(master, code.encode())
            read(0.5)
            os.write(master, b"\r")
            finish = time.monotonic() + 90
            token = None
            refused = None
            while token is None and refused is None and time.monotonic() < finish:
                if not read(0.5) and process.poll() is not None:
                    break
                after = output[output_before:]
                found = runs.TOKEN_RE.search(after)
                if found:
                    token = found.group(0)
                elif "Press Enter to retry" in after:
                    message = CLAUDE_ERROR_RE.search(after)
                    refused = " ".join(message.group(1).split()) if message else "an error"
            if token is None:
                tail = " ".join(runs.TOKEN_RE.sub("[token]", output[output_before:]).replace(code, "[code]").split())[-400:]
                log(f"sign-in {job_id} for {user}: no token; Claude printed: {tail!r}")
                raise RuntimeError(f"Claude refused the code ({refused or 'no token returned'}). Codes expire within minutes and must be copied whole; connect again and paste the new code.")
            runs.save_token(user, token)
            conn = self.connect()
            try:
                runs.connected(conn, user)
                conn.execute("UPDATE jobs SET state='completed', ended_at=?, error=NULL WHERE id=?", (_now(), job_id))
                conn.commit()
            finally:
                conn.close()
            log(f"Claude account connected for {user}")
        except TimeoutError as exc:
            cancelled = str(exc) == "cancelled"
            self.update(job_id, state="cancelled" if cancelled else "failed", input=None, error=None if cancelled else str(exc), ended_at=_now())
        except Exception as exc:  # noqa: BLE001 - report every sign-in failure to the page
            self.update(job_id, state="failed", input=None, error=str(exc) or type(exc).__name__, ended_at=_now())
        finally:
            if process and process.poll() is None:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            for descriptor in (master, slave):
                if descriptor >= 0:
                    try:
                        os.close(descriptor)
                    except OSError:
                        pass
            shutil.rmtree(home, ignore_errors=True)
            self.connects.pop(job_id, None)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--once", action="store_true", help="run one pass and exit")
    parser.add_argument("--interval", type=float, default=2.0)
    args = parser.parse_args(argv)
    worker = Worker()
    worker.workspace.db_path.parent.mkdir(parents=True, exist_ok=True)
    lock = open(worker.workspace.db_path.parent / "worker.lock", "a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log("another cockpit worker is running; exiting")
        return 0
    try:
        worker.recover()
    except Exception as exc:  # noqa: BLE001
        log(f"recovery failed: {type(exc).__name__}: {exc}")
    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    log("cockpit worker started")
    while True:
        try:
            worker.tick()
        except Exception as exc:  # noqa: BLE001 - one bad pass must not stop the service
            log(f"worker pass failed: {type(exc).__name__}: {exc}")
        if args.once or stop.wait(args.interval):
            break
    log("cockpit worker stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
