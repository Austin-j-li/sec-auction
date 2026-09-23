"""Runner checks using temporary inputs and mocks; no provider is launched."""

import argparse
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock
import zipfile

from sandbox import run_model


class RunnerTests(unittest.TestCase):
    def setUp(self):
        # Every test runs against a synthetic token file, never the operator's real one.
        tokens = tempfile.TemporaryDirectory()
        self.addCleanup(tokens.cleanup)
        token = Path(tokens.name) / "token"
        token.write_text("synthetic-token")
        token.chmod(0o600)
        patcher = mock.patch.object(run_model, "CLAUDE_TOKEN_FILE", token)
        patcher.start()
        self.addCleanup(patcher.stop)

    def prepare_fixture(self, root, revise=False, extra=()):
        project = root / "project"
        (project / "raw_filing").mkdir(parents=True)
        (project / run_model.INSTRUCTION_NAME).write_text("Synthetic instruction")
        (project / "raw_filing" / "sample.htm").write_text("Synthetic filing")
        run = root / "runs" / "sample"
        argv = [
            "prepare", "--provider", "opus", "--run-dir", str(run),
            "--deal", "sample", "--filing", "sample.htm", *extra,
        ]
        if revise:
            workbook = root / "draft.xlsx"
            self.write_workbook(workbook, "original")
            report = root / "findings.md"
            report.write_text("Synthetic findings")
            argv += ["--revise-from", str(workbook), "--report", str(report)]
        args = run_model.parser().parse_args(argv)
        with mock.patch.object(run_model, "PROJECT", project), contextlib.redirect_stdout(io.StringIO()):
            run_model.prepare(args)
        return run

    def write_workbook(self, path, value="synthetic", sheets=tuple(run_model.SHEETS)):
        workbook = run_model._openpyxl.Workbook()
        workbook.active.title = sheets[0]
        workbook.active.append([value])
        for name in sheets[1:]:
            workbook.create_sheet(name)
        workbook.save(path)
        workbook.close()

    def result_event(self, model="claude-opus-5-5", **fields):
        event = {
            "type": "result", "subtype": "success", "is_error": False, "session_id": "session-1",
            "stop_reason": "end_turn", "terminal_reason": "completed", "num_turns": 2,
            "total_cost_usd": 0.5, "duration_api_ms": 1000,
            "usage": {"input_tokens": 1, "output_tokens": 10, "output_tokens_details": {"thinking_tokens": 6},
                      "cache_creation": {"ephemeral_1h_input_tokens": 100, "ephemeral_5m_input_tokens": 0}},
            "modelUsage": {model: {"costUSD": 0.5}},
        }
        event.update(fields)
        return event

    def processes(self, run, *steps):
        """Patch Popen with one process per step: exit code, events, and what it saves.

        The last item is False, True (a four-sheet workbook) or workbook options, where
        "notes" also writes revision_notes.md and "workbook": False saves only the notes.
        """
        procs = []
        for exit_code, logged, save in steps:
            def wait(timeout=None, exit_code=exit_code, logged=logged, save=save):
                with (run / "events.jsonl").open("a") as log:
                    log.writelines(json.dumps(event) + "\n" for event in logged)
                options = {} if save in (True, False) else dict(save)
                if options.pop("notes", False):
                    (run / "extraction/revision_notes.md").write_text("Synthetic notes")
                if save and options.pop("workbook", True):
                    self.write_workbook(run / "extraction/sample.xlsx", **options)
                return exit_code
            procs.append(mock.Mock(pid=12345, wait=mock.Mock(side_effect=wait)))
        self.procs = procs
        return mock.patch.object(run_model.subprocess, "Popen", side_effect=procs)

    def run_worker(self, run, *steps):
        with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                self.processes(run, *steps) as popen:
            code = run_model.worker(argparse.Namespace(run_dir=run, provider="opus"))
        return code, json.loads((run / "status.json").read_text()), popen

    def test_prepare_creates_no_runtime_state_and_status_uses_requested_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = self.prepare_fixture(root)
            self.assertFalse((run / "state").exists())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run_model.status(argparse.Namespace(runs_dir=root / "runs"))
            self.assertEqual(json.loads(output.getvalue())["run"], "sample")

    def test_usage_comes_from_the_event_log_and_versions_are_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = self.prepare_fixture(root)
            versions = json.loads((run / "metadata.json").read_text())["library_versions"]
            self.assertEqual(set(versions), {"openpyxl", "beautifulsoup4", "lxml"})
            events = root / "events.jsonl"
            events.write_text("not json\n" + json.dumps({
                "type": "result", "total_cost_usd": 1.5,
                "usage": {"input_tokens": 4, "output_tokens": 9, "service_tier": "standard"},
            }) + "\n")
            self.assertEqual(run_model.run_usage(events), {
                "tokens": {"input_tokens": 4, "output_tokens": 9}, "cost_usd": 1.5,
            })
            events.write_text("".join(json.dumps({
                "type": "turn.completed", "usage": {"input_tokens": 2, "output_tokens": 3},
            }) + "\n" for _ in range(2)))
            self.assertEqual(run_model.run_usage(events), {
                "tokens": {"input_tokens": 4, "output_tokens": 6}, "cost_usd": None,
            })
            events.write_text("")
            self.assertIsNone(run_model.run_usage(events))

    def test_continued_claude_session_sums_usage_but_reports_cumulative_cost(self):
        # A resumed session reports usage for its own invocation, and cost and modelUsage for the whole session.
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events.jsonl"
            first = self.result_event()
            second = self.result_event(total_cost_usd=0.9, num_turns=3, duration_api_ms=2500)
            events.write_text(json.dumps({"type": "system", "subtype": "init", "claude_code_version": "9.9.9",
                                          "model": "claude-opus-5-5", "tools": ["Bash"]}) + "\n"
                              + json.dumps(first) + "\n" + json.dumps(second) + "\n")
            self.assertEqual(run_model.run_usage(events), {
                "tokens": {"input_tokens": 2, "output_tokens": 20}, "cost_usd": 0.9,
            })
            summary = run_model.claude_summary(events)
            self.assertEqual(summary["claude_code_version"], "9.9.9")
            self.assertEqual(summary["served_models"], ["claude-opus-5-5"])
            self.assertEqual((summary["invocations"], summary["num_turns"], summary["duration_api_ms"]), (2, 5, 2500))
            self.assertEqual((summary["thinking_tokens"], summary["cache_write_1h_tokens"]), (12, 200))
            self.assertFalse(summary["refusal"])
            events.write_text(json.dumps({"type": "assistant", "message": {"stop_reason": "refusal"}}) + "\n")
            self.assertTrue(run_model.claude_summary(events)["refusal"])

    def test_model_effort_and_timeout_come_from_prepared_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp), extra=("--effort", "medium", "--timeout-minutes", "120"))
            metadata = run_model.prepared_metadata(run, "opus")
            self.assertEqual((metadata["model"], metadata["effort"], metadata["timeout_seconds"]),
                             ("claude-opus-5-5", "medium", 7200))
            argv = run_model.provider_command(run, "opus", metadata)
            self.assertEqual(argv[argv.index("--model") + 1], "claude-opus-5-5")
            self.assertEqual(argv[argv.index("--tools") + 1], "Bash,Read,Write")  # the only tools the agent sees
            self.assertEqual(argv[argv.index("--effort") + 1], "medium")
            self.assertNotIn("--resume", argv)
            self.assertEqual(argv[-1], (run / "prompt.txt").read_text().strip())
            resumed = run_model.provider_command(run, "opus", metadata, "go on", "session-1")
            self.assertEqual(resumed[-3:], ["--resume", "session-1", "go on"])
            state = Path(tmp) / "state"
            state.mkdir()
            command = run_model.bwrap_base(run, "opus", state, Path(tmp) / "scratch")
            for name, value in run_model.CLAUDE_ENV.items():
                self.assertIn(["--setenv", name, value], [command[i:i + 3] for i in range(len(command))])

    def test_default_opus_run_is_opus_5_5(self):
        with tempfile.TemporaryDirectory() as tmp:
            metadata = json.loads((self.prepare_fixture(Path(tmp)) / "metadata.json").read_text())
        self.assertEqual((metadata["model"], metadata["effort"], metadata["timeout_seconds"]),
                         ("claude-opus-5-5", run_model.DEFAULT_EFFORT["opus"], run_model.TIMEOUT_SECONDS))

    def test_disallowed_model_effort_or_timeout_fails_before_creating_run(self):
        for extra, message in [(("--effort", "extreme"), "runs one of"), (("--model", "claude-sonnet-5"), "runs one of"),
                               (("--timeout-minutes", "5"), "between 10 and 360")]:
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaisesRegex(SystemExit, message):
                    self.prepare_fixture(Path(tmp), extra=extra)
                self.assertFalse((Path(tmp) / "runs").exists())

    def test_edited_model_or_effort_fails_before_launch(self):
        for key, value in [("model", "claude-sonnet-5"), ("effort", "--dangerously-skip-permissions"),
                           ("effort", None), ("timeout_seconds", 99999)]:
            with self.subTest(key=key, value=value), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp))
                metadata = json.loads((run / "metadata.json").read_text())
                metadata[key] = value
                run_model.write_json(run / "metadata.json", metadata)
                with mock.patch.object(run_model.subprocess, "Popen") as popen:
                    with self.assertRaisesRegex(SystemExit, "prepare a new run directory"):
                        run_model.launch(argparse.Namespace(run_dir=run, provider="opus"))
                popen.assert_not_called()

    def test_historical_opus_5_metadata_still_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp), extra=("--model", "claude-opus-5", "--effort", "high"))
            self.assertEqual(run_model.prepared_metadata(run, "opus")["model"], "claude-opus-5")

    def test_filing_dir_is_raw_filing_or_a_cockpit_deal_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            added = project / "_dev/cockpit/state/filings/added-deal"
            added.mkdir(parents=True)
            (added / "added.htm").write_text("Added filing")
            (project / "ref").mkdir()
            (project / "ref" / "added.htm").write_text("Not a filing folder")
            (project / run_model.INSTRUCTION_NAME).write_text("Synthetic instruction")
            for folder, allowed in ((added, True), (project / "ref", False), (added.parent, False)):
                run = root / "runs" / folder.name
                args = run_model.parser().parse_args(["prepare", "--provider", "opus", "--run-dir", str(run), "--deal", "added-deal",
                                                      "--filing", "added.htm", "--filing-dir", str(folder)])
                with self.subTest(folder=folder.name), mock.patch.object(run_model, "PROJECT", project), contextlib.redirect_stdout(io.StringIO()):
                    if allowed:
                        run_model.prepare(args)
                        self.assertEqual((run / "input/raw_filing/added.htm").read_text(), "Added filing")
                    else:
                        with self.assertRaisesRegex(SystemExit, "--filing-dir must be"):
                            run_model.prepare(args)
                        self.assertFalse(run.exists())

    def test_half_specified_revision_fails_before_creating_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            for flag in ["--revise-from", "--report"]:
                run = Path(tmp) / flag.removeprefix("--")
                args = run_model.parser().parse_args([
                    "prepare", "--provider", "opus", "--run-dir", str(run),
                    "--deal", "sample", "--filing", "sample.htm", flag, "missing",
                ])
                with self.assertRaisesRegex(SystemExit, "supplied together"):
                    run_model.prepare(args)
                self.assertFalse(run.exists())

    def test_provider_mismatch_fails_before_launch_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            with mock.patch.object(run_model.subprocess, "Popen") as popen:
                with self.assertRaisesRegex(SystemExit, "prepared provider is opus"):
                    run_model.launch(argparse.Namespace(run_dir=run, provider="sol"))
            popen.assert_not_called()
            self.assertFalse((run / "launcher.log").exists())

    def test_runtime_state_is_deleted_even_after_worker_failure(self):
        seen = []
        def fail(args, state, scratch):
            self.assertTrue(state.is_dir())
            seen.append(state)
            (state / "generated-state").write_text("temporary")
            raise RuntimeError("synthetic failure")
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            with mock.patch.object(run_model, "run_worker", side_effect=fail):
                with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
                    run_model.worker(argparse.Namespace(run_dir=run, provider="opus"))
            result = json.loads((run / "status.json").read_text())
            self.assertEqual(result["state"], "failed")
            self.assertIn("synthetic failure", result["error"])
        self.assertFalse(seen[0].exists())

    def test_changed_inputs_fail_before_launch_or_provider_start(self):
        inputs = [
            "input/" + run_model.INSTRUCTION_NAME,
            "input/raw_filing/sample.htm", "prompt.txt",
            "input/" + run_model.REPORT_NAME, "extraction/sample.xlsx",
        ]
        for relative in inputs:
            for entrypoint in ("launch", "run_worker"):
                with self.subTest(input=relative, entrypoint=entrypoint), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    run = self.prepare_fixture(root, revise=True)
                    with (run / relative).open("ab") as target:
                        target.write(b"changed after preparation")
                    with mock.patch.object(run_model.subprocess, "Popen") as popen, \
                            mock.patch.object(run_model, "preflight") as preflight:
                        with self.assertRaisesRegex(SystemExit, "prepared input hash mismatch"):
                            args = argparse.Namespace(run_dir=run, provider="opus")
                            if entrypoint == "launch":
                                run_model.launch(args)
                            else:
                                run_model.run_worker(args, root / "state", root / "scratch")
                    popen.assert_not_called()
                    preflight.assert_not_called()
                    self.assertFalse((run / "launcher.log").exists())

    def test_missing_or_extra_filing_fails_before_launch(self):
        for missing in (True, False):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp))
                filing = run / "input/raw_filing/sample.htm"
                if missing:
                    filing.unlink()
                else:
                    filing.with_name("extra.htm").write_text("extra filing")
                with mock.patch.object(run_model.subprocess, "Popen") as popen:
                    with self.assertRaisesRegex(SystemExit, "exactly the recorded filing"):
                        run_model.launch(argparse.Namespace(run_dir=run, provider="opus"))
                popen.assert_not_called()

    def test_legacy_extraction_hashes_work_but_revision_requires_report_hash(self):
        for revise in (False, True):
            with self.subTest(revise=revise), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp), revise=revise)
                metadata_path = run / "metadata.json"
                metadata = json.loads(metadata_path.read_text())
                if revise:
                    self.assertEqual(metadata["report_sha256"], run_model.sha256(run / "input" / run_model.REPORT_NAME))
                    self.assertEqual(metadata["revised_from_sha256"], run_model.sha256(run / "extraction/sample.xlsx"))
                del metadata["report_sha256"]
                run_model.write_json(metadata_path, metadata)
                if revise:
                    with mock.patch.object(run_model.subprocess, "Popen") as popen:
                        with self.assertRaisesRegex(SystemExit, "lacks report_sha256; prepare a new run"):
                            run_model.launch(argparse.Namespace(run_dir=run, provider="opus"))
                    popen.assert_not_called()
                else:
                    self.assertEqual(run_model.prepared_metadata(run, "opus"), metadata)

    def test_worker_records_input_failure_without_invoking_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            (run / "prompt.txt").write_text("changed after launcher validation")
            with mock.patch.object(run_model.subprocess, "Popen") as popen:
                with self.assertRaisesRegex(SystemExit, "prepared input hash mismatch"):
                    run_model.worker(argparse.Namespace(run_dir=run, provider="opus"))
            popen.assert_not_called()
            result = json.loads((run / "status.json").read_text())
            self.assertEqual(result["state"], "failed")
            self.assertIn("hash mismatch", result["error"])

    def test_worker_outcomes_distinguish_execution_failures(self):
        ok = self.result_event()
        cases = [
            (None, 0, [(0, [ok], True)]),
            ("provider_exit", 2, [(2, [ok], True)]),
            ("provider_refusal", 0, [(0, [self.result_event(stop_reason="refusal")], True)]),
            ("provider_error", 0, [(0, [self.result_event(subtype="error_during_execution", is_error=True)], True)]),
            ("provider_error", 0, [(0, [], True)]),
            ("model_mismatch", 0, [(0, [self.result_event(modelUsage={"claude-opus-5-5": {}, "claude-opus-5": {}})], True)]),
            # An incomplete workbook is also unfinished work, so it is resumed before it fails.
            ("workbook_incomplete", 0, [(0, [ok], {"sheets": ("Sheet",)})] * (run_model.MAX_CONTINUATIONS + 1)),
        ]
        for reason, exit_code, steps in cases:
            with self.subTest(reason=reason, steps=len(steps)), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp))
                code, result, _ = self.run_worker(run, *steps)
                self.assertEqual(code, 0 if reason is None else 1)
                self.assertEqual(result["state"], "completed" if reason is None else "failed")
                self.assertEqual(result["failure_reason"], reason)
                self.assertEqual(result["exit_code"], exit_code)
                self.assertEqual(result["continuations"], len(steps) - 1)
                self.assertTrue((run / "validation.json").is_file())
                self.assertEqual(json.loads((run / "provider-results.json").read_text()),
                                 [event for step in steps for event in step[1]])

    def rate_limit(self, status="allowed", resets=1790165400, weekly=0.29):
        return {"type": "rate_limit_event", "rate_limit_info": {
            "status": status, "rateLimitType": "five_hour", "resetsAt": resets,
            "unifiedWindows": {"five_hour": {"utilization": 0.1, "resetsAt": resets}, "seven_day": {"utilization": weekly, "resetsAt": resets + 3600}}}}

    def test_plan_usage_is_recorded_and_a_rejected_limit_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            _, result, _ = self.run_worker(run, (0, [self.rate_limit(weekly=0.2), self.rate_limit(weekly=0.3), self.result_event()], True))
            self.assertEqual((result["state"], result["plan_usage"]["unifiedWindows"]["seven_day"]["utilization"]), ("completed", 0.3))
            self.assertNotIn("usage_limit_resets_at", result)
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            limited = self.result_event(subtype="error_during_execution", is_error=True)
            _, result, popen = self.run_worker(run, (1, [self.rate_limit(), self.rate_limit(status="rejected"), limited], False))
            self.assertEqual((result["state"], result["failure_reason"], popen.call_count), ("failed", "usage_limit", 1))
            self.assertEqual(result["usage_limit_resets_at"], "2026-09-23T12:10:00+00:00")
            self.assertEqual(result["plan_usage"]["status"], "rejected")

    def test_fable_is_allowed_and_its_safeguard_block_is_a_refusal(self):
        blocked = self.result_event(model="claude-fable-5-1", subtype="success", is_error=True,
                                    result="API Error: Fable 5.1's safeguards flagged this message. Claude Code can't respond to this message with Fable 5.1.")
        for reason, steps in ((None, [(0, [self.result_event(model="claude-fable-5-1")], True)]), ("provider_refusal", [(1, [blocked], False)])):
            with self.subTest(reason=reason), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp), extra=("--model", "claude-fable-5-1", "--effort", "high"))
                self.assertEqual(run_model.prepared_metadata(run, "opus")["model"], "claude-fable-5-1")
                _, result, popen = self.run_worker(run, *steps)
                self.assertEqual((result["failure_reason"], popen.call_count), (reason, 1))

    def prepare_sol(self, root, model="gpt-6-astra"):
        project = root / "project"
        (project / "raw_filing").mkdir(parents=True)
        (project / run_model.INSTRUCTION_NAME).write_text("Synthetic instruction")
        (project / "raw_filing" / "sample.htm").write_text("Synthetic filing")
        run = root / "runs" / "sample"
        args = run_model.parser().parse_args(["prepare", "--provider", "sol", "--run-dir", str(run), "--deal", "sample",
                                              "--filing", "sample.htm", "--model", model, "--effort", "high"])
        with mock.patch.object(run_model, "PROJECT", project), contextlib.redirect_stdout(io.StringIO()):
            run_model.prepare(args)
        return run

    def test_astra_binds_the_named_codex_login_and_a_usage_limit_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = self.prepare_sol(root)
            auth = root / "users/alex/codex/auth.json"
            auth.parent.mkdir(parents=True)
            auth.write_text("{}")
            with mock.patch.object(run_model, "CODEX_AUTH_FILE", auth):
                command = run_model.bwrap_base(run, "sol", root / "state", root / "scratch")
            at = command.index(str(auth))
            self.assertEqual((command[at - 1], command[at + 1]), ("--ro-bind", str(run_model.SANDBOX_HOME / ".codex/auth.json")))
            host = str(run_model.HOME_HOST / ".codex/auth.json")
            self.assertFalse(any(command[i] == "--ro-bind" and command[i + 1] == host for i in range(len(command) - 1)))
            self.assertIn("gpt-6-astra", run_model.provider_command(run, "sol", run_model.prepared_metadata(run, "sol")))
            limited = {"type": "error", "message": "You've hit your usage limit. Upgrade to Pro or try again at 3:05 PM."}
            echoed = {"type": "item.completed", "item": {"type": "command_execution", "aggregated_output": "we hit your usage limit"}}
            with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                    self.processes(run, (1, [echoed, limited], False)):
                self.assertEqual(run_model.worker(argparse.Namespace(run_dir=run, provider="sol")), 1)
            result = json.loads((run / "status.json").read_text())
            self.assertEqual((result["failure_reason"], result["usage_limit_message"]),
                             ("usage_limit", "You've hit your usage limit. Upgrade to Pro or try again at 3:05 PM."))
        with tempfile.TemporaryDirectory() as tmp:  # filing text echoed by a command is not a usage limit
            run = self.prepare_sol(Path(tmp))
            with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                    self.processes(run, (1, [echoed], False)):
                run_model.worker(argparse.Namespace(run_dir=run, provider="sol"))
            self.assertEqual(json.loads((run / "status.json").read_text())["failure_reason"], "provider_exit")

    def test_codex_login_margin_uses_the_named_login(self):
        with tempfile.TemporaryDirectory() as tmp:
            import base64 as b64
            claims = b64.urlsafe_b64encode(json.dumps({"exp": int(time.time()) + 3600}).encode()).decode().rstrip("=")
            auth = Path(tmp) / "auth.json"
            auth.write_text(json.dumps({"tokens": {"access_token": f"x.{claims}.y"}}))
            binary = Path(tmp) / "bin/codex"
            binary.parent.mkdir()
            binary.write_text("")
            binary.chmod(0o755)
            with mock.patch.object(run_model, "CODEX_AUTH_FILE", auth), mock.patch.object(run_model, "CODEX_BIN", binary), \
                    mock.patch.object(run_model.shutil, "which", return_value="/usr/bin/bwrap"):
                with self.assertRaisesRegex(SystemExit, "expires in 1.0 h"):
                    run_model.preflight("sol")

    def test_sigterm_cancels_the_run_and_stops_the_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            killed = []
            def wait(timeout=None):
                run_model._cancel(run_model.signal.SIGTERM, None)  # as if the cockpit worker sent SIGTERM mid-run
                return -15
            proc = mock.Mock(pid=4321, wait=mock.Mock(side_effect=wait))
            with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                    mock.patch.object(run_model.subprocess, "Popen", return_value=proc) as popen, \
                    mock.patch.object(run_model.os, "killpg", side_effect=lambda pgid, sig: killed.append((pgid, sig))), \
                    mock.patch.object(run_model.threading, "Thread"):
                self.assertEqual(run_model.worker(argparse.Namespace(run_dir=run, provider="opus")), 1)
            result = json.loads((run / "status.json").read_text())
            self.assertEqual((result["state"], result["failure_reason"], popen.call_count), ("cancelled", "cancelled", 1))
            self.assertEqual(killed, [(4321, run_model.signal.SIGTERM)])
            self.assertTrue((run / "validation.json").is_file())

    def test_unreadable_workbook_and_timeout_are_distinguished(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            (run / "extraction/sample.xlsx").write_text("not a workbook")
            steps = [(0, [self.result_event()], False)] * (run_model.MAX_CONTINUATIONS + 1)
            _, result, _ = self.run_worker(run, *steps)
            self.assertEqual((result["failure_reason"], result["continuations"]),
                             ("workbook_unreadable", run_model.MAX_CONTINUATIONS))
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            proc = mock.Mock(pid=12345)
            proc.wait.side_effect = [run_model.subprocess.TimeoutExpired("synthetic", 1), -15]
            with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                    mock.patch.object(run_model.subprocess, "Popen", return_value=proc), \
                    mock.patch.object(run_model.os, "killpg"):
                self.assertEqual(run_model.worker(argparse.Namespace(run_dir=run, provider="opus")), 1)
            result = json.loads((run / "status.json").read_text())
            self.assertEqual((result["state"], result["failure_reason"], result["exit_code"]), ("timed_out", "timeout", -15))
            self.assertEqual(proc.wait.call_args_list[0].kwargs["timeout"] > 5000, True)

    def test_early_stop_is_resumed_until_the_workbook_is_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            code, result, popen = self.run_worker(
                run, (0, [self.result_event()], False), (0, [self.result_event(total_cost_usd=0.8)], True))
            self.assertEqual((code, result["state"], result["continuations"]), (0, "completed", 1))
            self.assertEqual(result["usage"]["cost_usd"], 0.8)
            self.assertEqual(result["provider"]["invocations"], 2)
            command = json.loads((run / "command.json").read_text())
            self.assertNotIn("--resume", command["provider_argv"])
            resumed = command["continuation_argv"][0]
            self.assertEqual(resumed[-3:-1], ["--resume", "session-1"])
            self.assertIn("extraction/sample.xlsx is not yet saved", resumed[-1])
            self.assertEqual(popen.call_count, 2)

    def test_continuations_are_bounded_and_never_follow_a_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            steps = [(0, [self.result_event()], False)] * (run_model.MAX_CONTINUATIONS + 1)
            _, result, popen = self.run_worker(run, *steps)
            self.assertEqual((result["failure_reason"], result["continuations"]), ("workbook_missing", run_model.MAX_CONTINUATIONS))
            self.assertEqual(popen.call_count, run_model.MAX_CONTINUATIONS + 1)
        for event in (self.result_event(stop_reason="refusal"), self.result_event(is_error=True, subtype="error_max_turns")):
            with self.subTest(event=event), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp))
                _, result, popen = self.run_worker(run, (0, [event], False))
                self.assertEqual((result["continuations"], popen.call_count), (0, 1))

    def test_provider_start_failure_does_not_leave_running_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                    mock.patch.object(run_model.subprocess, "Popen", side_effect=OSError("synthetic start failure")):
                with self.assertRaisesRegex(OSError, "synthetic start failure"):
                    run_model.worker(argparse.Namespace(run_dir=run, provider="opus"))
            result = json.loads((run / "status.json").read_text())
            self.assertEqual(result["state"], "failed")
            self.assertEqual(result["failure_reason"], "worker_error")

    def test_revised_workbook_can_change_and_completed_run_remains_inspectable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = self.prepare_fixture(root, revise=True)
            code, _, _ = self.run_worker(run, (0, [self.result_event()], {"value": "revised", "notes": True}))
            self.assertEqual(code, 0)
            self.assertTrue(run_model.validate_workbook(run)["valid_xlsx"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run_model.status(argparse.Namespace(runs_dir=root / "runs"))
            self.assertEqual(json.loads(output.getvalue())["state"], "completed")
            recorded_status = (run / "status.json").read_bytes()
            with mock.patch.object(run_model.subprocess, "Popen") as popen:
                with self.assertRaisesRegex(SystemExit, "refusing to overwrite prior run status"):
                    run_model.worker(argparse.Namespace(run_dir=run, provider="opus"))
            popen.assert_not_called()
            self.assertEqual((run / "status.json").read_bytes(), recorded_status)

    def test_continuation_keeps_the_same_scratch_home_and_tmp(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            _, result, popen = self.run_worker(
                run, (0, [self.result_event()], False), (0, [self.result_event()], True))
            self.assertEqual(result["continuations"], 1)
            first, second = (call.args[0] for call in popen.call_args_list)

            def mounts(command, target):
                return [command[i:i + 3] for i in range(len(command) - 2)
                        if command[i] in ("--bind", "--ro-bind", "--tmpfs") and target in command[i + 1:i + 3]]

            for target in (str(run_model.SANDBOX_HOME), "/tmp"):
                self.assertEqual(len(mounts(first, target)), 1)
                self.assertEqual(mounts(first, target)[0][0], "--bind")  # not a fresh tmpfs per invocation
                self.assertEqual(mounts(first, target), mounts(second, target))

    def test_continuation_waits_only_for_the_time_left(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            self.run_worker(run, (0, [self.result_event()], False), (0, [self.result_event()], True))
            limit = json.loads((run / "metadata.json").read_text())["timeout_seconds"]
            first, second = (proc.wait.call_args.kwargs["timeout"] for proc in self.procs)
            self.assertLessEqual(first, limit)
            self.assertLess(second, limit)
            self.assertLessEqual(second, first)

    def test_half_saved_workbook_is_resumed(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            _, result, popen = self.run_worker(
                run, (0, [self.result_event()], {"sheets": ("Deal ledger", "Rounds")}), (0, [self.result_event()], True))
            self.assertEqual((result["state"], result["continuations"], popen.call_count), ("completed", 1, 2))

    def test_revision_is_resumed_until_its_notes_are_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp), revise=True)
            _, result, popen = self.run_worker(
                run, (0, [self.result_event()], False), (0, [self.result_event()], {"notes": True, "workbook": False}))
            self.assertEqual((result["state"], result["continuations"]), ("completed", 1))
            resumed = json.loads((run / "command.json").read_text())["continuation_argv"][0]
            self.assertIn("revision_notes.md has not been written", resumed[-1])
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp), revise=True)
            steps = [(0, [self.result_event()], False)] * (run_model.MAX_CONTINUATIONS + 1)
            _, result, _ = self.run_worker(run, *steps)
            self.assertEqual(result["failure_reason"], "revision_notes_missing")

    def test_validation_reads_lazy_worksheet_content_and_handles_unreadable_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp))
            workbook = run / "extraction/sample.xlsx"
            self.write_workbook(workbook)
            with zipfile.ZipFile(workbook) as source:
                parts = {name: source.read(name) for name in source.namelist()}
            parts["xl/worksheets/sheet1.xml"] += b"<broken"
            with zipfile.ZipFile(workbook, "w") as target:
                for name, content in parts.items():
                    target.writestr(name, content)
            self.assertFalse(run_model.validate_workbook(run)["valid_xlsx"])
            with mock.patch.object(run_model, "sha256", side_effect=PermissionError("synthetic unreadable")):
                result = run_model.validate_workbook(run)
            self.assertFalse(result["valid_xlsx"])
            self.assertIn("synthetic unreadable", result["error"])

    def test_extract_mounts_do_not_include_stray_checker_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = self.prepare_fixture(root)
            report = run / "input" / run_model.REPORT_NAME
            report.write_text("Must not enter a blind extraction")
            state = root / "runtime-state"
            state.mkdir()
            command = run_model.bwrap_base(run, "opus", state, root / "scratch")
            self.assertNotIn(str(report), command)
            self.assertFalse(any(".credentials.json" in part for part in command))
            self.assertIn(str(run / "input" / run_model.INSTRUCTION_NAME), command)
            self.assertIn(str(run / "input" / "raw_filing" / "sample.htm"), command)
            self.assertIn(str(state), command)
            self.assertNotIn(str(run / "state"), command)

    def test_oauth_token_reaches_the_cli_through_a_pipe_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            token = Path(tmp) / "token"
            token.write_text("sk-ant-oat-synthetic\n")
            token.chmod(0o600)
            run = self.prepare_fixture(Path(tmp))
            with mock.patch.object(run_model, "CLAUDE_TOKEN_FILE", token):
                with run_model.claude_token("opus") as (args, fds):
                    self.assertEqual(args[:2], ["--setenv", "CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR"])
                    self.assertEqual(os.read(fds[0], 100), b"sk-ant-oat-synthetic")
                with self.assertRaises(OSError):
                    os.fstat(fds[0])  # closed once the invocation is over
                command = run_model.bwrap_base(run, "opus", Path(tmp) / "state", Path(tmp) / "scratch")
                self.assertNotIn(str(run_model.HOME_HOST / ".claude/.credentials.json"), command)
                _, result, popen = self.run_worker(run, (0, [self.result_event()], True))
            self.assertEqual(result["state"], "completed")
            call = popen.call_args
            self.assertEqual(len(call.kwargs["pass_fds"]), 1)
            self.assertIn("CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR", call.args[0])
            self.assertNotIn("sk-ant-oat-synthetic", " ".join(call.args[0]))
            self.assertNotIn("sk-ant-oat-synthetic", (run / "command.json").read_text())
            self.assertIn("inherited pipe", json.loads((run / "command.json").read_text())["credential_delivery"])

    def test_preflight_requires_usable_claude_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            token, home = Path(tmp) / "token", Path(tmp) / "home"
            (home / ".claude").mkdir(parents=True)
            # Even a host login with a token on disk is never shared with the sandbox.
            (home / ".claude/.credentials.json").write_text(json.dumps({"claudeAiOauth": {"accessToken": "host"}}))
            patches = [mock.patch.object(run_model, "CLAUDE_BIN", Path(run_model.__file__)),
                       mock.patch.object(run_model.os, "access", return_value=True),
                       mock.patch.object(run_model.shutil, "which", return_value="/usr/bin/bwrap"),
                       mock.patch.object(run_model, "CLAUDE_TOKEN_FILE", token),
                       mock.patch.object(run_model, "HOME_HOST", home)]
            with contextlib.ExitStack() as stack:
                for patch in patches:
                    stack.enter_context(patch)
                with self.assertRaisesRegex(SystemExit, "claude setup-token"):
                    run_model.preflight("opus")
                token.write_text("sk-ant-oat-synthetic")
                token.chmod(0o644)
                with self.assertRaisesRegex(SystemExit, "chmod 600"):
                    run_model.preflight("opus")
                token.chmod(0o600)
                self.assertEqual(run_model.preflight("opus"), Path(run_model.__file__))

    def test_sol_runs_gpt_6_sol_with_shell_and_patches_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.prepare_fixture(Path(tmp), extra=())
            metadata = json.loads((run / "metadata.json").read_text())
            argv = run_model.provider_command(run, "sol", {**metadata, "model": "gpt-6-sol", "effort": "high"})
        self.assertEqual(argv[argv.index("--model") + 1], "gpt-6-sol")
        self.assertIn('model_reasoning_effort="high"', argv)
        self.assertIn('web_search="disabled"', argv)
        disabled = {argv[i + 1] for i, part in enumerate(argv) if part == "--disable"}
        self.assertTrue({"apps", "plugins", "browser_use", "computer_use", "multi_agent"} <= disabled)
        self.assertNotIn("code_mode_host", disabled)  # GPT-6-Sol calls every tool through code mode
        self.assertNotIn("ultra", run_model.EFFORTS["sol"])

    def test_sol_preflight_refuses_a_codex_login_near_expiry(self):
        def token(hours):
            claims = base64.urlsafe_b64encode(json.dumps({"exp": time.time() + hours * 3600}).encode()).decode().rstrip("=")
            return {"tokens": {"access_token": f"header.{claims}.signature"}}
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()
            codex = home / "release/bin/codex"
            codex.parent.mkdir(parents=True)
            codex.write_text("")
            with mock.patch.object(run_model, "HOME_HOST", home), mock.patch.object(run_model, "CODEX_BIN", codex), \
                    mock.patch.object(run_model.os, "access", return_value=True), \
                    mock.patch.object(run_model.shutil, "which", return_value="/usr/bin/bwrap"):
                (home / ".codex/auth.json").write_text(json.dumps(token(2)))
                with self.assertRaisesRegex(SystemExit, "renew it outside the sandbox"):
                    run_model.preflight("sol")
                (home / ".codex/auth.json").write_text(json.dumps(token(30)))
                self.assertEqual(run_model.preflight("sol"), codex)

    def test_preflight_rejects_missing_provider_binary(self):
        with mock.patch.object(run_model, "CLAUDE_BIN", Path("/nonexistent/provider")), \
                mock.patch.object(run_model.shutil, "which", return_value="/usr/bin/bwrap"):
            with self.assertRaisesRegex(SystemExit, "provider executable not found"):
                run_model.preflight("opus")


if __name__ == "__main__":
    unittest.main()
