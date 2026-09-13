"""Compile immutable Transport source snapshots using only read-only shared dependencies."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,re,shutil,subprocess,tempfile,time,traceback
E=Path(__file__).resolve().parent;P=E.parents[1]
PACKAGES=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
LEAN=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean')
ORDER=['batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
TARGETS=['quadratic_forms_agree','later_quadratic_identity','interval_index_validity','fullPrefix_implies_canonical']
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--final',action='store_true');args=ap.parse_args()
    a=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));s=a/'source';s.mkdir()
    o=Path(tempfile.mkdtemp(prefix='nla-ke04-transport-objects-'))
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    r={'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'KE04 Transport proof development, not independent review','platform':platform.platform(),'final_requested':args.final,'private_prefix':str(o),'fresh_empty_prefix':not any(o.iterdir()),'inputs':{},'commands':[],'errors':[]}
    def run(cmd,cwd,label,timeout=120):
        now=time.monotonic()
        try:
            cp=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
            stdout,stderr,rc=cp.stdout,cp.stderr,cp.returncode
        except subprocess.TimeoutExpired as err:stdout,stderr,rc=err.stdout or b'',err.stderr or b'',None
        (a/(label+'.stdout')).write_bytes(stdout);(a/(label+'.stderr')).write_bytes(stderr)
        rec={'command':list(map(str,cmd)),'cwd':str(cwd),'exit_code':rc,'seconds':time.monotonic()-now,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr)}
        r['commands'].append(rec);save(a/'progress.json',r)
        assert rc==0,rec
        return stdout
    def pins(phase):
        records=[]
        for d in json.loads((P/'lake-manifest.json').read_text())['packages']:
            q=PACKAGES/d['name'];steps=[]
            for cmd in [['git','rev-parse','HEAD'],['git','status','--porcelain=v1','--untracked-files=all']]:
                cp=subprocess.run(cmd,cwd=q,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                steps.append({'command':cmd,'cwd':str(q),'exit_code':cp.returncode,'stdout':cp.stdout.decode(),'stderr':cp.stderr.decode()})
                assert cp.returncode==0,steps[-1]
            assert steps[0]['stdout'].strip()==d['rev'] and steps[1]['stdout']==''
            build=q/'.lake/build/lib/lean'
            if d['name'] in ORDER:assert build.is_dir()
            records.append({'name':d['name'],'expected_revision':d['rev'],'used_build_path':str(build) if d['name'] in ORDER else None,'checks':steps})
        r[phase+'_dependencies']=records;save(a/(phase+'-dependencies.json'),records)
    try:
        for name in ['NLA/KE04/Definitions.lean','NLA/KE04/Krylov.lean','NLA/KE04/Frames.lean','NLA/KE04/Spectral.lean','NLA/KE04/Transport.lean','Challenge.lean','lean-toolchain','lakefile.toml','lake-manifest.json','verification/proof-start.json','reviews/statement-freeze.json']:
            f=s/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((P/name).read_bytes());f.chmod(0o444)
            r['inputs'][name]={'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size}
        (s/'executed-runner.py.txt').write_bytes(Path(__file__).read_bytes())
        frozen=json.loads((P/'reviews/statement-freeze.json').read_text())['files']
        for name,h in frozen.items():assert sha((P/name).read_bytes())==h,name
        assert len(frozen)==1598
        assert r['inputs']['verification/proof-start.json']['sha256']=='5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624'
        assert r['inputs']['reviews/statement-freeze.json']['sha256']=='85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e'
        source=(s/'NLA/KE04/Transport.lean').read_text()
        assert 'import Challenge' not in source and not re.search(r'\b(sorry|axiom|native_decide|unsafe)\b',source)
        if args.final:
            contracts=dict(re.findall(r'^theorem (\w+)(.*?) := by sorry',(s/'Challenge.lean').read_text(),re.M|re.S))
            inspector='import NLA.KE04.Transport\nimport Lean.Util.FoldConsts\nnoncomputable section\nopen scoped BigOperators\nopen NLA.KE04\nnamespace KE04TransportExpected\n'
            for name in TARGETS:
                sig=contracts[name];depth=0;split=None
                for i,ch in enumerate(sig):
                    if ch in '({[':depth+=1
                    elif ch in ')}]':depth-=1
                    elif ch==':' and depth==0:split=i;break
                assert split is not None
                bind=sig[:split].strip();typ=sig[split+1:].strip()
                inspector+='def '+name+' : Prop := '+('∀ '+bind+',\n' if bind else '')+typ+'\n\n'
            inspector+='end KE04TransportExpected\nset_option leancert.trust "kernel"\nset_option maxHeartbeats 1600000\n'
            inspector+='\n'.join('#assert_trust kernel NLA.KE04._proved.'+n+'\n#print axioms NLA.KE04._proved.'+n for n in TARGETS)+'\n'
            inspector+='''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let targets : List (Name × Name) := [TARGET_PAIRS]
  for (actual, expected) in targets do
    let some ci := env.find? actual | throwError "Missing actual proof {actual}"
    let some expectedCI := env.find? expected | throwError "Missing exact target"
    let some expectedType := expectedCI.value? (allowOpaque := true) | throwError "Missing expected type"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq ci.type expectedType do throwError "Frozen type mismatch {actual}"
    logInfo m!"EXACT_CONTRACT {actual}: {ci.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." || n.toString.startsWith "_private.NLA.KE04."
  let mut pending := targets.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:6000] do
    match pending with
    | [] => pure ()
    | n :: rest =>
      pending := rest
      unless seen.contains n do
        seen := n :: seen
        let some ci := env.find? n | throwError "Missing project declaration {n}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial declaration {n}"
        let axs ← liftCoreM <| collectAxioms n
        for ax in axs do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonstandard actual axiom {n}: {ax}"
        let some body := ci.value? (allowOpaque := true) | throwError "Bodyless declaration {n}"
        let ds := ci.type.getUsedConstants.toList ++ body.getUsedConstants.toList
        used := ds ++ used
        pending := ds.filter isProject ++ pending
        logInfo m!"ACTUAL_PROJECT {n}: axioms={axs.toList}; dependencies={ds}"
  unless pending.isEmpty do throwError "Incomplete actual traversal"
  for bad in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains bad then throwError "Forbidden dependency {bad}"
  let required := [``NLA.KE04._proved.krylov_mono,
    ``NLA.KE04._proved.act_mem_krylov_succ,
    ``NLA.KE04._proved.frameProjection_fixed_iff,
    ``NLA.KE04._proved.frame_inner,
    ``NLA.KE04._proved.compression_action_coordinates,
    ``NLA.KE04._proved.quadratic_semantics,
    ``NLA.KE04._proved.inner_act_transpose,
    ``NLA.KE04.compressedQuadratic, ``NLA.KE04.quadraticMatrix,
    ``NLA.KE04.form, ``NLA.KE04.krylov, ``NLA.KE04.IsKrylovBasis,
    ``NLA.KE04.FullPrefixBlockLanczosClaim, ``NLA.KE04.BlockLanczosConjecture]
  for dep in required do
    unless used.contains dep do throwError "Missing material dependency {dep}"
    logInfo m!"MATERIAL_DEPENDENCY {dep}"
  logInfo m!"FINAL_COUNTS contracts={targets.length}, closure={seen.length}, material={required.length}"
'''.replace('TARGET_PAIRS',', '.join('(``NLA.KE04._proved.'+n+', ``KE04TransportExpected.'+n+')' for n in TARGETS))
            f=s/'Inspect.lean';f.write_text(inspector);f.chmod(0o444);r['inputs']['Inspect.lean']={'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size}
        pins('before')
        env['LEAN_PATH']=':'.join([str(o)]+[str(PACKAGES/d/'.lake/build/lib/lean') for d in ORDER]);env['LEAN_SRC_PATH']=str(s)
        r['LEAN_PATH']=env['LEAN_PATH'];r['LEAN_SRC_PATH']=env['LEAN_SRC_PATH'];r['lean_binary_sha256']=sha(LEAN.read_bytes())
        run([LEAN,'--version'],s,'version')
        for mod in ['NLA/KE04/Definitions','NLA/KE04/Krylov','NLA/KE04/Frames','NLA/KE04/Spectral','NLA/KE04/Transport']+(['Inspect'] if args.final else []):
            f=o/(mod+'.olean');f.parent.mkdir(parents=True,exist_ok=True)
            run([LEAN,'-o',f,mod+'.lean'],s,mod.replace('/','-'))
        log=(a/'NLA-KE04-Transport.stdout').read_text()
        reports=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log)
        assert len(reports)==11
        assert all(set(x.strip() for x in axs.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'} for name,axs in reports)
        r['module_kernel_assertions']=11;r['module_axiom_reports']=dict(reports)
        if args.final:
            il=(a/'Inspect.stdout').read_text();assert il.count('EXACT_CONTRACT ')==4 and 'FINAL_COUNTS contracts=4' in il
            r['final_inspection_counts']=re.search(r'FINAL_COUNTS contracts=(\d+), closure=(\d+), material=(\d+)',il).groups()
    except Exception:r['errors'].append(traceback.format_exc())
    finally:
        try:pins('after')
        except Exception:r['errors'].append(traceback.format_exc())
        r['objects']=[{'path':str(f.relative_to(o)),'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size} for f in sorted(o.rglob('*')) if f.is_file()]
        shutil.rmtree(o);r['own_prefix_removed']=not o.exists()
        r['success']=not r['errors'];r['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(a/'result.json',r)
    print(json.dumps({'attempt':str(a),'success':r['success'],'errors':r['errors'],'final_counts':r.get('final_inspection_counts'),'objects_removed':len(r['objects'])},indent=2))
    raise SystemExit(0 if r['success'] else 1)
if __name__=='__main__':main()
