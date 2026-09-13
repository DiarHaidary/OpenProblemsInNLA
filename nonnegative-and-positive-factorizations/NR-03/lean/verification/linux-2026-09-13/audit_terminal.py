#!/usr/bin/env python3
"""Audit the one retained NR03 canonical run; read Git only, never run Lean/Lake."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
WORK=Path('/tmp/nla-lean-nr03-publication-worktree')
COMMIT='f664d07e82aaa60bc9c78dd1946e763168c5c530'
PROJECT='nonnegative-and-positive-factorizations/NR-03/lean'
RUN=34785341662
JOB=103799711659
ALLOWED={'propext','Classical.choice','Quot.sound'}

def sha(data): return hashlib.sha256(data).hexdigest()
def gitfile(path):
    return subprocess.check_output(['git','-c','gc.auto=0','show',COMMIT+':'+path],cwd=WORK)
def save(path,value):
    data=(json.dumps(value,indent=2)+'\n').encode()
    if path.exists():
        assert path.read_bytes()==data, f'Refuse to rewrite retained evidence: {path}'
        return
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
    with os.fdopen(fd,'wb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
run=json.loads((ROOT/'run-final.json').read_text())
jobs=json.loads((ROOT/'jobs-final.json').read_text())['jobs']
verify=[j for j in jobs if j['name'].startswith('verify (')]
assert len(verify)==1 and verify[0]['id']==JOB
job=verify[0]
assert run['id']==RUN and run['head_sha']==COMMIT
assert run['status']==job['status']=='completed'
assert job['name']=='verify (NR-03, '+PROJECT+')'
artifacts=json.loads((ROOT/'artifacts-final.json').read_text())['artifacts']
assert len(artifacts)==1 and artifacts[0]['name']=='lean-NR-03'
artifact=artifacts[0]
archive=(ROOT/'artifact.zip').read_bytes()
assert artifact['digest']=='sha256:'+sha(archive)
with zipfile.ZipFile(ROOT/'artifact.zip') as z:
    for item in z.infolist():
        if not item.is_dir():
            assert z.read(item)==(ROOT/'extracted'/item.filename).read_bytes()
results=list((ROOT/'extracted').rglob('result.json'))
accepted=[p for p in results if json.loads(p.read_text()).get('result')=='comparator-accepted']
if not accepted:
    logs={str(p.relative_to(ROOT/'extracted')):p.read_text(errors='replace') for p in (ROOT/'extracted').rglob('*.log')}
    evidence={'scope':'Actual terminal failure audit; no complete acceptance',
        'run':RUN,'job':JOB,'commit':COMMIT,'run_conclusion':run['conclusion'],
        'job_conclusion':job['conclusion'],'accepted_result_count':0,
        'failed_job_steps':[s for s in job['steps'] if s.get('conclusion')=='failure'],
        'log_exit_markers':{p:re.findall(r'EXIT_STATUS=(-?\d+)',s) for p,s in logs.items()},
        'error_lines':{p:[line for line in s.splitlines() if re.search(r'error:|error |failed|timed? out|timeout|killed|abort',line,re.I)][-100:] for p,s in logs.items()},
        'raw_files_sha256':{str(p.relative_to(ROOT/'extracted')):sha(p.read_bytes()) for p in sorted((ROOT/'extracted').rglob('*')) if p.is_file()}}
    save(ROOT/'FAILURE-CHECKS.json',evidence)
    print(json.dumps({'terminal':'no accepted Comparator record','failure_checks':str(ROOT/'FAILURE-CHECKS.json'),'failed_steps':[s['name'] for s in evidence['failed_job_steps']]},indent=2))
    raise SystemExit(0)
assert len(accepted)==1 and run['conclusion']==job['conclusion']=='success'
result_path=accepted[0];raw=result_path.parent
result=json.loads(result_path.read_text())
assert result['repository_commit']==COMMIT and result['project']==PROJECT
config=json.loads(gitfile(PROJECT+'/comparator.json'))
assert result['config']==config
names=config['theorem_names']
assert len(names)==len(set(names))==10
assert config['definition_names']==[] and set(config['permitted_axioms'])==ALLOWED
inputs=result['input_sha256'];assert len(inputs)==113
input_receipt={}
for rel,digest in inputs.items():
    blob=gitfile(PROJECT+'/'+rel)
    assert sha(blob)==digest,rel
    input_receipt[rel]=digest
save(ROOT/'GIT-SOURCE-BINDINGS.json',{'scope':'Each raw canonical input hash independently recomputed from the exact retained Git commit','commit':COMMIT,'project':PROJECT,'input_sha256':input_receipt})
logs={p.name:p.read_text() for p in raw.glob('*.log')}
main=logs['comparator.log']
for marker in ['Building Challenge','Building Solution','Lean default kernel accepts the solution','Your solution is okay!']:
    assert marker in main,marker
assert main.rstrip().endswith('EXIT_STATUS=0')
all_axioms={n:{a.strip() for a in ax.split(',') if a.strip()} for n,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",main)}
all_axioms.update({n:set() for n in re.findall(r"'([^']+)' does not depend on any axioms",main)})
assert all(n in all_axioms for n in names)
assert all(all_axioms[n] <= ALLOWED for n in names)
solution=gitfile(PROJECT+'/Solution.lean').decode()
assert len(re.findall(r'^#assert_trust kernel ',solution,re.M))==10
assert 'import Challenge' not in solution
export=[line for line in main.splitlines() if line.startswith('Exporting #[') and line.endswith(' from Solution')]
assert len(export)==1 and all(n in export[0] for n in names)
expected_pins={v['name']:v['rev'] for v in json.loads(gitfile(PROJECT+'/lake-manifest.json'))['packages']}
actual_pins=dict(re.findall(r"info: ([^:]+): checking out revision '([0-9a-f]{40})'",logs['dependencies.log']))
assert len(expected_pins)==10 and actual_pins==expected_pins
assert logs['dependencies.log'].rstrip().endswith('EXIT_STATUS=0')
markers={
 'sandbox.log':['Sandbox UID: 1001','PASS AF_UNIX socket creation','PASS effective capabilities: none','PASS no_new_privs: set','PASS nested namespace write attempt','Outer and export fixture contents unchanged'],
 'kernel-controls.log':['PASS: all three actual Comparator.runBuiltinKernel cases behaved as required'],
 'comparator-controls.log':['PASS: all five Comparator regressions'],
 'negative-sorry.log':["Illegal axiom detected: 'sorryAx'"],
 'negative-native.log':["Illegal axiom detected: 'checked._native.native_decide.ax_1_1'"]}
for filename,needles in markers.items():
    for needle in needles:assert needle in logs[filename],(filename,needle)
    status=1 if filename.startswith('negative-') else 0
    assert logs[filename].rstrip().endswith(f'EXIT_STATUS={status}'),filename
assert logs['sandbox.log'].count('PASS effective capabilities: none')==2
assert logs['sandbox.log'].count('PASS no_new_privs: set')==2
assert result['tool_receipt']['forsythe_commit']=='8d1b0c0545a77b40245e84705aa7d273e6c81e62'
assert result['tool_receipt']['lean_toolchain']=='leanprover/lean4:v4.33.1'
assert result['source_lock_sha256']==sha(gitfile('tools/lean/source-lock.json'))
start=datetime.datetime.fromisoformat(job['started_at'].replace('Z','+00:00'))
end=datetime.datetime.fromisoformat(job['completed_at'].replace('Z','+00:00'))
checks={'scope':'Implementer operational audit of actual canonical evidence; independent full mathematical referee acceptance remains separate',
 'run':RUN,'job':JOB,'commit':COMMIT,'project':PROJECT,'job_elapsed_seconds':(end-start).total_seconds(),
 'artifact_id':artifact['id'],'artifact_bytes':len(archive),'artifact_sha256':sha(archive),
 'raw_result':str(result_path.relative_to(ROOT)),'input_count':len(inputs),'all_input_hashes_match_git':True,
 'actual_dependency_checkouts':actual_pins,'all_ten_public_exports':names,
 'actual_public_axioms':{n:sorted(all_axioms[n]) for n in names},
 'all_actual_axiom_diagnostics':{n:sorted(a) for n,a in all_axioms.items()},
 'all_ten_LeanCert_trust_assertions_in_compiled_Solution':True,
 'actual_default_kernel_accepts':True,'actual_Comparator_accepts':True,
 'actual_sandbox_and_replay_controls_pass':True,'actual_sorry_and_native_rejections_pass':True,
 'raw_sha256':{p.name:sha(p.read_bytes()) for p in sorted(raw.iterdir()) if p.is_file()},
 'local_Lean_Lake_executed':False,'new_run_or_restart_triggered':False,
 'independent_mathematical_acceptance_claim':False}
save(ROOT/'OPERATIONAL-CHECKS.json',checks)
print(json.dumps({k:v for k,v in checks.items() if k not in ['all_actual_axiom_diagnostics','raw_sha256','actual_dependency_checkouts','actual_public_axioms']},indent=2))
