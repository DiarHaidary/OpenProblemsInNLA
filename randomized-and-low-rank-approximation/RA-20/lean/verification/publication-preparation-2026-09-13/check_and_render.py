#!/usr/bin/env python3
"""Run actual publication checks and the unmodified canonical PDF renderer."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
E=Path(__file__).resolve().parent
P=E.parents[1];R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
env['PANDOC']=str(E/'pdf-tools/record-pandoc.py')
env['XELATEX']=str(E/'pdf-tools/record-xelatex.py')
commands=[
 ('ids-origin',['python3','tools/validate_problem_ids.py','--base-ref','origin/main']),
 ('ids-upstream',['python3','tools/validate_problem_ids.py','--base-ref','nla-upstream/main']),
 ('schema',['/tmp/nla-lean-formalization/venv/bin/python','tools/lean/validate_manifest.py',str(P.relative_to(R))]),
 ('math-normalize',['python3','tools/format_math.py','--write','RA-20']),
 ('catalog',['python3','tools/update_catalog.py','--base-ref','origin/main']),
 ('registry-tests',['python3','-m','unittest','discover','-s','tests','-p','test_problem_ids.py','-v']),
 ('math-check',['python3','tools/format_math.py','--check']),
 ('canonical-render',['python3','tools/render_problems.py','RA-20']),
 ('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(P.parent/'problem.pdf')]),
 ('pdf-text',['/opt/homebrew/bin/pdftotext','-layout',str(P.parent/'problem.pdf'),str(E/'pdf-text.txt')]),
 ('pdf-pages',['/opt/homebrew/bin/pdftoppm','-r','105','-png',str(P.parent/'problem.pdf'),str(E/'pdf-pages/page')]),
]
out=[]
(E/'commands').mkdir(exist_ok=True);(E/'pdf-pages').mkdir(exist_ok=True)
for name,cmd in commands:
 d=E/'commands'/name;assert not d.exists();d.mkdir()
 record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(R),'environment_overrides':{k:env[k] for k in ['PYTHONDONTWRITEBYTECODE','GIT_OPTIONAL_LOCKS','PANDOC','XELATEX']}}
 (d/'command.json').write_text(json.dumps(record,indent=2)+'\n')
 t=time.monotonic();r=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (d/'stdout').write_bytes(r.stdout);(d/'stderr').write_bytes(r.stderr)
 record.update(exit_code=r.returncode,seconds=time.monotonic()-t,stdout_sha256=sha(d/'stdout'),stderr_sha256=sha(d/'stderr'))
 (d/'result.json').write_text(json.dumps(record,indent=2)+'\n');out.append(record)
 (E/'CHECKS.json').write_text(json.dumps({'status':'AUTHOR_CHECKS_IN_PROGRESS','commands':out},indent=2)+'\n')
 print(name,r.returncode,r.stdout.decode()[-1600:],r.stderr.decode()[-800:],flush=True)
 assert r.returncode==0,name
(E/'CHECKS.json').write_text(json.dumps({'status':'AUTHOR_SCHEMA_ID_MATH_RENDER_CHECKS_PASS; visual inspection and independent publication review pending','commands':out},indent=2)+'\n')
