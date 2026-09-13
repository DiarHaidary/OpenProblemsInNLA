#!/usr/bin/env python3
"""Read-only complete RA20 operational seal checker. No network or Lean build."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
from privacy_and_supplemental import checks as privacy_checks

E=Path(__file__).resolve().parent
P=E.parents[1];G=P.parents[2]
SELF=E/'EVIDENCE-MANIFEST.json'
REPORT=P/'reviews/linux-operational-referee-2026-09-13.md'
OLD='7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
HEAD='43603b173beb294c2588d83f936a8a96246fd5f0'

def sha(p):
    assert p.is_file() and not p.is_symlink(),str(p)
    return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        assert k not in d,('duplicate JSON key',k)
        d[k]=v
    return d
def load(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def check(p,v,historical=False):
    p=p.resolve();h=v if isinstance(v,str) else v['sha256']
    if historical and p==P/'README.md' and h==OLD:p=P/'verification/pre-candidate-README.md'
    assert sha(p)==h,str(p)
    if isinstance(v,dict) and 'bytes' in v:assert p.stat().st_size==v['bytes'],str(p)

def scope():
    b=load(E/'source-binding.json')
    bound={(P/n).resolve() for n in b['candidate_inputs']}
    previous=P/'verification/candidate-packaging-referee-2026-09-13/EVIDENCE-MANIFEST.json'
    bound|={(previous.parent/n).resolve() for n in load(previous)['files']}
    bound|={(G/n).resolve() for n in b['repository_infrastructure']}
    bound|={G/'tools/validate_problem_ids.py',REPORT}
    bound|={p.resolve() for p in E.rglob('*') if p.is_file() and p.resolve()!=SELF}
    assert SELF not in bound
    return bound

def verify(m=None):
    m=load(SELF) if m is None else m
    assert m['candidate']==HEAD and m['verdict']=='APPROVE actual RA20 Ubuntu operational verification'
    assert m['exact_self_exclusion']=='EVIDENCE-MANIFEST.json'
    assert len(m['files'])==m['file_count']
    bound={(E/n).resolve() for n in m['files']}
    assert len(bound)==len(m['files']) and bound==scope() and SELF not in bound
    for n,v in m['files'].items():check(E/n,v)
    own={p.resolve() for p in E.rglob('*') if p.is_file() and p.resolve()!=SELF}
    assert {p for p in bound if p.is_relative_to(E)}==own
    assert len(own)==m['own_evidence_files_excluding_outer']
    b=load(E/'source-binding.json')
    assert b['candidate']==HEAD and len(b['candidate_inputs'])==1092
    for n,v in b['candidate_inputs'].items():check(P/n,v)
    # Original Git batch bytes independently identify every committed blob.
    batch=(E/'commands/source-003/stdout').read_bytes();offset=0
    for n,v in b['candidate_inputs'].items():
        end=batch.index(b'\n',offset);fields=batch[offset:end].decode().split()
        assert fields==[v['git_blob'],'blob',str(v['bytes'])]
        data=batch[end+1:end+1+v['bytes']];offset=end+2+v['bytes']
        assert hashlib.sha256(data).hexdigest()==v['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==v['git_blob']
        assert batch[offset-1:offset]==b'\n'
    assert offset==len(batch)
    for n,v in b['original_sources'].items():
        check(G/n,v);check(P/'verification/original-sources'/n,v)
    assert len(b['original_sources'])==16
    assert len(b['complete_nested_manifests'])==17
    for n,v in b['complete_nested_manifests'].items():
        path=P/n;check(path,v['sha256']);nested=load(path)
        parent=P if n=='reviews/statement-package-manifest.json' else path.parent
        assert len(nested['files'])==v['bound_files']
        for name,value in nested['files'].items():check(parent/name,value,True)
    for path,count in [(P/'verification/proof-freeze.json',521),(P/'reviews/statement-freeze.json',68)]:
        f=load(path);assert len(f['files'])==count
        for n,v in f['files'].items():check(P/n,v,True)
    for n,v in b['repository_infrastructure'].items():
        check(G/n,v);check(E/'infrastructure'/n,v)
    for n,v in b['checker_source_files'].items():check(E/'checker-source'/n,v)
    assert len(b['checker_source_files'])==58
    check(E/'checker-source/sandbox_probe_ci.py',b['derived_ci_probe_sha256'])
    commands=[]
    for d in sorted((E/'commands').iterdir()):
        assert d.is_dir()
        c=load(d/'command.json')
        if d.name=='000-network-sandbox':
            assert c['exit_code']==1
            assert 'error connecting to api.github.com' in (d/'raw.log').read_text()
            commands.append((d.name,1));continue
        r=load(d/'result.json');assert r['command']==c['command'] and r['cwd']==c['cwd']
        expected=1 if d.name in {'007-controls-job-log','008-select-job-log'} else 0
        assert r['exit_code']==expected
        check(d/'stdout',r['stdout_sha256']);check(d/'stderr.log',r['stderr_sha256'])
        if 'stdin_sha256' in r:check(d/'stdin',r['stdin_sha256'])
        commands.append((d.name,expected))
    assert len([n for n,c in commands if n.startswith('source-')])==50
    assert len([n for n,c in commands if c==1])==3
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    r=subprocess.run([sys.executable,'-B',str(E/'runtime_audit.py'),'--check-only'],
                     cwd=G,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    assert r.returncode==0,('read-only runtime audit failed',r.stderr.decode())
    outcome=json.loads(r.stdout)
    assert outcome['status']=='RUNTIME_AUDIT_PASS'
    privacy=privacy_checks()
    final=load(E/'FINAL.json')
    assert final['report_sha256']==sha(REPORT)
    assert final['source_binding_sha256']==sha(E/'source-binding.json')
    assert final['runtime_verification_sha256']==sha(E/'runtime-verification.json')
    return {'status':'INDEPENDENT_RA20_OPERATIONAL_SEAL_PASS','verdict':m['verdict'],
        'candidate':HEAD,'workflow_run':34743832047,'file_count':len(bound),
        'own_evidence_files_excluding_outer':len(own),'candidate_Git_inputs':1092,
        'all_nested_prior_inventories':17,'proof_inputs':521,'statement_inputs':68,'original_sources':16,
        'all_workflow_jobs':17,'all_original_artifact_ZIPs':16,'whole_workflow_log_members':217,
        'exports':12,'source_kernel_assertions':61,'printed_axiom_occurrences':57,'distinct_printed_names':45,
        'all_command_receipts':len(commands),'successful_command_receipts':sum(c==0 for _,c in commands),
        'retained_failed_command_receipts':3,'read_only_runtime_recheck':'PASS',
        'private_email_addresses_added':privacy['private_email_addresses_added'],
        'non_address_path_forms':privacy['exact_non_address_forms_allowed'],
        'new_mathematical_approval':False,'canonical_status':'Solved, unchanged',
        'root_operational_acceptance_and_publication':'pending'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
