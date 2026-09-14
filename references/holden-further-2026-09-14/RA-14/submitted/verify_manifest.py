from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
failures=[]
for entry in manifest['files']:
    p=ROOT/entry['path']
    if not p.is_file():failures.append((entry['path'],'missing'));continue
    data=p.read_bytes()
    if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
        failures.append((entry['path'],'mismatch'))
if failures:
    print(json.dumps(failures,indent=2));sys.exit(1)
print(f"Verified {len(manifest['files'])} file hashes. This is byte integrity, not a proof certificate.")
