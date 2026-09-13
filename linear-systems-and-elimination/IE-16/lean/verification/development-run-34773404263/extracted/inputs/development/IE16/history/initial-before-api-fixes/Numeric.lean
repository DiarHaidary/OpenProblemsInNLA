/-
  IE-16: finite exact arithmetic for the nine-point witness.

  This module is intentionally split from `Definitions.lean`: the latter is
  the reviewed statement boundary.  All constants below are the exact
  constants in Holden's finite counterexample; the only numerical automation
  intended here is kernel-checked `norm_num`, `ring_nf`, and the LeanCert
  verification tactic.
-/
import NLA.IE16.Definitions
import Mathlib.Analysis.Complex.Norm
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Tactic
import LeanCert.Tactic.Verification

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical
noncomputable section

namespace NLA.IE16

/- The cubic-root identities are the only irrational algebra used by the
   finite coordinate calculations.  Keeping them named makes later finite
   `fin_cases` proofs readable and keeps interval/numeric work out of Lean. -/
lemma omega_sq_add_omega_add_one : omega ^ 2 + omega + 1 = 0 := by
  apply Complex.ext <;>
    norm_num [omega, Complex.ext_iff, Real.sq_sqrt]

lemma omega_cube : omega ^ 3 = 1 := by
  have hs : omega ^ 2 = -omega - 1 := by
    linear_combination -omega_sq_add_omega_add_one
  calc
    omega ^ 3 = omega * (omega ^ 2) := by ring
    _ = omega * (-omega - 1) := by rw [hs]
    _ = 1 := by linear_combination -omega_sq_add_omega_add_one

lemma omega_ne_zero : omega ≠ 0 := by
  intro h
  have := congrArg Complex.re h
  norm_num [omega] at this

lemma clusterPoint_injective : Function.Injective clusterPoint := by
  intro x y h
  rcases x with ⟨a, b⟩
  rcases y with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [clusterPoint, omega, epsilon, Complex.ext_iff, Real.sq_sqrt] at h ⊢

lemma clusterPoint_ne_zero (a b : Fin 3) : clusterPoint a b ≠ 0 := by
  fin_cases a <;> fin_cases b <;>
    intro h
  all_goals
    have hr := congrArg Complex.re h
    have hi := congrArg Complex.im h
    norm_num [clusterPoint, omega, epsilon, Complex.ext_iff, Real.sq_sqrt] at hr hi

lemma explicitL_card : explicitL.card = 9 := by
  rw [explicitL, Finset.card_image_iff]
  · simp
  · exact clusterPoint_injective.injOn

lemma explicitL_admissible : admissible explicitL 9 := by
  refine ⟨explicitL_card, ?_⟩
  intro z hz
  rcases Finset.mem_image.mp hz with ⟨ab, hab, rfl⟩
  exact clusterPoint_ne_zero ab.1 ab.2

lemma witness_feasible : feasible explicitL 4 witnessPolynomial := by
  constructor
  · norm_num [witnessPolynomial]
  · simp [witnessPolynomial]

/- The nine norm computations are finite, but retain the square-norm form so
   that `norm_num` only has to certify rational identities and
   `(Real.sqrt 3)^2 = 3`. -/
lemma witness_eval_sq_norm (a b : Fin 3) :
    ‖witnessPolynomial.eval (clusterPoint a b)‖ ^ 2 = exactFullMinimum ^ 2 := by
  fin_cases a <;> fin_cases b <;>
    rw [Complex.sq_norm] <;>
    norm_num [witnessPolynomial, clusterPoint, omega, epsilon, denominator,
      Complex.normSq_apply, Real.sq_sqrt]

lemma witness_eval_norm (a b : Fin 3) :
    ‖witnessPolynomial.eval (clusterPoint a b)‖ = exactFullMinimum := by
  have hm : 0 ≤ exactFullMinimum := by norm_num [exactFullMinimum]
  have hn : 0 ≤ ‖witnessPolynomial.eval (clusterPoint a b)‖ :=
    Complex.norm_nonneg _
  nlinarith [witness_eval_sq_norm a b]

lemma witness_objective :
    maxModulus explicitL witnessPolynomial = exactFullMinimum := by
  have hne : explicitL.Nonempty := by
    rw [Finset.nonempty_iff_ne_empty]
    intro h
    have := explicitL_card
    simp [h] at this
  unfold maxModulus
  simp only [dif_pos hne]
  apply Finset.sup'_eq_of_forall
  intro z hz
  rcases Finset.mem_image.mp hz with ⟨ab, hab, rfl⟩
  exact witness_eval_norm ab.1 ab.2

/- These are the positive rational weights from the source certificate.  A
   diagonal pair (a=b) gets the first weight and every off-diagonal pair the
   second; this is the same as the source's dependence on (b-a) mod 3. -/
def witnessWeightDiagonal : ℝ := 332333665667 / 3003009003003
def witnessWeightOffDiagonal : ℝ := 334334667667 / 3003009003003
def witnessWeight (a b : Fin 3) : ℝ :=
  if a = b then witnessWeightDiagonal else witnessWeightOffDiagonal

lemma witnessWeight_pos (a b : Fin 3) : 0 < witnessWeight a b := by
  fin_cases a <;> fin_cases b <;>
    norm_num [witnessWeight, witnessWeightDiagonal, witnessWeightOffDiagonal]

lemma witnessWeight_sum :
    (∑ a : Fin 3, ∑ b : Fin 3, witnessWeight a b) = 1 := by
  norm_num [witnessWeight, witnessWeightDiagonal, witnessWeightOffDiagonal,
    Fin.sum_univ_succ]

/- Weighted orthogonality is checked in the exact field ℂ.  The four moments
   are the only moments needed for an arbitrary degree-four polynomial whose
   constant term vanishes; no floating-point or interval approximation enters
   this identity. -/
lemma weighted_moment (ell : Fin 4) :
    ∑ a : Fin 3, ∑ b : Fin 3,
      (witnessWeight a b : ℂ) *
          conj (witnessPolynomial.eval (clusterPoint a b)) *
          clusterPoint a b ^ (ell.val + 1) = 0 := by
  fin_cases ell <;>
    apply Complex.ext <;>
    norm_num [witnessWeight, witnessWeightDiagonal, witnessWeightOffDiagonal,
      witnessPolynomial, clusterPoint, omega, epsilon, denominator,
      Fin.sum_univ_succ, Complex.ext_iff, Real.sq_sqrt] <;>
    ring

end NLA.IE16
