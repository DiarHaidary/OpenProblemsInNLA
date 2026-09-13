#!/usr/bin/env python3
"""Author consistency checks of actual installed candidate documents, not an independent review."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time,urllib.parse
import yaml
E=Path(__file__).resolve().parent;P=E.parents[1];R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
H='7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
b=json.loads((E/'preflight.json').read_text());install=json.loads((E/'installation.json').read_text())
def historic(p,expected):
    p=p.resolve()
    if p==(P/'README.md').resolve() and expected==H:return P/'verification/pre-candidate-README.md'
    return p
def verify(p,value):
    h=value if isinstance(value,str) else value['sha256'];q=historic(p,h)
    assert sha(q)==h,(str(p),'unexpected content')
    if isinstance(value,dict) and 'bytes' in value:assert q.stat().st_size==value['bytes'],p
for n,v in b['baseline'].items():verify(P/n,v)
assert [n for n,v in b['baseline'].items() if sha(P/n)!=v['sha256']]==['README.md']
assert sha(P/'verification/final-review-acceptance.json')==b['root_gate_sha256']
assert sha(P/'README.md')==install['README_sha256'] and sha(P/'formalization.yaml')==install['YAML_sha256']
proof=json.loads((P/'verification/proof-freeze.json').read_text())
statement=json.loads((P/'reviews/statement-freeze.json').read_text())
for freeze in [proof,statement]:
    for n,h in freeze['files'].items():verify(P/n,h)
    for n,h in freeze['source_files'].items():
        assert sha(R/n)==h and sha(P/'verification/original-sources'/n)==h,n
nested=[]
for n in b['baseline']:
    if n.endswith('EVIDENCE-MANIFEST.json') or n=='reviews/statement-package-manifest.json':
        mf=P/n;m=json.loads(mf.read_text());base=P if n=='reviews/statement-package-manifest.json' else mf.parent
        for k,v in m['files'].items():verify(base/k,v)
        nested.append({'file':n,'sha256':sha(mf),'entries':len(m['files'])})
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['GIT_OPTIONAL_LOCKS']='0'
commands=[
 ['/tmp/nla-lean-formalization/venv/bin/python','tools/lean/validate_manifest.py','randomized-and-low-rank-approximation/RA-20/lean'],
 ['python3','tools/validate_problem_ids.py','--base-ref','origin/main'],
 ['python3','tools/validate_problem_ids.py','--base-ref','nla-upstream/main']]
records=[]
for i,cmd in enumerate(commands,1):
    record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(R),
            'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}}
    (E/('check-%d-command.json'%i)).write_text(json.dumps(record,indent=2)+'\n')
    t=time.monotonic();r=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (E/('check-%d.log'%i)).write_bytes(r.stdout)
    record.update(exit_code=r.returncode,seconds=time.monotonic()-t)
    (E/('check-%d-result.json'%i)).write_text(json.dumps(record,indent=2)+'\n');records.append(record)
    assert r.returncode==0,(cmd,r.stdout.decode())
metadata=yaml.safe_load((P/'formalization.yaml').read_text())
config=json.loads((P/'comparator.json').read_text())
assert [x['declaration'] for x in metadata['status']['main_results']]==config['theorem_names']
assert [x['declaration'] for x in metadata['alignment']]==config['theorem_names']
assert len(config['theorem_names'])==12 and config['definition_names']==[]
assert metadata['review']['coordinator_acceptance']['sha256']==b['root_gate_sha256']
assert metadata['review']['coordinator_acceptance']['status']=='accepted'
assert metadata['review']['linux_verification']['status']=='pending'
assert metadata['review']['candidate_documents']['independent_packaging_review']=='pending'
assert '**Status:** Solved' in (R/'randomized-and-low-rank-approximation/RA-20/README.md').read_text()
assert 'lake build Solution' in (P/'README.md').read_text()
assert not re.search(r'RA-09|RA09|Colbrook|Persson|Musco|concave|PSD', (P/'formalization.yaml').read_text())
allowed={'formalization.yaml','verification/pre-candidate-README.md'}
new=[str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in b['baseline']]
assert all(n in allowed or n.startswith('verification/linux-candidate-2026-09-13/') for n in new),new
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'AUTHOR_CHECKS_PASS; independent packaging review pending',
 'baseline_count':len(b['baseline']),'exact_existing_changes':['README.md'],'all_other_prior_files_preserved':len(b['baseline'])-1,
 'old_README_preserved_in_archive':True,'proof_inputs_rehashed':len(proof['files']),'statement_inputs_rehashed':len(statement['files']),
 'original_sources_and_snapshots_rehashed':len(proof['source_files']),'all_prior_nested_manifests':nested,
 'archive_mapping':{'only_original_path':'README.md','only_expected_sha256':H,'archive':'verification/pre-candidate-README.md'},
 'commands':records,'actual_main_results':config['theorem_names'],'README_sha256':sha(P/'README.md'),
 'YAML_sha256':sha(P/'formalization.yaml'),'no_mathematical_pin_Git_or_canonical_edit':True,
 'actual_Linux_Comparator_default_kernel_controls':'pending','operational_acceptance':'pending','publication':'pending'}
(E/'CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'status':'AUTHOR_CHECKS_PASS','baseline_count':len(b['baseline']),
                  'nested_manifests_rehashed':len(nested),'schema_and_ID_commands':len(records),'exports':len(config['theorem_names'])}))
