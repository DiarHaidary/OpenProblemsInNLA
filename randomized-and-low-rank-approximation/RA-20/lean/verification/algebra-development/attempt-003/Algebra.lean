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
  have h01 := h.1.apply 0 1
  have h02 := h.1.apply 0 2
  have h12 := h.1.apply 1 2
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [hollow, hd, h01, h02, h12]

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

def hollowPullback : Poly 3 →ₐ[ℂ] ABCPoly :=
  MvPolynomial.aeval (fun ij => polynomialHollow ij.1 ij.2)

def offDiagonalPullback : ABCPoly →ₐ[ℂ] Poly 3 :=
  MvPolynomial.aeval ![MvPolynomial.X (0, 1), MvPolynomial.X (0, 2),
    MvPolynomial.X (1, 2)]

theorem hollowPullback_offDiagonalPullback :
    hollowPullback.comp offDiagonalPullback = AlgHom.id ℂ ABCPoly := by
  ext i
  fin_cases i <;> simp [hollowPullback, offDiagonalPullback, polynomialHollow, hollow]

theorem hollowPullback_surjective : Function.Surjective hollowPullback := by
  intro p
  refine ⟨offDiagonalPullback p, ?_⟩
  exact DFunLike.congr_fun hollowPullback_offDiagonalPullback p

theorem abcPolynomial_squarefree : Squarefree abcPolynomial := by
  have hp (i : Fin 3) : Prime (MvPolynomial.X i : ABCPoly) := MvPolynomial.X_prime
  have hrel (i j : Fin 3) (hij : i ≠ j) :
      IsRelPrime (MvPolynomial.X i : ABCPoly) (MvPolynomial.X j) := by
    apply (hp i).irreducible.isRelPrime_iff_not_dvd.mpr
    simpa using hij
  exact squarefree_mul_iff.mpr
    ⟨(hrel 0 2 (by decide)).mul_left (hrel 1 2 (by decide)),
      squarefree_mul_iff.mpr
        ⟨hrel 0 1 (by decide), (hp 0).irreducible.squarefree, (hp 1).irreducible.squarefree⟩,
      (hp 2).irreducible.squarefree⟩

theorem abcIdeal_isRadical : abcIdeal.IsRadical :=
  isRadical_iff_span_singleton.mp abcPolynomial_squarefree.isRadical

theorem abcIdeal_zeroLocus :
    MvPolynomial.zeroLocus ℂ abcIdeal =
      {x : Fin 3 → ℂ | x 0 * x 1 * x 2 = 0} := by
  simp [abcIdeal, MvPolynomial.zeroLocus_span, abcPolynomial]

theorem abcIdeal_vanishing :
    MvPolynomial.vanishingIdeal ℂ {x : Fin 3 → ℂ | x 0 * x 1 * x 2 = 0} =
      abcIdeal := by
  rw [← abcIdeal_zeroLocus, MvPolynomial.vanishingIdeal_zeroLocus_eq_radical]
  exact abcIdeal_isRadical.radical

theorem aeval_hollowPullback (x : Fin 3 → ℂ) (p : Poly 3) :
    MvPolynomial.aeval x (hollowPullback p) =
      MvPolynomial.aeval (coordinates (hollow (x 0) (x 1) (x 2))) p := by
  rw [hollowPullback, MvPolynomial.comp_aeval_apply]
  congr 2
  funext ij
  rcases ij with ⟨i, j⟩
  fin_cases i <;> fin_cases j <;> simp [polynomialHollow, hollow, coordinates]

theorem definingIdeal_eq_comap_abcIdeal :
    definingIdeal 3 3 = Ideal.comap hollowPullback.toRingHom abcIdeal := by
  ext p
  rw [Ideal.mem_comap, ← abcIdeal_vanishing]
  change (∀ x ∈ coordinateVariety 3 3, MvPolynomial.aeval x p = 0) ↔
    ∀ x : Fin 3 → ℂ, x 0 * x 1 * x 2 = 0 →
      MvPolynomial.aeval x (hollowPullback p) = 0
  constructor
  · intro hp x hx
    rw [aeval_hollowPullback]
    apply hp
    exact (hollow_mem_variety_iff _ _ _).mpr hx
  · intro hp x hx
    have h := matrix_eq_hollow_of_mem hx
    have hz := (hollow_variety_semantics_proved.2 (matrixOfCoordinates x)).mp hx
    have he : coordinates (hollow (x (0, 1)) (x (0, 2)) (x (1, 2))) = x := by
      have he' := congrArg coordinates h
      exact he'.symm
    have hv := hp ![x (0, 1), x (0, 2), x (1, 2)] hz.2
    rw [aeval_hollowPullback] at hv
    simpa only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, he] using hv

def hollowQuotientMap : Poly 3 →ₐ[ℂ] ABCCoordinateRing :=
  (Ideal.Quotient.mkₐ ℂ abcIdeal).comp hollowPullback

theorem hollowQuotientMap_surjective : Function.Surjective hollowQuotientMap :=
  (Ideal.Quotient.mkₐ_surjective ℂ abcIdeal).comp hollowPullback_surjective

theorem hollowQuotientMap_ker :
    RingHom.ker hollowQuotientMap = definingIdeal 3 3 := by
  rw [definingIdeal_eq_comap_abcIdeal]
  ext p
  simp [hollowQuotientMap, RingHom.mem_ker]

def reducedCoordinateEquiv : CoordinateRing 3 3 ≃ₐ[ℂ] ABCCoordinateRing :=
  (Ideal.quotientEquivAlgOfEq ℂ hollowQuotientMap_ker.symm).trans
    (Ideal.quotientKerAlgEquivOfSurjective hollowQuotientMap_surjective)

theorem reducedCoordinateEquiv_mk_X (i j : Fin 3) :
    reducedCoordinateEquiv
        (Ideal.Quotient.mk (definingIdeal 3 3) (MvPolynomial.X (i, j))) =
      Ideal.Quotient.mk abcIdeal (polynomialHollow i j) := by
  simp [reducedCoordinateEquiv, hollowQuotientMap, hollowPullback]

theorem reduced_coordinate_ring_proved :
    ∃ e : CoordinateRing 3 3 ≃ₐ[ℂ] ABCCoordinateRing,
      ∀ i j : Fin 3,
        e (Ideal.Quotient.mk (definingIdeal 3 3) (MvPolynomial.X (i, j))) =
          Ideal.Quotient.mk abcIdeal (polynomialHollow i j) :=
  ⟨reducedCoordinateEquiv, reducedCoordinateEquiv_mk_X⟩

#assert_trust kernel hollow_rank_le_two
#assert_trust kernel abcPolynomial_squarefree
#assert_trust kernel abcIdeal_vanishing
#assert_trust kernel definingIdeal_eq_comap_abcIdeal
#assert_trust kernel reduced_coordinate_ring_proved
#print axioms reduced_coordinate_ring_proved

end NLA.RA20
