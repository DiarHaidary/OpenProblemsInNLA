"""Independent final referee 2: fresh explicit source build, no Lake or cache writes."""
from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, tempfile, time, traceback

E = Path(__file__).resolve().parent
P = E.parents[1]
LEAN = Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean')
DEPS = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
ORDER = ['Definitions','ExactCertificates','Scaling','QR','IntegerQR','Pivot','GEPP','LUTrajectory','Witness','GrowthBounds','Growth','Proof']
LIBS = ['batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
FREEZE_SHA = '72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')

def frozen():
    b=(P/'reviews/proof-freeze.json').read_bytes(); assert sha(b)==FREEZE_SHA
    f=json.loads(b); assert len(f['files'])==1800 and len(f['source_files'])==27
    for n,h in f['files'].items():
        q=P/n; assert not q.is_symlink() and q.is_file(),n
        b=q.read_bytes(); assert sha(b)==h and len(b)==f['file_sizes'][n],n
    return {'proof_freeze_sha256':FREEZE_SHA,'files':f['files'],'sizes':f['file_sizes'],'status':'PASS exact frozen scope; concurrent reviews excluded'}

def expected_types():
    s=(P/'Challenge.lean').read_text(); contracts=load(P/'comparator.json')['theorem_names']
    found=re.findall(r'^theorem\s+(\w+)\s*(.*?)\s*:= by sorry',s,re.M|re.S)
    assert ['NLA.IE05.'+n for n,_ in found]==contracts
    definitions=[]; records=[]
    for n,signature in found:
        depth=0; split=None
        for i,c in enumerate(signature):
            if c in '([{': depth+=1
            elif c in ')]}': depth-=1
            elif c==':' and depth==0: split=i; break
        assert split is not None,n
        binders,conclusion=signature[:split].strip(),signature[split+1:].strip()
        expr=('∀ '+binders+',\n  ' if binders else '')+conclusion
        definitions.append('def '+n+' : Prop :=\n  '+expr+'\n')
        records.append({'name':n,'frozen_signature':signature,'proof_free_expected_expression':expr})
    return contracts,definitions,records

def inspector():
    contracts,defs,records=expected_types()
    required_final=['NLA.IE05._proved.normalizedQRQ_of_gram_lu','NLA.IE05._proved.integer_factor_certificates','NLA.IE05._proved.integer_entry_certificates','NLA.IE05._proved.normalizedInteger_path_trajectory','NLA.IE05._proved.normalizedInteger_trajectory_entry','NLA.IE05._proved.scaledLU_trajectory','NLA.IE05._proved.witness_growth_lower','NLA.IE05._proved.candidate_growth_sq_upper','NLA.IE05._proved.numerical_gap_positive','NLA.IE05.orthogonalGrowthSet_bounded_proved','NLA.IE05.trajectory','NLA.IE05.schurStep','NLA.IE05.AdmissiblePath','NLA.IE05.Orthogonal','NLA.IE05.PositiveQR','NLA.IE05.normalizedQRQ','NLA.IE05.firstGrowth','NLA.IE05.growth','NLA.IE05.entryMax','NLA.IE05.peakMax','NLA.IE05.orthogonalGrowthSet','NLA.IE05.orthogonalGrowthSup','NLA.IE05.OrthogonalExtremizerConjecture','Real.sq_sqrt','le_csSup','InnerProductSpace.gramSchmidtNormed','of_decide_eq_true']
    pairs=',\n    '.join('(``'+n+', ``NLA.IE05.Referee2Expected.'+n.split('.')[-1]+')' for n in contracts)
    refs=', '.join('``'+n for n in required_final)
    code='import Solution\nimport Lean.Util.FoldConsts\n\nset_option leancert.trust "kernel"\nset_option maxHeartbeats 4000000\nnoncomputable section\nnamespace NLA.IE05.Referee2Expected\n'+'\n'.join(defs)+'\nend NLA.IE05.Referee2Expected\n'
    code+='''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [PAIRS]
  for (actual, expectedName) in pairs do
    let some ci := env.find? actual | throwError "Missing export {actual}"
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Export not a theorem {actual}"
    let some ei := env.find? expectedName | throwError "Missing expected type {expectedName}"
    let some expected := ei.value? | throwError "Expected Prop has no body"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq ci.type expected do throwError "Type mismatch {actual}"
    logInfo m!"EXACT_TYPE {actual}: {ci.type}"
  let audit (label : String) (roots required : List Name) : CommandElabM Unit := do
    let mut todo := roots
    let mut seen : List Name := []
    let mut used : List Name := []
    for _ in [:30000] do
      match todo with
      | [] => pure ()
      | name :: rest =>
        todo := rest
        unless seen.contains name do
          if name.toString.startsWith "NLA.IE05.Referee2Expected." then
            throwError "Reference expression used by proof {name}"
          seen := name :: seen
          let some ci := env.find? name | throwError "Missing reached declaration {name}"
          if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial reached declaration {name}"
          let axioms ← liftCoreM <| collectAxioms name
          for ax in axioms do
            unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
              throwError "Forbidden transitive axiom {name}: {ax}"
          let body ← match ci.value? (allowOpaque := true) with
            | some b => pure b.getUsedConstants.toList
            | none => match ci with
              | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
              | _ => throwError "Unexpected bodyless declaration {name}"
          let deps := ci.type.getUsedConstants.toList ++ body
          used := deps ++ used
          let next := deps.filter fun x => x.toString.startsWith "NLA.IE05." ||
            x.toString.startsWith "_private.NLA.IE05."
          todo := next ++ todo
          logInfo m!"ACTUAL_DECL {label} {name} AXIOMS {axioms.toList}"
          logInfo m!"ACTUAL_EDGE {label} {name}: {next}"
    unless todo.isEmpty do throwError "Traversal cap reached"
    for n in required do
      unless used.contains n do throwError "Missing retained dependency {label}: {n}"
      logInfo m!"RETAINED {label} {n}"
    logInfo m!"AUDIT_COMPLETE {label} roots={roots.length} closure={seen.length} required={required.length}"
  audit "FINAL" [``NLA.IE05.orthogonalExtremizerConjecture] [REFS]
  audit "ALL" (pairs.map Prod.fst) [``NLA.IE05.firstPath_semantics_proved,
    ``NLA.IE05.gepp_growth_bound_proved, ``NLA.IE05._proved.candidate_positiveQR]
'''.replace('PAIRS',pairs).replace('REFS',refs)
    for n in contracts: code+='\n#print axioms '+n+'\n#assert_trust kernel '+n+'\n'
    return code,records,required_final

def main():
    attempt=Path(tempfile.mkdtemp(prefix='attempt-',dir=E)); source=attempt/'source';source.mkdir()
    out=Path(tempfile.mkdtemp(prefix='ie05-referee2-output-')); assert not list(out.iterdir())
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/mf16_final_referee','attempt':attempt.name,'empty_private_output_prefix':str(out),'commands':[],'errors':[]}
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',LEAN_PATH=os.pathsep.join([str(out)]+[str(DEPS/n/'.lake/build/lib/lean') for n in LIBS]))
    def run(args,label,cwd=source):
        start=time.monotonic(); cp=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (attempt/(label+'.stdout')).write_bytes(cp.stdout); (attempt/(label+'.stderr')).write_bytes(cp.stderr)
        record={'command':args,'cwd':str(cwd),'exit_code':cp.returncode,'seconds':time.monotonic()-start,'stdout':label+'.stdout','stderr':label+'.stderr','stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)}
        result['commands'].append(record);save(attempt/'progress.json',result)
        assert cp.returncode==0,record
        return cp.stdout
    def pins(label):
        values=[]
        for pkg in load(P/'lake-manifest.json')['packages']:
            n=pkg['name']; head=run(['git','rev-parse','HEAD'],label+'-'+n+'-head',DEPS/n).decode().strip()
            status=run(['git','status','--porcelain=v1','--untracked-files=no'],label+'-'+n+'-status',DEPS/n)
            assert head==pkg['rev'] and not status,(n,head,status)
            values.append({'name':n,'head':head,'clean_tracked_sources':True,'built_path':str(DEPS/n/'.lake/build/lib/lean') if n in LIBS else None})
        return values
    try:
        save(attempt/'frozen-before.json',frozen())
        inputs=['NLA/IE05/'+n+'.lean' for n in ORDER]+['Solution.lean','Challenge.lean','comparator.json','lake-manifest.json','lean-toolchain','lakefile.toml']
        identities={}
        for n in inputs:
            b=(P/n).read_bytes(); q=source/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);q.chmod(0o444);identities[n]={'sha256':sha(b),'bytes':len(b)}
        code,records,required=inspector(); (source/'Inspect.lean').write_text(code); (source/'Inspect.lean').chmod(0o444)
        identities['Inspect.lean']={'sha256':sha(code.encode()),'bytes':len(code.encode()),'reviewer_generated':True}
        save(attempt/'source-inputs.json',identities);save(attempt/'expected-types.json',records)
        save(attempt/'runner.json',{'source_sha256':sha(Path(__file__).read_bytes()),'LEAN_PATH':env['LEAN_PATH'],'only_target_objects_created':True,'explicit_order':ORDER+['Solution','Inspect'],'required_final_dependencies':required})
        (attempt/'runner.py').write_bytes(Path(__file__).read_bytes())
        result['tool']={'path':str(LEAN),'sha256':sha(LEAN.read_bytes()),'version':run([str(LEAN),'--version'],'lean-version').decode(),'host':run(['uname','-a'],'host').decode()}
        result['pins_before']=pins('before')
        outputs=[]
        for number,n in enumerate(['NLA/IE05/'+x for x in ORDER]+['Solution','Inspect'],1):
            obj=out/(n+'.olean');obj.parent.mkdir(parents=True,exist_ok=True)
            log=run([str(LEAN),'-o',str(obj),n+'.lean'],str(number).zfill(2)+'-'+n.replace('/','-'))
            outputs.append(log.decode())
            print('PASS',n,flush=True)
        allout='\n'.join(outputs)
        assert 'warning:' not in allout and 'error:' not in allout, 'Compiler diagnostic present'
        assert len(re.findall(r'^EXACT_TYPE ',allout,re.M))==17
        audits=re.findall(r'AUDIT_COMPLETE (\w+) roots=(\d+) closure=(\d+) required=(\d+)',allout)
        assert len(audits)==2 and {a[0] for a in audits}=={'FINAL','ALL'}
        result['audits']=[dict(zip(['scope','roots','closure','required'],a)) for a in audits]
        result['exact_type_count']=17
        axiom_lines=[x for x in allout.splitlines() if 'depends on axioms:' in x or 'does not depend on any axioms' in x]
        trust_lines=[x for x in allout.splitlines() if 'Trust level' in x or 'trust level' in x or 'kernel (axioms:' in x]
        result['axiom_report_count']=len(axiom_lines);result['trust_report_matching_lines']=len(trust_lines)
        result['lean_command_count']=14
        result['pins_after']=pins('after');assert result['pins_before']==result['pins_after']
        save(attempt/'frozen-after.json',frozen())
        result['status']='PASS independent fresh complete source build, actual types and proof/type/axiom closure'
    except Exception:
        result['errors'].append(traceback.format_exc());result['status']='FAIL retained actual attempt'
    finally:
        objects=[]
        for q in sorted(out.rglob('*')):
            if q.is_file():objects.append({'path':str(q.relative_to(out)),'sha256':sha(q.read_bytes()),'bytes':q.stat().st_size})
        save(attempt/'objects-before-cleanup.json',{'owned_prefix':str(out),'files':objects,'deletion_scope':'Only this reviewer-created completed prefix; no source/log/dependency removal'})
        shutil.rmtree(out)
        result['owned_output_removed_after_hashing']=not out.exists();result['object_count']=len(objects)
        result['success']=not result['errors'];save(attempt/'result.json',result)
        save(E/'LATEST.json',{'attempt':attempt.name,'result_sha256':sha((attempt/'result.json').read_bytes()),'success':result['success']})
    print(json.dumps({'attempt':attempt.name,'success':result['success'],'audits':result.get('audits'),'axiom_report_count':result.get('axiom_report_count'),'errors':result['errors']},indent=2),flush=True)
    raise SystemExit(0 if result['success'] else 1)

if __name__=='__main__': main()
