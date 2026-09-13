#!/usr/bin/env python3
"""Read-only verification of the complete sealed first-referee phase.

This checks exact project membership at that phase. Later independently owned
phase additions must receive a new enclosing inventory; do not rewrite this one.
It does not run Lean, download dependencies, or claim a Linux/Comparator result.
"""
from pathlib import Path
import hashlib, json

E=Path(__file__).resolve().parent
K=E.parent.parent
OUTER=E/'EVIDENCE-MANIFEST.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
def row(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
m=json.loads(OUTER.read_text())
self_path=str(OUTER.relative_to(K))
assert m['excluded_paths']==[self_path]
assert m['scope']=='complete KE-04 project at independent statement referee 1 seal'
actual={str(p.relative_to(K)) for p in K.rglob('*') if p.is_file()}
assert all(not p.is_symlink() for p in K.rglob('*'))
assert actual-{self_path}==set(m['files']),{'added':sorted(actual-{self_path}-set(m['files'])),'missing':sorted(set(m['files'])-actual)}
assert len(m['files'])==m['input_count']
for path,expected in m['files'].items():
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    assert row(K/path)==expected,path
b=json.loads((E/'baseline.json').read_text())
assert b['original_file_count']==168 and b['exact_inventory_membership']
assert len(b['files'])==168
for p,v in b['files'].items():assert row(K/p)==v,p
d=json.loads((K/'DRAFT-INVENTORY.json').read_text())
assert d['input_count']==167 and d['excluded_paths']==['DRAFT-INVENTORY.json']
assert set(d['files'])|{'DRAFT-INVENTORY.json'}==set(b['files'])
for p,v in d['files'].items():assert row(K/p)==v,p
assert not d['proof_authorized'] and not d['statement_frozen']
assert row(K/'STATEMENT-HANDOFF.md')['sha256']=='f46ec1cb54a9eed22dd7fc2cf640531be64b2ec86d48251d09075a64e94fa8a9'
assert row(K/'DRAFT-INVENTORY.json')['sha256']=='e82c391cc2d8d3ad1ee12e4f19266e2495e469e4b39272d31697a2e4a873a9fa'
r=json.loads((E/'RESULT.json').read_text())
assert r['verdict']=='APPROVE' and r['definitions']==27 and r['definition_closure']==33
assert r['contracts']==24 and r['kernel_trust_commands']==27
assert not r['proof_implemented'] and not r['linux_comparator_run'] and not r['statement_frozen']
assert r['recorded_child_commands']==408 and r['own_objects_hashed_and_removed']==10
for path,expected in [(r['accepted_attempt']+'/result.json',r['accepted_attempt_result']),
                      (r['accepted_provenance_audit']+'/result.json',r['accepted_provenance_result'])]:
    assert row(K/path)==expected,path
for a in r['all_attempts']:
    folder=E/a['path']
    assert row(folder/'result.json')==a['result']
    data=json.loads((folder/'result.json').read_text())
    assert data['success']==a['success'] and len(data['commands'])==a['commands']
    for c in data['commands']:
        assert row(folder/c['stdout'])==c['stdout_identity']
        assert row(folder/c['stderr'])==c['stderr_identity']
    if 'private_output' in data:
        assert data['private_objects_removed'] and not Path(data['private_output']).exists()
source_inventory=json.loads((K/'verification/original-source-inventory.json').read_text())
assert len(source_inventory['files'])==17
for p,v in source_inventory['files'].items():
    assert row(K/p)=={key:v[key] for key in ['bytes','sha256']}
    data=(K/p).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==v['git_blob']
api=json.loads((K/'verification/api-evidence-complete/manifest.json').read_text())
assert len(api['files'])==33
for p,v in api['files'].items():
    assert row(K/p)=={key:v[key] for key in ['bytes','sha256']}
    data=(K/p).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==v['git_blob']
checks=json.loads((E/'SEAL-CHECKS.json').read_text())
assert checks['report']==row(K/'reviews/statement-referee-1.md')
assert checks['result']==row(E/'RESULT.json')
assert checks['bound_file_count']==m['input_count']
assert not (K/'Solution.lean').exists() and not (K/'formalization.yaml').exists()
print(json.dumps({'result':'SEALED_STATEMENT_REFEREE_1_PASS','bound_files':m['input_count'],
                  'original_inputs':168,'definitions':27,'closure':33,'contracts':24,
                  'statement_only':True,'proof_authorized':False,
                  'outer_sha256':sha(OUTER.read_bytes())},indent=2))
