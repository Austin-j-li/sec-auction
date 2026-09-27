1. **Major — Missing D18 price crosswalk.** [_dev/tools/diff_workbooks.py:65](/Users/austinli/Projects/sec-auction/_dev/tools/diff_workbooks.py:65). A legacy Other-scope bid priced at 10 compared with blank modern prices produces two ordinary price changes. VM evidence explicitly requires these blanks to be counted, not listed, under D18. **Fix:** restore the D18 suppression and summary count, with regression coverage in both comparison directions.

2. **Minor — Deadline crosswalk is unreachable.** [_dev/tools/diff_workbooks.py:160](/Users/austinli/Projects/sec-auction/_dev/tools/diff_workbooks.py:160). Crosswalk processing requires Deal-ledger headers, so it never reaches `Rounds.Deadline outcome`. Reproduced: `Late bids accepted` → `Extended (late bid accepted)` lacks the evidenced **“D11 (wider)”** label. **Fix:** pass workbook-level schema direction into the Rounds comparison and restore that label.

Both findings are supported by [/tmp/recov/all_calls_since_0924.jsonl:1110](/tmp/recov/all_calls_since_0924.jsonl:1110), the main-tree README read at **2026-09-26T20:45:16.451Z**.

Verification: both Mac-Gray comparisons reproduced the reported 816/593 lines; the fresh checker returned 0 errors/2 warnings; runner help confirmed Opus 5.5 medium. Findings rendering passed with an in-memory output sink. Full pytest verification was blocked by temporary-file restrictions: 65 tests failed on unavailable writable temporary storage; 3 tests and 8 subtests passed. No files were changed.

**ACCEPT-WITH-FIXES**