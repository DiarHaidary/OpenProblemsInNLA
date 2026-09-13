"""Transparent raw-command capture for the repository's unchanged PDF renderer."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time

def run(kind):
 e=Path(__file__).resolve().parents[1]
 parent=e/'pdf-build';parent.mkdir(exist_ok=True)
 i=1
 while (parent/(kind+'-'+str(i))).exists():i+=1
 d=parent/(kind+'-'+str(i));d.mkdir()
 binary={'pandoc':'/tmp/nla-submission-tools/pandoc-3.11-arm64/bin/pandoc','xelatex':'/Library/TeX/texbin/xelatex'}[kind]
 args=[binary]+sys.argv[1:]
 data=sys.stdin.buffer.read() if kind=='pandoc' else None
 if data is not None:(d/'stdin.md').write_bytes(data)
 for arg in args:
  if arg.startswith('--metadata-file='):(d/'metadata.json').write_bytes(Path(arg.split('=',1)[1]).read_bytes())
  if arg.startswith('--template='):(d/'template.tex').write_bytes(Path(arg.split('=',1)[1]).read_bytes())
 if kind=='xelatex':(d/'problem.tex').write_bytes(Path('problem.tex').read_bytes())
 rec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':args,'cwd':os.getcwd(),'transparent_stdout_and_stderr_forwarding':True}
 (d/'command.json').write_text(json.dumps(rec,indent=2)+'\n')
 t=time.monotonic();r=subprocess.run(args,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (d/'stdout').write_bytes(r.stdout);(d/'stderr').write_bytes(r.stderr)
 if kind=='xelatex':
  for n in ['problem.log','problem.pdf']:
   if Path(n).exists():(d/n).write_bytes(Path(n).read_bytes())
 rec.update(exit_code=r.returncode,seconds=time.monotonic()-t)
 (d/'result.json').write_text(json.dumps(rec,indent=2)+'\n')
 sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr)
 return r.returncode
