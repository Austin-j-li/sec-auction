#!/usr/bin/env python3
"""Prepare, launch, and monitor isolated Sol/Opus extraction runs."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time


BASE = Path(__file__).resolve().parent
PROJECT = BASE.parents[2]
HOME_HOST = Path.home()
SANDBOX_HOME = Path("/home/uctpiaj")
WORK = SANDBOX_HOME / "work"
INSTRUCTION_NAME = "SEC_Deal_Ledger_Extraction_Instruction.md"
CODEX_BIN = Path(os.environ.get("SEC_CODEX_BIN") or shutil.which("codex") or "/missing/codex").resolve()
CODEX_RELEASE = CODEX_BIN.parent.parent
CLAUDE_BIN = Path(os.environ.get("SEC_CLAUDE_BIN") or shutil.which("claude") or "/missing/claude").resolve()
CODEX_SANDBOX = Path("/opt/codex")
CLAUDE_SANDBOX = Path("/opt/claude")
MINIFORGE = HOME_HOST / "miniforge3"  # Ubuntu laptop; absent on the VM, where system Python is used
import openpyxl as _openpyxl
PYLIB_HOST = Path(_openpyxl.__file__).resolve().parents[1]  # site-packages that holds openpyxl
PYLIB = Path("/opt/pylib")
REPORT_NAME = "checker_report.md"
TIMEOUT_SECONDS = 90 * 60
RUNS = PROJECT / "_dev" / "runs"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def prepare(args: argparse.Namespace) -> None:
    if bool(args.revise_from) != bool(args.report):
        raise SystemExit("--revise-from and --report must be supplied together")
    if Path(args.filing).name != args.filing or Path(args.deal).name != args.deal or args.deal in ("", ".", ".."):
        raise SystemExit("--filing and --deal must be bare names, not paths")
    if args.revise_from and (not Path(args.revise_from).is_file() or not Path(args.report).is_file()):
        raise SystemExit("revision workbook or findings report is missing")
    run_dir = Path(args.run_dir).resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        raise SystemExit(f"refusing to overwrite non-empty run directory: {run_dir}")
    instruction_src = PROJECT / INSTRUCTION_NAME
    filing_src = PROJECT / "raw_filing" / args.filing
    if not instruction_src.is_file() or not filing_src.is_file():
        raise SystemExit("instruction or filing source is missing")

    input_dir = run_dir / "input"
    raw_dir = input_dir / "raw_filing"
    output_dir = run_dir / "extraction"
    raw_dir.mkdir(parents=True)
    output_dir.mkdir()
    shutil.copy2(instruction_src, input_dir / INSTRUCTION_NAME)
    shutil.copy2(filing_src, raw_dir / args.filing)

    prompt = (
        f"Read {INSTRUCTION_NAME} in this folder and follow it. "
        f"Extract the deal whose filing is in raw_filing/ and save the finished workbook "
        f"in extraction/ as {args.deal}.xlsx. Work only from this instruction and this filing."
    )
    if args.revise_from:
        # Revision pass: the agent starts from a finished workbook and the checker's findings on it.
        shutil.copy2(args.revise_from, output_dir / f"{args.deal}.xlsx")
        shutil.copy2(args.report, input_dir / REPORT_NAME)
        prompt = (
            f"extraction/{args.deal}.xlsx is a finished ledger for the filing in raw_filing/, made by following "
            f"{INSTRUCTION_NAME} in this folder. {REPORT_NAME} lists what an automatic checker found in it. "
            f"Read the instruction, then go through the findings one by one against the filing. Mechanical errors "
            f"identify failed checks. Mechanical review leads are warnings, not necessarily errors; do not discard "
            f"required evidence just to silence one. Change the workbook only where a "
            f"finding shows a real error under the instruction; do not add rows the instruction would fold into a "
            f"note, and do not change anything no finding points to. Save the revised workbook under the same name, "
            f"and write extraction/revision_notes.md listing each finding, what you decided and why. "
            f"Work only from the instruction, the filing, the workbook and the findings."
        )
    (run_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    metadata = {
        "prepared_at": now_iso(),
        "provider": args.provider,
        "deal": args.deal,
        "filing_name": args.filing,
        "instruction_name": INSTRUCTION_NAME,
        "instruction_sha256": sha256(input_dir / INSTRUCTION_NAME),
        "filing_sha256": sha256(raw_dir / args.filing),
        "prompt_sha256": hashlib.sha256((prompt + "\n").encode()).hexdigest(),
        "expected_output": f"{args.deal}.xlsx",
        "mode": "revise" if args.revise_from else "extract",
        "revised_from_sha256": sha256(Path(args.revise_from)) if args.revise_from else None,
        "model": "gpt-5.6-sol" if args.provider == "sol" else "claude-opus-5",
        "effort": "xhigh" if args.provider == "sol" else "high",
        "timeout_seconds": TIMEOUT_SECONDS,
        "runner_sha256": sha256(Path(__file__)),
        "python_version": sys.version,
        "sandbox": "bubblewrap fresh home/state/tmp; one instruction; one filing; one output directory",
    }
    write_json(run_dir / "metadata.json", metadata)
    print(json.dumps(metadata, sort_keys=True))


def bwrap_base(run_dir: Path, provider: str, state: Path) -> list[str]:
    metadata = prepared_metadata(run_dir, provider)
    instruction = run_dir / "input" / INSTRUCTION_NAME
    filings = list((run_dir / "input" / "raw_filing").glob("*"))
    if len(filings) != 1:
        raise SystemExit(f"expected exactly one filing in {run_dir}")
    filing = filings[0]
    output = run_dir / "extraction"
    h = str(SANDBOX_HOME)
    work = str(WORK)

    command = [
        "bwrap", "--unshare-all", "--share-net", "--die-with-parent", "--new-session", "--clearenv",
        "--ro-bind", "/usr", "/usr",
        "--symlink", "usr/bin", "/bin",
        "--symlink", "usr/sbin", "/sbin",
        "--symlink", "usr/lib", "/lib",
        "--symlink", "usr/lib64", "/lib64",
        "--ro-bind", "/etc/ssl", "/etc/ssl",
        "--ro-bind", "/etc/resolv.conf", "/etc/resolv.conf",
        "--ro-bind", "/etc/hosts", "/etc/hosts",
        "--ro-bind", "/etc/nsswitch.conf", "/etc/nsswitch.conf",
        "--ro-bind", "/etc/alternatives", "/etc/alternatives",
        "--ro-bind", "/etc/passwd", "/etc/passwd",
        "--ro-bind", "/etc/group", "/etc/group",
        "--ro-bind", "/etc/localtime", "/etc/localtime",
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/run",
        "--dir", "/home", "--tmpfs", h,
        "--dir", work,
        "--dir", f"{work}/raw_filing",
        "--dir", f"{work}/extraction",
        "--ro-bind", str(instruction), f"{work}/{INSTRUCTION_NAME}",
        "--ro-bind", str(filing), f"{work}/raw_filing/{filing.name}",
        "--bind", str(output), f"{work}/extraction",
        "--setenv", "HOME", h,
        "--setenv", "USER", "uctpiaj",
        "--setenv", "LANG", "C.UTF-8",
        "--setenv", "TMPDIR", "/tmp",
        "--ro-bind", str(PYLIB_HOST), str(PYLIB),
        "--setenv", "PYTHONPATH", str(PYLIB),
    ]
    for certs in ["/etc/ca-certificates", "/etc/pki", "/etc/crypto-policies"]:  # Debian and Red Hat layouts
        if Path(certs).exists():
            command += ["--ro-bind", certs, certs]
    if MINIFORGE.is_dir():
        command += ["--ro-bind", str(MINIFORGE), str(MINIFORGE), "--setenv", "PATH", f"{MINIFORGE}/bin:/usr/bin:/bin"]
    else:
        command += ["--setenv", "PATH", "/usr/bin:/bin"]
    report = run_dir / "input" / REPORT_NAME
    if metadata.get("mode") == "revise":
        if not report.is_file():
            raise SystemExit(f"revision findings are missing: {report}")
        command += ["--ro-bind", str(report), f"{work}/{REPORT_NAME}"]

    if provider == "sol":
        command += [
            "--dir", str(SANDBOX_HOME / ".codex"),
            "--bind", str(state), str(SANDBOX_HOME / ".codex"),
        ]
        command += [
            "--ro-bind", str(CODEX_RELEASE), str(CODEX_SANDBOX),
            "--ro-bind", str(HOME_HOST / ".codex/auth.json"), str(SANDBOX_HOME / ".codex/auth.json"),
            "--setenv", "CODEX_HOME", str(SANDBOX_HOME / ".codex"),
        ]
    else:
        command += [
            "--ro-bind", str(CLAUDE_BIN), str(CLAUDE_SANDBOX),
            "--bind", str(state), str(SANDBOX_HOME / ".claude"),
            "--ro-bind", str(HOME_HOST / ".claude/.credentials.json"), str(SANDBOX_HOME / ".claude/.credentials.json"),
        ]
    command += ["--chdir", work]
    return command


def provider_command(run_dir: Path, provider: str) -> list[str]:
    prompt = (run_dir / "prompt.txt").read_text(encoding="utf-8").strip()
    if provider == "sol":
        codex = CODEX_SANDBOX / "bin/codex"
        return [
            str(codex), "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox",
            "--json", "--color", "never", "--model", "gpt-5.6-sol",
            "-c", 'model_reasoning_effort="xhigh"', "-C", str(WORK), prompt,
        ]
    return [
        str(CLAUDE_SANDBOX), "--print", "--output-format", "stream-json", "--verbose",
        "--model", "claude-opus-5", "--effort", "high", "--safe-mode",
        "--disable-slash-commands", "--no-chrome", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', "--allowedTools", "Bash,Read,Write",
        "--disallowedTools", "WebFetch,WebSearch,Task", "--dangerously-skip-permissions",
        "--no-session-persistence", prompt,
    ]


def validate_workbook(run_dir: Path) -> dict[str, object]:
    metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
    workbook = run_dir / "extraction" / metadata["expected_output"]
    result: dict[str, object] = {"path": str(workbook), "exists": workbook.is_file()}
    if not workbook.is_file():
        result["valid_xlsx"] = False
        result["error"] = "expected workbook missing"
        return result
    result["bytes"] = workbook.stat().st_size
    result["sha256"] = sha256(workbook)
    try:
        from openpyxl import load_workbook

        opened = load_workbook(workbook, read_only=True, data_only=False)
        result["sheet_names"] = opened.sheetnames
        result["valid_xlsx"] = True
        opened.close()
    except Exception as exc:  # validation evidence, not repair
        result["valid_xlsx"] = False
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def preflight(provider: str) -> Path:
    if not shutil.which("bwrap"):
        raise SystemExit("bubblewrap (bwrap) is required")
    binary = CODEX_BIN if provider == "sol" else CLAUDE_BIN
    if not binary.is_file() or not os.access(binary, os.X_OK):
        raise SystemExit(f"provider executable not found: {binary}; set SEC_CODEX_BIN or SEC_CLAUDE_BIN")
    if provider == "sol" and (binary.parent.name != "bin" or binary.name != "codex"):
        raise SystemExit("SEC_CODEX_BIN must resolve to a standalone release's bin/codex")
    credential = HOME_HOST / (".codex/auth.json" if provider == "sol" else ".claude/.credentials.json")
    if not credential.is_file():
        raise SystemExit(f"provider authentication file is missing: {credential}")
    return binary


def prepared_metadata(run_dir: Path, provider: str) -> dict:
    path = run_dir / "metadata.json"
    if not path.is_file():
        raise SystemExit(f"run is not prepared: {run_dir}")
    metadata = json.loads(path.read_text(encoding="utf-8"))
    if metadata["provider"] != provider:
        raise SystemExit(f"prepared provider is {metadata['provider']}, not {provider}")
    return metadata


def run_worker(args: argparse.Namespace, state: Path) -> None:
    run_dir = Path(args.run_dir).resolve()
    prepared_metadata(run_dir, args.provider)
    binary = preflight(args.provider)
    if args.provider == "sol":
        cache = HOME_HOST / ".codex/models_cache.json"
        if cache.is_file():
            shutil.copy2(cache, state / "models_cache.json")

    provider_argv = provider_command(run_dir, args.provider)
    command = bwrap_base(run_dir, args.provider, state) + provider_argv
    started = time.monotonic()
    started_at = now_iso()
    write_json(run_dir / "command.json", {
        "provider": args.provider,
        "provider_argv": provider_argv,
        "credential_delivery": "read-only external credential bind; no credential copied to run directory",
        "runtime_state": "temporary directory outside the run; removed after worker completion",
        "provider_binary": str(binary),
        "provider_binary_sha256": sha256(binary),
        "started_at": started_at,
    })
    write_json(run_dir / "status.json", {
        "state": "running", "worker_pid": os.getpid(), "started_at": started_at,
    })

    stdout_path = run_dir / "events.jsonl"
    stderr_path = run_dir / "stderr.log"
    exit_code: int | None = None
    timed_out = False
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
            close_fds=True,
        )
        write_json(run_dir / "status.json", {
            "state": "running", "worker_pid": os.getpid(), "client_pid": proc.pid,
            "started_at": started_at,
        })
        try:
            exit_code = proc.wait(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                exit_code = proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                exit_code = proc.wait()

    validation = validate_workbook(run_dir)
    write_json(run_dir / "validation.json", validation)
    ended_at = now_iso()
    write_json(run_dir / "status.json", {
        "state": "timed_out" if timed_out else "completed",
        "worker_pid": os.getpid(),
        "client_pid": proc.pid,
        "started_at": started_at,
        "ended_at": ended_at,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "workbook_exists": validation.get("exists", False),
        "workbook_valid_xlsx": validation.get("valid_xlsx", False),
    })


def worker(args: argparse.Namespace) -> None:
    with tempfile.TemporaryDirectory(prefix="sec-extraction-state-") as state:
        run_worker(args, Path(state))


def launch(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).resolve()
    prepared_metadata(run_dir, args.provider)
    preflight(args.provider)
    status_path = run_dir / "status.json"
    if status_path.exists():
        old = json.loads(status_path.read_text(encoding="utf-8"))
        if old.get("state") == "running":
            raise SystemExit(f"run already marked running: {run_dir}")
        raise SystemExit(f"refusing to overwrite prior run status: {run_dir}")
    launcher_log = (run_dir / "launcher.log").open("ab")
    argv = [sys.executable, str(Path(__file__).resolve()), "worker", "--provider", args.provider, "--run-dir", str(run_dir)]
    proc = subprocess.Popen(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=launcher_log,
        stderr=launcher_log,
        start_new_session=True,
        close_fds=True,
        cwd=str(BASE),
    )
    launcher_log.close()
    write_json(run_dir / "launch.json", {"launcher_pid": proc.pid, "launched_at": now_iso(), "argv": argv})
    print(json.dumps({"run_dir": str(run_dir), "worker_pid": proc.pid, "provider": args.provider}, sort_keys=True))


def status(args: argparse.Namespace) -> None:
    for path in sorted(Path(args.runs_dir).glob("*")):
        if not path.is_dir():
            continue
        status_path = path / "status.json"
        payload = {"run": path.name, "state": "prepared"}
        if status_path.exists():
            payload.update(json.loads(status_path.read_text(encoding="utf-8")))
        print(json.dumps(payload, sort_keys=True))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    sub = root.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--provider", choices=["sol", "opus"], required=True)
    p.add_argument("--run-dir", required=True)
    p.add_argument("--deal", required=True)
    p.add_argument("--filing", required=True)
    p.add_argument("--revise-from", help="finished workbook to revise (revision pass)")
    p.add_argument("--report", help="checker findings in plain text, required with --revise-from")
    p.set_defaults(func=prepare)
    p = sub.add_parser("launch")
    p.add_argument("--provider", choices=["sol", "opus"], required=True)
    p.add_argument("--run-dir", required=True)
    p.set_defaults(func=launch)
    p = sub.add_parser("worker")
    p.add_argument("--provider", choices=["sol", "opus"], required=True)
    p.add_argument("--run-dir", required=True)
    p.set_defaults(func=worker)
    p = sub.add_parser("status")
    p.add_argument("--runs-dir", type=Path, default=RUNS, help="run root to inspect (default: _dev/runs)")
    p.set_defaults(func=status)
    return root


if __name__ == "__main__":
    parsed = parser().parse_args()
    parsed.func(parsed)
