import Challenge
import Lean.Util.FoldConsts
set_option maxHeartbeats 1200000
open NLA.KE04
noncomputable section
namespace KE04Referee2Expected
def real_matrix_semantics : Prop := ∀ {n m : ℕ} (A : Mat n) (M : Rect n m),
(A.IsHermitian ↔ A.transpose = A) ∧
      (∀ (x : Vec m) i, act M x i = ∑ j, M i j * x j) ∧
      (M.transpose * M = 1 ↔ Orthonormal ℝ (column M))

def krylov_range_semantics : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ),
krylov A V ell = LinearMap.range (krylovCombination A V ell) ∧
      (∀ x, x ∈ krylov A V ell ↔ ∃ c : Fin ell × Fin p → ℝ,
        x = ∑ rc, c rc • column (A ^ rc.1.val * V) rc.2) ∧
      Module.finrank ℝ (krylov A V ell) ≤ ell * p

def krylov_nesting_and_shift : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p),
krylov A V 0 = ⊥ ∧ Monotone (krylov A V) ∧
      ∀ ell x, x ∈ krylov A V ell → act A x ∈ krylov A V (ell + 1)

def fullBlockDimension_iff_independent : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ),
(FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell)) ∧
      (FullColumnRank V ↔ FullBlockDimension A V 1)

def fullBlockDimension_prefix : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (s : ℕ) (hs : FullBlockDimension A V s),
∀ ell, ell ≤ s → FullBlockDimension A V ell ∧
      Function.Injective (krylovCombination A V ell)

def lastFullBlockIteration_exists : Prop := ∀ {n p : ℕ} (hp : 0 < p)
    (A : Mat n) (V : Rect n p) (hV : FullColumnRank V),
∃ s, 1 ≤ s ∧ LastFullBlockIteration A V s

def krylovBasis_exists : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (hfull : FullBlockDimension A V ell),
∃ Q : Rect n (ell * p), IsKrylovBasis A V ell Q

def frameProjection_semantics : Prop := ∀ {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1),
(frameProjection Q).IsHermitian ∧
      frameProjection Q * frameProjection Q = frameProjection Q ∧
      (∀ x, x ∈ columnSpace Q ↔ act (frameProjection Q) x = x) ∧
      ∀ x y, y ∈ columnSpace Q →
        inner ℝ y (x - act (frameProjection Q) x) = 0

def compression_semantics : Prop := ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1),
compression A Q = Q.transpose * A * Q ∧ (compression A Q).IsHermitian ∧
      ∀ x, x ∈ columnSpace Q →
        act Q (act (compression A Q) (act Q.transpose x)) =
          act (frameProjection Q) (act A x)

def orderedSpectrum_semantics : Prop := ∀ {m : ℕ} (M : Mat m) (hM : M.IsHermitian),
Monotone (orderedEigenvalues M hM) ∧
      (∀ r, act M (orderedEigenbasis M hM r) =
        orderedEigenvalues M hM r • orderedEigenbasis M hM r) ∧
      M.charpoly.roots = Finset.univ.val.map (orderedEigenvalues M hM) ∧
      ∀ i (hi : i < m), eigenvalueAt M hM i = orderedEigenvalues M hM ⟨i, hi⟩

def compression_basis_independent : Prop := ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q R : Rect n m) (hQ : Q.transpose * Q = 1) (hR : R.transpose * R = 1)
    (hspan : columnSpace Q = columnSpace R),
(∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R

def interval_index_validity : Prop := ∀ (k p i : ℕ) (hk : 1 ≤ k)
    (hi : 1 ≤ i) (hu : i ≤ (k - 1) * p),
2 ≤ k ∧ 0 < p ∧ i - 1 < k * p ∧ i + p - 1 < k * p

def quadratic_semantics : Prop := ∀ {m : ℕ} (M : Mat m) (a b : ℝ),
(monicQuadratic a b).Monic ∧ (monicQuadratic a b).natDegree = 2 ∧
      quadraticMatrix M a b = Polynomial.aeval M (monicQuadratic a b) ∧
      quadraticMatrix M a b = M ^ 2 - (a + b) • M + (a * b) • (1 : Mat m)

def spectral_gap_quadratic_psd : Prop := ∀ {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ) (hab : a ≤ b)
    (hgap : ∀ r, ¬ (a < orderedEigenvalues M hM r ∧ orderedEigenvalues M hM r < b)),
(quadraticMatrix M a b).PosSemidef

def spectral_window_subspace : Prop := ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) (i p : ℕ) (hi : i + p < m),
∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0

def krylov_intersection_nonzero : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 1 ≤ k) (hfull : FullBlockDimension A V k)
    (hprev : FullBlockDimension A V (k - 1)) (E : Submodule ℝ (Vec n))
    (hE : E ≤ krylov A V k) (hdim : Module.finrank ℝ E = p + 1),
∃ x : Vec n, x ≠ 0 ∧ x ∈ E ∧ x ∈ krylov A V (k - 1)

def psd_zero_form_iff_kernel : Prop := ∀ {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m),
form M x = 0 ↔ act M x = 0

def compressedQuadratic_semantics : Prop := ∀ {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (a b : ℝ),
(∀ x, form (compressedQuadratic A Q a b) x =
      form (quadraticMatrix (compression A Q) a b) (act Q.transpose x)) ∧
      ((quadraticMatrix (compression A Q) a b).PosSemidef →
        (compressedQuadratic A Q a b).PosSemidef)

def quadratic_forms_agree : Prop := ∀ {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j)
    (Qk : Rect n (k * p)) (Qj : Rect n (j * p))
    (hQk : IsKrylovBasis A V k Qk) (hQj : IsKrylovBasis A V j Qj)
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (a b : ℝ),
form (compressedQuadratic A Qk a b) x =
      form (compressedQuadratic A Qj a b) x

def later_quadratic_identity : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j) (Qj : Rect n (j * p))
    (hQj : IsKrylovBasis A V j Qj) (x : Vec n)
    (hx : x ∈ krylov A V (k - 1)) (a b : ℝ),
act (compressedQuadratic A Qj a b) x = act (quadraticMatrix A a b) x

def fullRank_quadratic_nonannihilation : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 2 ≤ k) (hfull : FullBlockDimension A V (k + 1))
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (hne : x ≠ 0) (a b : ℝ),
act (quadraticMatrix A a b) x ≠ 0

def strictIntervalOccupancy : Prop := FullPrefixBlockLanczosClaim

def fullPrefix_implies_canonical : Prop := FullPrefixBlockLanczosClaim → BlockLanczosConjecture

def blockLanczosConjecture : Prop := BlockLanczosConjecture

end KE04Referee2Expected
set_option pp.all true

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs : List (Name × Name) := [(``NLA.KE04.real_matrix_semantics, ``KE04Referee2Expected.real_matrix_semantics), (``NLA.KE04.krylov_range_semantics, ``KE04Referee2Expected.krylov_range_semantics), (``NLA.KE04.krylov_nesting_and_shift, ``KE04Referee2Expected.krylov_nesting_and_shift), (``NLA.KE04.fullBlockDimension_iff_independent, ``KE04Referee2Expected.fullBlockDimension_iff_independent), (``NLA.KE04.fullBlockDimension_prefix, ``KE04Referee2Expected.fullBlockDimension_prefix), (``NLA.KE04.lastFullBlockIteration_exists, ``KE04Referee2Expected.lastFullBlockIteration_exists), (``NLA.KE04.krylovBasis_exists, ``KE04Referee2Expected.krylovBasis_exists), (``NLA.KE04.frameProjection_semantics, ``KE04Referee2Expected.frameProjection_semantics), (``NLA.KE04.compression_semantics, ``KE04Referee2Expected.compression_semantics), (``NLA.KE04.orderedSpectrum_semantics, ``KE04Referee2Expected.orderedSpectrum_semantics), (``NLA.KE04.compression_basis_independent, ``KE04Referee2Expected.compression_basis_independent), (``NLA.KE04.interval_index_validity, ``KE04Referee2Expected.interval_index_validity), (``NLA.KE04.quadratic_semantics, ``KE04Referee2Expected.quadratic_semantics), (``NLA.KE04.spectral_gap_quadratic_psd, ``KE04Referee2Expected.spectral_gap_quadratic_psd), (``NLA.KE04.spectral_window_subspace, ``KE04Referee2Expected.spectral_window_subspace), (``NLA.KE04.krylov_intersection_nonzero, ``KE04Referee2Expected.krylov_intersection_nonzero), (``NLA.KE04.psd_zero_form_iff_kernel, ``KE04Referee2Expected.psd_zero_form_iff_kernel), (``NLA.KE04.compressedQuadratic_semantics, ``KE04Referee2Expected.compressedQuadratic_semantics), (``NLA.KE04.quadratic_forms_agree, ``KE04Referee2Expected.quadratic_forms_agree), (``NLA.KE04.later_quadratic_identity, ``KE04Referee2Expected.later_quadratic_identity), (``NLA.KE04.fullRank_quadratic_nonannihilation, ``KE04Referee2Expected.fullRank_quadratic_nonannihilation), (``NLA.KE04.strictIntervalOccupancy, ``KE04Referee2Expected.strictIntervalOccupancy), (``NLA.KE04.fullPrefix_implies_canonical, ``KE04Referee2Expected.fullPrefix_implies_canonical), (``NLA.KE04.blockLanczosConjecture, ``KE04Referee2Expected.blockLanczosConjecture)]
  let forbidden := pairs.map Prod.fst
  for (actual, expected) in pairs do
    let some a := env.find? actual | throwError "Missing actual target {actual}"
    let some b := env.find? expected | throwError "Missing separately elaborated proposition {expected}"
    let some expectedType := b.value? (allowOpaque := true) | throwError "Missing proposition body"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Target is not a theorem {actual}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type expectedType do
        throwError "Exact reviewed type mismatch {actual}"
    let axioms ← liftCoreM <| collectAxioms expected
    for ax in axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Nonstandard axiom in proposition, not proof: {actual}: {ax}"
    let direct := a.type.getUsedConstants.toList
    for dep in direct do
      if forbidden.contains dep || dep == ``sorryAx then
        throwError "A target type depends on a reference hole: {actual}: {dep}"
    logInfo m!"EXACT_REVIEWED_TYPE {actual}: {a.type}"
    logInfo m!"TYPE_ONLY_SAFE {actual}: axioms={axioms.toList}; direct={direct}"
  logInfo m!"TYPE_COUNTS exact={pairs.length}; Challenge_bodies_not_used_as_proofs"
