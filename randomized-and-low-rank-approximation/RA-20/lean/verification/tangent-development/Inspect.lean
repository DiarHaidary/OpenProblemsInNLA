/- RA-20 tangent helper author's diagnostic checks. This is not an
independent final review, Linux run or Comparator result. Traversal structure is
adapted from the completed RA-09 referee-2 inspector; every result is rerun here.
The reference changes the frozen Challenge namespace only. -/
import NLA.RA20.Tangent
import verification.«tangent-development».Reference
import Lean.Util.FoldConsts

set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.RA20.algebraic_tangent_space_proved,
    ``NLA.RA20.TangentReference.algebraic_tangent_space)]
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual theorem {actual}"
    let some b := env.find? reference | throwError "Missing frozen reference {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Actual export is not a theorem {actual}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type b.type do
        throwError "Frozen signature mismatch {actual}"
    unless (← liftCoreM <| collectAxioms reference).contains ``sorryAx do
      throwError "Expected diagnostic reference admission {reference}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.RA20." ||
    n.toString.startsWith "_private.NLA.RA20."
  let mut pending := pairs.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.RA20.TangentReference." then
          throwError "Actual proof reached admitted reference {name}"
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
  let required := [``NLA.RA20.TangentVector, ``NLA.RA20.polyDirectional,
    ``NLA.RA20.polyDirectional_hollowPullback, ``NLA.RA20.polyDirectional_mul,
    ``NLA.RA20.polyDirectional_sub, ``NLA.RA20.polyDirectional_X,
    ``NLA.RA20.polyDirectional_abc, ``NLA.RA20.diagonalPolynomial_mem,
    ``NLA.RA20.symmetryPolynomial_mem, ``NLA.RA20.genericPolynomial_mem,
    ``NLA.RA20.matrix_eq_hollow_of_symm_diag,
    ``NLA.RA20.definingIdeal_eq_comap_abcIdeal,
    ``NLA.RA20.abcIdeal_vanishing, ``NLA.RA20.abcIdeal,
    ``NLA.RA20.hollowPullback, ``NLA.RA20.aeval_hollowPullback,
    ``MvPolynomial.pderiv, ``MvPolynomial.pderiv_mul,
    ``MvPolynomial.induction_on, ``Ideal.mem_span_singleton,
    ``MvPolynomial.vanishingIdeal_zeroLocus_eq_radical]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.RA20.algebraic_tangent_space_proved
#assert_trust kernel NLA.RA20.polyDirectional_hollowPullback
#assert_trust kernel NLA.RA20.polyDirectional_mul
#assert_trust kernel NLA.RA20.definingIdeal_eq_comap_abcIdeal
#print axioms NLA.RA20.algebraic_tangent_space_proved
#print axioms NLA.RA20.polyDirectional_hollowPullback
#print axioms NLA.RA20.polyDirectional_mul
#print axioms NLA.RA20.definingIdeal_eq_comap_abcIdeal
set_option pp.all true in
#print NLA.RA20.TangentVector
set_option pp.all true in
#print NLA.RA20.polyDirectional
set_option pp.proofs true in
#print NLA.RA20.polyDirectional_hollowPullback
set_option pp.proofs true in
#print NLA.RA20.algebraic_tangent_space_proved
