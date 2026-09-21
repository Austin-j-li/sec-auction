# Report implementation and validation notes

The primary question is whether the eight completed v1.11 extractions can support research on bidder participation, rounds, formality, information, event order and prices. This is a technical validation report for the researcher. It is not a new extraction, a causal analysis, or an estimate of generalization accuracy.

Report structure follows the technical reporting specification: verdict; supported findings; convention choices and counterexamples; scope/provenance and methods; next corrections and questions; validation limits. Case evidence and independent challenges follow the synthesis. No global accuracy score is defined because a complete gold standard is absent.

The single coverage chart uses the verified workbook profile. Grain: one of eight current workbooks. Measure: nonempty Deal ledger rows excluding the header, summed to 473. It describes inspection coverage, not accuracy or the true number of source events. A horizontal bar chart has eight observations, one blue palette root, zero-based quantitative axis, long case labels and direct values. Round/question counts remain available in the source verification file. The comparison table carries qualitative verdicts and source-provenance categories; its ordering is a reading order, not a numerical quality score. All defect evidence is textual and cell-level, so an error-rate chart would be misleading.

Source hierarchy: supplied filing for facts; operative v1.11 for compliance; direct newer Alex voice for intended economic interpretation; older personally edited versus inherited RA rows identified explicitly; historical Claude summary treated only as context. No external web lookup or historical model grading was used.

Preparation uses deterministic, read-only DOCX XML, HTML and XLSX exports and PDF text extraction. Text exports do not evaluate visual layout. The reference audit inspected original workbook font colors and DOCX run colors. Source hashes and byte identity against the checked run workbook justify reusing the existing mechanical reports without a repeated checker run. All substantive conclusions come from the case reviews and targeted challenges, not from mechanical validation.

Deliverable mode: local self-contained HTML from the canonical artifact contract, plus readable source review records. The existing data-analytics portable builder validates payload, provenance and rendering. Its widget contract requires SQL provenance: the generator executes the disclosed SQLite queries over the two local JSON inputs to project the chart and table. Those queries present the reviewed judgments and counts; they do not independently validate substantive correctness. No website is published and no local server is required.

## Delivery validation result

The Markdown index and linked case reports are the primary deliverable. Canonical artifact validation and HTML packaging passed, but automatic browser verification was structural-only because no default headless-shell was available. An explicit attempt using the installed VM Chrome failed the builder's requested browser-environment check. No plugin or browser configuration was changed to bypass that check.

A separate check opened the HTML in the existing visible VM Chrome session. All eight case headings and the coverage chart rendered, the chart showed the correct eight row counts, and a reload produced no page-script errors. However, a chart options button was blocked by overlapping native viewer controls, and visual inspection found an unintended paragraph/list split. The HTML is therefore a preview, not a fully verified report reader; source-dialog, mobile-layout and interaction checks are not certified. The Markdown records do not depend on that viewer.

Final source-hash verification passed and all reviewed inputs remained unchanged. The repository-wide `git diff --check` reported pre-existing CRLF trailing-whitespace entries in `raw_filing/MANIFEST.csv`; those unrelated entries were left untouched.
