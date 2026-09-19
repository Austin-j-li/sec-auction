# TypeSafe follow-up experiments

Read `RESULTS.md` for conclusions and proposed changes. This is a research harness, not a production checker. It never writes an extraction workbook or edits the working instruction.

Files:

- `PLAN.md`: scope and first-phase evaluation rules recorded before API calls.
- `cases.json`: frozen first-phase cases, exact source packets, assistant-authored labels, filing hashes and questions.
- `raw/`, `run.json`: credential-free requests/responses, usage, latencies and status attempts.
- `ablation_cases.json`, `ablation_raw/`, `ablation_run.json`: adaptive diagnostic comparison designed after observing the first phase; not a holdout.
- `summary.json`: metrics, failure records and descriptive overall-condition outputs.
- `docs/`: live official documentation snapshots used to design the tests.

Requirements are Python, `httpx`, `beautifulsoup4`, and `lxml`, available in the current environment. From the repository root:

```bash
python _dev/typesafe_followup_2026-09-19/experiment.py run
python _dev/typesafe_followup_2026-09-19/experiment.py run --phase ablation
python _dev/typesafe_followup_2026-09-19/analyze.py
```

The runner reads `TYPESAFE_API_KEY`, or prompts without echoing it. It saves no credential. Existing identical requests replay their saved responses; no fresh API call is made for cached requests. An API key prompt still occurs on fully cached runs. `analyze.py` requires no credential and performs no network requests.

To rebuild first-phase cases from the raw filings, use `experiment.py build`; to rebuild the second phase, use `build_ablation.py`. Rebuilding replaces the case manifests; preserve the originals when changing the experiment. `--repeat` selects a separate cache for an explicit first-phase repeat, not a cache bypass on subsequent repeats. No repeat was run for this report.

Paragraph IDs are zero-based indices in this harness's normalized HTML paragraph list, not SEC page or official paragraph numbers. Each request contains the source text itself. These tests were authored from publicly available filings and synthetic candidate rows. They are not a new clean extraction, blind human grading, or a measurement of reviewer time saved.
