"""Summaries for RESULTS.md from saved results; no network."""
import json, glob, statistics
from collections import Counter
from pathlib import Path
H = Path(__file__).resolve().parent
for f in ["results_price.json", "results_price_leadin.json", "results_price_wide8.json"]:
    R = json.loads((H / f).read_text()); print("==", f)
    for v in ["orig", "swap_same_party", "swap_near_party"]:
        S = [r for r in R if r["variant"] == v]
        print(f"  {v:16} n={len(S):3} scoped={dict(Counter(r['scoped'] for r in S))} actor_only_yes={sum(r['actor_only'] >= .5 for r in S)}")
    pl = [r["scoped_conf"] for r in R if r["variant"] != "orig"]; print("  planted confidence min", min(pl))
O = json.loads((H / "results_omit.json").read_text())
print("== omission queue per workbook (none / none>=0.75 / none>=0.9 of tagged sentences)")
for d in ["mac-gray", "petsmart", "providence-worcester"]:
    for m in ["opus", "sol", "deepseek"]:
        X = [r for r in O if r["deal"] == d and r["model"] == m]; N = [r for r in X if r["choice"] == "none"]
        print(f"  {d:22}{m:9} {len(N):2} / {sum(r['confidence'] >= .75 for r in N):2} / {sum(r['confidence'] >= .9 for r in N):2} of {len(X)}")
raw = [json.loads(Path(f).read_text()) for f in glob.glob(str(H / "raw/*.json"))]
tok = sum(r["response"]["usage"]["input_tokens"] for r in raw)
print(f"== {len(raw)} calls, {tok} input tokens, ${tok * 0.042 / 1e6:.3f} at $0.042/M, median latency {statistics.median(r['latency_s'] for r in raw):.2f}s")
