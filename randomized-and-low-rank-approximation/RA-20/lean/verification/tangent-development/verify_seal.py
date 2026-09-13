"""Read-only verification of every tangent and nested input byte."""
from pathlib import Path
import hashlib, json, os
E = Path(__file__).resolve().parent
P = E.parents[1]
A = P/'verification/algebra-development'
M = E/'EVIDENCE-MANIFEST.json'
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
m = json.loads(M.read_text())
for n,v in m['files'].items():
    f = E/n
    assert f.is_file() and sha(f)==v['sha256'] and f.stat().st_size==v['bytes'], n
actual = {str(f.relative_to(E)) for f in E.rglob('*') if f.is_file() and f!=M}
inside = {n for n in m['files'] if not n.startswith('../')}
assert actual==inside and len(inside)==m['own_evidence_files']
expected = {(P/'NLA/RA20/Tangent.lean').resolve(), (A/'EVIDENCE-MANIFEST.json').resolve()}
for n,v in json.loads((A/'EVIDENCE-MANIFEST.json').read_text())['files'].items():
    f = (A/n).resolve()
    assert sha(f)==v['sha256'], n
    expected.add(f)
assert {n for n in m['files'] if n.startswith('../')} == {os.path.relpath(f,E) for f in expected}
frozen = json.loads((P/'reviews/statement-freeze.json').read_text())
for n,h in frozen['files'].items(): assert sha(P/n)==h, n
for n,h in frozen['source_files'].items():
    b = (P/'verification/original-sources'/n).read_bytes()
    assert hashlib.sha256(b).hexdigest()==h, n
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==frozen['source_git_blobs'][n], n
assert len(m['files'])==m['file_count']==m['own_evidence_files']+m['bound_input_files']
assert 'EVIDENCE-MANIFEST.json' not in m['files']
print(json.dumps({'status':'PASS','files':len(m['files']),'own_evidence_files':len(inside),'bound_input_files':len(expected),'manifest_sha256':sha(M),'helper_sha256':sha(P/'NLA/RA20/Tangent.lean'),'handoff_sha256':sha(E/'HANDOFF.md')}))
