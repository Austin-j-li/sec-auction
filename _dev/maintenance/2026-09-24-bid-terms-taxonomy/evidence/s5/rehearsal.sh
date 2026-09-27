set -u
R=$TMPDIR/rehearse; rm -rf $R $TMPDIR/rh-*.json && rsync -a --exclude node_modules --exclude __pycache__ /home/uctpiaj/work/tmp/v114-scratch/pkg/s5/ $R/ && cd $R
echo "== deploy state, in place: verify, then a second run to the same output"
python3 _dev/tools/cockpit/verify_catalog.py --root $R --output $TMPDIR/rh-deploy.json; echo "exit=$?"
python3 _dev/tools/cockpit/verify_catalog.py --root $R --output $TMPDIR/rh-deploy.json; echo "exit=$? (2 = refused)"
echo "== step 2: move the nine workbooks"
W=_dev/reviews/2026-09-22-opus55-reextraction/workbooks; mkdir -p $W
for d in datalink kraton mac-gray meredith penford petsmart providence-worcester stec synacor; do mv extraction/$d.xlsx $W/$d.xlsx; done
ls extraction
echo "== step 3: repoint the catalog paths"
cp _dev/cockpit/catalog.json $TMPDIR/rh-catalog-before.json
python3 - <<'EOF'
import json
from pathlib import Path
path = Path("_dev/cockpit/catalog.json")
catalog = json.loads(path.read_text(encoding="utf-8"))
for slug, item in catalog["deals"].items():
    for version in item["versions"]:
        if version["id"] == "opus55-medium" and version["path"] == f"extraction/{slug}.xlsx":
            version["path"] = f"_dev/reviews/2026-09-22-opus55-reextraction/workbooks/{slug}.xlsx"
path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
EOF
diff $TMPDIR/rh-catalog-before.json _dev/cockpit/catalog.json | grep '^[<>]'
echo "== deploy-state lookup with extraction/ empty"
python3 -c "import sys; sys.path.insert(0, '_dev/tools'); from pathlib import Path; from cockpit import data; print(data.Cockpit(Path('.')).slugs())"
echo "== step 4: apply the release patch"
git apply --check $TMPDIR/d25/d25-tools.patch && git apply $TMPDIR/d25/d25-tools.patch && echo applied
python3 _dev/tools/cockpit/import_results.py --root $R --output $TMPDIR/rh-import.json
python3 -c "import json; print('importer catalog equals repointed catalog:', json.load(open('$TMPDIR/rh-import.json')) == json.load(open('_dev/cockpit/catalog.json')))"
echo "== step 5: export dry run"
python3 _dev/tools/cockpit/export_repo.py --repo-root $R deal kraton --version working; echo "exit=$?"
echo "== step 6: verify"
python3 _dev/tools/cockpit/verify_catalog.py --root $R; echo "exit=$?"
ls _dev/reviews/2026-09-22-opus55-reextraction/
