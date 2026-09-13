#!/usr/bin/env python3
"""Read all remaining small artifact ZIPs of this exact completed workflow.
Only RA20 and checker-controls receive proof/control semantic audits; every
workflow artifact receives API/upload/ZIP identity checking. No cache objects.
"""
from pathlib import Path
import concurrent.futures, json, os, subprocess, sys

E=Path(__file__).resolve().parent
G=E.parents[4]
gh='/tmp/nla-submission-tools/gh_2.100.0_macOS_arm64/bin/gh'
data=json.loads((E/'commands/015-final-artifacts/stdout').read_text())
assert len(data['artifacts'])==data['total_count']==16
tasks=[]
for a in data['artifacts']:
    assert a['workflow_run']['id']==34743832047
    assert a['workflow_run']['head_sha']=='43603b173beb294c2588d83f936a8a96246fd5f0'
    assert not a['expired'] and a['size_in_bytes']<2_000_000
    if a['name'] in {'lean-RA-20','lean-checker-controls'}:continue
    endpoint='repos/sgstepaniants/OpenProblemsInNLA/actions/artifacts/'+str(a['id'])+'/zip'
    tasks.append([sys.executable,str(E/'record_command.py'),'020-artifact-'+str(a['id']),
                  gh,'api',endpoint,'--allow-escape-sequences'])
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
def run(args):
    p=subprocess.run(args,cwd=G,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return {'command':args,'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,tasks))
(E/'remaining-artifacts-retrieval.json').write_text(json.dumps(results,indent=2)+'\n')
assert len(results)==14 and all(r['exit_code']==0 for r in results)
print(json.dumps({'status':'REMAINING_ARTIFACTS_DOWNLOADED','artifacts':14,
                  'semantic_scope':'RA20 and checker-controls only; all16 artifacts bound by original ZIP identity'}))
