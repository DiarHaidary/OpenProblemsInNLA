"""Read-only verification of the full scoped conclusion evidence closure."""
from pathlib import Path
import hashlib,json,os
E=Path(__file__).resolve().parent;P=E.parents[1];M=E/'EVIDENCE-MANIFEST.json'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=json.loads(M.read_text())
for n,v in m['files'].items():
    f=E/n;assert f.is_file() and sha(f)==v['sha256'] and f.stat().st_size==v['bytes'],n
actual={str(f.relative_to(E)) for f in E.rglob('*') if f.is_file() and f!=M}
inside={n for n in m['files'] if not n.startswith('../')}
assert actual==inside and len(inside)==m['own_evidence_files']
expected={(P/n).resolve() for n in ['NLA/RA20/Count.lean','NLA/RA20/Proof.lean','Solution.lean']}
assert len(m['prior_manifests'])==7
for record in m['prior_manifests']:
    mf=P/record['manifest'];assert sha(mf)==record['sha256']
    old=json.loads(mf.read_text());assert len(old['files'])==record['bound_files'];expected.add(mf.resolve())
    for n,v in old['files'].items():
        f=(mf.parent/n).resolve();h=v if isinstance(v,str) else v['sha256']
        assert sha(f)==h,(record['manifest'],n);expected.add(f)
assert {n for n in m['files'] if n.startswith('../')}=={os.path.relpath(f,E) for f in expected}
frozen=json.loads((P/'reviews/statement-freeze.json').read_text())
for n,h in frozen['files'].items():assert sha(P/n)==h,n
for n,h in frozen['source_files'].items():
    b=(P/'verification/original-sources'/n).read_bytes()
    assert hashlib.sha256(b).hexdigest()==h,n
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==frozen['source_git_blobs'][n],n
assert len(m['files'])==m['file_count']==m['own_evidence_files']+m['bound_input_files']
assert 'EVIDENCE-MANIFEST.json' not in m['files']
cleanup=json.loads((E/'owned-prefix-cleanup.json').read_text())
assert cleanup['removed'] and cleanup['postcheck_all_absent']
assert all(not Path(r['prefix']).exists() for r in cleanup['roots'])
print(json.dumps({'status':'PASS','bound_files':len(m['files']),'own_files':len(inside),'input_files':len(expected),'prior_manifests':len(m['prior_manifests']),'manifest_sha256':sha(M),'handoff_sha256':sha(E/'HANDOFF.md'),'validation_sha256':sha(E/'validation.json')}))
