"""Portable read-only verification of exact author and independent review inputs.

The independent review seal retains its original logical roots. Resolve them
without duplicating the complete proof tree or changing any sealed manifest.
"""
from pathlib import Path, PurePosixPath
import hashlib, json
P=Path(__file__).resolve().parents[2]
R=P/'verification/coordinator-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ident(p):return {'sha256':sha(p),'bytes':p.stat().st_size}
def load(p):return json.loads(p.read_text())
def safe(p):
    q=p.resolve();assert q.is_relative_to(P.resolve()) and q.is_file() and not p.is_symlink(),str(p)
    return p
wrappers=load(P/'verification/candidate-package/ARCHIVE-MAP.json')['wrapper_archives']
def original(name,r):
    w=wrappers.get(name)
    if w and r['sha256']==w['expected']['sha256']:
        assert r==w['expected'];return safe(P/w['archive'])
    return safe(P/name)
def author(name):
    if name.startswith('lean/'):return safe(P/name[5:])
    return safe(R/'author-external'/name)
outer=R/'independent-packaging/EVIDENCE-MANIFEST.json'
assert sha(outer)=='a44510a7778510a7fd2988278fd8cdd0eeab07e92895f247848a4ddabd88312e'
d=load(outer);assert d['exact_self_exclusion']=='evidence/EVIDENCE-MANIFEST.json'
counts={k:0 for k in ['evidence','author_package','original']}
for n,r in d['files'].items():
    root,name=n.split('/',1);assert str(PurePosixPath(name))==name
    if root=='evidence':q=safe(R/'independent-packaging'/name)
    elif root=='author_package':q=author(name)
    elif root=='original':q=original(name,r)
    else:raise AssertionError(root)
    assert ident(q)==r,(n,str(q));counts[root]+=1
assert counts==d['root_file_counts'] and sum(counts.values())==d['file_count']==4854
actual={str(q.relative_to(R/'independent-packaging')) for q in (R/'independent-packaging').rglob('*') if q.is_file()}
assert actual=={n[9:] for n in d['files'] if n.startswith('evidence/')}|{'EVIDENCE-MANIFEST.json'}
authorseal=R/'author-external/AUTHOR-HANDOFF-MANIFEST.json'
assert sha(authorseal)=='5e809e2ef80cd790ca08736ff705dab2fc5a854ee96b09a719c6bc01282777c8'
ad=load(authorseal)
for n,r in ad['files'].items():assert ident(author(n))==r,n
candidate=load(P/'verification/candidate-inputs.json')
assert len(candidate['files'])==2404 and candidate['exact_self_exclusion']=='verification/candidate-inputs.json'
for n,r in candidate['files'].items():assert ident(safe(P/n))==r,n
for n,r in load(R/'installed-external-inputs.json').items():assert ident(safe(P/n))==r,n
assert sha(R/'independent-packaging/REPORT.md')=='c14f6635b8e702fde6217b92bd49cfe25d2b693c191570fcadd0e4bb4dd681a3'
print(json.dumps({'status':'PASS installed unchanged exact author and independent packaging evidence',
    'independent_review_members':4854,'root_counts':counts,'candidate_fixed_members':2404,
    'candidate_outer_sha256':sha(P/'verification/candidate-inputs.json'),
    'independent_report_sha256':sha(R/'independent-packaging/REPORT.md'),
    'independent_verdict':'APPROVE concrete packaging only', 'actual_Linux_Comparator':'pending'},indent=2))
