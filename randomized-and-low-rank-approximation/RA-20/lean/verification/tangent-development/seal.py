"""Bind complete tangent evidence, its immutable Algebra closure and prior manifests."""
from pathlib import Path
import datetime, hashlib, json, os
E = Path(__file__).resolve().parent
P = E.parents[1]
A = P/'verification/algebra-development'
M = E/'EVIDENCE-MANIFEST.json'
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
files = {f.resolve() for f in E.rglob('*') if f.is_file() and f != M}
files.add((P/'NLA/RA20/Tangent.lean').resolve())
files.add((A/'EVIDENCE-MANIFEST.json').resolve())
for n,v in json.loads((A/'EVIDENCE-MANIFEST.json').read_text())['files'].items():
    f = (A/n).resolve()
    assert f.is_relative_to(P) and sha(f) == v['sha256'], n
    files.add(f)
assert M.resolve() not in files
rows = {os.path.relpath(f,E): {'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(files)}
inside = sum(f.is_relative_to(E) for f in files)
r = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'scope':'RA20 author tangent helper contract4, local macOS only',
     'owner':'/root/formal_review_standards',
     'inventory_rule':'All own evidence, helper and complete sealed Algebra input closure, retaining nested manifests. Exclude only this exact outer manifest from its own inventory.',
     'file_count':len(rows),'own_evidence_files':inside,'bound_input_files':len(rows)-inside,'files':rows}
M.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(M),'files':len(rows),'own':inside,'inputs':len(rows)-inside,'handoff_sha256':sha(E/'HANDOFF.md')}))
