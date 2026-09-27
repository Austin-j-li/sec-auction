1. **Minor — incorrect replay evidence pointer.** [/tmp/recov/reports/A_checker.md:5](/tmp/recov/reports/A_checker.md:5) lists `19:17:40` as a checker edit. The actual edit adding `is_process_question` occurred at **2026-09-26T19:16:09.121Z**, JSONL line **844**. The 19:17:40 call created `retest_acceptance.py`. **Fix:** correct the timestamp; no code change is needed.

Independent verification found no recovery defects: both files match the evidence replay, apart from a trailing newline in the checker. All **21** cockpit versions match summaries and complete issue details; all **14** legacy versions also match checker `679d4fc`.

The pytest rerun was blocked by the read-only sandbox’s inability to create temporary fixtures. I could not independently confirm the reported 57-test pass.

**ACCEPT-WITH-FIXES**