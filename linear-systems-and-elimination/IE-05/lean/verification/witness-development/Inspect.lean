/- Witness author inspection only; expected types are Prop definitions from
exact frozen headers, never reference proofs or assumptions. -/
import NLA.IE05.Witness
import Lean.Util.FoldConsts
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.WitnessExpected
def canonical_integer_identification : Prop :=
    candidateQ 8 = normalizedInteger false ∧
      firstPath (candidateQ 8) = noSwapPath 8

def witness_orthogonal_path : Prop :=
    Orthogonal witnessQ ∧ firstPath witnessQ = noSwapPath 8 ∧
      FirstAvailablePath witnessQ (noSwapPath 8) ∧
      AdmissiblePath witnessQ (noSwapPath 8)
end NLA.IE05.WitnessExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.IE05._proved.canonical_integer_identification, ``NLA.IE05.WitnessExpected.canonical_integer_identification),
    (``NLA.IE05._proved.witness_orthogonal_path, ``NLA.IE05.WitnessExpected.witness_orthogonal_path)]
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual theorem {actual}"
    let some b := env.find? reference | throwError "Missing expected type {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Actual export is not a theorem {actual}"
    let some expected := b.value? | throwError "Expected type has no value {reference}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type expected do
        throwError "Frozen signature mismatch {actual}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.IE05." ||
    n.toString.startsWith "_private.NLA.IE05."
  let mut pending := [``NLA.IE05._proved.castIntegerMatrix_transpose, ``NLA.IE05._proved.castIntegerMatrix_mul, ``NLA.IE05._proved.castIntegerMatrix_diagonal, ``NLA.IE05._proved.castIntegerMatrix_tailProduct, ``NLA.IE05._proved.castIntegerMatrix_unitLower, ``NLA.IE05._proved.castIntegerMatrix_upper, ``NLA.IE05._proved.castIntegerMatrix_lower_bound, ``NLA.IE05._proved.real_factor_certificates, ``NLA.IE05._proved.normalizedInteger_orthogonal, ``NLA.IE05._proved.normalizedInteger_path_trajectory, ``NLA.IE05._proved.normalizedInteger_trajectory_entry, ``NLA.IE05._proved.normalizedInteger_firstGrowth, ``NLA.IE05._proved.integerLower_false_prescribed, ``NLA.IE05._proved.canonical_integer_identification, ``NLA.IE05._proved.witness_orthogonal_path]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.IE05.WitnessExpected." then
          throwError "Actual proof reached diagnostic type {name}"
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing declaration {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial declaration {name}"
        let axioms ← liftCoreM <| collectAxioms name
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Forbidden transitive axiom {name}: {ax}"
        logInfo m!"ACTUAL_AXIOMS {name}: {axioms.toList}"
        let body ← match ci.value? (allowOpaque := true) with
          | some b => pure b.getUsedConstants.toList
          | none => match ci with
            | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
            | _ => throwError "Unexplained bodyless declaration {name}"
        let deps := ci.type.getUsedConstants.toList ++ body
        used := deps ++ used
        let follow := deps.filter isProject
        logInfo m!"PROJECT_EDGE {name}: {follow}"
        pending := follow ++ pending
  unless pending.isEmpty do throwError "Incomplete traversal"
  let required := [``NLA.IE05._proved.castIntegerMatrix_mul,
    ``NLA.IE05._proved.castIntegerMatrix_diagonal,
    ``NLA.IE05._proved.castIntegerMatrix_tailProduct,
    ``NLA.IE05._proved.castIntegerMatrix_unitLower,
    ``NLA.IE05._proved.castIntegerMatrix_upper,
    ``NLA.IE05._proved.castIntegerMatrix_lower_bound,
    ``NLA.IE05._proved.real_factor_certificates,
    ``NLA.IE05._proved.normalizedInteger_orthogonal,
    ``NLA.IE05._proved.normalizedInteger_path_trajectory,
    ``NLA.IE05._proved.integerLower_false_prescribed,
    ``NLA.IE05._proved.integer_factor_certificates,
    ``NLA.IE05._proved.integerLowerZeroDecidable,
    ``NLA.IE05._proved.integerTZeroDecidable,
    ``NLA.IE05._proved.normalizedQRQ_of_gram_lu,
    ``NLA.IE05._proved.normalizedQRQ_eq_of_positiveQR,
    ``NLA.IE05._proved.gramSchmidt_eq_of_positiveQR,
    ``NLA.IE05._proved.scaledColumns_orthogonal,
    ``NLA.IE05._proved.scaledLU_trajectory,
    ``NLA.IE05._proved.scaled_noSwap_trajectory,
    ``NLA.IE05._proved.scaled_tail_schur,
    ``NLA.IE05._proved.scaled_tail_firstAvailable,
    ``NLA.IE05.firstPath_eq_of_firstAvailable_proved,
    ``NLA.IE05.candidateQ,
    ``NLA.IE05.prescribedLower,
    ``NLA.IE05.normalizedQRQ,
    ``NLA.IE05.euclideanColumns,
    ``NLA.IE05.PositiveQR,
    ``NLA.IE05.Orthogonal,
    ``NLA.IE05.castIntegerMatrix,
    ``NLA.IE05.integerH,
    ``NLA.IE05.integerT,
    ``NLA.IE05.integerD,
    ``NLA.IE05.integerLower,
    ``NLA.IE05.witnessQ,
    ``NLA.IE05.normalizedInteger,
    ``NLA.IE05.tailProduct,
    ``NLA.IE05.scaledColumns,
    ``NLA.IE05.growth,
    ``NLA.IE05.firstGrowth,
    ``NLA.IE05.noSwapPath,
    ``NLA.IE05.trajectory,
    ``NLA.IE05.rowSwap,
    ``NLA.IE05.schurStep,
    ``NLA.IE05.firstPath,
    ``NLA.IE05.FirstAvailablePath,
    ``NLA.IE05.FirstAvailablePivot,
    ``NLA.IE05.AdmissiblePath,
    ``NLA.IE05.AdmissiblePivot,
    ``of_decide_eq_true,
    ``Int.instDecidableEq,
    ``InnerProductSpace.gramSchmidtNormed,
    ``Real.sqrt,
    ``Matrix.mul_nonsing_inv,
    ``Matrix.invertibleOfIsUnitDet,
    ``Matrix.det_of_isUpperTriangular,
    ``Matrix.blockTriangular_inv_of_blockTriangular]
  let mut missing : List Name := []
  for need in required do
    if used.contains need then
      logInfo m!"RETAINED_DEPENDENCY {need}"
    else
      missing := need :: missing
  unless missing.isEmpty do throwError "Missing material dependencies {missing}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_transpose
#print axioms NLA.IE05._proved.castIntegerMatrix_transpose
#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_mul
#print axioms NLA.IE05._proved.castIntegerMatrix_mul
#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_diagonal
#print axioms NLA.IE05._proved.castIntegerMatrix_diagonal
#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_tailProduct
#print axioms NLA.IE05._proved.castIntegerMatrix_tailProduct
#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_unitLower
#print axioms NLA.IE05._proved.castIntegerMatrix_unitLower
#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_upper
#print axioms NLA.IE05._proved.castIntegerMatrix_upper
#assert_trust kernel NLA.IE05._proved.castIntegerMatrix_lower_bound
#print axioms NLA.IE05._proved.castIntegerMatrix_lower_bound
#assert_trust kernel NLA.IE05._proved.real_factor_certificates
#print axioms NLA.IE05._proved.real_factor_certificates
#assert_trust kernel NLA.IE05._proved.normalizedInteger_orthogonal
#print axioms NLA.IE05._proved.normalizedInteger_orthogonal
#assert_trust kernel NLA.IE05._proved.normalizedInteger_path_trajectory
#print axioms NLA.IE05._proved.normalizedInteger_path_trajectory
#assert_trust kernel NLA.IE05._proved.normalizedInteger_trajectory_entry
#print axioms NLA.IE05._proved.normalizedInteger_trajectory_entry
#assert_trust kernel NLA.IE05._proved.normalizedInteger_firstGrowth
#print axioms NLA.IE05._proved.normalizedInteger_firstGrowth
#assert_trust kernel NLA.IE05._proved.integerLower_false_prescribed
#print axioms NLA.IE05._proved.integerLower_false_prescribed
#assert_trust kernel NLA.IE05._proved.canonical_integer_identification
#print axioms NLA.IE05._proved.canonical_integer_identification
#assert_trust kernel NLA.IE05._proved.witness_orthogonal_path
#print axioms NLA.IE05._proved.witness_orthogonal_path
set_option pp.all true in
#print NLA.IE05.normalizedQRQ
set_option pp.all true in
#print NLA.IE05.euclideanColumns
set_option pp.all true in
#print NLA.IE05.castIntegerMatrix
set_option pp.all true in
#print NLA.IE05.normalizedInteger
set_option pp.all true in
#print NLA.IE05.witnessQ
set_option pp.proofs true in
#print NLA.IE05._proved.real_factor_certificates
set_option pp.proofs true in
#print NLA.IE05._proved.normalizedInteger_path_trajectory
set_option pp.proofs true in
#print NLA.IE05._proved.normalizedInteger_trajectory_entry
set_option pp.proofs true in
#print NLA.IE05._proved.canonical_integer_identification
set_option pp.proofs true in
#print NLA.IE05._proved.witness_orthogonal_path
