"""Read-only verification of the scoped RA20 differential seal and full input closure."""
from pathlib import Path
import hashlib,json,os
E=Path(__file__).resolve().parent;P=E.parents[1];M=E/'EVIDENCE-MANIFEST.json'
load=lambda f:json.loads(f.read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=load(M)
for n,v in m['files'].items():
 f=E/n;assert f.is_file() and sha(f)==v['sha256'] and f.stat().st_size==v['bytes'],n
actual={str(f.relative_to(E)) for f in E.rglob('*') if f.is_file() and f!=M}
inside={n for n in m['files'] if not n.startswith('../')}
assert actual==inside and len(inside)==m['own_evidence_files']
frozen=load(P/'reviews/statement-freeze.json')
expected={P/n for n in frozen['files']}
expected|={P/n for n in ['NLA/RA20/Differential.lean','verification/proof-start.json','verification/implementation-roles.json','reviews/statement-freeze.json']}
for name,base in [('reviews/statement-package-manifest.json',P),
 ('reviews/statement-referee-1-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-1-evidence'),
 ('reviews/statement-referee-2-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-2-evidence')]:
 expected.add(P/name)
 for n,v in load(P/name)['files'].items():
  f=(base/n).resolve();assert sha(f)==(v if isinstance(v,str) else v['sha256']);expected.add(f)
expected={os.path.relpath(f.resolve(),E) for f in expected}
assert {n for n in m['files'] if n.startswith('../')}==expected
for n,h in frozen['source_files'].items():
 f=P/'verification/original-sources'/n;b=f.read_bytes()
 assert sha(f)==h and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==frozen['source_git_blobs'][n]
assert len(m['files'])==m['file_count']==m['own_evidence_files']+m['bound_input_files']
assert 'EVIDENCE-MANIFEST.json' not in m['files']
c=load(E/'owned-prefix-cleanup.json');assert c['removed'] and not Path(c['prefix']).exists()
print(json.dumps({'status':'PASS','files':len(m['files']),'own_evidence_files':len(inside),'bound_input_files':len(expected),'original_source_blobs':len(frozen['source_files']),'manifest_sha256':sha(M),'helper_sha256':sha(P/'NLA/RA20/Differential.lean'),'handoff_sha256':sha(E/'HANDOFF.md')}))
