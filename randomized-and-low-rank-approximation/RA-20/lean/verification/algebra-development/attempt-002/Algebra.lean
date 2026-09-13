import NLA.RA20.Definitions
import Mathlib.Algebra.MvPolynomial.Division
import Mathlib.Algebra.Squarefree.Basic
import Mathlib.RingTheory.Nilpotent.Lemmas
import Mathlib.RingTheory.Polynomial.UniqueFactorization
import Mathlib.RingTheory.Ideal.Quotient.Operations
import Mathlib.Tactic
import LeanCert.Tactic.Verification

/-!
# RA-20: the actual matrix variety and its reduced coordinate ring

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
The mathematical negative resolution is the repository's Codex automated
maintainer audit. The conjecture is due to Kubjas, Sodomaco and Tsigaridas.

The rank calculation uses explicit width-two factorizations. The coordinate-ring
calculation uses the actual vanishing ideal and the radicality of the squarefree
polynomial `abc`; it does not redefine the variety by its proposed equations.
-/

noncomputable section
open scoped BigOperators
namespace NLA.RA20

theorem hollow_det (a b c : ℂ) : (hollow a b c).det = 2 * a * b * c := by
  simp [Matrix.det_fin_three, hollow]
  ring

theorem hollow_isSymm (a b c : ℂ) : (hollow a b c).IsSymm := by
  apply Matrix.IsSymm.ext
  intro i j
  fin_cases i <;> fin_cases j <;> rfl

theorem hollow_rank_le_two (a b c : ℂ) (h : a * b * c = 0) :
    (hollow a b c).rank ≤ 2 := by
  rcases mul_eq_zero.mp h with hab | hc
  · rcases mul_eq_zero.mp hab with ha | hb
    · subst a
      let L : Matrix (Fin 3) (Fin 2) ℂ := !![b, 0; c, 0; 0, 1]
      let R : Matrix (Fin 2) (Fin 3) ℂ := !![0, 0, 1; b, c, 0]
      have heq : hollow 0 b c = L * R := by
        ext i j
        fin_cases i <;> fin_cases j <;>
          simp [hollow, L, R, Matrix.mul_apply, Fin.sum_univ_succ]
      rw [heq]
      exact (Matrix.rank_mul_le_left L R).trans (Matrix.rank_le_width L)
    · subst b
      let L : Matrix (Fin 3) (Fin 2) ℂ := !![a, 0; 0, 1; c, 0]
      let R : Matrix (Fin 2) (Fin 3) ℂ := !![0, 1, 0; a, 0, c]
      have heq : hollow a 0 c = L * R := by
        ext i j
        fin_cases i <;> fin_cases j <;>
          simp [hollow, L, R, Matrix.mul_apply, Fin.sum_univ_succ]
      rw [heq]
      exact (Matrix.rank_mul_le_left L R).trans (Matrix.rank_le_width L)
  · subst c
    let L : Matrix (Fin 3) (Fin 2) ℂ := !![1, 0; 0, a; 0, b]
    let R : Matrix (Fin 2) (Fin 3) ℂ := !![0, a, b; 1, 0, 0]
    have heq : hollow a b 0 = L * R := by
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [hollow, L, R, Matrix.mul_apply, Fin.sum_univ_succ]
    rw [heq]
    exact (Matrix.rank_mul_le_left L R).trans (Matrix.rank_le_width L)

theorem hollow_mem_variety_iff (a b c : ℂ) :
    hollow a b c ∈ variety 3 3 ↔ a * b * c = 0 := by
  constructor
  · intro h
    by_contra hn
    have hd : (hollow a b c).det ≠ 0 := by
      rw [hollow_det]
      simpa only [mul_assoc] using mul_ne_zero (by norm_num : (2 : ℂ) ≠ 0) hn
    have hr := Matrix.rank_of_det_ne_zero hd
    have hle := h.2.1
    rw [hr] at hle
    norm_num at hle
  · intro h
    refine ⟨hollow_isSymm a b c, hollow_rank_le_two a b c h, ?_⟩
    intro i _
    fin_cases i <;> rfl

theorem matrix_eq_hollow_of_mem {X : Mat 3} (h : X ∈ variety 3 3) :
    X = hollow (X 0 1) (X 0 2) (X 1 2) := by
  have hd : ∀ i : Fin 3, X i i = 0 := fun i => h.2.2 i i.isLt
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [hollow, hd, h.1.apply]

theorem hollow_variety_semantics_proved :
    (∀ a b c : ℂ, (hollow a b c).det = 2 * a * b * c ∧
      (hollow a b c ∈ variety 3 3 ↔ a * b * c = 0)) ∧
    (∀ X : Mat 3, X ∈ variety 3 3 ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧ X 0 1 * X 0 2 * X 1 2 = 0) := by
  refine ⟨fun a b c => ⟨hollow_det a b c, hollow_mem_variety_iff a b c⟩, ?_⟩
  intro X
  constructor
  · intro h
    have he := matrix_eq_hollow_of_mem h
    exact ⟨he, (hollow_mem_variety_iff _ _ _).mp (he ▸ h)⟩
  · rintro ⟨he, hz⟩
    rw [he]
    exact (hollow_mem_variety_iff _ _ _).mpr hz

#assert_trust kernel hollow_variety_semantics_proved
#print axioms hollow_variety_semantics_proved

end NLA.RA20
