/- Admission-free helper inspection. No Challenge/reference module is imported.
Completion inspection only; no whole-proof independent approval or Linux run. -/
import NLA.IE05.IntegerQR
import NLA.IE05.ExactCertificates
import Lean.Util.FoldConsts
set_option maxHeartbeats 4000000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.CertificatesQRExpected
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

def numerical_gap_positive : Prop :=
((5272 : ℝ) / 63) ^ 2 - (17948132 : ℝ) / 2601 =
      (117335164 : ℝ) / 1147041 ∧
      0 < (117335164 : ℝ) / 1147041
def normalizedQRQ_of_gram_lu : Prop :=
  ∀ {n : ℕ} (L H T : Mat n) (d : Fin n → ℝ),
    (∀ j, 0 < d j) → H.transpose * H = Matrix.diagonal d →
    H = L * T → UpperTriangular T → (∀ i, 0 < T i i) →
    normalizedQRQ L = scaledColumns H d
end NLA.IE05.CertificatesQRExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [
    (``NLA.IE05._proved.integer_factor_certificates, ``NLA.IE05.CertificatesQRExpected.integer_factor_certificates),
    (``NLA.IE05._proved.integer_entry_certificates, ``NLA.IE05.CertificatesQRExpected.integer_entry_certificates),
    (``NLA.IE05._proved.numerical_gap_positive, ``NLA.IE05.CertificatesQRExpected.numerical_gap_positive),
    (``NLA.IE05._proved.normalizedQRQ_of_gram_lu, ``NLA.IE05.CertificatesQRExpected.normalizedQRQ_of_gram_lu)]
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual {actual}"
    let some b := env.find? reference | throwError "Missing expected {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Not a theorem {actual}"
    let some expected := b.value? | throwError "Expected type body missing"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type expected do throwError "TYPE MISMATCH {actual}"
    logInfo m!"EXACT_EXPECTED_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.IE05." ||
    n.toString.startsWith "_private.NLA.IE05."
  let materialInt := [``Int.instDecidableEq, ``Int.decEq]
  let mut pending := pairs.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:10000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.IE05.CertificatesQRExpected." then
          throwError "Actual proof depends on inspector definition {name}"
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial {name}"
        let ax ← liftCoreM <| collectAxioms name
        for a in ax do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
            throwError "Forbidden axiom {name}: {a}"
        let kind := match ci with
          | .thmInfo _ => "theorem"
          | .defnInfo _ => "definition"
          | .opaqueInfo _ => "opaque"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
          | .axiomInfo _ => "axiom"
          | .quotInfo _ => "quotient"
        logInfo m!"ACTUAL_DECL {name} KIND {kind} AXIOMS {ax.toList}"
        let body ← match ci.value? (allowOpaque := true) with
          | some b => pure b.getUsedConstants.toList
          | none => match ci with
            | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
            | _ => throwError "Unexplained bodyless {name}"
        let deps := ci.type.getUsedConstants.toList ++ body
        used := deps ++ used
        let follow := deps.filter (fun n => isProject n || materialInt.contains n)
        logInfo m!"ACTUAL_EDGE {name}: {follow}"
        pending := follow ++ pending
  unless pending.isEmpty do throwError "Incomplete declaration traversal"
  let required := [``NLA.IE05._proved.integerLowerZeroDecidable,
    ``NLA.IE05._proved.integerTZeroDecidable, ``Int.instDecidableEq, ``Int.decEq,
    ``NLA.IE05.integerH, ``NLA.IE05.integerLower, ``NLA.IE05.integerT,
    ``NLA.IE05.integerD, ``NLA.IE05.tailProduct, ``NLA.IE05.UnitLower,
    ``NLA.IE05.UpperTriangular, ``NLA.IE05.normalizedQRQ, ``NLA.IE05.scaledColumns,
    ``NLA.IE05._proved.scaledColumns_orthogonal,
    ``NLA.IE05._proved.normalizedQRQ_eq_of_positiveQR,
    ``Matrix.det_of_isUpperTriangular,
    ``Matrix.blockTriangular_inv_of_blockTriangular,
    ``Matrix.mul_nonsing_inv, ``Real.sqrt_pos]
  for n in required do
    unless used.contains n do throwError "Missing genuine dependency {n}"
    logInfo m!"REQUIRED_ACTUAL_DEPENDENCY {n}"
  for n in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains n then throwError "Forbidden dependency {n}"
  logInfo m!"COMPLETE_HELPER_CLOSURE {seen.length} REQUIRED {required.length}"

#assert_trust kernel NLA.IE05._proved.integer_factor_certificates
#print axioms NLA.IE05._proved.integer_factor_certificates
#assert_trust kernel NLA.IE05._proved.integer_entry_certificates
#print axioms NLA.IE05._proved.integer_entry_certificates
#assert_trust kernel NLA.IE05._proved.numerical_gap_positive
#print axioms NLA.IE05._proved.numerical_gap_positive
#assert_trust kernel NLA.IE05._proved.normalizedQRQ_of_gram_lu
#print axioms NLA.IE05._proved.normalizedQRQ_of_gram_lu
#assert_trust kernel NLA.IE05._proved.integerLowerZeroDecidable
#print axioms NLA.IE05._proved.integerLowerZeroDecidable
#assert_trust kernel NLA.IE05._proved.integerTZeroDecidable
#print axioms NLA.IE05._proved.integerTZeroDecidable
#assert_trust kernel Int.instDecidableEq
#print axioms Int.instDecidableEq
#assert_trust kernel Int.decEq
#print axioms Int.decEq
set_option pp.all true in
#print NLA.IE05._proved.integerLowerZeroDecidable
set_option pp.all true in
#print NLA.IE05._proved.integerTZeroDecidable
#print Int.instDecidableEq
#print Int.decEq
