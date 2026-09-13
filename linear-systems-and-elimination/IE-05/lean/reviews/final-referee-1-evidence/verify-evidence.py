from pathlib import Path
import hashlib,json
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[1];OUTER=OWN/'EVIDENCE-MANIFEST.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads(OUTER.read_text());freeze=json.loads((ROOT/d['proof_freeze']).read_text())
assert d['exact_self_exclusion']==str(OUTER.relative_to(ROOT)) and d['frozen_input_count']==1800
own={str(p.relative_to(ROOT)) for p in OWN.rglob('*') if p.is_file() and p!=OUTER}
expected=set(freeze['files'])|own|{d['report'],d['proof_freeze']}
assert set(d['files'])==expected and len(expected)==d['file_count']
assert len(own)==d['own_evidence_file_count']
assert not any(p.startswith('reviews/final-referee-2') for p in d['files'])
for rel,v in d['files'].items():
    p=ROOT/rel
    assert not p.is_symlink() and p.is_file() and p.resolve().is_relative_to(ROOT)
    assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes'],rel
for rel,h in freeze['files'].items():assert d['files'][rel]['sha256']==h
assert not list((OWN/'attempt-001/objects').iterdir())
print('VERIFIED',d['file_count'],'exact sealed files; outer SHA-256',sha(OUTER))
