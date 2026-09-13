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
open scoped BigOperators Classical ComplexConjugate
noncomputable section

namespace NLA.IE16

/- Normalize powers of the one real algebraic generator symbolically.
   This avoids interval subdivision and repeated nonlinear searches. -/
private lemma sqrt_three_pow_even (n : ℕ) :
    (Real.sqrt 3) ^ (2 * n) = (3 : ℝ) ^ n := by
  rw [pow_mul, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]

private lemma sqrt_three_pow_odd (n : ℕ) :
    (Real.sqrt 3) ^ (2 * n + 1) = (3 : ℝ) ^ n * Real.sqrt 3 := by
  rw [pow_succ, pow_mul, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]


private lemma sqrt_three_pow_2 :
    (Real.sqrt 3) ^ 2 = (3 : ℝ) := by
  exact Real.sq_sqrt (by norm_num)

private lemma sqrt_three_pow_3 :
    (Real.sqrt 3) ^ 3 = (3 * Real.sqrt 3 : ℝ) := by
  have h := sqrt_three_pow_odd 1
  norm_num at h
  exact h

private lemma sqrt_three_pow_4 :
    (Real.sqrt 3) ^ 4 = (9 : ℝ) := by
  have h := sqrt_three_pow_even 2
  norm_num at h
  exact h

private lemma sqrt_three_pow_5 :
    (Real.sqrt 3) ^ 5 = (9 * Real.sqrt 3 : ℝ) := by
  have h := sqrt_three_pow_odd 2
  norm_num at h
  exact h

private lemma sqrt_three_pow_6 :
    (Real.sqrt 3) ^ 6 = (27 : ℝ) := by
  have h := sqrt_three_pow_even 3
  norm_num at h
  exact h

private lemma sqrt_three_pow_7 :
    (Real.sqrt 3) ^ 7 = (27 * Real.sqrt 3 : ℝ) := by
  have h := sqrt_three_pow_odd 3
  norm_num at h
  exact h


/- The cubic-root identities are the only irrational algebra used by the
   finite coordinate calculations.  Keeping them named makes later finite
   `fin_cases` proofs readable and keeps interval/numeric work out of Lean. -/
lemma omega_sq_add_omega_add_one : omega ^ 2 + omega + 1 = 0 := by
  apply Complex.ext <;>
    norm_num [omega, Complex.ext_iff, pow_succ] <;>
    ring_nf <;>
    norm_num [Real.sq_sqrt]

lemma omega_cube : omega ^ 3 = 1 := by
  have hs : omega ^ 2 = -omega - 1 := by
    linear_combination omega_sq_add_omega_add_one
  calc
    omega ^ 3 = omega * (omega ^ 2) := by ring
    _ = omega * (-omega - 1) := by rw [hs]
    _ = 1 := by linear_combination -omega_sq_add_omega_add_one

lemma omega_ne_zero : omega ≠ 0 := by
  intro h
  have := congrArg Complex.re h
  norm_num [omega] at this

/- Exact rational coordinates of the three cubic roots. The only irrational
   generator is factored out before the finite injectivity comparisons. -/
private def rootReal (a : Fin 3) : ℝ :=
  if a.val = 0 then 1 else -(1 / 2)

private def rootImag (a : Fin 3) : ℝ :=
  if a.val = 0 then 0 else if a.val = 1 then 1 / 2 else -(1 / 2)

private lemma omega_pow_re (a : Fin 3) :
    (omega ^ a.val).re = rootReal a := by
  fin_cases a <;>
    norm_num [omega, rootReal, pow_succ] <;>
    nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]

private lemma omega_pow_im (a : Fin 3) :
    (omega ^ a.val).im = Real.sqrt 3 * rootImag a := by
  fin_cases a <;>
    norm_num [omega, rootImag, pow_succ] <;>
    ring

private lemma clusterPoint_re (a b : Fin 3) :
    (clusterPoint a b).re = rootReal a + (1 / 1000 : ℝ) * rootReal b := by
  norm_num [clusterPoint, epsilon, Complex.mul_re, omega_pow_re]

private lemma clusterPoint_im (a b : Fin 3) :
    (clusterPoint a b).im =
      Real.sqrt 3 * (rootImag a + (1 / 1000 : ℝ) * rootImag b) := by
  norm_num [clusterPoint, epsilon, Complex.mul_im, omega_pow_im]
  ring

private lemma clusterPoint_coordinates (a b : Fin 3) :
    clusterPoint a b =
      (⟨rootReal a + (1 / 1000 : ℝ) * rootReal b,
        Real.sqrt 3 * (rootImag a + (1 / 1000 : ℝ) * rootImag b)⟩ : ℂ) := by
  exact Complex.ext (clusterPoint_re a b) (clusterPoint_im a b)

lemma clusterPoint_injective :
    Function.Injective (fun ab : Fin 3 × Fin 3 => clusterPoint ab.1 ab.2) := by
  intro x y h
  rcases x with ⟨a, b⟩
  rcases y with ⟨c, d⟩
  have hre := congrArg Complex.re h
  have him := congrArg Complex.im h
  rw [clusterPoint_re, clusterPoint_re] at hre
  rw [clusterPoint_im, clusterPoint_im] at him
  have hs : Real.sqrt 3 ≠ 0 := ne_of_gt (by positivity : 0 < Real.sqrt 3)
  have hcoeff : rootImag a + (1 / 1000 : ℝ) * rootImag b =
      rootImag c + (1 / 1000 : ℝ) * rootImag d := mul_left_cancel₀ hs him
  clear h him
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    first | rfl | norm_num [rootReal, rootImag] at *

lemma clusterPoint_ne_zero (a b : Fin 3) : clusterPoint a b ≠ 0 := by
  intro h
  have hr := congrArg Complex.re h
  rw [clusterPoint_re] at hr
  clear h
  fin_cases a <;> fin_cases b <;>
    norm_num [rootReal] at hr

lemma explicitL_card : explicitL.card = 9 := by
  rw [explicitL, Finset.card_image_of_injective _ clusterPoint_injective]
  simp

lemma explicitL_admissible : admissible explicitL 9 := by
  refine ⟨explicitL_card, ?_⟩
  intro z hz
  rcases Finset.mem_image.mp hz with ⟨ab, hab, rfl⟩
  exact clusterPoint_ne_zero ab.1 ab.2

lemma witness_feasible : feasible explicitL 4 witnessPolynomial := by
  constructor
  · unfold witnessPolynomial
    refine (Polynomial.natDegree_sub_le _ _).trans (max_le ?_ ?_)
    · norm_num
    · exact (Polynomial.natDegree_C_mul_X_pow_le _ 3).trans (by norm_num)
  · simp [witnessPolynomial]

/- The nine norm computations are finite, but retain the square-norm form so
   that `norm_num` only has to certify rational identities and
   `(Real.sqrt 3)^2 = 3`. -/
lemma witness_eval_sq_norm (a b : Fin 3) :
    ‖witnessPolynomial.eval (clusterPoint a b)‖ ^ 2 = exactFullMinimum ^ 2 := by
  fin_cases a <;> fin_cases b <;>
    rw [Complex.sq_norm] <;>
    norm_num [witnessPolynomial, clusterPoint_coordinates, rootReal, rootImag,
      epsilon, denominator, exactFullMinimum, Complex.normSq_apply, pow_succ] <;>
    ring_nf <;>
    norm_num [sqrt_three_pow_2, sqrt_three_pow_3, sqrt_three_pow_4,
      sqrt_three_pow_5, sqrt_three_pow_6, sqrt_three_pow_7] <;>
    ring

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
  simp only [Fin.sum_univ_three, witnessWeight, Fin.ext_iff,
    Fin.val_zero, Fin.val_one, Fin.val_two]
  norm_num [witnessWeightDiagonal, witnessWeightOffDiagonal]

/- Weighted orthogonality is checked in the exact field ℂ.  The four moments
   are the only moments needed for an arbitrary degree-four polynomial whose
   constant term vanishes; no floating-point or interval approximation enters
   this identity. -/
/- The algebraic degree has already been reduced to seven. This finite
   four-moment certificate receives a theorem-local heartbeat allowance;
   the remote process wall-clock, memory, and thread limits remain fixed. -/
set_option maxHeartbeats 800000 in
lemma weighted_moment (ell : Fin 4) :
    ∑ a : Fin 3, ∑ b : Fin 3,
      (witnessWeight a b : ℂ) *
          conj (witnessPolynomial.eval (clusterPoint a b)) *
          clusterPoint a b ^ (ell.val + 1) = 0 := by
  fin_cases ell <;>
    simp only [Fin.sum_univ_three, witnessWeight, Fin.ext_iff,
      Fin.val_zero, Fin.val_one, Fin.val_two] <;>
    apply Complex.ext <;>
    norm_num [witnessWeightDiagonal, witnessWeightOffDiagonal,
      witnessPolynomial, clusterPoint_coordinates, rootReal, rootImag,
      epsilon, denominator, Complex.ext_iff, pow_succ] <;>
    ring_nf <;>
    norm_num [sqrt_three_pow_2, sqrt_three_pow_3, sqrt_three_pow_4,
      sqrt_three_pow_5, sqrt_three_pow_6, sqrt_three_pow_7] <;>
    ring

end NLA.IE16
