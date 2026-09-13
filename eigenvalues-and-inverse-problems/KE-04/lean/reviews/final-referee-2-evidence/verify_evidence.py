"""Read-only verification of this exact review seal; later additions permitted."""
from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent;P=E.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
d=json.loads((E/'EVIDENCE-MANIFEST.json').read_text())
for rel,r in d['files'].items():
    p=P/rel
    assert p.is_file(),rel
    assert p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256'],rel
assert str((E/'EVIDENCE-MANIFEST.json').relative_to(P)) not in d['files']
print(json.dumps({'verified_bound_files':len(d['files']),'report_sha256':d['report_sha256'],'success':True}))
