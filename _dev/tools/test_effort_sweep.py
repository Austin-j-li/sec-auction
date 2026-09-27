"""Effort-sweep planning, recording and summaries on synthetic runs; no provider is launched."""

import argparse
import contextlib
import gzip
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import effort_sweep
from sandbox import run_model

PIN = {"binaries": {"opus": {"path": "/pinned/claude", "sha256": "claude-binary", "version": "9.9.9 (Claude Code)"},
                    "sol": {"path": "/pinned/codex", "sha256": "codex-binary", "version": "codex-cli 9.9"}},
       "instruction_sha256": "instruction", "runner_sha256": "runner"}
ARMS = ["opus:claude-opus-5-5:medium", "opus:claude-opus-5-5:high", "sol:gpt-6-sol:high"]


def plan_args(packet, **overrides):
    values = dict(packet=str(packet), deals="kraton,penford", arms=ARMS, replicates=2, seed=7, timeout_minutes=120)
    values.update(overrides)
    return argparse.Namespace(**values)


def make_cell(deal="kraton", effort="low", replicate=1, timeout=90, provider="opus", model="claude-opus-5-5"):
    arm = f"{model.removeprefix('claude-')}-{effort}"
    return {"id": f"{deal}-{arm}-r{replicate}", "deal": deal, "filing": f"{deal}.htm", "arm": arm,
            "provider": provider, "model": model, "effort": effort, "replicate": replicate, "timeout_minutes": timeout}


class EffortSweepTests(unittest.TestCase):
    def test_stats_separate_other_scope_bids_and_process_question(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.xlsx"
            book = run_model._openpyxl.Workbook()
            book.active.title = "Deal ledger"
            book.active.append(["#", "Event", "Price low", "Price high", "Date from", "Note"])
            book.active.append([1, "Bid", 10, 10, "d1", "two words"])
            book.active.append([2, "Other-scope bid", None, None, "d2", " ".join(["word"] * 45)])
            book.active.append([3, "Process restarted", None, None, None, None])
            book.create_sheet("Rounds").append(["header"])
            questions = book.create_sheet("Questions")
            questions.append(["Q", "Question", "Rows affected"])
            questions.append(["Q1", "Is the break a new process?", "#3"])
            questions.append(["Q2", "Another issue", "#1"])
            book.create_sheet("Deal facts").append(["header"])
            book.save(path)
            stats = effort_sweep.ledger_stats(path)
        self.assertEqual((stats["bids"], stats["other_scope_bids"]), (1, 1))
        self.assertEqual((stats["note_words_max"], stats["notes_over_40"]), (45, 1))
        self.assertEqual((stats["questions"], stats["questions_counted"], stats["process_question"]), (2, 1, True))

    def make_plan(self, packet, **overrides):
        with contextlib.redirect_stdout(io.StringIO()):
            effort_sweep.plan(plan_args(packet, **overrides))
        return json.loads((packet / "plan.json").read_text())

    def test_plan_interleaves_every_pair_in_each_replicate_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            sweep = self.make_plan(Path(tmp) / "a")
            again = self.make_plan(Path(tmp) / "b")
            other = self.make_plan(Path(tmp) / "c", seed=8)
        cells = sweep["cells"]
        self.assertEqual(cells, again["cells"])  # the seed fixes the order
        self.assertNotEqual([c["id"] for c in cells], [c["id"] for c in other["cells"]])
        self.assertEqual(len(cells), 12)
        blocks = [[(c["deal"], c["arm"]) for c in cells if c["replicate"] == replicate] for replicate in (1, 2)]
        unshuffled = [(d, a) for d in ("kraton", "penford") for a in ("opus-5-5-medium", "opus-5-5-high", "gpt-6-sol-high")]
        for block in blocks:
            self.assertEqual(sorted(block), sorted(unshuffled))
        self.assertNotEqual(blocks[0], blocks[1])
        self.assertFalse(all(block == unshuffled for block in blocks))
        self.assertEqual({c["timeout_minutes"] for c in cells}, {120})
        self.assertEqual(cells[0]["filing"], effort_sweep.filings()[cells[0]["deal"]]["filing"])
        sol = [c for c in cells if c["provider"] == "sol"]
        self.assertEqual({(c["model"], c["effort"], c["arm"]) for c in sol}, {("gpt-6-sol", "high", "gpt-6-sol-high")})
        self.assertTrue(all(c["id"] == f"{c['deal']}-{c['arm']}-r{c['replicate']}" for c in cells))

    def test_plan_pins_candidate_instruction_and_added_filing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.md"
            candidate.write_text("candidate instruction")
            added = root / "zep"
            added.mkdir()
            (added / "filing.htm").write_text("synthetic filing")
            with contextlib.redirect_stdout(io.StringIO()):
                effort_sweep.plan(plan_args(root / "packet", deals="zep", arms=["opus:claude-opus-5-5:medium"],
                                            replicates=1, filing_dir=[str(added)], instruction=str(candidate)))
            sweep = json.loads((root / "packet/plan.json").read_text())
            self.assertEqual(sweep["instruction"], {"path": str(candidate.resolve()), "sha256": run_model.sha256(candidate)})
            self.assertEqual((sweep["cells"][0]["filing"], sweep["cells"][0]["filing_dir"]),
                             ("filing.htm", str(added.resolve())))

    def test_plan_rejects_unknown_values_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            for bad, message in ((dict(deals="nosuchdeal"), "not an available"),
                                 (dict(arms=["opus:claude-opus-5-5:extreme"]), "not an available"),
                                 (dict(arms=["opus:claude-sonnet-5:high"]), "not an available"),
                                 (dict(arms=["sol:gpt-6-sol:ultra"]), "not an available"),
                                 (dict(arms=["gemini:x:high"]), "not an available"),
                                 (dict(timeout_minutes=5), "--timeout-minutes")):
                with self.subTest(bad=bad), self.assertRaisesRegex(SystemExit, message):
                    effort_sweep.plan(plan_args(Path(tmp) / "bad", **bad))
            self.make_plan(Path(tmp) / "once")
            with self.assertRaisesRegex(SystemExit, "refusing to overwrite"):
                effort_sweep.plan(plan_args(Path(tmp) / "once"))

    def test_the_pin_is_recorded_once_and_drift_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = Path(tmp)

            def live(codex="codex-binary", instruction="instruction"):
                return {"binaries": {"opus": {"path": "/pinned/claude", "sha256": "claude-binary"},
                                     "sol": {"path": "/pinned/codex", "sha256": codex}},
                        "instruction_sha256": instruction, "runner_sha256": "runner"}
            with mock.patch.object(effort_sweep, "current_pin", return_value=live()), \
                    mock.patch.object(effort_sweep.subprocess, "run") as version:
                version.return_value.stdout = "9.9.9\n"
                self.assertEqual(effort_sweep.pin_sweep(packet, {"opus", "sol"})["binaries"]["sol"]["version"], "9.9.9")
                self.assertEqual(effort_sweep.pin_sweep(packet, {"opus", "sol"})["binaries"]["opus"]["sha256"], "claude-binary")
            for changed, message in ((live(instruction="edited"), "instruction_sha256"), (live(codex="updated"), "sol binary")):
                with mock.patch.object(effort_sweep, "current_pin", return_value=changed):
                    with self.assertRaisesRegex(SystemExit, message):
                        effort_sweep.pin_sweep(packet, {"opus", "sol"})

    def test_runner_calls_carry_the_pinned_binaries(self):
        with mock.patch.object(effort_sweep.subprocess, "run") as call:
            effort_sweep.run_command(PIN, "status")
        env = call.call_args.kwargs["env"]
        self.assertEqual((env["SEC_CLAUDE_BIN"], env["SEC_CODEX_BIN"]), ("/pinned/claude", "/pinned/codex"))

    def test_network_web_and_delegation_use_is_found_for_both_providers(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events.jsonl"
            calls = [("Bash", "python3 -c 'import openpyxl'"), ("Bash", "curl -s https://www.sec.gov/x"),
                     ("Read", "https://example.com"), ("Bash", "python3 -c 'import urllib.request'"), ("Agent", "")]
            lines = [json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": name, "input": {"command": command}}]}}) for name, command in calls]
            lines += [json.dumps({"type": "item.completed", "item": item}) for item in (
                {"type": "command_execution", "command": "/bin/bash -lc 'wget http://x'"},
                {"type": "command_execution", "command": "/bin/bash -lc 'ls'"},
                {"type": "web_search", "query": "datalink merger"})]
            events.write_text("\n".join(lines) + "\n")
            found = effort_sweep.audit_events(events)
        self.assertEqual(len(found["network_commands"]), 3)
        self.assertEqual(found["web_or_delegation"], ["Agent", "web_search"])

    def write_run(self, run_dir, cell, bids=(), rounds=2, state="completed", failure=None, sheets=None,
                  usage=True, events=None, **metadata_overrides):
        (run_dir / "extraction").mkdir(parents=True)
        book = run_model._openpyxl.Workbook()
        ledger = book.active
        ledger.title = "Deal ledger"
        ledger.append(["#", "Event", "Price low", "Price high", "Date from", "Note"])
        for number, (low, high, day) in enumerate(bids, 1):
            ledger.append([number, "Bid", low, high, day, "three word note"])
        ledger.append([len(bids) + 1, "NDA signed", None, None, None, "one"])
        for name, count in (("Rounds", rounds), ("Questions", 1), ("Deal facts", 1)):
            if sheets is None or name in sheets:
                sheet = book.create_sheet(name)
                sheet.append(["header"])
                for _ in range(count):
                    sheet.append(["value"])
        book.save(run_dir / "extraction" / f"{cell['deal']}.xlsx")
        run_model.write_json(run_dir / "metadata.json", {
            "mode": "extract", "provider": cell["provider"], "deal": cell["deal"], "filing_name": cell["filing"], "model": cell["model"],
            "effort": cell["effort"], "timeout_seconds": cell["timeout_minutes"] * 60,
            "instruction_sha256": PIN["instruction_sha256"], "runner_sha256": PIN["runner_sha256"], **metadata_overrides})
        run_model.write_json(run_dir / "command.json", {"provider_binary_sha256": PIN["binaries"][cell["provider"]]["sha256"],
                                                        "runner_sha256": PIN["runner_sha256"]})
        run_model.write_json(run_dir / "status.json", {
            "state": state, "failure_reason": failure, "workbook_valid_xlsx": True, "continuations": 0,
            "elapsed_seconds": 100.0,
            "usage": {"tokens": {"input_tokens": 10, "output_tokens": 1_000_000, "cache_read_input_tokens": 1_000_000,
                                 "cache_creation_input_tokens": 1_000_000}, "cost_usd": 12.34} if usage else None,
            "provider": {"served_models": ["claude-opus-5-5"], "thinking_tokens": 600_000, "num_turns": 20,
                         "duration_api_ms": 90_000, "cache_write_1h_tokens": 1_000_000, "cache_write_5m_tokens": 0},
        })
        (run_dir / "events.jsonl").write_text("".join(json.dumps(event) + "\n" for event in events or [{"type": "result"}]))

    def record(self, root, cell, **run):
        self.write_run(root / cell["id"], cell, **run)
        with mock.patch.object(effort_sweep.check_lean, "LeanChecker") as checker:
            checker.return_value.run.return_value = {"summary": {"errors": 0, "warnings": 1}, "issues": []}
            return effort_sweep.record(cell, root / cell["id"], root / "packet", PIN)

    def test_record_copies_receipts_and_checks_outside_the_sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cell = make_cell()
            self.write_run(root / "run", cell, bids=[(10, 10, "2020-01-01")])
            report = {"summary": {"errors": 1, "warnings": 2}, "issues": []}
            with mock.patch.object(effort_sweep.check_lean, "LeanChecker") as checker:
                checker.return_value.run.return_value = report
                receipt = effort_sweep.record(cell, root / "run", root / "packet", PIN)
            dest = root / "packet/runs" / cell["id"]
            self.assertEqual(checker.call_args.args[1], effort_sweep.PROJECT / "raw_filing" / "kraton.htm")
            self.assertEqual((receipt["state"], receipt["check_summary"], receipt["mismatches"]), ("completed", report["summary"], []))
            self.assertTrue((dest / "kraton.xlsx").is_file())
            self.assertEqual(json.loads((dest / "check.json").read_text()), report)
            with gzip.open(dest / "events.jsonl.gz", "rt") as events:
                self.assertIn('"result"', events.read())

    def test_mismatched_runs_are_flagged_and_never_averaged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = self.record(root, make_cell(replicate=1))
            stale = self.record(root, make_cell(replicate=2), effort="high", instruction_sha256="older")
            self.assertEqual(good["mismatches"], [])
            self.assertEqual(stale["mismatches"], ["metadata effort", "metadata instruction_sha256"])
            with contextlib.redirect_stdout(io.StringIO()):
                effort_sweep.summarize(argparse.Namespace(packet=str(root / "packet")))
            low = json.loads((root / "packet/summary.json").read_text())["by_arm"]["opus-5-5-low"]
            self.assertEqual((low["cells"], low["completed"], low["excluded_mismatched"]), (1, 1, 1))

    def test_summary_reprices_every_cell_and_measures_replicate_agreement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs = [("low", 1, [(10, 10, "d1"), (12, 12, "d2")], 2), ("low", 2, [(10, 10, "d1")], 3),
                    ("high", 1, [(10, 10, "d1"), (12, 12, "d2")], 2), ("high", 2, [(10, 10, "d1"), (12, 12, "d2")], 2)]
            for effort, replicate, bids, rounds in runs:
                self.record(root, make_cell(effort=effort, replicate=replicate), bids=bids, rounds=rounds)
            # A workbook without the four sheets and a timed-out run must not break the summary.
            self.record(root, make_cell(effort="high", replicate=3), state="failed", failure="workbook_incomplete",
                        sheets=("Rounds",))
            killed = [{"type": "assistant", "message": {"id": "m1", "usage": {"output_tokens": 500_000,
                       "cache_creation": {"ephemeral_1h_input_tokens": 0}}}}] * 2
            self.record(root, make_cell(effort="high", replicate=4), state="timed_out", failure="timeout",
                        usage=False, events=killed)
            run_model.write_json(root / "packet/grades.json", {"kraton-opus-5-5-high-r1": {"score": 90},
                                                              "kraton-opus-5-5-high-r2": {"score": 80}})
            with contextlib.redirect_stdout(io.StringIO()) as table:
                effort_sweep.summarize(argparse.Namespace(packet=str(root / "packet")))
            summary = json.loads((root / "packet/summary.json").read_text())
        rows = {row["id"]: row for row in summary["runs"]}
        # 1M output at $20, 1M cache reads at $0.20, 1M one-hour writes at $8, 10 input tokens at $4/M.
        self.assertAlmostEqual(rows["kraton-opus-5-5-low-r1"]["cost_repriced"], 28.2, places=3)
        timed_out = rows["kraton-opus-5-5-high-r4"]
        self.assertEqual((timed_out["cost_repriced"], timed_out["cost_is_partial"]), (10.0, True))  # one message, counted once
        low, high = summary["by_arm"]["opus-5-5-low"], summary["by_arm"]["opus-5-5-high"]
        self.assertEqual((low["mean_bid_jaccard"], low["mean_bid_count_gap"], low["same_round_count_share"]), (0.5, 1, 0.0))
        self.assertEqual((high["mean_bid_jaccard"], high["same_round_count_share"], high["mean_score"]), (1.0, 1.0, 85))
        self.assertEqual((high["cells"], high["completed"]), (4, 2))
        self.assertAlmostEqual(high["total_spend_repriced"], 28.2 * 3 + 10.0, places=2)
        self.assertAlmostEqual(high["spend_per_completed"], (28.2 * 3 + 10.0) / 2, places=2)
        self.assertEqual(high["mean_thinking_tokens"], 600_000)
        self.assertIn("| opus-5-5-high |", table.getvalue())

    def test_repeated_provider_failures_stop_new_cells_and_can_be_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet, runs = root / "packet", root / "runs"
            cells = [make_cell(effort=effort) for effort in ("low", "medium", "high", "xhigh")]
            packet.mkdir()
            run_model.write_json(packet / "plan.json", {"cells": cells})
            launched = []

            def fake_runner(pin, *argv):
                run_dir = Path(argv[argv.index("--run-dir") + 1])
                cell = next(c for c in cells if c["id"] == run_dir.name)
                if argv[0] == "prepare":
                    self.write_run(run_dir, cell, state="running")
                    (run_dir / "status.json").unlink()
                else:
                    launched.append(cell["id"])
                    run_model.write_json(run_dir / "status.json", {"state": "failed", "failure_reason": "provider_exit"})

            args = argparse.Namespace(packet=str(packet), runs_dir=str(runs), only=None, concurrency=1, poll=0,
                                      retry_failed=False)
            with mock.patch.object(effort_sweep, "pin_sweep", return_value=PIN), \
                    mock.patch.object(effort_sweep, "current_pin", return_value={**PIN, "binaries": {"opus": {"path": "/pinned/claude", "sha256": "claude-binary"}}}), \
                    mock.patch.object(effort_sweep, "run_command", side_effect=fake_runner), \
                    contextlib.redirect_stdout(io.StringIO()):
                effort_sweep.run(args)
                self.assertEqual(len(launched), effort_sweep.MAX_CONSECUTIVE_RETRYABLE)
                args.retry_failed = True
                effort_sweep.run(args)
            self.assertEqual(len(list((packet / "retried").iterdir())), effort_sweep.MAX_CONSECUTIVE_RETRYABLE)
            self.assertTrue(all((runs / "retried" / f"{cell_id}-attempt1").is_dir() for cell_id in launched[:3]))


if __name__ == "__main__":
    unittest.main()
