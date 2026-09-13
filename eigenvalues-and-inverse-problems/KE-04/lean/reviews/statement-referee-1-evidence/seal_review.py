#!/usr/bin/env python3
"""One-shot complete first-referee inventory. Never rerun over an existing seal."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess

E=Path(__file__).resolve().parent
K=E.parent.parent
OUTER=E/'EVIDENCE-MANIFEST.json'
CHECKS=E/'SEAL-CHECKS.json'
assert not OUTER.exists() and not CHECKS.exists()
def row(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
b=json.loads((E/'baseline.json').read_text())['files']
for p,v in b.items():assert row(K/p)==v,p
paths={str(p.relative_to(K)) for p in K.rglob('*') if p.is_file()}
own={str(p.relative_to(K)) for p in E.rglob('*') if p.is_file()}|{'reviews/statement-referee-1.md'}
assert paths==set(b)|own
assert len(b)==168
report=K/'reviews/statement-referee-1.md'
result=json.loads((E/'RESULT.json').read_text())
assert result['verdict']=='APPROVE'
write(CHECKS,{'phase':'independent statement referee 1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'all_original_inputs_unchanged':168,'complete_scope_before_seal':True,
              'bound_file_count':len(paths)+1,'report':row(report),'result':row(E/'RESULT.json'),
              'accepted_attempt_result':result['accepted_attempt_result'],
              'accepted_provenance_result':result['accepted_provenance_result'],
              'proof_authorized':False,'statement_frozen':False,'linux_run':False})
files={str(p.relative_to(K)):row(p) for p in sorted(K.rglob('*')) if p.is_file() and p!=OUTER}
write(OUTER,{'schema_version':1,'scope':'complete KE-04 project at independent statement referee 1 seal',
             'reviewer':'/root/ra20_final_referee2','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'excluded_paths':[str(OUTER.relative_to(K))],'input_count':len(files),'files':files})
r=subprocess.run(['python3',str(E/'verify_inventory.py')],cwd=K,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
print(r.stdout.decode(),end='')
if r.stderr:print(r.stderr.decode(),end='')
assert r.returncode==0,r.returncode
print(json.dumps({'report':row(report),'outer':row(OUTER),'result':row(E/'RESULT.json'),
                  'seal_checks':row(CHECKS),'accepted_attempt_result':result['accepted_attempt_result'],
                  'accepted_provenance_result':result['accepted_provenance_result']},indent=2))
