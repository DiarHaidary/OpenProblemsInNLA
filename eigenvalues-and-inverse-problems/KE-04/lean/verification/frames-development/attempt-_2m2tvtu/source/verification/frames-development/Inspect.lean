/- Frames author inspection: expected types are exact frozen propositions,
not admitted reference proofs. All actual roots are inspected independently. -/
import NLA.KE04.Frames
import Lean.Util.FoldConsts
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.KE04.FramesExpected
def real_matrix_semantics : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (M : Rect n m),
    (A.IsHermitian ↔ A.transpose = A) ∧
      (∀ (x : Vec m) i, act M x i = ∑ j, M i j * x j) ∧
      (M.transpose * M = 1 ↔ Orthonormal ℝ (column M))

def krylovBasis_exists : Prop :=
  ∀ {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (hfull : FullBlockDimension A V ell),
    ∃ Q : Rect n (ell * p), IsKrylovBasis A V ell Q

def frameProjection_semantics : Prop :=
  ∀ {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1),
    (frameProjection Q).IsHermitian ∧
      frameProjection Q * frameProjection Q = frameProjection Q ∧
      (∀ x, x ∈ columnSpace Q ↔ act (frameProjection Q) x = x) ∧
      ∀ x y, y ∈ columnSpace Q →
        inner ℝ y (x - act (frameProjection Q) x) = 0

def compression_semantics : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1),
    compression A Q = Q.transpose * A * Q ∧ (compression A Q).IsHermitian ∧
      ∀ x, x ∈ columnSpace Q →
        act Q (act (compression A Q) (act Q.transpose x)) =
          act (frameProjection Q) (act A x)

def compressedQuadratic_semantics : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (a b : ℝ),
    (∀ x, form (compressedQuadratic A Q a b) x =
      form (quadraticMatrix (compression A Q) a b) (act Q.transpose x)) ∧
      ((quadraticMatrix (compression A Q) a b).PosSemidef →
        (compressedQuadratic A Q a b).PosSemidef)
end NLA.KE04.FramesExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.KE04._proved.real_matrix_semantics, ``NLA.KE04.FramesExpected.real_matrix_semantics),
    (``NLA.KE04._proved.krylovBasis_exists, ``NLA.KE04.FramesExpected.krylovBasis_exists),
    (``NLA.KE04._proved.frameProjection_semantics, ``NLA.KE04.FramesExpected.frameProjection_semantics),
    (``NLA.KE04._proved.compression_semantics, ``NLA.KE04.FramesExpected.compression_semantics),
    (``NLA.KE04._proved.compressedQuadratic_semantics, ``NLA.KE04.FramesExpected.compressedQuadratic_semantics)]
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
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  let mut pending := [``NLA.KE04._proved.act_apply, ``NLA.KE04._proved.act_mul, ``NLA.KE04._proved.act_one, ``NLA.KE04._proved.inner_eq_sum, ``NLA.KE04._proved.inner_act_transpose, ``NLA.KE04._proved.inner_act_left, ``NLA.KE04._proved.inner_columns, ``NLA.KE04._proved.frame_iff_orthonormal, ``NLA.KE04._proved.real_matrix_semantics, ``NLA.KE04._proved.act_eq_column_sum, ``NLA.KE04._proved.columnSpace_eq_range_act, ``NLA.KE04._proved.act_transpose_act, ``NLA.KE04._proved.frameProjection_act, ``NLA.KE04._proved.frameProjection_fixed_iff, ``NLA.KE04._proved.frameProjection_semantics, ``NLA.KE04._proved.submodule_frame_exists, ``NLA.KE04._proved.krylovBasis_exists, ``NLA.KE04._proved.compression_semantics, ``NLA.KE04._proved.compressedQuadratic_semantics]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.KE04.FramesExpected." then
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
  let required := [``NLA.KE04._proved.act_mul,
    ``NLA.KE04._proved.act_one,
    ``NLA.KE04._proved.inner_eq_sum,
    ``NLA.KE04._proved.inner_act_transpose,
    ``NLA.KE04._proved.inner_act_left,
    ``NLA.KE04._proved.inner_columns,
    ``NLA.KE04._proved.frame_iff_orthonormal,
    ``NLA.KE04._proved.act_eq_column_sum,
    ``NLA.KE04._proved.columnSpace_eq_range_act,
    ``NLA.KE04._proved.act_transpose_act,
    ``NLA.KE04._proved.frameProjection_act,
    ``NLA.KE04._proved.frameProjection_fixed_iff,
    ``NLA.KE04._proved.submodule_frame_exists,
    ``NLA.KE04.column,
    ``NLA.KE04.act,
    ``NLA.KE04.columnSpace,
    ``NLA.KE04.krylov,
    ``NLA.KE04.FullBlockDimension,
    ``NLA.KE04.IsKrylovBasis,
    ``NLA.KE04.frameProjection,
    ``NLA.KE04.compression,
    ``NLA.KE04.compressedQuadratic,
    ``NLA.KE04.quadraticMatrix,
    ``NLA.KE04.form,
    ``Matrix.toLpLin,
    ``Matrix.toLpLin_mul_same,
    ``Matrix.toLpLin_one,
    ``stdOrthonormalBasis,
    ``OrthonormalBasis.reindex,
    ``Orthonormal.comp_linearIsometry,
    ``Submodule.map_span,
    ``Module.Basis.span_eq,
    ``Matrix.PosSemidef.mul_mul_conjTranspose_same,
    ``Matrix.isHermitian_conjTranspose_mul_mul]
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

#assert_trust kernel NLA.KE04._proved.act_apply
#print axioms NLA.KE04._proved.act_apply
#assert_trust kernel NLA.KE04._proved.act_mul
#print axioms NLA.KE04._proved.act_mul
#assert_trust kernel NLA.KE04._proved.act_one
#print axioms NLA.KE04._proved.act_one
#assert_trust kernel NLA.KE04._proved.inner_eq_sum
#print axioms NLA.KE04._proved.inner_eq_sum
#assert_trust kernel NLA.KE04._proved.inner_act_transpose
#print axioms NLA.KE04._proved.inner_act_transpose
#assert_trust kernel NLA.KE04._proved.inner_act_left
#print axioms NLA.KE04._proved.inner_act_left
#assert_trust kernel NLA.KE04._proved.inner_columns
#print axioms NLA.KE04._proved.inner_columns
#assert_trust kernel NLA.KE04._proved.frame_iff_orthonormal
#print axioms NLA.KE04._proved.frame_iff_orthonormal
#assert_trust kernel NLA.KE04._proved.real_matrix_semantics
#print axioms NLA.KE04._proved.real_matrix_semantics
#assert_trust kernel NLA.KE04._proved.act_eq_column_sum
#print axioms NLA.KE04._proved.act_eq_column_sum
#assert_trust kernel NLA.KE04._proved.columnSpace_eq_range_act
#print axioms NLA.KE04._proved.columnSpace_eq_range_act
#assert_trust kernel NLA.KE04._proved.act_transpose_act
#print axioms NLA.KE04._proved.act_transpose_act
#assert_trust kernel NLA.KE04._proved.frameProjection_act
#print axioms NLA.KE04._proved.frameProjection_act
#assert_trust kernel NLA.KE04._proved.frameProjection_fixed_iff
#print axioms NLA.KE04._proved.frameProjection_fixed_iff
#assert_trust kernel NLA.KE04._proved.frameProjection_semantics
#print axioms NLA.KE04._proved.frameProjection_semantics
#assert_trust kernel NLA.KE04._proved.submodule_frame_exists
#print axioms NLA.KE04._proved.submodule_frame_exists
#assert_trust kernel NLA.KE04._proved.krylovBasis_exists
#print axioms NLA.KE04._proved.krylovBasis_exists
#assert_trust kernel NLA.KE04._proved.compression_semantics
#print axioms NLA.KE04._proved.compression_semantics
#assert_trust kernel NLA.KE04._proved.compressedQuadratic_semantics
#print axioms NLA.KE04._proved.compressedQuadratic_semantics
set_option pp.all true in
#print NLA.KE04.act
set_option pp.all true in
#print NLA.KE04.column
set_option pp.all true in
#print NLA.KE04.columnSpace
set_option pp.all true in
#print NLA.KE04.frameProjection
set_option pp.all true in
#print NLA.KE04.compression
set_option pp.all true in
#print NLA.KE04.compressedQuadratic
set_option pp.proofs true in
#print NLA.KE04._proved.real_matrix_semantics
set_option pp.proofs true in
#print NLA.KE04._proved.krylovBasis_exists
set_option pp.proofs true in
#print NLA.KE04._proved.frameProjection_semantics
set_option pp.proofs true in
#print NLA.KE04._proved.compression_semantics
set_option pp.proofs true in
#print NLA.KE04._proved.compressedQuadratic_semantics
set_option pp.proofs true in
#print NLA.KE04._proved.submodule_frame_exists
