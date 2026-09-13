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

private def sourceSeeds : Array (String × String) := #[("NLA.IE05.Definitions", "NLA.IE05.Mat"),
    ("NLA.IE05.Definitions", "NLA.IE05.IntMat"),
    ("NLA.IE05.Definitions", "NLA.IE05.PivotPath"),
    ("NLA.IE05.Definitions", "NLA.IE05.Orthogonal"),
    ("NLA.IE05.Definitions", "NLA.IE05.UpperTriangular"),
    ("NLA.IE05.Definitions", "NLA.IE05.UnitLower"),
    ("NLA.IE05.Definitions", "NLA.IE05.prescribedLower"),
    ("NLA.IE05.Definitions", "NLA.IE05.euclideanColumns"),
    ("NLA.IE05.Definitions", "NLA.IE05.normalizedQRQ"),
    ("NLA.IE05.Definitions", "NLA.IE05.candidateQ"),
    ("NLA.IE05.Definitions", "NLA.IE05.candidateR"),
    ("NLA.IE05.Definitions", "NLA.IE05.PositiveQR"),
    ("NLA.IE05.Definitions", "NLA.IE05.rowSwap"),
    ("NLA.IE05.Definitions", "NLA.IE05.schurStep"),
    ("NLA.IE05.Definitions", "NLA.IE05.trajectory"),
    ("NLA.IE05.Definitions", "NLA.IE05.AdmissiblePivot"),
    ("NLA.IE05.Definitions", "NLA.IE05.FirstAvailablePivot"),
    ("NLA.IE05.Definitions", "NLA.IE05.AdmissiblePath"),
    ("NLA.IE05.Definitions", "NLA.IE05.FirstAvailablePath"),
    ("NLA.IE05.Definitions", "NLA.IE05.firstPivotIndex"),
    ("NLA.IE05.Definitions", "NLA.IE05.firstTrajectory"),
    ("NLA.IE05.Definitions", "NLA.IE05.firstPath"),
    ("NLA.IE05.Definitions", "NLA.IE05.noSwapPath"),
    ("NLA.IE05.Definitions", "NLA.IE05.entryMaxNN"),
    ("NLA.IE05.Definitions", "NLA.IE05.entryMax"),
    ("NLA.IE05.Definitions", "NLA.IE05.activeMaxNN"),
    ("NLA.IE05.Definitions", "NLA.IE05.activeMax"),
    ("NLA.IE05.Definitions", "NLA.IE05.growth"),
    ("NLA.IE05.Definitions", "NLA.IE05.firstGrowth"),
    ("NLA.IE05.Definitions", "NLA.IE05.orthogonalGrowthSet"),
    ("NLA.IE05.Definitions", "NLA.IE05.orthogonalGrowthSup"),
    ("NLA.IE05.Definitions", "NLA.IE05.OrthogonalExtremizerConjecture"),
    ("NLA.IE05.Definitions", "NLA.IE05.scaledColumns"),
    ("NLA.IE05.Definitions", "NLA.IE05.tailProduct"),
    ("NLA.IE05.Definitions", "NLA.IE05.integerLower"),
    ("NLA.IE05.Definitions", "NLA.IE05.integerH"),
    ("NLA.IE05.Definitions", "NLA.IE05.integerD"),
    ("NLA.IE05.Definitions", "NLA.IE05.integerT"),
    ("NLA.IE05.Definitions", "NLA.IE05.castIntegerMatrix"),
    ("NLA.IE05.Definitions", "NLA.IE05.normalizedInteger"),
    ("NLA.IE05.Definitions", "NLA.IE05.witnessQ"),
    ("NLA.IE05.ExactCertificates", "NLA.IE05._proved.integerLowerZeroDecidable"),
    ("NLA.IE05.ExactCertificates", "NLA.IE05._proved.integerTZeroDecidable"),
    ("NLA.IE05.ExactCertificates", "NLA.IE05._proved.integer_factor_certificates"),
    ("NLA.IE05.ExactCertificates", "NLA.IE05._proved.integer_entry_certificates"),
    ("NLA.IE05.ExactCertificates", "NLA.IE05._proved.numerical_gap_positive"),
    ("NLA.IE05.GEPP", "NLA.IE05.entryMax_nonneg_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeMax_nonneg_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.abs_le_entryMax_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.abs_le_activeMax_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeMax_le_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.entryMax_semantics_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeMax_zero_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.swap_active"),
    ("NLA.IE05.GEPP", "NLA.IE05.schurStep_bound_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.peakMax"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeMax_le_peakMax_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.peakMax_le_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.entryMax_le_peakMax_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.gepp_stage_bound_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.gepp_growth_bound_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.ActiveInjective"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeInjective_initial_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeInjective_nonzero_column_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeInjective_rowSwap_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.schurStep_mulVec_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.activeInjective_schur_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.firstTrajectory_activeInjective_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.firstPath_semantics_proved"),
    ("NLA.IE05.GEPP", "NLA.IE05.orthogonalGrowthSet_bounded_proved"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.integerD_real_pos"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.witness_entryMax_upper"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.witness_final_pivot"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.witness_peak_lower"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.witness_growth_lower"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.candidate_entryMax_lower"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.candidate_peak_upper"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.candidate_growth_nonneg"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.candidate_growth_upper"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.candidate_growth_sq_upper"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.bounded_growth_data"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.witness_strict_growth"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.supremum_strict_gap"),
    ("NLA.IE05.Growth", "NLA.IE05._proved.orthogonalExtremizerConjecture"),
    ("NLA.IE05.GrowthBounds", "NLA.IE05._proved.abs_div_sqrt_le"),
    ("NLA.IE05.GrowthBounds", "NLA.IE05._proved.abs_div_sqrt_le_sqrt"),
    ("NLA.IE05.GrowthBounds", "NLA.IE05._proved.entryMax_le_from_entries"),
    ("NLA.IE05.GrowthBounds", "NLA.IE05._proved.growth_nonneg"),
    ("NLA.IE05.IntegerQR", "NLA.IE05._proved.normalizedQRQ_of_gram_lu"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.tailProduct_zero"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.tailProduct_terminal"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.tailProduct_pivot_row"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.tailProduct_pivot_column"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.tailProduct_split"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.scaled_tail_schur"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.scaled_tail_firstAvailable"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.scaled_noSwap_trajectory"),
    ("NLA.IE05.LUTrajectory", "NLA.IE05._proved.scaledLU_trajectory"),
    ("NLA.IE05.Pivot", "NLA.IE05.pivotScore"),
    ("NLA.IE05.Pivot", "NLA.IE05.pivotUpdate"),
    ("NLA.IE05.Pivot", "NLA.IE05.pivotUpdate_active"),
    ("NLA.IE05.Pivot", "NLA.IE05.pivotFold_active"),
    ("NLA.IE05.Pivot", "NLA.IE05.pivotScore_lt_iff"),
    ("NLA.IE05.Pivot", "NLA.IE05.pivotFold_argAux"),
    ("NLA.IE05.Pivot", "NLA.IE05.firstPivotIndex_spec_proved"),
    ("NLA.IE05.Pivot", "NLA.IE05.firstPivotIndex_eq_of_firstAvailable_proved"),
    ("NLA.IE05.Pivot", "NLA.IE05.firstPivotIndex_firstAvailable_proved"),
    ("NLA.IE05.Pivot", "NLA.IE05.trajectory_firstPath_eq_proved"),
    ("NLA.IE05.Pivot", "NLA.IE05.firstPath_eq_of_firstAvailable_proved"),
    ("NLA.IE05.Proof", "NLA.IE05.entryMax_semantics"),
    ("NLA.IE05.Proof", "NLA.IE05.schurStep_bound"),
    ("NLA.IE05.Proof", "NLA.IE05.gepp_growth_bound"),
    ("NLA.IE05.Proof", "NLA.IE05.firstPath_semantics"),
    ("NLA.IE05.Proof", "NLA.IE05.orthogonalGrowthSet_bounded"),
    ("NLA.IE05.Proof", "NLA.IE05.candidate_positiveQR"),
    ("NLA.IE05.Proof", "NLA.IE05.scaledColumns_orthogonal"),
    ("NLA.IE05.Proof", "NLA.IE05.scaledLU_trajectory"),
    ("NLA.IE05.Proof", "NLA.IE05.integer_factor_certificates"),
    ("NLA.IE05.Proof", "NLA.IE05.integer_entry_certificates"),
    ("NLA.IE05.Proof", "NLA.IE05.canonical_integer_identification"),
    ("NLA.IE05.Proof", "NLA.IE05.witness_orthogonal_path"),
    ("NLA.IE05.Proof", "NLA.IE05.bounded_growth_data"),
    ("NLA.IE05.Proof", "NLA.IE05.numerical_gap_positive"),
    ("NLA.IE05.Proof", "NLA.IE05.witness_strict_growth"),
    ("NLA.IE05.Proof", "NLA.IE05.supremum_strict_gap"),
    ("NLA.IE05.Proof", "NLA.IE05.orthogonalExtremizerConjecture"),
    ("NLA.IE05.QR", "NLA.IE05._proved.euclideanColumns_inner"),
    ("NLA.IE05.QR", "NLA.IE05._proved.orthogonal_iff_orthonormal_columns"),
    ("NLA.IE05.QR", "NLA.IE05._proved.euclideanColumns_linearIndependent"),
    ("NLA.IE05.QR", "NLA.IE05._proved.euclideanColumns_normalizedQRQ"),
    ("NLA.IE05.QR", "NLA.IE05._proved.normalizedQRQ_orthogonal"),
    ("NLA.IE05.QR", "NLA.IE05._proved.gramSchmidt_inner_original"),
    ("NLA.IE05.QR", "NLA.IE05._proved.normalizedQRQ_upper"),
    ("NLA.IE05.QR", "NLA.IE05._proved.normalizedQRQ_diagonal_pos"),
    ("NLA.IE05.QR", "NLA.IE05._proved.normalizedQRQ_positiveQR"),
    ("NLA.IE05.QR", "NLA.IE05._proved.prescribedLower_det"),
    ("NLA.IE05.QR", "NLA.IE05._proved.positiveQR_inner"),
    ("NLA.IE05.QR", "NLA.IE05._proved.positiveQR_column"),
    ("NLA.IE05.QR", "NLA.IE05._proved.gramSchmidt_eq_of_positiveQR"),
    ("NLA.IE05.QR", "NLA.IE05._proved.normalizedQRQ_eq_of_positiveQR"),
    ("NLA.IE05.QR", "NLA.IE05._proved.candidate_positiveQR"),
    ("NLA.IE05.Scaling", "NLA.IE05._proved.scaledColumns_orthogonal"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_transpose"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_mul"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_diagonal"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_tailProduct"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_unitLower"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_upper"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.castIntegerMatrix_lower_bound"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.real_factor_certificates"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.normalizedInteger_orthogonal"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.normalizedInteger_path_trajectory"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.normalizedInteger_trajectory_entry"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.normalizedInteger_firstGrowth"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.integerLower_false_prescribed"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.canonical_integer_identification"),
    ("NLA.IE05.Witness", "NLA.IE05._proved.witness_orthogonal_path")]

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
    let candidates := env.constants.toList.filterMap fun (name, _) =>
      if project name then some name else none
    let mut inventory : Array Json := #[]
    for name in candidates do
      let some ci := env.checked.get.find? name | throwError "Missing declaration {name}"
      inventory := inventory.push (Json.mkObj [
        ("name", toJson name.toString), ("module", toJson (modName name)),
        ("kind", toJson (declarationKind ci)), ("unsafe", toJson ci.isUnsafe),
        ("partial", toJson ci.isPartial),
        ("references", toJson (ci.getUsedConstantsAsSet.toArray.map Name.toString))])
    liftM <| IO.FS.writeFile "/private/tmp/nla-lean-formalization/next-ie05-statements-draft/lean/reviews/final-referee-1-evidence/inspection-001/all-project-declarations.json" (Json.arr inventory).pretty
    let mut seeds : Array Name := #[]
    for (mod, printed) in sourceSeeds do
      let found := candidates.filter fun name =>
        modName name == mod && (name.toString == printed || name.toString.endsWith ("." ++ printed))
      unless found.length == 1 do throwError "Source declaration resolves ambiguously: {printed}: {found}"
      seeds := seeds.push found.head!
    let mut work := seeds
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
      ("source_seed_names", toJson (seeds.map Name.toString)),
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
