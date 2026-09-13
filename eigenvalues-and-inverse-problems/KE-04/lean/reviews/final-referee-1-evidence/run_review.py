"""Independent KE-04 final referee 1 fresh direct-source validation.

Invoke only after receiving the complete proof freeze. Reuses the author's
read-only dependency cache, never any target object. Retains every command and
failure. This is local macOS elaboration and trust inspection, not Comparator.
"""
from pathlib import Path
import datetime, hashlib, json, os, platform, re, subprocess, sys, tempfile, time, traceback
P=Path(__file__).resolve().parents[2]
E=Path(__file__).resolve().parent
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
G=Path('/tmp/nla-lean-ra20-worktree')
STANDARD={'propext','Classical.choice','Quot.sound'}
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
phase=sys.argv[1]
state=E/'execution.json'
if phase=='build':
    assert len(sys.argv)==3 and not state.exists()
    R={'reviewer':'/root/ra09_final_referee1','role':'Independent KE-04 final mathematical referee 1',
       'independence':'No KE-04 statement, design, proof or mathematical-fix contribution',
       'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'platform':platform.platform(),'proof_freeze_sha256':sys.argv[2],
       'commands':[],'status':'RUNNING','scope':'Fresh target-only direct-source macOS check; 10 pinned Git sources and 9 dependency object directories read-only; not Linux, Comparator or external default-kernel replay.'}
else:
    R=json.loads(state.read_text())
def save():state.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n')
def cmd(label,argv,cwd=P,env=None,allowed=(0,),timeout=180):
    idx=len(R['commands']); stem=f'command-{idx:03d}-{label}'
    t=time.monotonic()
    timed_out=False
    try:
        cp=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        timed_out=True
        cp=subprocess.CompletedProcess(argv,124,exc.stdout or b'',exc.stderr or b'')
    out=E/(stem+'.stdout');err=E/(stem+'.stderr')
    assert not out.exists() and not err.exists()
    out.write_bytes(cp.stdout);err.write_bytes(cp.stderr)
    row={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'exit_code':cp.returncode,
         'allowed_exit_codes':list(allowed),
         'seconds':round(time.monotonic()-t,3),'timed_out':timed_out,'stdout':out.name,'stdout_sha256':sha(out),
         'stderr':err.name,'stderr_sha256':sha(err)}
    R['commands'].append(row);save()
    assert cp.returncode in allowed,(stem,cp.returncode)
    return cp.stdout
def frozen():
    checks=[]
    for rel,h in [('reviews/proof-freeze.json',R['proof_freeze_sha256']),
                  ('reviews/statement-freeze.json','85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e')]:
        f=P/rel;assert sha(f)==h,rel
        d=json.loads(f.read_text())
        for name,digest in d['files'].items():
            assert sha(P/name)==digest,(rel,name)
            if 'file_sizes' in d:assert (P/name).stat().st_size==d['file_sizes'][name]
        checks.append({'path':rel,'sha256':h,'files':len(d['files'])})
    return checks
def pins(label):
    rows=[];env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    for dep in json.loads((P/'lake-manifest.json').read_text())['packages']:
        name=dep['name'];d=C/name
        head=cmd(label+'-'+name+'-head',['git','rev-parse','HEAD'],d,env).decode().strip()
        assert head==dep['rev'],name
        status=cmd(label+'-'+name+'-clean',['git','status','--porcelain=v1'],d,env)
        assert not status,name
        obj=d/'.lake/build/lib/lean'
        rows.append({'name':name,'rev':head,'path':str(d),'clean':True,
                     'object_directory':str(obj),'object_directory_exists':obj.is_dir(),
                     'used_in_lean_path':name!='Cli'})
        assert obj.is_dir()==(name!='Cli'),name
    assert len(rows)==10
    return rows
def provenance():
    records=[]; env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    inv=json.loads((P/'verification/original-source-inventory.json').read_text())
    for i,(rel,d) in enumerate(inv['files'].items()):
        b=cmd(f'original-{i:02d}',['git','show',d['commit']+':'+d['upstream_path']],G,env)
        assert b==(P/rel).read_bytes() and blob(b)==d['git_blob']
        assert sha(P/rel)==d['sha256'] and len(b)==d['bytes']
        records.append({'kind':'original','path':rel,'sha256':sha(P/rel),'git_blob':blob(b),'commit':d['commit']})
    assert len(records)==17
    api=json.loads((P/'verification/api-evidence-complete/manifest.json').read_text())
    for i,(rel,d) in enumerate(api['files'].items()):
        b=(P/rel).read_bytes()
        assert sha(P/rel)==d['sha256'] and len(b)==d['bytes'] and blob(b)==d['git_blob']
        if '/tauceti/' not in rel:
            actual=cmd(f'api-{i:02d}',['git','show',d['commit']+':'+d['upstream_path']],Path(d['repo']),env)
            assert actual==b,rel
        else:
            assert Path(d['repo'],d['upstream_path']).read_bytes()==b,rel
        records.append({'kind':'api','path':rel,'sha256':sha(P/rel),'git_blob':blob(b),'commit':d['commit']})
    assert len(records)==50
    return records
def key_objects():
    paths=[L/'bin/lean', C/'leancert/.lake/build/lib/lean/LeanCert/Tactic/Verification.olean',
      C/'mathlib/.lake/build/lib/lean/Mathlib/Analysis/InnerProductSpace/Spectrum.olean',
      C/'mathlib/.lake/build/lib/lean/Mathlib/Analysis/Matrix/Order.olean',
      C/'mathlib/.lake/build/lib/lean/Mathlib/LinearAlgebra/LinearIndependent/Defs.olean',
      C/'mathlib/.lake/build/lib/lean/Mathlib/Analysis/InnerProductSpace/PiL2.olean']
    return [{'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f)} for f in paths]
try:
    save()
    if phase=='build':
        R['frozen_before']=frozen();save()
        R['lean_version']=cmd('lean-version',[str(L/'bin/lean'),'--version']).decode().strip()
        R['pins_before']=pins('before');save()
        R['provenance']=provenance();R['key_objects_before']=key_objects();save()
        cmd('reuse-spectral',['rg','-n','eigenvalues_antitone|roots_charpoly_eq_eigenvalues|apply_eigenvectorBasis|eigenvalues_eq_eigenvalues_iff',
            'Mathlib/Analysis/InnerProductSpace/Spectrum.lean'],C/'mathlib')
        cmd('reuse-dimension-kernel',['rg','-n','finrank_sup_add_finrank_inf_eq|dotProduct_mulVec_zero_iff|linearIndependent_iff_injective_fintypeLinearCombination',
            'Mathlib/LinearAlgebra/FiniteDimensional/Lemmas.lean','Mathlib/Analysis/Matrix/Order.lean',
            'Mathlib/LinearAlgebra/LinearIndependent/Defs.lean'],C/'mathlib')
        cmd('reuse-Krylov-Lanczos',['rg','-n','Krylov|Lanczos|krylov|lanczos','Mathlib'],C/'mathlib',allowed=(0,1))
        prefix=Path(tempfile.mkdtemp(prefix='ke04-final-referee1-',dir='/tmp/nla-lean-formalization/independent-prefixes'))
        assert not list(prefix.iterdir())
        order=['batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
        R['prefix']=str(prefix);R['prefix_initially_empty']=True
        R['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
        save()
        source=(P/'Challenge.lean').read_text()
        assert source.count('namespace NLA.KE04\n')==1 and source.count('end NLA.KE04\n')==1
        reference=source.replace('namespace NLA.KE04\n','namespace NLA.KE04.FinalReferee1Reference\n').replace('end NLA.KE04\n','end NLA.KE04.FinalReferee1Reference\n')
        (E/'Reference.lean').write_text(reference)
        (E/'reference-derivation.json').write_text(json.dumps({'source':'Challenge.lean','source_sha256':sha(P/'Challenge.lean'),'derived_sha256':sha(E/'Reference.lean'),'only_change':'namespace and matching end NLA.KE04 -> NLA.KE04.FinalReferee1Reference','reference_admissions':24,'implementation_must_not_depend_on_reference':True},indent=2)+'\n')
        sources=['NLA/KE04/'+n+'.lean' for n in ['Definitions','Krylov','Frames','Spectral','SpectralWindow','Transport','Intersection','Nonannihilation','Completion','Proof']]+['Solution.lean','reviews/final-referee-1-evidence/Reference.lean','reviews/final-referee-1-evidence/Inspect.lean']
        env=dict(os.environ,LEAN_PATH=R['LEAN_PATH'])
        R['source_inputs']=[];R['lean_modules']=[]
        for rel in sources:
            f=P/rel;stem=rel.replace('/','-').replace('.lean','')
            snapshot=E/(stem+'.source.txt');assert not snapshot.exists()
            snapshot.write_bytes(f.read_bytes())
            target=prefix/Path(rel).with_suffix('.olean');target.parent.mkdir(parents=True,exist_ok=True)
            assert not target.exists()
            R['source_inputs'].append({'path':rel,'sha256':sha(f),'snapshot':snapshot.name});save()
            out=cmd('compile-'+stem,[str(L/'bin/lean'),'-o',str(target),'-i',str(target.with_suffix('.ilean')),str(f)],P,env).decode()
            assert sha(f)==sha(snapshot),rel
            if rel.endswith('/Reference.lean'):
                assert out.count('warning: declaration uses `sorry`')==24 and out.count('warning:')==24
            else:
                assert 'error:' not in out,rel
                for closure in re.findall(r'depends on axioms:\s*\[(.*?)\]',out,re.S):
                    assert {s.strip() for s in closure.split(',') if s.strip()}<=STANDARD,closure
            R['lean_modules'].append({'path':rel,'stdout':R['commands'][-1]['stdout'],'exit_code':0,
                'warning_count':out.count('warning:')});save()
            print(rel,'PASS',R['commands'][-1]['seconds'],flush=True)
        R['pins_after']=pins('after');assert R['pins_after']==R['pins_before']
        R['frozen_after']=frozen();assert R['frozen_after']==R['frozen_before']
        R['key_objects_after']=key_objects();assert R['key_objects_after']==R['key_objects_before']
        R['status']='PASS_LOCAL_SOURCE_AND_INSPECTION'
    elif phase=='cleanup':
        assert R['status']=='PASS_LOCAL_SOURCE_AND_INSPECTION'
        assert frozen()==R['frozen_before']
        prefix=Path(R['prefix']);assert prefix.is_dir()
        owned=[{'path':str(f.relative_to(prefix)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(prefix.rglob('*')) if f.is_file()]
        R['owned_generated_before_cleanup']=owned;save()
        for r in owned:
            f=prefix/r['path'];assert sha(f)==r['sha256'] and f.stat().st_size==r['bytes'];f.unlink()
        for d in sorted([x for x in prefix.rglob('*') if x.is_dir()],key=lambda x:len(x.parts),reverse=True):d.rmdir()
        prefix.rmdir();R['only_recorded_owned_generated_objects_removed']=True
    else:raise ValueError(phase)
    R['last_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    R['runner_sha256']=sha(__file__);save()
except BaseException:
    R['status']='FAIL';R['failure']=traceback.format_exc();save();raise
