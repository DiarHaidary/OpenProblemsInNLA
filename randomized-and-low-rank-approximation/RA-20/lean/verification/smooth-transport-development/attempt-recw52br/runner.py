from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,tempfile,os,time,re
P=Path('/tmp/nla-lean-formalization/next-ra-statements-draft/RA-20/lean');D=P/'verification/smooth-transport-development'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=json.loads((P/'reviews/statement-freeze.json').read_text())
for r,v in F['files'].items():assert h(P/r)==v,r
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages');L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
pins=json.loads((P/'lake-manifest.json').read_text())['packages']
def pincheck():
    result=[]
    for p in pins:
        repo=C/p['name'];rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip();status=subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True)
        assert rev==p['rev'] and not status,p['name'];result.append(dict(name=p['name'],rev=rev,clean=True))
    assert len(result)==10;return result
before=pincheck();A=Path(tempfile.mkdtemp(prefix='attempt-',dir=D));prefix=Path(tempfile.mkdtemp(prefix='root-ra20-smooth-transport-',dir='/tmp/nla-lean-formalization/independent-prefixes'))
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert'];env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
name='NLA/RA20/SmoothTransport.lean';src=P/name;(A/'source.lean.txt').write_bytes(src.read_bytes());(A/'runner.py').write_bytes(Path(__file__).read_bytes());dest=prefix/Path(name).with_suffix('.olean');dest.parent.mkdir(parents=True)
cmd=[str(L/'bin/lean'),'-o',str(dest),'-i',str(dest.with_suffix('.ilean')),str(src)]
start=time.monotonic();r=subprocess.run(cmd,cwd=P,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(A/'lean.log').write_bytes(r.stdout)
rec=dict(utc=datetime.now(timezone.utc).isoformat(),owner='/root',role='RA20 implementation helper, not an independent review',gate_ownership_sha256=h(D/'gate-and-ownership.json'),source=name,source_sha256=h(src),command=cmd,exit_code=r.returncode,seconds=time.monotonic()-start,LEAN_PATH=env['LEAN_PATH'],fresh_prefix=str(prefix),prior_target_objects_used=False,pins_before=before,pins_after=pincheck(),raw_log_sha256=h(A/'lean.log'),scope='One fresh macOS source check of general smooth-locus transport; no claim of Linux replay or full RA20 proof')
objects=[]
for f in prefix.rglob('*'):
    if f.is_file():objects.append(dict(path=str(f.relative_to(prefix)),sha256=h(f),bytes=f.stat().st_size));f.unlink()
rec['generated_objects_hashed_then_removed']=objects
for rel,v in F['files'].items():assert h(P/rel)==v,rel
rec['frozen_statement_inputs_preserved']=68
if r.returncode==0:
    text=r.stdout.decode();assert 'error:' not in text and 'warning:' not in text
    rows=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text);assert len(rows)==1
    for row in rows:assert {x.strip() for x in row.split(',')} <= {'propext','Classical.choice','Quot.sound'}
    rec['actual_explicit_kernel_and_standard_three_reports']=1;rec['verdict']='PASS'
else:rec['verdict']='FAILED, actual diagnostic retained'
(A/'result.json').write_text(json.dumps(rec,indent=2)+'\n');(D/'latest.json').write_text(json.dumps({'attempt':str(A.relative_to(D)),'result_sha256':h(A/'result.json'),'verdict':rec['verdict']},indent=2)+'\n')
print(json.dumps({'attempt':str(A),'verdict':rec['verdict'],'source_sha256':h(src),'log':r.stdout.decode()},indent=2));raise SystemExit(r.returncode)
