import Solution
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
    (`NLA.IE05.entryMax_semantics, `Referee1Expected.type_0),
    (`NLA.IE05.schurStep_bound, `Referee1Expected.type_1),
    (`NLA.IE05.gepp_growth_bound, `Referee1Expected.type_2),
    (`NLA.IE05.firstPath_semantics, `Referee1Expected.type_3),
    (`NLA.IE05.orthogonalGrowthSet_bounded, `Referee1Expected.type_4),
    (`NLA.IE05.candidate_positiveQR, `Referee1Expected.type_5),
    (`NLA.IE05.scaledColumns_orthogonal, `Referee1Expected.type_6),
    (`NLA.IE05.scaledLU_trajectory, `Referee1Expected.type_7),
    (`NLA.IE05.integer_factor_certificates, `Referee1Expected.type_8),
    (`NLA.IE05.integer_entry_certificates, `Referee1Expected.type_9),
    (`NLA.IE05.canonical_integer_identification, `Referee1Expected.type_10),
    (`NLA.IE05.witness_orthogonal_path, `Referee1Expected.type_11),
    (`NLA.IE05.bounded_growth_data, `Referee1Expected.type_12),
    (`NLA.IE05.numerical_gap_positive, `Referee1Expected.type_13),
    (`NLA.IE05.witness_strict_growth, `Referee1Expected.type_14),
    (`NLA.IE05.supremum_strict_gap, `Referee1Expected.type_15),
    (`NLA.IE05.orthogonalExtremizerConjecture, `Referee1Expected.type_16)]

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
    liftM <| IO.FS.writeFile "/private/tmp/nla-lean-formalization/next-ie05-statements-draft/lean/reviews/final-referee-1-evidence/inspection-001/actual-environment.json" out.pretty
    logInfo m!"Independent review: {typeRows.size} actual contract types; {projectRows.size} project declarations; {graph.size} safe, nonpartial transitive declarations."

#assert_trust kernel NLA.IE05.entryMax_semantics
#assert_trust kernel NLA.IE05.schurStep_bound
#assert_trust kernel NLA.IE05.gepp_growth_bound
#assert_trust kernel NLA.IE05.firstPath_semantics
#assert_trust kernel NLA.IE05.orthogonalGrowthSet_bounded
#assert_trust kernel NLA.IE05.candidate_positiveQR
#assert_trust kernel NLA.IE05.scaledColumns_orthogonal
#assert_trust kernel NLA.IE05.scaledLU_trajectory
#assert_trust kernel NLA.IE05.integer_factor_certificates
#assert_trust kernel NLA.IE05.integer_entry_certificates
#assert_trust kernel NLA.IE05.canonical_integer_identification
#assert_trust kernel NLA.IE05.witness_orthogonal_path
#assert_trust kernel NLA.IE05.bounded_growth_data
#assert_trust kernel NLA.IE05.numerical_gap_positive
#assert_trust kernel NLA.IE05.witness_strict_growth
#assert_trust kernel NLA.IE05.supremum_strict_gap
#assert_trust kernel NLA.IE05.orthogonalExtremizerConjecture
