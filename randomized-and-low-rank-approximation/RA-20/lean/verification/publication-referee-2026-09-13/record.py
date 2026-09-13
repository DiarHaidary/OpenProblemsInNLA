#!/usr/bin/env python3
"""Run an explicitly supplied review command, retaining its exact output and exit."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,shutil
E=Path(__file__).resolve().parent
label=sys.argv[1]; cmd=sys.argv[2:]
assert label.replace('-','').replace('_','').isalnum() and cmd
out=E/'receipts'/label
assert not out.with_suffix('.json').exists()
env=os.environ.copy(); env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(cmd,cwd=E.parents[4],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
finish=datetime.datetime.now(datetime.timezone.utc).isoformat()
out.with_suffix('.stdout').write_bytes(r.stdout);out.with_suffix('.stderr').write_bytes(r.stderr)
x=shutil.which(cmd[0]); d={'argv':cmd,'cwd':str(E.parents[4]),'start_utc':start,'finish_utc':finish,'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'},'exit_code':r.returncode,'executable_resolved':x,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
if x and Path(x).is_file():d['executable_sha256']=hashlib.sha256(Path(x).read_bytes()).hexdigest()
out.with_suffix('.json').write_text(json.dumps(d,indent=2)+'\n')
sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr)
raise SystemExit(r.returncode)
