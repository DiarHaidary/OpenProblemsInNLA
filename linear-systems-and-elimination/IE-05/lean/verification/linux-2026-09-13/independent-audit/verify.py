#!/usr/bin/env python3
"""Read-only validation of the complete IE05 operational evidence seal."""
from pathlib import Path
import hashlib,json,zipfile
E=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate JSON key: '+k)
        d[k]=v
    return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
m=load(E/'EVIDENCE-MANIFEST.json')
assert m['exact_self_exclusion']=='EVIDENCE-MANIFEST.json'
actual={str(p.relative_to(E)) for p in E.rglob('*') if p.is_file() and p!=E/'EVIDENCE-MANIFEST.json'}
assert actual==set(m['files']) and len(actual)==m['file_count']
for n,r in m['files'].items():
    p=E/n;assert p.resolve().is_relative_to(E.resolve()) and not p.is_symlink()
    assert digest(p)==r['sha256'] and p.stat().st_size==r['bytes'],n
latest=load(E/'AUDIT-LATEST.json');result=E/latest['directory']/'result.json'
assert digest(result)==latest['result']['sha256'] and load(result)['success'] is True
report=E/'OPERATIONAL-REVIEW.md';f=load(E/'FINAL.json')
assert digest(report)==f['report_sha256'] and f['candidate_commit']=='71cf72f9db2af0f01b5cfa7f18a69e28310eb52f' and f['attempt']==1
assert f['verdict']=='PASS: IE-05 operational verification only'
d=E/'downloads-dk41f3yi';md=load(E/'api-jlvyv9bw/artifacts.json')
for name in ['lean-IE-05','lean-checker-controls']:
    a=next(a for a in md['artifacts'] if a['name']==name);z=d/(name+'.zip')
    assert a['digest']=='sha256:'+digest(z) and a['size_in_bytes']==z.stat().st_size
    with zipfile.ZipFile(z) as zz:
        assert zz.testzip() is None
        members={i.filename for i in zz.infolist() if not i.is_dir()}
        assert members=={str(p.relative_to(d/name)) for p in (d/name).rglob('*') if p.is_file()}
        for n in members:assert zz.read(n)==(d/name/n).read_bytes()
print(json.dumps({'verdict':'PASS','bound_files':len(actual),'candidate_inputs':2543,'attempt':1,'report_sha256':digest(report),'outer_sha256':digest(E/'EVIDENCE-MANIFEST.json')},indent=2))
