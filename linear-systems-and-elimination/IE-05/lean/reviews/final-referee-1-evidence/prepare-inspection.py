from pathlib import Path
import importlib.util, re

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review',HERE/'review.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
ROOT=r.ROOT; OWN=r.OWN
dst=OWN/'inspection-001'; dst.mkdir(exist_ok=False)
(dst/'executed-prepare-inspection.py').write_bytes(Path(__file__).read_bytes())
challenge=(ROOT/'Challenge.lean').read_text()
items=re.findall(r'\btheorem\s+(\w+)(.*?)\s*:= by sorry',challenge,re.S)
assert len(items)==17
definitions=['import NLA.IE05.Definitions','noncomputable section','open NLA.IE05','namespace Referee1Expected']
extraction={}
for i,(name,signature) in enumerate(items):
    depth=0; split=None
    for at,ch in enumerate(signature):
        if ch in '({[': depth+=1
        elif ch in ')}]': depth-=1
        elif ch==':' and depth==0: split=at; break
    assert split is not None
    params=signature[:split].strip(); conclusion=signature[split+1:].strip()
    value=('∀ '+params+',\n    ' if params else '')+conclusion
    definitions.append('def type_'+str(i)+' : Prop :=\n    '+value+'\n')
    extraction[name]={'index':i,'original_signature':signature,'proof_free_value':value}
definitions.append('end Referee1Expected')
(dst/'RefereeReference.lean').write_text('\n\n'.join(definitions)+'\n')
r.save(dst/'extraction.json',{'challenge_sha256':r.sha(ROOT/'Challenge.lean'),'contracts':extraction})
pairs=',\n    '.join('(`NLA.IE05.'+name+', `Referee1Expected.type_'+str(i)+')' for i,(name,_) in enumerate(items))
checks='\n'.join('#assert_trust kernel NLA.IE05.'+name for name,_ in items)
template='''import Solution
import RefereeReference
import Lean.Util.CollectAxioms
import Lean.Util.FoldConsts

open Lean Elab Command Meta
set_option maxRecDepth 20000
set_option maxHeartbeats 0
set_option pp.universes true
set_option pp.proofs true
set_option pp.fullNames true
set_option leancert.trust "kernel"

private def refereePairs : Array (Name × Name) := #[
    PAIRS]

private def declarationKind : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"

run_cmd do
  liftTermElabM do
    let env := (← getEnv).setExporting false
    let modName (name : Name) : String :=
      match env.getModuleIdxFor? name with
      | some idx => env.allImportedModuleNames[idx.toNat]!.toString
      | none => "<current>"
    let project (name : Name) : Bool :=
      (modName name).startsWith "NLA.IE05."
    let mut typeRows : Array Json := #[]
    for (name, expectedName) in refereePairs do
      let ci ← getConstInfo name
      let ec ← getConstInfo expectedName
      unless declarationKind ci == "theorem" do throwError "Not a theorem: {name}"
      unless ci.levelParams.isEmpty do throwError "Unexpected universe parameters: {name}"
      let some expected := ec.value? true | throwError "Missing proof-free type {expectedName}"
      unless ← isDefEq ci.type expected do throwError "Contract mismatch: {name}"
      if expected.hasMVar || ci.type.hasMVar then throwError "Metavariable in {name}"
      typeRows := typeRows.push (Json.mkObj [
        ("name", toJson name.toString), ("expected", toJson expectedName.toString),
        ("actual_type", toJson (← ppExpr ci.type).pretty),
        ("expected_expression", toJson (← ppExpr expected).pretty),
        ("definitional_equality", toJson true)])
    let seeds := env.constants.toList.filterMap fun (name, _) =>
      if project name then some name else none
    let mut work := seeds.toArray
    let mut seen : NameSet := {}
    let mut graph : Array Json := #[]
    let mut projectRows : Array Json := #[]
    let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
    while !work.isEmpty do
      let name := work.back!
      work := work.pop
      if seen.contains name then continue
      seen := seen.insert name
      let some ci := env.checked.get.find? name | throwError "Missing kernel declaration {name}"
      if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial reachable constant: {name}"
      if declarationKind ci == "axiom" && !allowed.contains name then
        throwError "Nonstandard axiom: {name}"
      let typeRefs := ci.type.getUsedConstants
      let bodyRefs := match ci.value? true with
        | some body => body.getUsedConstants
        | none => #[]
      let mut refs := ci.getUsedConstantsAsSet
      for ref in typeRefs ++ bodyRefs do refs := refs.insert ref
      for ref in refs do work := work.push ref
      let mut row := [
        ("name", toJson name.toString), ("module", toJson (modName name)),
        ("kind", toJson (declarationKind ci)), ("unsafe", toJson ci.isUnsafe),
        ("partial", toJson ci.isPartial),
        ("type_references", toJson (typeRefs.map Name.toString)),
        ("body_references", toJson (bodyRefs.map Name.toString)),
        ("all_references", toJson (refs.toArray.map Name.toString))]
      graph := graph.push (Json.mkObj row)
      if project name then
        let axioms ← collectAxioms name
        unless axioms.all allowed.contains do throwError "Axiom audit failed for {name}: {axioms}"
        if ci.type.hasMVar then throwError "Type metavariable in {name}"
        row := row ++ [("axioms", toJson (axioms.map Name.toString)),
          ("type", toJson (← ppExpr ci.type).pretty)]
        if let some body := ci.value? true then
          if body.hasMVar then throwError "Body metavariable in {name}"
          row := row ++ [("body", toJson (← ppExpr body).pretty)]
        projectRows := projectRows.push (Json.mkObj row)
    let out := Json.mkObj [
      ("contracts", Json.arr typeRows), ("contract_count", toJson typeRows.size),
      ("project_declarations", Json.arr projectRows),
      ("project_declaration_count", toJson projectRows.size),
      ("transitive_graph", Json.arr graph), ("transitive_count", toJson graph.size),
      ("imported_modules", toJson (env.allImportedModuleNames.map Name.toString)),
      ("status", toJson "PASS")]
    liftIO <| IO.FS.writeFile "OUTPUT" out.pretty
    logInfo m!"Independent review: {typeRows.size} actual contract types; {projectRows.size} project declarations; {graph.size} safe, nonpartial transitive declarations."

CHECKS
'''
(dst/'RefereeInspect.lean').write_text(template.replace('PAIRS',pairs).replace('CHECKS',checks).replace('OUTPUT',str(dst/'actual-environment.json')))
r.save(dst/'source-manifest.json',{p.name:{'sha256':r.sha(p),'bytes':p.stat().st_size} for p in dst.glob('*.lean')})
print('Prepared 17 proof-free reference expressions and independent actual-environment inspector')
