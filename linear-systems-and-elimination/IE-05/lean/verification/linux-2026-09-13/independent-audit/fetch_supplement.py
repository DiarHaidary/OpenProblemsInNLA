"""Read only: retain exact attempt-one supporting job logs, never rerun CI."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,os,subprocess,tempfile
E=Path(__file__).resolve().parent
A=Path(tempfile.mkdtemp(prefix='supplement-',dir=E))
(A/'executed.py').write_bytes(Path(__file__).read_bytes())
GH='/tmp/nla-submission-tools/gh_2.100.0_macOS_arm64/bin/gh'
def one(row):
    name,num=row
    cmd=[GH,'api',f'repos/sgstepaniants/OpenProblemsInNLA/actions/jobs/{num}/logs','--allow-escape-sequences']
    cp=subprocess.run(cmd,capture_output=True,env=dict(os.environ,GH_PROMPT_DISABLED='1'))
    (A/(name+'.log')).write_bytes(cp.stdout);(A/(name+'.stderr')).write_bytes(cp.stderr)
    return name,dict(argv=cmd,exit_code=cp.returncode,sha256=hashlib.sha256(cp.stdout).hexdigest(),bytes=len(cp.stdout))
with ThreadPoolExecutor(max_workers=4) as pool:
    rows=dict(pool.map(one,[('MI06-attempt1',103708463532),('RA07-attempt1',103708463566),('permanent-IDs',103708437437),('selection',103708437382)]))
(A/'result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':rows,'attempt':1},indent=2)+'\n')
print(json.dumps({'directory':str(A),'commands':rows},indent=2))
assert all(r['exit_code']==0 for r in rows.values())
