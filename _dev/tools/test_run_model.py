"""Runner checks using temporary inputs and mocks; no provider is launched."""

import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from sandbox import run_model


class RunnerTests(unittest.TestCase):
    def prepare_fixture(self, root):
        project = root / "project"
        (project / "raw_filing").mkdir(parents=True)
        (project / run_model.INSTRUCTION_NAME).write_text("Synthetic instruction")
        (project / "raw_filing" / "sample.htm").write_text("Synthetic filing")
        run = root / "runs" / "sample"
        args = run_model.parser().parse_args([
            "prepare", "--provider", "opus", "--run-dir", str(run),
            "--deal", "sample", "--filing", "sample.htm",
        ])
        with mock.patch.object(run_model, "PROJECT", project), contextlib.redirect_stdout(io.StringIO()):
            run_model.prepare(args)
        return run

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
        with mock.patch.object(run_model, "run_worker", side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
                run_model.worker(argparse.Namespace())
        self.assertFalse(seen[0].exists())

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
