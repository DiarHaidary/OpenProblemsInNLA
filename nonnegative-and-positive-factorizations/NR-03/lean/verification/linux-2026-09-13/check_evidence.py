#!/usr/bin/env python3
"""Offline integrity checks of retained NR03 canonical evidence, not a new Lean run."""
from pathlib import Path
import hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parent
COMMIT='f664d07e82aaa60bc9c78dd1946e763168c5c530'
PROJECT='nonnegative-and-positive-factorizations/NR-03/lean'
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
run=json.loads((ROOT/'run-final.json').read_text())
jobs=json.loads((ROOT/'jobs-final.json').read_text())['jobs']
verify=[j for j in jobs if j['name'].startswith('verify (')]
assert len(verify)==1
job=verify[0]
assert run['id']==34785341662 and run['head_sha']==COMMIT
assert job['id']==103799711659 and job['name']=='verify (NR-03, '+PROJECT+')'
assert run['status']==job['status']=='completed'
assert run['conclusion']==job['conclusion']=='success'
artifacts=json.loads((ROOT/'artifacts-final.json').read_text())['artifacts']
assert len(artifacts)==1
artifact=artifacts[0]
assert artifact['name']=='lean-NR-03' and not artifact['expired']
assert artifact['digest']=='sha256:'+sha(ROOT/'artifact.zip')
with zipfile.ZipFile(ROOT/'artifact.zip') as z:
    for info in z.infolist():
        path=Path(info.filename)
        assert not path.is_absolute() and '..' not in path.parts
        if not info.is_dir(): assert z.read(info)==(ROOT/'extracted'/path).read_bytes()
accepted=[]
for path in (ROOT/'extracted').rglob('result.json'):
    if json.loads(path.read_text()).get('result')=='comparator-accepted': accepted.append(path)
assert len(accepted)==1
result=json.loads(accepted[0].read_text());raw=accepted[0].parent
assert result['repository_commit']==COMMIT and result['project']==PROJECT
binding=json.loads((ROOT/'GIT-SOURCE-BINDINGS.json').read_text())
assert binding['commit']==COMMIT and binding['project']==PROJECT
assert result['input_sha256']==binding['input_sha256'] and len(result['input_sha256'])==113
ops=json.loads((ROOT/'OPERATIONAL-CHECKS.json').read_text())
assert ops['commit']==COMMIT and ops['run']==run['id'] and ops['job']==job['id']
assert ops['artifact_sha256']==sha(ROOT/'artifact.zip')
config=result['config'];names=config['theorem_names']
assert len(names)==len(set(names))==10 and config['definition_names']==[]
assert set(config['permitted_axioms'])==ALLOWED
logs={p.name:p.read_text() for p in raw.glob('*.log')}
for filename,digest in ops['raw_sha256'].items():assert sha(raw/filename)==digest
main=logs['comparator.log']
for needle in ['Building Challenge','Building Solution','Lean default kernel accepts the solution','Your solution is okay!']:
    assert needle in main
assert main.rstrip().endswith('EXIT_STATUS=0')
axioms={n:{a.strip() for a in ax.split(',') if a.strip()} for n,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",main)}
axioms.update({n:set() for n in re.findall(r"'([^']+)' does not depend on any axioms",main)})
for n in names:
    assert axioms[n] <= ALLOWED and set(ops['actual_public_axioms'][n])==axioms[n]
exports=[line for line in main.splitlines() if line.startswith('Exporting #[') and line.endswith(' from Solution')]
assert len(exports)==1 and all(n in exports[0] for n in names)
actual_pins=dict(re.findall(r"info: ([^:]+): checking out revision '([0-9a-f]{40})'",logs['dependencies.log']))
assert len(actual_pins)==10 and actual_pins==ops['actual_dependency_checkouts']
assert logs['dependencies.log'].rstrip().endswith('EXIT_STATUS=0')
for filename,needles,status in [
 ('sandbox.log',['Sandbox UID: 1001','PASS AF_UNIX socket creation','PASS effective capabilities: none','PASS no_new_privs: set','PASS nested namespace write attempt','Outer and export fixture contents unchanged'],0),
 ('kernel-controls.log',['PASS: all three actual Comparator.runBuiltinKernel cases behaved as required'],0),
 ('comparator-controls.log',['PASS: all five Comparator regressions'],0),
 ('negative-sorry.log',["Illegal axiom detected: 'sorryAx'"],1),
 ('negative-native.log',["Illegal axiom detected: 'checked._native.native_decide.ax_1_1'"],1)]:
    for needle in needles:assert needle in logs[filename],(filename,needle)
    assert logs[filename].rstrip().endswith('EXIT_STATUS='+str(status)),filename
assert result['tool_receipt']['lean_toolchain']=='leanprover/lean4:v4.33.1'
assert result['tool_receipt']['forsythe_commit']=='8d1b0c0545a77b40245e84705aa7d273e6c81e62'
manifest=ROOT/'EVIDENCE-MANIFEST.json'
if manifest.exists():
    for rel,digest in json.loads(manifest.read_text())['files'].items():assert sha(ROOT/rel)==digest,rel
print('PASS: retained exact NR03 canonical run/job/artifact, 113 source bindings, ten actual dependency checkouts, ten public exports with standard axioms, built-in kernel, Comparator, sandbox and rejection controls. No new compiler execution or independent mathematical-review claim.')
