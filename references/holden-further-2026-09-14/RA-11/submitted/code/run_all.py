"""Run both suites and retain stdout, stderr, and return codes."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
records=[]
for script in ['exact_checks.py','numerical_checks.py']:
    start=time.time()
    try:
        proc=subprocess.run([sys.executable,str(ROOT/'code'/script)],capture_output=True,text=True,
                            timeout=100,env=env)
        (ROOT/'results'/(script+'.stdout.txt')).write_text(proc.stdout)
        (ROOT/'results'/(script+'.stderr.txt')).write_text(proc.stderr)
        records.append({'script':script,'returncode':proc.returncode,
                        'status':'passed' if proc.returncode==0 else 'failed',
                        'seconds':time.time()-start})
    except Exception as exc:
        records.append({'script':script,'status':'execution_error','error':repr(exc),
                        'seconds':time.time()-start})
(ROOT/'results'/'execution_status.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
sys.exit(0 if all(r['status']=='passed' for r in records) else 1)
