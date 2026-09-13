#!/usr/bin/env python3
"""Record an actual read-only operational audit command without printing secrets."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

E = Path(__file__).resolve().parent
G = E.parents[4]
name = sys.argv[1]
args = sys.argv[2:]
assert args and '/' not in name and '..' not in name
d = E / 'commands' / name
d.mkdir()
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['GIT_OPTIONAL_LOCKS'] = '0'
env['GH_PAGER'] = 'cat'
env['GH_PROMPT_DISABLED'] = '1'
record = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'command':args,'cwd':str(G),
          'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0',
                                   'GH_PAGER':'cat','GH_PROMPT_DISABLED':'1'}}
(d/'command.json').write_text(json.dumps(record,indent=2)+'\n')
start = time.monotonic()
with (d/'stdout').open('wb') as out, (d/'stderr.log').open('wb') as err:
    proc = subprocess.run(args,cwd=G,env=env,stdout=out,stderr=err)
record.update(exit_code=proc.returncode,seconds=time.monotonic()-start,
              stdout_sha256=hashlib.sha256((d/'stdout').read_bytes()).hexdigest(),
              stderr_sha256=hashlib.sha256((d/'stderr.log').read_bytes()).hexdigest())
(d/'result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'record':str(d),'exit_code':proc.returncode,
                  'stdout_bytes':(d/'stdout').stat().st_size,'stderr_bytes':(d/'stderr.log').stat().st_size}))
sys.exit(proc.returncode)
