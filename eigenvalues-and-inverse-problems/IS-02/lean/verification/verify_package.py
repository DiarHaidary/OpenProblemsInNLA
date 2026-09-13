"""Check the current portable package inventory and completed-proof metadata.

Run from a full repository checkout with tools/lean/requirements.txt installed.
This checks file identity and metadata, not mathematical truth or Linux results.
The live inventory is refreshed explicitly when publication evidence is added;
immutable reviewed mathematical hashes remain in reviews/*ACCEPTANCE.json.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
project = Path(__file__).resolve().parents[1]
inventory = project / "verification/package-inputs.json"
expected = json.loads(inventory.read_text())["files"]
actual = {}
for path in sorted(project.rglob("*")):
    rel = path.relative_to(project)
    if path.is_symlink():
        raise SystemExit(f"Unexpected symlink: {rel}")
    if not path.is_file() or path == inventory:
        continue
    if any(part in {".lake", "__pycache__"} for part in rel.parts) or path.suffix in {
        ".olean", ".ilean", ".pyc", ".o", ".so", ".a"
    }:
        raise SystemExit(f"Unexpected generated artifact: {rel}")
    actual[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit("Package inventory mismatch; inspect missing, changed or added files")
for name in ("STATEMENT-ACCEPTANCE.json", "FINAL-ACCEPTANCE.json"):
    receipt = json.loads((project / "reviews" / name).read_text())
    for file, digest in receipt["boundary_files"].items():
        if actual[file] != digest:
            raise SystemExit(f"Reviewed mathematical boundary changed: {file}")
repository = project.parents[2]
subprocess.run(
    [sys.executable, str(repository / "tools/lean/validate_manifest.py"), str(project)],
    check=True,
)
print(f"Current package and reviewed source inventories: PASS ({len(actual)} files)")
