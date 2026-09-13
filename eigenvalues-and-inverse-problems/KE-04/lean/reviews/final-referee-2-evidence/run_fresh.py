"""Independent KE04 fresh-source review; no Lake or dependency mutation.

Operational layout follows this reviewer's earlier NLA reviews and the inspected
KE04 author runner. The namespace-only Challenge copy, two independent closure
roots, exact imported-module provenance, and inspector are new reviewer checks.
This is macOS source elaboration, not Linux Comparator/default-kernel replay.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,re,shutil,subprocess,tempfile,time,traceback

E=Path(__file__).resolve().parent; P=E.parents[1]
PKG=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
LEAN=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean')
ORDER=['batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
MODULES=['Definitions','Krylov','Frames','Spectral','SpectralWindow','Transport','Intersection','Nonannihilation','Completion','Proof']
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')

def inspector(targets):
    text='''import Solution
import Reference
import Lean.Util.FoldConsts
set_option leancert.trust "kernel"
set_option maxHeartbeats 4000000
set_option pp.universes true
set_option pp.proofs false
'''
    text+='\n'.join('#assert_trust kernel '+n+'\n#print axioms '+n for n in targets)+'\n'
    text+='''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  logInfo m!"LOCAL_ELABORATION_TRUST_LEVEL {env.header.trustLevel}"
  for n in env.header.moduleNames do logInfo m!"IMPORTED_MODULE {n}"
  let targets : List Name := [TARGETS]
  for n in targets do
    let expected := ("NLA.KE04.Reference." ++ (n.toString.splitOn ".").getLast!).toName
    let some actualCI := env.find? n | throwError "No actual theorem {n}"
    let some refCI := env.find? expected | throwError "No reference theorem {expected}"
    unless actualCI.isTheorem do throwError "Not a theorem: {n}"
    liftTermElabM do
      unless ← Meta.isDefEq actualCI.type refCI.type do throwError "Type differs: {n}"
    let axs ← liftCoreM <| collectAxioms n
    for ax in axs do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unallowed axiom at actual target {n}: {ax}"
    let referenceAxioms ← liftCoreM <| collectAxioms expected
    unless referenceAxioms.contains ``sorryAx do throwError "Reference did not retain deliberate hole {expected}"
    logInfo m!"EXACT_FROZEN_TYPE {n}: {actualCI.type}"
    logInfo m!"REFERENCE_ONLY_PLACEHOLDER {expected}"
  let isProject := fun n : Name =>
    (n.toString.startsWith "NLA.KE04." && !n.toString.startsWith "NLA.KE04.Reference.") ||
    n.toString.startsWith "_private.NLA.KE04."
  let groups : List (String × List Name) :=
    [("FINAL_TARGET", [``NLA.KE04.blockLanczosConjecture]), ("ALL_EXPORTS", targets)]
  for (label, roots) in groups do
    let mut pending := roots
    let mut seen : List Name := []
    let mut used : List Name := []
    for _ in [:20000] do
      match pending with
      | [] => pure ()
      | n :: tail =>
        pending := tail
        unless seen.contains n do
          seen := n :: seen
          let some ci := env.find? n | throwError "Unknown reached declaration {n}"
          if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial {n}"
          let some body := ci.value? (allowOpaque := true) | throwError "Missing body {n}"
          let axs ← liftCoreM <| collectAxioms n
          for ax in axs do
            unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
              throwError "Nonstandard reached axiom {n}: {ax}"
          let ds := ci.type.getUsedConstants.toList ++ body.getUsedConstants.toList
          for dep in ds do
            if dep.toString.startsWith "NLA.KE04.Reference." || dep == ``sorryAx ||
                dep == ``Lean.ofReduceBool || dep == ``Lean.ofReduceNat || dep == ``Lean.trustCompiler then
              throwError "Forbidden reached dependency {dep} in {n}"
          used := ds ++ used
          pending := ds.filter isProject ++ pending
          logInfo m!"REACHED {label} {n}; AXIOMS {axs.toList}; DIRECT {ds}"
    unless pending.isEmpty do throwError "Traversal incomplete {label}"
    let requiredFinal : List Name := [
      ``NLA.KE04._proved.strictIntervalOccupancy,
      ``NLA.KE04._proved.interval_index_validity,
      ``NLA.KE04._proved.spectral_window_subspace,
      ``NLA.KE04._proved.spectral_gap_quadratic_psd,
      ``NLA.KE04._proved.krylov_intersection_nonzero,
      ``NLA.KE04._proved.quadratic_forms_agree,
      ``NLA.KE04._proved.later_quadratic_identity,
      ``NLA.KE04._proved.psd_zero_form_iff_kernel,
      ``NLA.KE04._proved.fullRank_quadratic_nonannihilation,
      ``NLA.KE04._proved.fullRank_krylov_eigenvector_zero,
      ``NLA.KE04._proved.blockShift_eq_smul_extend,
      ``NLA.KE04._proved.fullBlockDimension_prefix,
      ``NLA.KE04._proved.act_mem_krylov_succ,
      ``NLA.KE04._proved.krylov_mono,
      ``NLA.KE04._proved.orderedSpectrum_semantics,
      ``NLA.KE04._proved.compressedQuadratic_semantics,
      ``NLA.KE04.act, ``NLA.KE04.krylov, ``NLA.KE04.krylovCombination,
      ``NLA.KE04.FullBlockDimension, ``NLA.KE04.IsKrylovBasis,
      ``NLA.KE04.orderedEigenvalues, ``NLA.KE04.orderedEigenbasis,
      ``NLA.KE04.ritzValueAt, ``NLA.KE04.ritzValues,
      ``NLA.KE04.compression, ``NLA.KE04.quadraticMatrix,
      ``NLA.KE04.compressedQuadratic, ``NLA.KE04.IterationOccupancy,
      ``NLA.KE04.BlockLanczosConjecture, ``NLA.KE04.FullPrefixBlockLanczosClaim]
    let requiredAll : List Name := [
      ``NLA.KE04._proved.lastFullBlockIteration_exists,
      ``NLA.KE04._proved.submodule_frame_exists,
      ``NLA.KE04._proved.compression_basis_independent,
      ``Matrix.toEuclideanLin,
      ``Fintype.linearCombination,
      ``Submodule.finrank_sup_add_finrank_inf_eq,
      ``LinearMap.IsSymmetric.eigenvalues_antitone,
      ``LinearMap.IsSymmetric.roots_charpoly_eq_eigenvalues,
      ``Matrix.PosSemidef.dotProduct_mulVec_zero_iff]
    let required := requiredFinal ++ (if label == "ALL_EXPORTS" then requiredAll else [])
    for dep in required do
      unless used.contains dep || seen.contains dep do throwError "Unreached material dependency {label}: {dep}"
      logInfo m!"REQUIRED_DEPENDENCY {label} {dep}"
    logInfo m!"CLOSURE_TOTAL {label} reached={seen.length} required={required.length}"
'''.replace('TARGETS',', '.join('``'+t for t in targets))
    return text

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--freeze-sha256',required=True);a=ap.parse_args()
    freeze_bytes=(P/'reviews/proof-freeze.json').read_bytes();assert sha(freeze_bytes)==a.freeze_sha256
    frozen=json.loads(freeze_bytes)
    for rel,h in frozen['files'].items():assert sha((P/rel).read_bytes())==h,rel
    A=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));S=A/'source';S.mkdir()
    O=Path(tempfile.mkdtemp(prefix='nla-ke04-referee2-objects-'))
    R={'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'Independent final mathematical referee 2','platform':platform.platform(),'freeze_sha256':a.freeze_sha256,'source_inputs':{},'commands':[],'errors':[],'object_prefix':str(O),'prefix_started_empty':not any(O.iterdir())}
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
    def run(cmd,cwd,label,timeout=180):
        t=time.monotonic();cmd=list(map(str,cmd))
        try:
            cp=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=timeout);out,err,rc=cp.stdout,cp.stderr,cp.returncode
        except subprocess.TimeoutExpired as ex:out,err,rc=ex.stdout or b'',ex.stderr or b'',None
        (A/(label+'.stdout')).write_bytes(out);(A/(label+'.stderr')).write_bytes(err)
        r={'argv':cmd,'cwd':str(cwd),'exit_code':rc,'seconds':time.monotonic()-t,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(out),'stderr_sha256':sha(err)}
        R['commands'].append(r);save(A/'progress.json',R)
        assert rc==0,r
        return out
    def pins(phase):
        records=[]
        for x in json.loads((P/'lake-manifest.json').read_text())['packages']:
            q=PKG/x['name'];head=run(['git','rev-parse','HEAD'],q,phase+'-'+x['name']+'-head').decode().strip()
            status=run(['git','status','--porcelain=v1','--untracked-files=all'],q,phase+'-'+x['name']+'-status').decode()
            assert head==x['rev'] and not status,(head,status,x)
            build=q/'.lake/build/lib/lean';used=x['name'] in ORDER
            assert not used or build.is_dir()
            records.append({'package':x['name'],'revision':head,'clean':not status,'read_only_build':str(build) if used else None})
        save(A/(phase+'-pins.json'),records);R[phase+'_pins']=records
    try:
        inputs=['NLA/KE04/'+m+'.lean' for m in MODULES]+['Solution.lean','Challenge.lean','comparator.json','lakefile.toml','lake-manifest.json','lean-toolchain','reviews/proof-freeze.json','verification/proof-start.json']
        for rel in inputs:
            b=(P/rel).read_bytes();q=S/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);q.chmod(0o444);R['source_inputs'][rel]={'sha256':sha(b),'bytes':len(b)}
        challenge=(S/'Challenge.lean').read_text();assert challenge.count('namespace NLA.KE04\n')==1 and challenge.count('end NLA.KE04')==1
        ref=challenge.replace('namespace NLA.KE04\n','namespace NLA.KE04.Reference\n').replace('end NLA.KE04','end NLA.KE04.Reference')
        (S/'Reference.lean').write_text(ref)
        targets=json.loads((S/'comparator.json').read_text())['theorem_names'];assert len(targets)==24
        (S/'Inspector.lean').write_text(inspector(targets))
        (S/'executed-runner.py.txt').write_bytes(Path(__file__).read_bytes())
        for rel in ['Reference.lean','Inspector.lean','executed-runner.py.txt']:
            q=S/rel;q.chmod(0o444);R['source_inputs'][rel]={'sha256':sha(q.read_bytes()),'bytes':q.stat().st_size}
        save(A/'namespace-transformation.json',{'source':'Challenge.lean','destination':'Reference.lean','only_changes':[['namespace NLA.KE04','namespace NLA.KE04.Reference'],['end NLA.KE04','end NLA.KE04.Reference']],'purpose':'Compile frozen signatures alone before Solution, then compare actual types without using the reference proof bodies.'})
        for m in MODULES+['Solution']:
            q=S/('Solution.lean' if m=='Solution' else 'NLA/KE04/'+m+'.lean')
            assert not re.search(r'^import\s+(Challenge|Reference)\b',q.read_text(),re.M)
            assert not re.search(r'\b(sorry|admit|native_decide|axiom|unsafe)\b',re.sub(r'/\-.*?\-/|--[^\n]*','',q.read_text(),flags=re.S)),m
        pins('before')
        paths=[O]+[PKG/x/'.lake/build/lib/lean' for x in ORDER]
        env['LEAN_PATH']=':'.join(map(str,paths));env['LEAN_SRC_PATH']=str(S)
        R['LEAN_PATH']=env['LEAN_PATH'];R['LEAN_SRC_PATH']=env['LEAN_SRC_PATH'];R['lean_binary_sha256']=sha(LEAN.read_bytes())
        run([LEAN,'--version'],S,'lean-version')
        mods=['NLA/KE04/Definitions','Reference']+['NLA/KE04/'+m for m in MODULES[1:]]+['Solution','Inspector']
        for i,m in enumerate(mods):
            o=O/(m+'.olean');o.parent.mkdir(parents=True,exist_ok=True)
            run([LEAN,'-o',o,m+'.lean'],S,f'{i:02d}-'+m.replace('/','-'))
            print('PASS '+m,flush=True)
        il=(A/'12-Inspector.stdout').read_text() if (A/'12-Inspector.stdout').exists() else (A/(f'{len(mods)-1:02d}-Inspector.stdout')).read_text()
        assert il.count('EXACT_FROZEN_TYPE ')==24 and il.count('REFERENCE_ONLY_PLACEHOLDER ')==24
        R['actual_closures']=re.findall(r'CLOSURE_TOTAL (\w+) reached=(\d+) required=(\d+)',il);assert len(R['actual_closures'])==2
        imported=re.findall(r'^IMPORTED_MODULE (\S+)',il,re.M)
        objects=[]
        for mod in imported:
            rel=Path(*mod.split('.')).with_suffix('.olean');candidates=paths+[LEAN.parent.parent/'lib/lean']
            found=next((b/rel for b in candidates if (b/rel).is_file()),None);assert found is not None,mod
            b=found.read_bytes();objects.append({'module':mod,'path':str(found),'sha256':sha(b),'bytes':len(b),'origin':'own fresh prefix' if found.is_relative_to(O) else 'read-only dependency/toolchain'})
        save(A/'actual-imported-objects.json',objects);R['imported_modules']=len(objects)
        reports=[]
        for q in A.glob('*.stdout'):
            reports.extend([{'log':q.name,'declaration':n,'printed_axioms':a,'axioms':[re.sub(r'\.\{[^}]*\}','',x.strip()) for x in a.split(',') if x.strip()]} for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",q.read_text())])
        assert all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in reports)
        R['standard_axiom_reports']=reports;R['exact_target_count']=24
    except Exception:R['errors'].append(traceback.format_exc())
    finally:
        try:pins('after')
        except Exception:R['errors'].append(traceback.format_exc())
        try:
            assert sha((P/'reviews/proof-freeze.json').read_bytes())==a.freeze_sha256
            for rel,h in frozen['files'].items():assert sha((P/rel).read_bytes())==h,rel
            R['all_frozen_inputs_preserved_after']=True
        except Exception:R['errors'].append(traceback.format_exc())
        R['own_objects']=[{'path':str(q.relative_to(O)),'sha256':sha(q.read_bytes()),'bytes':q.stat().st_size} for q in sorted(O.rglob('*')) if q.is_file()]
        shutil.rmtree(O);R['own_prefix_removed']=not O.exists();R['success']=not R['errors'];R['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(A/'result.json',R)
    print(json.dumps({'attempt':str(A),'success':R['success'],'errors':R['errors'],'closures':R.get('actual_closures'),'objects_cleaned':len(R['own_objects'])},indent=2));return 0 if R['success'] else 1
if __name__=='__main__':raise SystemExit(main())
