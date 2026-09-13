"""Read-only GitHub provenance collection for the completed IE05 job.

No dispatch, rerun, PR change, dependency build or candidate mutation.
Every requested response and failed request is retained in a new attempt.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,os,subprocess,tempfile
E=Path(__file__).resolve().parent
GH='/tmp/nla-submission-tools/gh_2.100.0_macOS_arm64/bin/gh'
REPO='repos/sgstepaniants/OpenProblemsInNLA';RUN=34751393873
sha=lambda b:hashlib.sha256(b).hexdigest()
A=Path(tempfile.mkdtemp(prefix='api-',dir=E));(A/'executed.py').write_bytes(Path(__file__).read_bytes())
requests=[('run.json',f'{REPO}/actions/runs/{RUN}'),('jobs.json',f'{REPO}/actions/runs/{RUN}/jobs?per_page=100'),('artifacts.json',f'{REPO}/actions/runs/{RUN}/artifacts?per_page=100'),('ie05-job.json',f'{REPO}/actions/jobs/103708463461'),('ie05-job.log',f'{REPO}/actions/jobs/103708463461/logs'),('controls-job.json',f'{REPO}/actions/jobs/103708463293'),('controls-job.log',f'{REPO}/actions/jobs/103708463293/logs'),('ids-run.json',f'{REPO}/actions/runs/34751393871'),('commit.json',f'{REPO}/commits/71cf72f9db2af0f01b5cfa7f18a69e28310eb52f')]
def one(row):
    name,url=row;cmd=[GH,'api',url];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    cp=subprocess.run(cmd,capture_output=True,env=dict(os.environ,GH_PROMPT_DISABLED='1'))
    (A/name).write_bytes(cp.stdout);(A/(name+'.stderr')).write_bytes(cp.stderr)
    r={'argv':cmd,'utc_start':start,'exit_code':cp.returncode,'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr),'bytes':len(cp.stdout)}
    (A/(name+'.command.json')).write_text(json.dumps(r,indent=2)+'\n');return name,r
with ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(one,requests))
out={'commands':results,'success':all(r['exit_code']==0 for r in results.values())}
(A/'result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'attempt':str(A),'success':out['success'],'exit_codes':{n:r['exit_code'] for n,r in results.items()}},indent=2))
raise SystemExit(0 if out['success'] else 1)
