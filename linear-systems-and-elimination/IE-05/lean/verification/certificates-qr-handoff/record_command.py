#!/usr/bin/env python3
"""Retain exact helper audit command source, streams and exit in own evidence."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
E=Path(__file__).resolve().parent;P=E.parents[1]
label=sys.argv[1];cmd=sys.argv[2:];assert label.replace('-','').isalnum() and cmd
D=E/'commands'/label;D.mkdir(parents=True,exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[]
for arg in cmd:
 p=Path(arg) if Path(arg).is_absolute() else P/arg
 if p.is_file() and p.suffix=='.py':
  q=D/('executed-'+p.name);q.write_bytes(p.read_bytes())
  sources.append({'path':str(p),'sha256':sha(p),'snapshot':q.name})
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
rec={'argv':cmd,'cwd':str(P),'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'},'actual_script_sources':sources}
(D/'command.json').write_text(json.dumps(rec,indent=2)+'\n')
r=subprocess.run(cmd,cwd=P,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(D/'stdout').write_bytes(r.stdout);(D/'stderr').write_bytes(r.stderr)
rec.update(exit_code=r.returncode,finish_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 stdout_sha256=sha(D/'stdout'),stderr_sha256=sha(D/'stderr'))
(D/'result.json').write_text(json.dumps(rec,indent=2)+'\n')
sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr)
raise SystemExit(r.returncode)
