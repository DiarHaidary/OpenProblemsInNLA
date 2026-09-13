"""Independent statement/type audit only; admitted Challenge bodies are never proofs.

Exact contract propositions are separately elaborated as Prop-valued definitions.
This mechanical equality check supplements the reviewer's source-first judgment.
No Lake invocation, dependency download, or shared-cache write is performed.
"""
from pathlib import Path
import datetime, hashlib, json, os, platform, re, shutil, subprocess, tempfile, time, traceback

E=Path(__file__).resolve().parent
P=E.parents[1]
DEPS=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
LEAN=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean')
ORDER=['batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

def main():
    attempt=Path(tempfile.mkdtemp(prefix='attempt-',dir=E))
    src=attempt/'source';src.mkdir()
    obj=Path(tempfile.mkdtemp(prefix='nla-ke04-referee2-objects-'))
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    result={'phase':'second independent KE04 statement review','reviewer':'/root/mf16_final_referee','platform':platform.platform(),'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'private_prefix':str(obj),'no_prior_private_objects':not any(obj.iterdir()),'runner_sha256':sha(Path(__file__).read_bytes()),'commands':[],'inputs':{},'objects':[],'errors':[],'proof_build':False,'Comparator_run':False,'Linux_gate':False}
    save(attempt/'preflight.json',result)
    def cmd(args,cwd,label,timeout=60):
        start=time.monotonic()
        try:
            cp=subprocess.run(list(map(str,args)),cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
            out,err,rc=cp.stdout,cp.stderr,cp.returncode
        except subprocess.TimeoutExpired as exc:
            out,err,rc=exc.stdout or b'',exc.stderr or b'',None
        (attempt/(label+'.stdout')).write_bytes(out);(attempt/(label+'.stderr')).write_bytes(err)
        r={'command':list(map(str,args)),'cwd':str(cwd),'exit_code':rc,'seconds':time.monotonic()-start,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(out),'stderr_sha256':sha(err)}
        result['commands'].append(r);save(attempt/'progress.json',result)
        assert rc==0,r
        return out
    def pins(phase):
        manifest=json.loads((P/'lake-manifest.json').read_text())
        rows=[]
        for d in manifest['packages']:
            path=DEPS/d['name']
            head=cmd(['git','rev-parse','HEAD'],path,phase+'-'+d['name']+'-head').decode().strip()
            status=cmd(['git','status','--porcelain=v1','--untracked-files=all'],path,phase+'-'+d['name']+'-status')
            assert head==d['rev'] and status==b''
            build=path/'.lake/build/lib/lean'
            if d['name'] in ORDER:assert build.is_dir()
            rows.append({'name':d['name'],'revision':head,'clean':True,'compiled_path_used':str(build) if d['name'] in ORDER else None})
        assert len(rows)==10
        result[phase+'_dependencies']=rows
    try:
        for name in ['NLA/KE04/Definitions.lean','Challenge.lean','lean-toolchain','lakefile.toml','lake-manifest.json','comparator.json']:
            f=src/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((P/name).read_bytes());f.chmod(0o444)
            result['inputs'][name]={'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size}
        definitions=(src/'NLA/KE04/Definitions.lean').read_text();challenge=(src/'Challenge.lean').read_text()
        defs=['NLA.KE04.'+x for x in re.findall(r'^(?:abbrev|def) (\w+)',definitions,re.M)]
        contracts=re.findall(r'^theorem (\w+)(.*?) := by sorry',challenge,re.M|re.S)
        names=['NLA.KE04.'+n for n,s in contracts]
        cfg=json.loads((src/'comparator.json').read_text())
        assert len(defs)==27 and len(contracts)==24 and cfg['theorem_names']==names
        assert cfg['definition_names']==[] and set(cfg['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
        inspect='import NLA.KE04.Definitions\nimport LeanCert.Tactic.Verification\nimport Lean.Util.FoldConsts\nset_option leancert.trust "kernel"\nset_option maxHeartbeats 1200000\n'
        inspect+='\n'.join('#assert_trust kernel '+n+'\n#print axioms '+n for n in defs)+'\n'
        inspect+='''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let roots : List Name := [ROOTS]
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  let mut pending := roots
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:4000] do
    match pending with
    | [] => pure ()
    | n :: rest =>
      pending := rest
      unless seen.contains n do
        seen := n :: seen
        let some ci := env.find? n | throwError "Missing actual definition {n}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial definition {n}"
        let axioms ← liftCoreM <| collectAxioms n
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonstandard definition axiom {n}: {ax}"
        let some v := ci.value? (allowOpaque := true) | throwError "Bodyless definition {n}"
        let ds := ci.type.getUsedConstants.toList ++ v.getUsedConstants.toList
        used := ds ++ used
        pending := ds.filter isProject ++ pending
        logInfo m!"DEFINITION_CLOSURE {n}: axioms={axioms.toList}; dependencies={ds}"
  unless pending.isEmpty do throwError "Incomplete definition traversal"
  for bad in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains bad then throwError "Forbidden definition dependency {bad}"
  logInfo m!"DEFINITION_COUNTS roots={roots.length}, closure={seen.length}"
'''.replace('ROOTS',', '.join('``'+n for n in defs))
        inspect+='set_option pp.all true\n'+'\n'.join('#print '+n for n in defs)+'\n'
        types='import Challenge\nimport Lean.Util.FoldConsts\nset_option maxHeartbeats 1200000\nopen NLA.KE04\nnoncomputable section\nnamespace KE04Referee2Expected\n'
        for name,sig in contracts:
            depth=0;split=None
            for i,ch in enumerate(sig):
                if ch in '({[':depth+=1
                elif ch in ')}]':depth-=1
                elif ch==':' and depth==0:split=i;break
            assert split is not None,name
            binders=sig[:split].strip();prop=sig[split+1:].strip()
            types+='def '+name+' : Prop := '+('∀ '+binders+',\n' if binders else '')+prop+'\n\n'
        types+='end KE04Referee2Expected\nset_option pp.all true\n'
        types+='''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs : List (Name × Name) := [PAIRS]
  let forbidden := pairs.map Prod.fst
  for (actual, expected) in pairs do
    let some a := env.find? actual | throwError "Missing actual target {actual}"
    let some b := env.find? expected | throwError "Missing separately elaborated proposition {expected}"
    let some expectedType := b.value? (allowOpaque := true) | throwError "Missing proposition body"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Target is not a theorem {actual}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type expectedType do
        throwError "Exact reviewed type mismatch {actual}"
    let axioms ← liftCoreM <| collectAxioms expected
    for ax in axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Nonstandard axiom in proposition, not proof: {actual}: {ax}"
    let direct := a.type.getUsedConstants.toList
    for dep in direct do
      if forbidden.contains dep || dep == ``sorryAx then
        throwError "A target type depends on a reference hole: {actual}: {dep}"
    logInfo m!"EXACT_REVIEWED_TYPE {actual}: {a.type}"
    logInfo m!"TYPE_ONLY_SAFE {actual}: axioms={axioms.toList}; direct={direct}"
  logInfo m!"TYPE_COUNTS exact={pairs.length}; Challenge_bodies_not_used_as_proofs"
'''.replace('PAIRS',', '.join('(``NLA.KE04.'+n+', ``KE04Referee2Expected.'+n+')' for n,s in contracts))
        for name,body in [('InspectDefinitions.lean',inspect),('InspectTypes.lean',types)]:
            f=src/name;f.write_text(body);f.chmod(0o444);result['inputs'][name]={'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size,'role':'reviewer-generated exact definition/type inspector'}
        result['definition_names']=defs;result['target_names']=names
        pins('before')
        env['LEAN_PATH']=':'.join([str(obj)]+[str(DEPS/d/'.lake/build/lib/lean') for d in ORDER])
        env['LEAN_SRC_PATH']=str(src)
        result['LEAN_PATH']=env['LEAN_PATH'];result['LEAN_SRC_PATH']=env['LEAN_SRC_PATH'];result['lean_binary_sha256']=sha(LEAN.read_bytes())
        version=cmd([LEAN,'--version'],src,'Lean-version').decode()
        assert '4.33.1' in version
        for name in ['NLA/KE04/Definitions','InspectDefinitions','Challenge','InspectTypes']:
            out=obj/(name+'.olean');out.parent.mkdir(parents=True,exist_ok=True)
            cmd([LEAN,'-o',out,name+'.lean'],src,name.replace('/','-'))
        dl=(attempt/'InspectDefinitions.stdout').read_text();tl=(attempt/'InspectTypes.stdout').read_text()
        assert 'DEFINITION_COUNTS roots=27, closure=33' in dl
        assert tl.count('EXACT_REVIEWED_TYPE ')==24 and tl.count('TYPE_ONLY_SAFE ')==24
        assert 'TYPE_COUNTS exact=24; Challenge_bodies_not_used_as_proofs' in tl
        reports={}
        for name,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",dl):reports[name]=[x.strip() for x in ax.split(',') if x.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms",dl):reports[name]=[]
        assert set(reports)==set(defs) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in reports.values())
        assert (attempt/'Challenge.stdout').read_text().count('declaration uses `sorry`')==24
        result['actual_successful_Lean_commands']=4;result['kernel_assertions']=27;result['definition_closure']=33;result['exact_types']=24;result['definition_axioms']=reports
    except Exception:
        result['errors'].append(traceback.format_exc())
    finally:
        try:pins('after')
        except Exception:result['errors'].append(traceback.format_exc())
        for name,r in result['inputs'].items():
            if (P/name).exists():assert sha((P/name).read_bytes())==r['sha256'],name
        for f in sorted(obj.rglob('*')):
            if f.is_file():result['objects'].append({'path':str(f.relative_to(obj)),'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size})
        shutil.rmtree(obj);result['own_private_prefix_removed']=not obj.exists()
        result['success']=not result['errors'];result['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        save(attempt/'result.json',result)
    print(json.dumps({'attempt':str(attempt),'success':result['success'],'errors':result['errors'],'commands':result.get('actual_successful_Lean_commands'),'types':result.get('exact_types'),'kernel_assertions':result.get('kernel_assertions'),'closure':result.get('definition_closure'),'own_objects_removed':len(result['objects'])},indent=2))
    raise SystemExit(0 if result['success'] else 1)

if __name__=='__main__':main()
