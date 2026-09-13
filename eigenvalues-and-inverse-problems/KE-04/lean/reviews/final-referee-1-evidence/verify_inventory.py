"""Read-only verification of this final review's exact historical membership."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
outer=E/'EVIDENCE-MANIFEST.json';d=json.loads(outer.read_text())
assert d['exact_self_exclusion']==str(outer.relative_to(P))
assert str(outer.relative_to(P)) not in d['files']
for rel,r in d['files'].items():
    p=P/rel;assert not p.is_symlink() and sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],rel
own={str(f.relative_to(P)) for f in E.rglob('*') if f.is_file() and f!=outer}
sealed_own={rel for rel in d['files'] if rel.startswith(str(E.relative_to(P))+'/')}
assert own==sealed_own
assert sha(P/'reviews/proof-freeze.json')==d['proof_freeze_sha256']
print(json.dumps({'success':True,'checked_files':len(d['files']),'exact_own_membership':True,
    'manifest_sha256':sha(outer),'scope':'This exact frozen review; subsequent other-reviewer/packaging additions are permitted and are not claimed as reviewed'},indent=2))
