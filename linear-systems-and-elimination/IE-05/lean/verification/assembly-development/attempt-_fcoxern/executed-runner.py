"""Fresh author check of the completed IE05 source and all 17 target types."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess, tempfile, time
P=Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean').resolve()
E=P/'verification/assembly-development'
D=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages').resolve()
T=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ident=lambda p:{'sha256':sha(p),'bytes':p.stat().st_size}
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
assert sha(P/'verification/proof-start.json')=='2a8e4b4029a6ba005856c9ec56178cc7fefc8b8b16e945df27599ce471c95726'
frozen=json.loads((P/'reviews/statement-freeze.json').read_text())
assert len(frozen['files'])==733
for n,h in frozen['files'].items():assert sha(P/n)==h,n
A=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));S=A/'source';S.mkdir()
prefix=Path(tempfile.mkdtemp(prefix='ie05-root-assembly-',dir='/tmp/nla-lean-formalization/independent-prefixes')).resolve()
assert not list(prefix.iterdir())
(A/'executed-runner.py').write_bytes(Path(__file__).read_bytes())
mods=['Definitions','Scaling','QR','Pivot','GEPP','IntegerQR','ExactCertificates','LUTrajectory','Witness','GrowthBounds','Growth','Proof']
mapping={f'NLA/IE05/{m}.lean':f'NLA/IE05/{m}.lean' for m in mods}
mapping['Solution.lean']='Solution.lean'
mapping['verification/assembly-development/Inspect.lean']='Inspect.lean'
sources={}
for live,rel in mapping.items():
    dst=S/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((P/live).read_bytes())
    sources[live]={'snapshot':rel,**ident(dst)}
    assert 'import Challenge' not in dst.read_text()
save(A/'source-inputs.json',sources)
commands=[];baseenv=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
def run(label,argv,cwd,env=baseenv):
    start=time.monotonic();c=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for k in ['stdout','stderr']:(A/(label+'.'+k)).write_bytes(getattr(c,k))
    row={'label':label,'argv':argv,'cwd':str(cwd),'exit_code':c.returncode,'seconds':time.monotonic()-start,
         'stdout_sha256':sha(A/(label+'.stdout')),'stderr_sha256':sha(A/(label+'.stderr'))}
    commands.append(row);save(A/'commands.json',commands)
    if c.returncode:print(c.stdout.decode(errors='replace')+c.stderr.decode(errors='replace'),flush=True)
    assert c.returncode==0,(label,str(A))
    return c.stdout.decode()
def pins(phase):
    rows=[]
    for pkg in json.loads((P/'lake-manifest.json').read_text())['packages']:
        loc=D/pkg['name'];rev=run(phase+'-'+pkg['name']+'-head',['git','rev-parse','HEAD'],loc).strip()
        status=run(phase+'-'+pkg['name']+'-status',['git','status','--porcelain','--untracked-files=no'],loc)
        assert rev==pkg['rev'] and not status
        rows.append({'name':pkg['name'],'revision':rev,'clean':True,'compiled_path_used':str(loc/'.lake/build/lib/lean') if (loc/'.lake/build/lib/lean').is_dir() else None})
    return rows
result={'utc_start':datetime.now(timezone.utc).isoformat(),'phase':'Author full source/type/axiom inspection; no independent final or Linux approval',
        'fresh_private_prefix':str(prefix),'initial_prefix_empty':True,'sources':sources,'pass':False}
try:
    before=pins('before');paths=[prefix]+[Path(r['compiled_path_used']) for r in before if r['compiled_path_used']]+[T/'lib/lean']
    assert len(before)==10 and len(paths)==11
    env=dict(baseenv,LEAN_PATH=':'.join(map(str,paths)),LEAN_SRC_PATH=str(S))
    version=run('lean-version',[str(T/'bin/lean'),'--version'],P)
    result.update(before_dependencies=before,LEAN_PATH=env['LEAN_PATH'],Lean_version=version,Lean_binary_sha256=sha(T/'bin/lean'))
    for live,rel in mapping.items():
        out=prefix/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
        label=Path(rel).stem
        log=run(label,[str(T/'bin/lean'),'-o',str(out),rel],S,env)
        assert not re.search(r'\b(?:error|warning):',log),label
        print(json.dumps({'module':label,'exit_code':0,'seconds':commands[-1]['seconds']}),flush=True)
    after=pins('after');assert before==after
    for n,h in frozen['files'].items():assert sha(P/n)==h,n
    for n,r in sources.items():assert ident(P/n)=={k:v for k,v in r.items() if k!='snapshot'},n
    log=(A/'Inspect.stdout').read_text()
    exact=re.findall(r'EXACT_FROZEN_TYPE (\S+):',log)
    assert exact==json.loads((P/'comparator.json').read_text())['theorem_names']
    summary=re.search(r'COMPLETE_ASSEMBLY roots=(\d+), closure=(\d+), required=(\d+)',log)
    assert summary and int(summary.group(1))==17
    ax=[]
    for rel in mapping.values():
        txt=(A/(Path(rel).stem+'.stdout')).read_text()
        for name,raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",txt):
            axioms=[x.strip() for x in raw.split(',') if x.strip()]
            assert set(axioms)<={'propext','Classical.choice','Quot.sound'}
            ax.append({'name':name,'axioms':axioms})
    save(A/'axioms.json',ax)
    result.update(pass_=True,after_dependencies=after,source_commands=len(mapping),exact_types=exact,
                  actual_project_closure=int(summary.group(2)),actual_material_dependencies=int(summary.group(3)),
                  actual_printed_axiom_reports=len(ax),actual_kernel_assertions=sum((S/rel).read_text().count('#assert_trust kernel ') for rel in mapping.values()),warnings=0)
    result['pass']=result.pop('pass_')
except Exception as e:
    result['error']=repr(e)
finally:
    objects={str(p.relative_to(prefix)):ident(p) for p in sorted(prefix.rglob('*')) if p.is_file()}
    save(A/'objects.json',objects);result.update(objects=objects,utc_end=datetime.now(timezone.utc).isoformat(),commands=commands)
    save(A/'result.json',result)
    save(E/'latest.json',{'attempt':str(A.relative_to(P)),'pass':result['pass'],'result_sha256':sha(A/'result.json')})
    print(json.dumps({'attempt':str(A),'pass':result['pass'],'source_commands':result.get('source_commands'),'types':len(result.get('exact_types',[])),'closure':result.get('actual_project_closure'),'axiom_reports':result.get('actual_printed_axiom_reports'),'error':result.get('error')}),flush=True)
    if not result['pass']:raise SystemExit(1)
