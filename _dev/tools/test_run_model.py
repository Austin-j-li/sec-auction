"""Runner checks using temporary inputs and mocks; no provider is launched."""

import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

from sandbox import run_model


class RunnerTests(unittest.TestCase):
    def prepare_fixture(self, root, revise=False):
        project = root / "project"
        (project / "raw_filing").mkdir(parents=True)
        (project / run_model.INSTRUCTION_NAME).write_text("Synthetic instruction")
        (project / "raw_filing" / "sample.htm").write_text("Synthetic filing")
        run = root / "runs" / "sample"
        argv = [
            "prepare", "--provider", "opus", "--run-dir", str(run),
            "--deal", "sample", "--filing", "sample.htm",
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

    def write_workbook(self, path, value="synthetic"):
        workbook = run_model._openpyxl.Workbook()
        workbook.active.append([value])
        workbook.save(path)
        workbook.close()

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
            events.write_text("".join(json.dumps({"type": "step_finish", "part": {
                "tokens": {"total": 9, "input": 1, "output": 2, "cache": {"read": 6, "write": 0}}, "cost": 0.25,
            }}) + "\n" for _ in range(2)))
            self.assertEqual(run_model.run_usage(events), {"tokens": {
                "input_tokens": 2, "output_tokens": 4, "cache_read_tokens": 12, "cache_write_tokens": 0,
            }, "cost_usd": 0.5})
            events.write_text("")
            self.assertIsNone(run_model.run_usage(events))

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
        def fail(args, state):
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
                                run_model.run_worker(args, root / "state")
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
        cases = [
            (0, "valid", False, "completed", None),
            (2, "valid", False, "failed", "provider_exit"),
            (0, "missing", False, "failed", "workbook_missing"),
            (0, "unreadable", False, "failed", "workbook_unreadable"),
            (-15, "valid", True, "timed_out", "timeout"),
        ]
        for exit_code, output, timed_out, state, reason in cases:
            with self.subTest(exit_code=exit_code, output=output, timed_out=timed_out), tempfile.TemporaryDirectory() as tmp:
                run = self.prepare_fixture(Path(tmp))
                workbook = run / "extraction/sample.xlsx"
                if output == "valid":
                    self.write_workbook(workbook)
                elif output == "unreadable":
                    workbook.write_text("not a workbook")
                proc = mock.Mock(pid=12345)
                proc.wait.side_effect = [
                    run_model.subprocess.TimeoutExpired("synthetic", 1), exit_code,
                ] if timed_out else [exit_code]
                with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                        mock.patch.object(run_model.subprocess, "Popen", return_value=proc), \
                        mock.patch.object(run_model.os, "killpg"):
                    result_code = run_model.worker(argparse.Namespace(run_dir=run, provider="opus"))
                result = json.loads((run / "status.json").read_text())
                self.assertEqual(result_code, 0 if state == "completed" else 1)
                self.assertEqual(result["state"], state)
                self.assertEqual(result["failure_reason"], reason)
                self.assertEqual(result["exit_code"], exit_code)
                self.assertEqual(result["workbook_valid_xlsx"], output == "valid")
                self.assertTrue((run / "validation.json").is_file())

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
            def finish(**kwargs):
                self.write_workbook(run / "extraction/sample.xlsx", "revised")
                return 0
            proc = mock.Mock(pid=12345)
            proc.wait.side_effect = finish
            with mock.patch.object(run_model, "preflight", return_value=Path(run_model.__file__)), \
                    mock.patch.object(run_model.subprocess, "Popen", return_value=proc):
                self.assertEqual(run_model.worker(argparse.Namespace(run_dir=run, provider="opus")), 0)
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
            command = run_model.bwrap_base(run, "opus", state)
            self.assertNotIn(str(report), command)
            self.assertIn(str(run / "input" / run_model.INSTRUCTION_NAME), command)
            self.assertIn(str(run / "input" / "raw_filing" / "sample.htm"), command)
            self.assertIn(str(state), command)
            self.assertNotIn(str(run / "state"), command)

    def test_preflight_rejects_missing_provider_binary(self):
        with mock.patch.object(run_model, "CLAUDE_BIN", Path("/nonexistent/provider")), \
                mock.patch.object(run_model.shutil, "which", return_value="/usr/bin/bwrap"):
            with self.assertRaisesRegex(SystemExit, "provider executable not found"):
                run_model.preflight("opus")


if __name__ == "__main__":
    unittest.main()
