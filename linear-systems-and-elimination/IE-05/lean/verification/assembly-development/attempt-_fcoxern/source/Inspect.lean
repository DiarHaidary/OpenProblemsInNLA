import Solution
import Lean.Util.FoldConsts

/- Author inspection: actual complete exports, no imported reference proof. -/
set_option leancert.trust "kernel"
set_option maxHeartbeats 4000000
noncomputable section
namespace NLA.IE05.AssemblyExpected
def entryMax_semantics : Prop :=
  ∀ {n : ℕ} (hn : 1 ≤ n) (A : Mat n),
    0 ≤ entryMax A ∧ (∀ i j, |A i j| ≤ entryMax A) ∧
      ∃ i j, entryMax A = |A i j|

def schurStep_bound : Prop :=
  ∀ {n : ℕ} (S : Mat n) (k p : Fin n)
    (hp : AdmissiblePivot S k p),
    activeMax (schurStep S k p) (k.val + 1) ≤ 2 * activeMax S k.val

def gepp_growth_bound : Prop :=
  ∀ {n : ℕ} (hn : 1 ≤ n) (A : Mat n)
    (path : PivotPath n) (hp : AdmissiblePath A path),
    0 < entryMax A ∧ 1 ≤ growth A path ∧ growth A path ≤ (2 : ℝ) ^ (n - 1)

def firstPath_semantics : Prop :=
  ∀ {n : ℕ} (A : Mat n) (hA : A.det ≠ 0),
    FirstAvailablePath A (firstPath A) ∧
      (∀ k, trajectory A (firstPath A) k = firstTrajectory A k) ∧
      ∀ path, FirstAvailablePath A path → path = firstPath A

def orthogonalGrowthSet_bounded : Prop :=
  ∀ (n : ℕ) (hn : 2 ≤ n),
    (orthogonalGrowthSet n).Nonempty ∧ BddAbove (orthogonalGrowthSet n) ∧
      ∀ r ∈ orthogonalGrowthSet n, 1 ≤ r ∧ r ≤ (2 : ℝ) ^ (n - 1)

def candidate_positiveQR : Prop :=
  ∀ (n : ℕ) (hn : 2 ≤ n),
    PositiveQR (prescribedLower n) (candidateQ n) (candidateR n) ∧
      ∀ Q R, PositiveQR (prescribedLower n) Q R →
        Q = candidateQ n ∧ R = candidateR n

def scaledColumns_orthogonal : Prop :=
  ∀ {n : ℕ} (H : Mat n) (d : Fin n → ℝ)
    (hd : ∀ j, 0 < d j) (hH : H.transpose * H = Matrix.diagonal d),
    Orthogonal (scaledColumns H d)

def scaledLU_trajectory : Prop :=
  ∀ {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hLb : ∀ i j, j < i → |L i j| ≤ 1)
    (hT : UpperTriangular T) (hTp : ∀ i, 0 < T i i) (hd : ∀ j, 0 < d j),
    FirstAvailablePath (scaledColumns (L * T) d) (noSwapPath n) ∧
      firstPath (scaledColumns (L * T) d) = noSwapPath n ∧
      ∀ k, k ≤ n → trajectory (scaledColumns (L * T) d) (noSwapPath n) k =
        scaledColumns (tailProduct L T k) d

def integer_factor_certificates : Prop :=
  ∀ b : Bool,
      (integerH b).transpose * integerH b = Matrix.diagonal (integerD b) ∧
      integerH b = integerLower b * integerT b ∧
      UnitLower (integerLower b) ∧ UpperTriangular (integerT b) ∧
      (∀ i j, j < i → |integerLower b i j| ≤ 1) ∧
      (∀ i, 0 < integerT b i i) ∧ (∀ j, 0 < integerD b j)

def integer_entry_certificates : Prop :=
  (∀ i j : Fin 8, 5272 * (integerH true i j) ^ 2 ≤ 3969 * integerD true j) ∧
    integerD true 7 = 5272 ∧
    integerH false 2 2 = 51 ∧ integerD false 2 = 3286 ∧
    (∀ k i j : Fin 8, k ≤ i → k ≤ j →
      (tailProduct (integerLower false) (integerT false) k.val i j) ^ 2 ≤
        5462 * integerD false j) ∧
    tailProduct (integerLower true) (integerT true) 7 7 7 = 5272

def canonical_integer_identification : Prop :=
  candidateQ 8 = normalizedInteger false ∧
      firstPath (candidateQ 8) = noSwapPath 8

def witness_orthogonal_path : Prop :=
  Orthogonal witnessQ ∧ firstPath witnessQ = noSwapPath 8 ∧
      FirstAvailablePath witnessQ (noSwapPath 8) ∧
      AdmissiblePath witnessQ (noSwapPath 8)

def bounded_growth_data : Prop :=
  entryMax witnessQ ≤ 63 / Real.sqrt 5272 ∧
      (5272 : ℝ) / 63 ≤ firstGrowth witnessQ ∧
      51 / Real.sqrt 3286 ≤ entryMax (candidateQ 8) ∧
      0 ≤ firstGrowth (candidateQ 8) ∧
      (firstGrowth (candidateQ 8)) ^ 2 ≤ (17948132 : ℝ) / 2601

def numerical_gap_positive : Prop :=
  ((5272 : ℝ) / 63) ^ 2 - (17948132 : ℝ) / 2601 =
      (117335164 : ℝ) / 1147041 ∧
      0 < (117335164 : ℝ) / 1147041

def witness_strict_growth : Prop :=
  firstGrowth (candidateQ 8) < firstGrowth witnessQ

def supremum_strict_gap : Prop :=
  firstGrowth (candidateQ 8) < orthogonalGrowthSup 8

def orthogonalExtremizerConjecture : Prop :=
  ¬ OrthogonalExtremizerConjecture

end NLA.IE05.AssemblyExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [
    (``NLA.IE05.entryMax_semantics, ``NLA.IE05.AssemblyExpected.entryMax_semantics),
    (``NLA.IE05.schurStep_bound, ``NLA.IE05.AssemblyExpected.schurStep_bound),
    (``NLA.IE05.gepp_growth_bound, ``NLA.IE05.AssemblyExpected.gepp_growth_bound),
    (``NLA.IE05.firstPath_semantics, ``NLA.IE05.AssemblyExpected.firstPath_semantics),
    (``NLA.IE05.orthogonalGrowthSet_bounded, ``NLA.IE05.AssemblyExpected.orthogonalGrowthSet_bounded),
    (``NLA.IE05.candidate_positiveQR, ``NLA.IE05.AssemblyExpected.candidate_positiveQR),
    (``NLA.IE05.scaledColumns_orthogonal, ``NLA.IE05.AssemblyExpected.scaledColumns_orthogonal),
    (``NLA.IE05.scaledLU_trajectory, ``NLA.IE05.AssemblyExpected.scaledLU_trajectory),
    (``NLA.IE05.integer_factor_certificates, ``NLA.IE05.AssemblyExpected.integer_factor_certificates),
    (``NLA.IE05.integer_entry_certificates, ``NLA.IE05.AssemblyExpected.integer_entry_certificates),
    (``NLA.IE05.canonical_integer_identification, ``NLA.IE05.AssemblyExpected.canonical_integer_identification),
    (``NLA.IE05.witness_orthogonal_path, ``NLA.IE05.AssemblyExpected.witness_orthogonal_path),
    (``NLA.IE05.bounded_growth_data, ``NLA.IE05.AssemblyExpected.bounded_growth_data),
    (``NLA.IE05.numerical_gap_positive, ``NLA.IE05.AssemblyExpected.numerical_gap_positive),
    (``NLA.IE05.witness_strict_growth, ``NLA.IE05.AssemblyExpected.witness_strict_growth),
    (``NLA.IE05.supremum_strict_gap, ``NLA.IE05.AssemblyExpected.supremum_strict_gap),
    (``NLA.IE05.orthogonalExtremizerConjecture, ``NLA.IE05.AssemblyExpected.orthogonalExtremizerConjecture)]
  for (actual, expectedName) in pairs do
    let some ci := env.find? actual | throwError "Missing theorem {actual}"
    let some ref := env.find? expectedName | throwError "Missing expected type {expectedName}"
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Not a theorem: {actual}"
    let some expected := ref.value? | throwError "Missing Prop body"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq ci.type expected do throwError "Wrong target type {actual}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {ci.type}"
  let project := fun n : Name => n.toString.startsWith "NLA.IE05." || n.toString.startsWith "_private.NLA.IE05."
  let mut pending := pairs.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:20000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.IE05.AssemblyExpected." then throwError "Proof depends on reference type {name}"
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial {name}"
        let ax ← liftCoreM <| collectAxioms name
        for a in ax do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
            throwError "Forbidden axiom {name}: {a}"
        let body ← match ci.value? (allowOpaque := true) with
          | some b => pure b.getUsedConstants.toList
          | none => match ci with
            | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
            | _ => throwError "Unexplained bodyless {name}"
        let deps := ci.type.getUsedConstants.toList ++ body
        used := deps ++ used
        let next := deps.filter project
        pending := next ++ pending
        logInfo m!"ACTUAL_DECL {name} AXIOMS {ax.toList}"
        logInfo m!"ACTUAL_EDGE {name}: {next}"
  unless pending.isEmpty do throwError "Incomplete traversal"
  let required := [``NLA.IE05._proved.normalizedQRQ_of_gram_lu,
    ``NLA.IE05._proved.integer_factor_certificates, ``NLA.IE05._proved.integer_entry_certificates,
    ``NLA.IE05._proved.normalizedInteger_path_trajectory,
    ``NLA.IE05._proved.normalizedInteger_trajectory_entry,
    ``NLA.IE05._proved.scaledLU_trajectory, ``NLA.IE05._proved.witness_growth_lower,
    ``NLA.IE05._proved.candidate_growth_sq_upper, ``NLA.IE05._proved.numerical_gap_positive,
    ``NLA.IE05.firstPath_semantics_proved, ``NLA.IE05.gepp_growth_bound_proved,
    ``NLA.IE05.orthogonalGrowthSet_bounded_proved, ``NLA.IE05.trajectory,
    ``NLA.IE05.firstPath, ``NLA.IE05.schurStep, ``NLA.IE05.AdmissiblePath,
    ``NLA.IE05.Orthogonal, ``NLA.IE05.PositiveQR, ``NLA.IE05.normalizedQRQ,
    ``NLA.IE05.firstGrowth, ``NLA.IE05.growth, ``NLA.IE05.entryMax,
    ``NLA.IE05.peakMax, ``NLA.IE05.orthogonalGrowthSet, ``NLA.IE05.orthogonalGrowthSup,
    ``NLA.IE05.OrthogonalExtremizerConjecture,
    ``Real.sq_sqrt, ``le_csSup, ``InnerProductSpace.gramSchmidtNormed, ``of_decide_eq_true]
  for n in required do
    unless used.contains n do throwError "Missing material dependency {n}"
    logInfo m!"RETAINED_DEPENDENCY {n}"
  logInfo m!"COMPLETE_ASSEMBLY roots={pairs.length}, closure={seen.length}, required={required.length}"

#print axioms NLA.IE05.entryMax_semantics
#assert_trust kernel NLA.IE05.entryMax_semantics
#print axioms NLA.IE05.schurStep_bound
#assert_trust kernel NLA.IE05.schurStep_bound
#print axioms NLA.IE05.gepp_growth_bound
#assert_trust kernel NLA.IE05.gepp_growth_bound
#print axioms NLA.IE05.firstPath_semantics
#assert_trust kernel NLA.IE05.firstPath_semantics
#print axioms NLA.IE05.orthogonalGrowthSet_bounded
#assert_trust kernel NLA.IE05.orthogonalGrowthSet_bounded
#print axioms NLA.IE05.candidate_positiveQR
#assert_trust kernel NLA.IE05.candidate_positiveQR
#print axioms NLA.IE05.scaledColumns_orthogonal
#assert_trust kernel NLA.IE05.scaledColumns_orthogonal
#print axioms NLA.IE05.scaledLU_trajectory
#assert_trust kernel NLA.IE05.scaledLU_trajectory
#print axioms NLA.IE05.integer_factor_certificates
#assert_trust kernel NLA.IE05.integer_factor_certificates
#print axioms NLA.IE05.integer_entry_certificates
#assert_trust kernel NLA.IE05.integer_entry_certificates
#print axioms NLA.IE05.canonical_integer_identification
#assert_trust kernel NLA.IE05.canonical_integer_identification
#print axioms NLA.IE05.witness_orthogonal_path
#assert_trust kernel NLA.IE05.witness_orthogonal_path
#print axioms NLA.IE05.bounded_growth_data
#assert_trust kernel NLA.IE05.bounded_growth_data
#print axioms NLA.IE05.numerical_gap_positive
#assert_trust kernel NLA.IE05.numerical_gap_positive
#print axioms NLA.IE05.witness_strict_growth
#assert_trust kernel NLA.IE05.witness_strict_growth
#print axioms NLA.IE05.supremum_strict_gap
#assert_trust kernel NLA.IE05.supremum_strict_gap
#print axioms NLA.IE05.orthogonalExtremizerConjecture
#assert_trust kernel NLA.IE05.orthogonalExtremizerConjecture
