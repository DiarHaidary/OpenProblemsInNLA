import NLA.RA20.Algebra

/-!
# RA-20: tangent directions for the entire reduced vanishing ideal

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
Original negative-resolution mathematics: the repository's Codex automated
maintainer audit; original conjecture: Kubjas, Sodomaco and Tsigaridas.

The formal differential below is the frozen finite sum of evaluated partial
derivatives. A proved substitution rule and the actual ideal pullback reduce
every vanishing polynomial to a multiple of `abc`, including at singular points.
-/

noncomputable section
open scoped BigOperators
namespace NLA.RA20

def polyDirectional {σ : Type*} [Fintype σ] (x z : σ → ℂ)
    (p : MvPolynomial σ ℂ) : ℂ :=
  ∑ i, MvPolynomial.eval x (MvPolynomial.pderiv i p) * z i

theorem polyDirectional_zero {σ : Type*} [Fintype σ] (x z : σ → ℂ) :
    polyDirectional x z 0 = 0 := by
  simp [polyDirectional]

theorem polyDirectional_C {σ : Type*} [Fintype σ] (x z : σ → ℂ) (r : ℂ) :
    polyDirectional x z (MvPolynomial.C r) = 0 := by
  simp [polyDirectional]

theorem polyDirectional_add {σ : Type*} [Fintype σ] (x z : σ → ℂ)
    (p q : MvPolynomial σ ℂ) :
    polyDirectional x z (p + q) = polyDirectional x z p + polyDirectional x z q := by
  simp [polyDirectional, add_mul, Finset.sum_add_distrib]

theorem polyDirectional_sub {σ : Type*} [Fintype σ] (x z : σ → ℂ)
    (p q : MvPolynomial σ ℂ) :
    polyDirectional x z (p - q) = polyDirectional x z p - polyDirectional x z q := by
  simp [polyDirectional, sub_mul, Finset.sum_sub_distrib]

theorem polyDirectional_mul {σ : Type*} [Fintype σ] (x z : σ → ℂ)
    (p q : MvPolynomial σ ℂ) :
    polyDirectional x z (p * q) =
      polyDirectional x z p * MvPolynomial.eval x q +
        MvPolynomial.eval x p * polyDirectional x z q := by
  simp only [polyDirectional, MvPolynomial.pderiv_mul, map_add, map_mul, add_mul,
    Finset.sum_add_distrib, Finset.sum_mul, Finset.mul_sum]
  congr 1 <;> apply Finset.sum_congr rfl <;> intro i _ <;> ring

theorem polyDirectional_X {σ : Type*} [Fintype σ] (x z : σ → ℂ) (i : σ) :
    polyDirectional x z (MvPolynomial.X i) = z i := by
  classical
  simp [polyDirectional, MvPolynomial.pderiv_X, Pi.single_apply, ite_mul]

theorem polyDirectional_hollowPullback (a b c da db dc : ℂ) (p : Poly 3) :
    polyDirectional ![a, b, c] ![da, db, dc] (hollowPullback p) =
      polyDirectional (coordinates (hollow a b c)) (coordinates (hollow da db dc)) p := by
  induction p using MvPolynomial.induction_on with
  | C r => simp [hollowPullback, polyDirectional_C]
  | add p q hp hq => simp only [map_add, polyDirectional_add, hp, hq]
  | mul_X p ij hp =>
    rw [map_mul, polyDirectional_mul, polyDirectional_mul, hp]
    have he : MvPolynomial.eval ![a, b, c] (hollowPullback p) =
        MvPolynomial.eval (coordinates (hollow a b c)) p :=
      aeval_hollowPullback ![a, b, c] p
    rw [he]
    rcases ij with ⟨i, j⟩
    fin_cases i <;> fin_cases j <;>
      simp [hollowPullback, polynomialHollow, hollow, coordinates,
        polyDirectional_X, polyDirectional_zero]

theorem polyDirectional_abc (a b c da db dc : ℂ) :
    polyDirectional ![a, b, c] ![da, db, dc] abcPolynomial =
      b * c * da + a * c * db + a * b * dc := by
  simp [abcPolynomial, polyDirectional_mul, polyDirectional_X]
  ring

theorem diagonalPolynomial_mem (i : Fin 3) :
    (MvPolynomial.X (i, i) : Poly 3) ∈ definingIdeal 3 3 := by
  rw [definingIdeal_eq_comap_abcIdeal]
  change hollowPullback (MvPolynomial.X (i, i)) ∈ abcIdeal
  fin_cases i <;> simp [hollowPullback, polynomialHollow, hollow]

theorem symmetryPolynomial_mem (i j : Fin 3) :
    (MvPolynomial.X (j, i) - MvPolynomial.X (i, j) : Poly 3) ∈ definingIdeal 3 3 := by
  rw [definingIdeal_eq_comap_abcIdeal]
  change hollowPullback (MvPolynomial.X (j, i) - MvPolynomial.X (i, j)) ∈ abcIdeal
  fin_cases i <;> fin_cases j <;>
    simp [hollowPullback, polynomialHollow, hollow]

theorem genericPolynomial_mem : genericPolynomial ∈ definingIdeal 3 3 := by
  rw [definingIdeal_eq_comap_abcIdeal]
  change hollowPullback genericPolynomial ∈ abcIdeal
  have hm : abcPolynomial ∈ abcIdeal := Ideal.subset_span (by simp)
  simpa only [hollowPullback, genericPolynomial, abcPolynomial, map_mul,
    MvPolynomial.aeval_X] using hm

theorem matrix_eq_hollow_of_symm_diag (Z : Mat 3) (hs : Z.IsSymm)
    (hd : ∀ i : Fin 3, Z i i = 0) :
    Z = hollow (Z 0 1) (Z 0 2) (Z 1 2) := by
  have h01 := hs.apply 0 1
  have h02 := hs.apply 0 2
  have h12 := hs.apply 1 2
  ext i j
  fin_cases i <;> fin_cases j <;> simp [hollow, hd, h01, h02, h12]

theorem algebraic_tangent_space_proved (a b c : ℂ) (h : a * b * c = 0) (Z : Mat 3) :
    TangentVector 3 3 (hollow a b c) Z ↔
      Z.IsSymm ∧ (∀ i : Fin 3, Z i i = 0) ∧
        b * c * Z 0 1 + a * c * Z 0 2 + a * b * Z 1 2 = 0 := by
  constructor
  · intro hZ
    have hz (p : Poly 3) (hp : p ∈ definingIdeal 3 3) :
        polyDirectional (coordinates (hollow a b c)) (coordinates Z) p = 0 := hZ p hp
    refine ⟨?_, ?_, ?_⟩
    · apply Matrix.IsSymm.ext
      intro i j
      have ht := hz _ (symmetryPolynomial_mem i j)
      rw [polyDirectional_sub, polyDirectional_X, polyDirectional_X] at ht
      exact sub_eq_zero.mp ht
    · intro i
      have ht := hz _ (diagonalPolynomial_mem i)
      rwa [polyDirectional_X] at ht
    · have ht := hz genericPolynomial genericPolynomial_mem
      simp [genericPolynomial, polyDirectional_mul, polyDirectional_X,
        coordinates, hollow] at ht
      linear_combination ht
  · rintro ⟨hs, hd, hg⟩ p hp
    have he := matrix_eq_hollow_of_symm_diag Z hs hd
    have hm : hollowPullback p ∈ abcIdeal := by
      rw [definingIdeal_eq_comap_abcIdeal] at hp
      exact hp
    obtain ⟨q, hq⟩ := Ideal.mem_span_singleton.mp hm
    change polyDirectional (coordinates (hollow a b c)) (coordinates Z) p = 0
    rw [he, ← polyDirectional_hollowPullback, hq, polyDirectional_mul,
      polyDirectional_abc]
    simp [hg, abcPolynomial, h]

#assert_trust kernel polyDirectional_hollowPullback
#assert_trust kernel algebraic_tangent_space_proved
#print axioms polyDirectional_hollowPullback
#print axioms algebraic_tangent_space_proved

end NLA.RA20
