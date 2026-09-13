import NLA.IS02.Definitions
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Eigenspace.Charpoly
import Mathlib.LinearAlgebra.Charpoly.ToMatrix
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
noncomputable section
open scoped BigOperators Matrix
namespace NLA.IS02
open Polynomial


open Polynomial

set_option maxHeartbeats 800000 in
theorem test_membership :
    counterexample ∈ symmetricStochastic 4 := by
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> rfl
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> norm_num [counterexample]
  · intro i
    fin_cases i <;> norm_num [counterexample, Fin.sum_univ_succ]

theorem test_trace : trace counterexample = 1 := by
  norm_num [trace, counterexample, Fin.sum_univ_succ]

theorem test_positive_trace : 0 < trace counterexample := by
  rw [test_trace]
  norm_num

theorem test_spectrum :
    sameSpectrum counterexample
      (!![(1 : ℝ), 0, 0, 0;
          0, 1, 0, 0;
          0, 0, 0, 0;
          0, 0, 0, (-1 : ℝ)]) := by
  unfold sameSpectrum
  have hc : counterexample.charmatrix =
      !![X, -1, 0, 0;
         -1, X, 0, 0;
         0, 0, X - C (1 / 2 : ℝ), -C (1 / 2 : ℝ);
         0, 0, -C (1 / 2 : ℝ), X - C (1 / 2 : ℝ)] := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [counterexample, Matrix.charmatrix_apply]
  have hd :
      (!![(1 : ℝ), 0, 0, 0;
          0, 1, 0, 0;
          0, 0, 0, 0;
          0, 0, 0, (-1 : ℝ)] : Mat 4) =
        Matrix.diagonal (![1, 1, 0, -1] : Fin 4 → ℝ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal]
  have hcHalf : (C (1 / 2 : ℝ) : ℝ[X]) * 2 = 1 := by
    rw [← C_ofNat, ← C_1, ← C_mul]
    norm_num
  rw [Matrix.charpoly, hc, Matrix.det_succ_row_zero, Fin.sum_univ_four]
  norm_num [Matrix.det_fin_three, Matrix.submatrix_apply, Fin.succAbove,
    Matrix.cons_val_two, Matrix.cons_val_three, Fin.reduceSucc,
    Fin.reduceCastSucc, Fin.ext_iff]
  norm_num
  ring_nf
  rw [hd, Matrix.charpoly_diagonal]
  norm_num [Fin.prod_univ_succ]
  rw [show C (1 / 2 : ℝ) * X * 2 = X * (C (1 / 2 : ℝ) * 2) by ring]
  rw [show C (1 / 2 : ℝ) * X ^ 3 * 2 = X ^ 3 * (C (1 / 2 : ℝ) * 2) by ring]
  rw [hcHalf]
  ring


open Polynomial

lemma custom_to_hermitian {n : ℕ} {A : Mat n} (hA : symmetric A) : Matrix.IsHermitian A := by
  apply Matrix.isHermitian_iff_isSymm.mpr
  apply Matrix.IsSymm.ext
  intro i j
  exact (hA i j).symm

theorem test_spectrum_bridge {n : ℕ} {A B : Mat n} (hA : symmetric A) (hB : symmetric B) :
    sameSpectrum A B ↔ realEigenvalueMultiset A = realEigenvalueMultiset B := by
  have hAh : Matrix.IsHermitian A := custom_to_hermitian hA
  have hBh : Matrix.IsHermitian B := custom_to_hermitian hB
  constructor
  · intro h
    exact congrArg Polynomial.roots h
  · intro h
    unfold realEigenvalueMultiset at h
    unfold sameSpectrum
    rw [hAh.splits_charpoly.eq_prod_roots_of_monic (Matrix.charpoly_monic A),
      hBh.splits_charpoly.eq_prod_roots_of_monic (Matrix.charpoly_monic B), h]

theorem test_trace_from_spectrum {B : Mat 4} (hspec : sameSpectrum counterexample B) : trace B = 1 := by
  have hnext : (Matrix.charpoly B).nextCoeff =
      (Matrix.charpoly counterexample).nextCoeff := by
    rw [hspec]
  calc
    trace B = -(Matrix.charpoly B).nextCoeff := Matrix.trace_eq_neg_charpoly_nextCoeff B
    _ = -(Matrix.charpoly counterexample).nextCoeff := by rw [hnext]
    _ = trace counterexample := (Matrix.trace_eq_neg_charpoly_nextCoeff counterexample).symm
    _ = 1 := test_trace

set_option maxHeartbeats 800000 in
theorem test_minus_one_root :
    IsRoot (Matrix.charpoly counterexample) (-1 : ℝ) := by
  have hd :
      (!![(1 : ℝ), 0, 0, 0;
          0, 1, 0, 0;
          0, 0, 0, 0;
          0, 0, 0, (-1 : ℝ)] : Mat 4) =
        Matrix.diagonal (![1, 1, 0, -1] : Fin 4 → ℝ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal]
  rw [test_spectrum]
  rw [hd, Matrix.charpoly_diagonal]
  norm_num [Fin.prod_univ_succ]

set_option maxHeartbeats 800000 in
theorem test_minus_one_eigenvector {B : Mat 4}
    (hspec : sameSpectrum counterexample B) :
    ∃ z : Fin 4 → ℝ, z ≠ 0 ∧ B *ᵥ z = -z := by
  have hroot : IsRoot (Matrix.charpoly B) (-1 : ℝ) := by
    rw [← hspec]
    exact test_minus_one_root
  have heval : Module.End.HasEigenvalue (Matrix.toLin' B) (-1 : ℝ) :=
    (Module.End.hasEigenvalue_iff_isRoot_charpoly (Matrix.toLin' B) (-1 : ℝ)).2 (by
      simpa only [Matrix.charpoly_toLin'] using hroot)
  obtain ⟨z, hz⟩ := Module.End.HasEigenvalue.exists_hasEigenvector heval
  refine ⟨z, ?_, ?_⟩
  · exact (Module.End.hasEigenvector_iff.mp hz).2
  · have h := hz.apply_eq_smul
    simpa only [Matrix.toLin'_apply, smul_eq_mul, mul_one, neg_mul, one_mul, neg_one_smul] using h

set_option maxHeartbeats 800000 in
theorem test_quad_zero {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hz : B *ᵥ z = -z) :
    ∀ i j, B i j * (z i + z j)^2 = 0 := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hcol : ∀ j, (∑ i : Fin 4, B i j) = 1 := by
    intro j
    calc
      (∑ i : Fin 4, B i j) = ∑ i : Fin 4, B j i := by
        apply Finset.sum_congr rfl
        intro i hi
        exact hsym i j
      _ = 1 := hstoch j
  have heig : ∀ i, (∑ j : Fin 4, B i j * z j) = - z i := by
    intro i
    have hi := congrFun hz i
    simpa [Matrix.mulVec, dotProduct] using hi
  have hfirst : (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z i)^2) =
      ∑ i : Fin 4, (z i)^2 := by
    apply Finset.sum_congr rfl
    intro i hi
    rw [← Finset.sum_mul]
    rw [hstoch i]
    ring
  have hmiddle : (∑ i : Fin 4, ∑ j : Fin 4, B i j * (2 * z i * z j)) =
      -2 * (∑ i : Fin 4, (z i)^2) := by
    calc
      (∑ i : Fin 4, ∑ j : Fin 4, B i j * (2 * z i * z j)) =
          ∑ i : Fin 4, 2 * z i * (∑ j : Fin 4, B i j * z j) := by
            apply Finset.sum_congr rfl
            intro i hi
            calc
              (∑ j : Fin 4, B i j * (2 * z i * z j)) =
                  ∑ j : Fin 4, (2 * z i) * (B i j * z j) := by
                    apply Finset.sum_congr rfl
                    intro j hj
                    ring
              _ = 2 * z i * (∑ j : Fin 4, B i j * z j) := by
                    rw [Finset.mul_sum]
      _ = ∑ i : Fin 4, 2 * z i * (-z i) := by
            apply Finset.sum_congr rfl
            intro i hi
            rw [heig i]
      _ = -2 * (∑ i : Fin 4, (z i)^2) := by
            calc
              (∑ i : Fin 4, 2 * z i * (-z i)) =
                  ∑ i : Fin 4, (-2) * (z i)^2 := by
                    apply Finset.sum_congr rfl
                    intro i hi
                    ring
              _ = -2 * (∑ i : Fin 4, (z i)^2) := by
                    rw [Finset.mul_sum]
  have hthird : (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z j)^2) =
      ∑ j : Fin 4, (z j)^2 := by
    calc
      (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z j)^2) =
          ∑ j : Fin 4, ∑ i : Fin 4, B i j * (z j)^2 := by
            rw [Finset.sum_comm]
      _ = ∑ j : Fin 4, (∑ i : Fin 4, B i j) * (z j)^2 := by
            apply Finset.sum_congr rfl
            intro j hj
            rw [Finset.sum_mul]
      _ = ∑ j : Fin 4, (z j)^2 := by
            apply Finset.sum_congr rfl
            intro j hj
            rw [hcol j]
            ring
  have hsum : (∑ i : Fin 4, ∑ j : Fin 4,
      B i j * (z i + z j)^2) = 0 := by
    calc
      (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z i + z j)^2) =
          (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z i)^2) +
          (∑ i : Fin 4, ∑ j : Fin 4, B i j * (2 * z i * z j)) +
          (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z j)^2) := by
            have hpoint : ∀ i : Fin 4,
                (∑ j : Fin 4, B i j * (z i + z j)^2) =
                  (∑ j : Fin 4, B i j * (z i)^2) +
                  (∑ j : Fin 4, B i j * (2 * z i * z j)) +
                  (∑ j : Fin 4, B i j * (z j)^2) := by
              intro i
              rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
              apply Finset.sum_congr rfl
              intro j hj
              ring
            rw [show (∑ i : Fin 4, ∑ j : Fin 4, B i j * (z i + z j)^2) =
                ∑ i : Fin 4, ((∑ j : Fin 4, B i j * (z i)^2) +
                  (∑ j : Fin 4, B i j * (2 * z i * z j)) +
                  (∑ j : Fin 4, B i j * (z j)^2)) by
                    apply Finset.sum_congr rfl
                    intro i hi
                    exact hpoint i]
            rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      _ = 0 := by rw [hfirst, hmiddle, hthird]; ring
  intro i j
  have hnonterm : 0 ≤ B i j * (z i + z j)^2 :=
    mul_nonneg (hnon i j) (sq_nonneg _)
  have hle : B i j * (z i + z j)^2 ≤
      ∑ k : Fin 4, ∑ l : Fin 4, B k l * (z k + z l)^2 := by
    calc
      B i j * (z i + z j)^2 ≤ ∑ l : Fin 4, B i l * (z i + z l)^2 := by
        refine Finset.single_le_sum (s := (Finset.univ : Finset (Fin 4))) (f := fun l : Fin 4 => B i l * (z i + z l)^2) ?_ ?_
        · intro l hl
          exact mul_nonneg (hnon i l) (sq_nonneg _)
        · exact Finset.mem_univ j
      _ ≤ ∑ k : Fin 4, ∑ l : Fin 4, B k l * (z k + z l)^2 := by
        refine Finset.single_le_sum (s := (Finset.univ : Finset (Fin 4)))
          (f := fun k : Fin 4 => ∑ l : Fin 4, B k l * (z k + z l)^2) ?_ ?_
        · intro k hk
          exact Finset.sum_nonneg (fun l hl => mul_nonneg (hnon k l) (sq_nonneg _))
        · exact Finset.mem_univ i
  nlinarith [hsum]

set_option maxHeartbeats 800000 in
theorem test_pair01 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (htrace : trace B = 1)
    (hza : z 0 ≠ 0) (hzb : z 1 ≠ 0)
    (hzc : z 2 = 0) (hzd : z 3 = 0) :
    B = permute ((1 : Equiv.Perm (Fin 4))) counterexample := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have haa : B 0 0 = 0 := hdiag 0 hza
  have hbb : B 1 1 = 0 := hdiag 1 hzb
  have ha2 : B 0 2 = 0 := hedge 0 2 hza hzc
  have hb2 : B 1 2 = 0 := hedge 1 2 hzb hzc
  have h2a : B 2 0 = 0 := by rw [hsym 2 0, ha2]
  have h2b : B 2 1 = 0 := by rw [hsym 2 1, hb2]
  have ha3 : B 0 3 = 0 := hedge 0 3 hza hzd
  have hb3 : B 1 3 = 0 := hedge 1 3 hzb hzd
  have h3a : B 3 0 = 0 := by rw [hsym 3 0, ha3]
  have h3b : B 3 1 = 0 := by rw [hsym 3 1, hb3]
  have hab : B 0 1 = 1 := by
    have sa := hstoch 0
    norm_num [Fin.sum_univ_succ] at sa
    change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sa
    rw [haa, ha2, ha3] at sa
    linarith [sa]
  have hba : B 1 0 = 1 := by rw [hsym 1 0, hab]
  have sc := hstoch 2
  norm_num [Fin.sum_univ_succ] at sc
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at sc
  rw [h2a, h2b] at sc
  have hcsum : B 2 2 + B 2 3 = 1 := by linarith [sc]
  have sd := hstoch 3
  norm_num [Fin.sum_univ_succ] at sd
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at sd
  rw [h3a, h3b] at sd
  have hdsum : B 3 2 + B 3 3 = 1 := by linarith [sd]
  have hdc : B 3 2 = B 2 3 := hsym 3 2
  have htrsum : B 2 2 + B 3 3 = 1 := by
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [haa, hbb] at ht
    linarith [ht]
  have hcc' : B 2 2 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdd' : B 3 3 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hcd' : B 2 3 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdc' : B 3 2 = (1 / 2 : ℝ) := by rw [hdc, hcd']
  have hr0 : ((1 : Equiv.Perm (Fin 4)) : Equiv.Perm (Fin 4)) 0 = 0 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr1 : ((1 : Equiv.Perm (Fin 4)) : Equiv.Perm (Fin 4)) 1 = 1 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr2 : ((1 : Equiv.Perm (Fin 4)) : Equiv.Perm (Fin 4)) 2 = 2 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr3 : ((1 : Equiv.Perm (Fin 4)) : Equiv.Perm (Fin 4)) 3 = 3 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  ext i j
  fin_cases i <;> fin_cases j <;>
    unfold permute <;>
    simp [hr0, hr1, hr2, hr3, counterexample, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
      haa, hbb, hcc', hdd', ha2, ha3, hb2, hb3, h2a, h3a, h2b, h3b, hab, hba, hcd', hdc']
set_option maxHeartbeats 800000 in
theorem test_pair02 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (htrace : trace B = 1)
    (hza : z 0 ≠ 0) (hzb : z 2 ≠ 0)
    (hzc : z 1 = 0) (hzd : z 3 = 0) :
    B = permute (Equiv.swap 1 2) counterexample := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have haa : B 0 0 = 0 := hdiag 0 hza
  have hbb : B 2 2 = 0 := hdiag 2 hzb
  have ha1 : B 0 1 = 0 := hedge 0 1 hza hzc
  have hb1 : B 2 1 = 0 := hedge 2 1 hzb hzc
  have h1a : B 1 0 = 0 := by rw [hsym 1 0, ha1]
  have h1b : B 1 2 = 0 := by rw [hsym 1 2, hb1]
  have ha3 : B 0 3 = 0 := hedge 0 3 hza hzd
  have hb3 : B 2 3 = 0 := hedge 2 3 hzb hzd
  have h3a : B 3 0 = 0 := by rw [hsym 3 0, ha3]
  have h3b : B 3 2 = 0 := by rw [hsym 3 2, hb3]
  have hab : B 0 2 = 1 := by
    have sa := hstoch 0
    norm_num [Fin.sum_univ_succ] at sa
    change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sa
    rw [haa, ha1, ha3] at sa
    linarith [sa]
  have hba : B 2 0 = 1 := by rw [hsym 2 0, hab]
  have sc := hstoch 1
  norm_num [Fin.sum_univ_succ] at sc
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at sc
  rw [h1a, h1b] at sc
  have hcsum : B 1 1 + B 1 3 = 1 := by linarith [sc]
  have sd := hstoch 3
  norm_num [Fin.sum_univ_succ] at sd
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at sd
  rw [h3a, h3b] at sd
  have hdsum : B 3 1 + B 3 3 = 1 := by linarith [sd]
  have hdc : B 3 1 = B 1 3 := hsym 3 1
  have htrsum : B 1 1 + B 3 3 = 1 := by
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [haa, hbb] at ht
    linarith [ht]
  have hcc' : B 1 1 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdd' : B 3 3 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hcd' : B 1 3 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdc' : B 3 1 = (1 / 2 : ℝ) := by rw [hdc, hcd']
  have hr0 : (Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 0 = 0 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr1 : (Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 1 = 2 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr2 : (Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 2 = 1 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr3 : (Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 3 = 3 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  ext i j
  fin_cases i <;> fin_cases j <;>
    unfold permute <;>
    simp [hr0, hr1, hr2, hr3, counterexample, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
      haa, hbb, hcc', hdd', ha1, ha3, hb1, hb3, h1a, h3a, h1b, h3b, hab, hba, hcd', hdc']
set_option maxHeartbeats 800000 in
theorem test_pair03 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (htrace : trace B = 1)
    (hza : z 0 ≠ 0) (hzb : z 3 ≠ 0)
    (hzc : z 1 = 0) (hzd : z 2 = 0) :
    B = permute (Equiv.swap 1 3 * Equiv.swap 1 2) counterexample := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have haa : B 0 0 = 0 := hdiag 0 hza
  have hbb : B 3 3 = 0 := hdiag 3 hzb
  have ha1 : B 0 1 = 0 := hedge 0 1 hza hzc
  have hb1 : B 3 1 = 0 := hedge 3 1 hzb hzc
  have h1a : B 1 0 = 0 := by rw [hsym 1 0, ha1]
  have h1b : B 1 3 = 0 := by rw [hsym 1 3, hb1]
  have ha2 : B 0 2 = 0 := hedge 0 2 hza hzd
  have hb2 : B 3 2 = 0 := hedge 3 2 hzb hzd
  have h2a : B 2 0 = 0 := by rw [hsym 2 0, ha2]
  have h2b : B 2 3 = 0 := by rw [hsym 2 3, hb2]
  have hab : B 0 3 = 1 := by
    have sa := hstoch 0
    norm_num [Fin.sum_univ_succ] at sa
    change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sa
    rw [haa, ha1, ha2] at sa
    linarith [sa]
  have hba : B 3 0 = 1 := by rw [hsym 3 0, hab]
  have sc := hstoch 1
  norm_num [Fin.sum_univ_succ] at sc
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at sc
  rw [h1a, h1b] at sc
  have hcsum : B 1 1 + B 1 2 = 1 := by linarith [sc]
  have sd := hstoch 2
  norm_num [Fin.sum_univ_succ] at sd
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at sd
  rw [h2a, h2b] at sd
  have hdsum : B 2 1 + B 2 2 = 1 := by linarith [sd]
  have hdc : B 2 1 = B 1 2 := hsym 2 1
  have htrsum : B 1 1 + B 2 2 = 1 := by
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [haa, hbb] at ht
    linarith [ht]
  have hcc' : B 1 1 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdd' : B 2 2 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hcd' : B 1 2 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdc' : B 2 1 = (1 / 2 : ℝ) := by rw [hdc, hcd']
  have hr0 : (Equiv.swap 1 3 * Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 0 = 0 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr1 : (Equiv.swap 1 3 * Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 1 = 2 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr2 : (Equiv.swap 1 3 * Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 2 = 3 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr3 : (Equiv.swap 1 3 * Equiv.swap 1 2 : Equiv.Perm (Fin 4)) 3 = 1 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  ext i j
  fin_cases i <;> fin_cases j <;>
    unfold permute <;>
    simp [hr0, hr1, hr2, hr3, counterexample, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
      haa, hbb, hcc', hdd', ha1, ha2, hb1, hb2, h1a, h2a, h1b, h2b, hab, hba, hcd', hdc']
set_option maxHeartbeats 800000 in
theorem test_pair12 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (htrace : trace B = 1)
    (hza : z 1 ≠ 0) (hzb : z 2 ≠ 0)
    (hzc : z 0 = 0) (hzd : z 3 = 0) :
    B = permute (Equiv.swap 1 2 * Equiv.swap 0 1) counterexample := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have haa : B 1 1 = 0 := hdiag 1 hza
  have hbb : B 2 2 = 0 := hdiag 2 hzb
  have ha0 : B 1 0 = 0 := hedge 1 0 hza hzc
  have hb0 : B 2 0 = 0 := hedge 2 0 hzb hzc
  have h0a : B 0 1 = 0 := by rw [hsym 0 1, ha0]
  have h0b : B 0 2 = 0 := by rw [hsym 0 2, hb0]
  have ha3 : B 1 3 = 0 := hedge 1 3 hza hzd
  have hb3 : B 2 3 = 0 := hedge 2 3 hzb hzd
  have h3a : B 3 1 = 0 := by rw [hsym 3 1, ha3]
  have h3b : B 3 2 = 0 := by rw [hsym 3 2, hb3]
  have hab : B 1 2 = 1 := by
    have sa := hstoch 1
    norm_num [Fin.sum_univ_succ] at sa
    change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at sa
    rw [haa, ha0, ha3] at sa
    linarith [sa]
  have hba : B 2 1 = 1 := by rw [hsym 2 1, hab]
  have sc := hstoch 0
  norm_num [Fin.sum_univ_succ] at sc
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sc
  rw [h0a, h0b] at sc
  have hcsum : B 0 0 + B 0 3 = 1 := by linarith [sc]
  have sd := hstoch 3
  norm_num [Fin.sum_univ_succ] at sd
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at sd
  rw [h3a, h3b] at sd
  have hdsum : B 3 0 + B 3 3 = 1 := by linarith [sd]
  have hdc : B 3 0 = B 0 3 := hsym 3 0
  have htrsum : B 0 0 + B 3 3 = 1 := by
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [haa, hbb] at ht
    linarith [ht]
  have hcc' : B 0 0 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdd' : B 3 3 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hcd' : B 0 3 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdc' : B 3 0 = (1 / 2 : ℝ) := by rw [hdc, hcd']
  have hr0 : (Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 0 = 2 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr1 : (Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 1 = 0 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr2 : (Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 2 = 1 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr3 : (Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 3 = 3 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  ext i j
  fin_cases i <;> fin_cases j <;>
    unfold permute <;>
    simp [hr0, hr1, hr2, hr3, counterexample, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
      haa, hbb, hcc', hdd', ha0, ha3, hb0, hb3, h0a, h3a, h0b, h3b, hab, hba, hcd', hdc']
set_option maxHeartbeats 800000 in
theorem test_pair13 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (htrace : trace B = 1)
    (hza : z 1 ≠ 0) (hzb : z 3 ≠ 0)
    (hzc : z 0 = 0) (hzd : z 2 = 0) :
    B = permute (Equiv.swap 1 3 * Equiv.swap 1 2 * Equiv.swap 0 1) counterexample := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have haa : B 1 1 = 0 := hdiag 1 hza
  have hbb : B 3 3 = 0 := hdiag 3 hzb
  have ha0 : B 1 0 = 0 := hedge 1 0 hza hzc
  have hb0 : B 3 0 = 0 := hedge 3 0 hzb hzc
  have h0a : B 0 1 = 0 := by rw [hsym 0 1, ha0]
  have h0b : B 0 3 = 0 := by rw [hsym 0 3, hb0]
  have ha2 : B 1 2 = 0 := hedge 1 2 hza hzd
  have hb2 : B 3 2 = 0 := hedge 3 2 hzb hzd
  have h2a : B 2 1 = 0 := by rw [hsym 2 1, ha2]
  have h2b : B 2 3 = 0 := by rw [hsym 2 3, hb2]
  have hab : B 1 3 = 1 := by
    have sa := hstoch 1
    norm_num [Fin.sum_univ_succ] at sa
    change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at sa
    rw [haa, ha0, ha2] at sa
    linarith [sa]
  have hba : B 3 1 = 1 := by rw [hsym 3 1, hab]
  have sc := hstoch 0
  norm_num [Fin.sum_univ_succ] at sc
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sc
  rw [h0a, h0b] at sc
  have hcsum : B 0 0 + B 0 2 = 1 := by linarith [sc]
  have sd := hstoch 2
  norm_num [Fin.sum_univ_succ] at sd
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at sd
  rw [h2a, h2b] at sd
  have hdsum : B 2 0 + B 2 2 = 1 := by linarith [sd]
  have hdc : B 2 0 = B 0 2 := hsym 2 0
  have htrsum : B 0 0 + B 2 2 = 1 := by
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [haa, hbb] at ht
    linarith [ht]
  have hcc' : B 0 0 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdd' : B 2 2 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hcd' : B 0 2 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdc' : B 2 0 = (1 / 2 : ℝ) := by rw [hdc, hcd']
  have hr0 : (Equiv.swap 1 3 * Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 0 = 2 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr1 : (Equiv.swap 1 3 * Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 1 = 0 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr2 : (Equiv.swap 1 3 * Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 2 = 3 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr3 : (Equiv.swap 1 3 * Equiv.swap 1 2 * Equiv.swap 0 1 : Equiv.Perm (Fin 4)) 3 = 1 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  ext i j
  fin_cases i <;> fin_cases j <;>
    unfold permute <;>
    simp [hr0, hr1, hr2, hr3, counterexample, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
      haa, hbb, hcc', hdd', ha0, ha2, hb0, hb2, h0a, h2a, h0b, h2b, hab, hba, hcd', hdc']
set_option maxHeartbeats 800000 in
theorem test_pair23 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (htrace : trace B = 1)
    (hza : z 2 ≠ 0) (hzb : z 3 ≠ 0)
    (hzc : z 0 = 0) (hzd : z 1 = 0) :
    B = permute (Equiv.swap 1 3 * Equiv.swap 0 2) counterexample := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have haa : B 2 2 = 0 := hdiag 2 hza
  have hbb : B 3 3 = 0 := hdiag 3 hzb
  have ha0 : B 2 0 = 0 := hedge 2 0 hza hzc
  have hb0 : B 3 0 = 0 := hedge 3 0 hzb hzc
  have h0a : B 0 2 = 0 := by rw [hsym 0 2, ha0]
  have h0b : B 0 3 = 0 := by rw [hsym 0 3, hb0]
  have ha1 : B 2 1 = 0 := hedge 2 1 hza hzd
  have hb1 : B 3 1 = 0 := hedge 3 1 hzb hzd
  have h1a : B 1 2 = 0 := by rw [hsym 1 2, ha1]
  have h1b : B 1 3 = 0 := by rw [hsym 1 3, hb1]
  have hab : B 2 3 = 1 := by
    have sa := hstoch 2
    norm_num [Fin.sum_univ_succ] at sa
    change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at sa
    rw [haa, ha0, ha1] at sa
    linarith [sa]
  have hba : B 3 2 = 1 := by rw [hsym 3 2, hab]
  have sc := hstoch 0
  norm_num [Fin.sum_univ_succ] at sc
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sc
  rw [h0a, h0b] at sc
  have hcsum : B 0 0 + B 0 1 = 1 := by linarith [sc]
  have sd := hstoch 1
  norm_num [Fin.sum_univ_succ] at sd
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at sd
  rw [h1a, h1b] at sd
  have hdsum : B 1 0 + B 1 1 = 1 := by linarith [sd]
  have hdc : B 1 0 = B 0 1 := hsym 1 0
  have htrsum : B 0 0 + B 1 1 = 1 := by
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [haa, hbb] at ht
    linarith [ht]
  have hcc' : B 0 0 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdd' : B 1 1 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hcd' : B 0 1 = (1 / 2 : ℝ) := by linarith [hcsum, hdsum, hdc, htrsum]
  have hdc' : B 1 0 = (1 / 2 : ℝ) := by rw [hdc, hcd']
  have hr0 : (Equiv.swap 1 3 * Equiv.swap 0 2 : Equiv.Perm (Fin 4)) 0 = 2 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr1 : (Equiv.swap 1 3 * Equiv.swap 0 2 : Equiv.Perm (Fin 4)) 1 = 3 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr2 : (Equiv.swap 1 3 * Equiv.swap 0 2 : Equiv.Perm (Fin 4)) 2 = 0 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  have hr3 : (Equiv.swap 1 3 * Equiv.swap 0 2 : Equiv.Perm (Fin 4)) 3 = 1 := by
    simp [Equiv.Perm.mul_apply, Equiv.swap_apply_def]
  ext i j
  fin_cases i <;> fin_cases j <;>
    unfold permute <;>
    simp [hr0, hr1, hr2, hr3, counterexample, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
      haa, hbb, hcc', hdd', ha0, ha1, hb0, hb1, h0a, h1a, h0b, h1b, hab, hba, hcd', hdc']
set_option maxHeartbeats 800000 in
theorem test_single0 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 ≠ 0) (h1 : z 1 = 0) (h2 : z 2 = 0) (h3 : z 3 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hdiagc : B 0 0 = 0 := hdiag 0 h0
  have h01 : B 0 1 = 0 := hedge 0 1 h0 h1
  have h02 : B 0 2 = 0 := hedge 0 2 h0 h2
  have h03 : B 0 3 = 0 := hedge 0 3 h0 h3
  have sc := hstoch 0
  norm_num [Fin.sum_univ_succ] at sc
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at sc
  rw [hdiagc, h01, h02, h03] at sc
  linarith [sc]
set_option maxHeartbeats 800000 in
theorem test_single1 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 = 0) (h1 : z 1 ≠ 0) (h2 : z 2 = 0) (h3 : z 3 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hdiagc : B 1 1 = 0 := hdiag 1 h1
  have h10 : B 1 0 = 0 := hedge 1 0 h1 h0
  have h12 : B 1 2 = 0 := hedge 1 2 h1 h2
  have h13 : B 1 3 = 0 := hedge 1 3 h1 h3
  have sc := hstoch 1
  norm_num [Fin.sum_univ_succ] at sc
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at sc
  rw [hdiagc, h10, h12, h13] at sc
  linarith [sc]
set_option maxHeartbeats 800000 in
theorem test_single2 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 = 0) (h1 : z 1 = 0) (h2 : z 2 ≠ 0) (h3 : z 3 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hdiagc : B 2 2 = 0 := hdiag 2 h2
  have h20 : B 2 0 = 0 := hedge 2 0 h2 h0
  have h21 : B 2 1 = 0 := hedge 2 1 h2 h1
  have h23 : B 2 3 = 0 := hedge 2 3 h2 h3
  have sc := hstoch 2
  norm_num [Fin.sum_univ_succ] at sc
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at sc
  rw [hdiagc, h20, h21, h23] at sc
  linarith [sc]
set_option maxHeartbeats 800000 in
theorem test_single3 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 = 0) (h1 : z 1 = 0) (h2 : z 2 = 0) (h3 : z 3 ≠ 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hdiagc : B 3 3 = 0 := hdiag 3 h3
  have h30 : B 3 0 = 0 := hedge 3 0 h3 h0
  have h31 : B 3 1 = 0 := hedge 3 1 h3 h1
  have h32 : B 3 2 = 0 := hedge 3 2 h3 h2
  have sc := hstoch 3
  norm_num [Fin.sum_univ_succ] at sc
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at sc
  rw [hdiagc, h30, h31, h32] at sc
  linarith [sc]
set_option maxHeartbeats 800000 in
theorem test_three123 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hz : B *ᵥ z = -z)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h1 : z 1 ≠ 0) (h2 : z 2 ≠ 0) (h3 : z 3 ≠ 0) (h0 : z 0 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have h11 : B 1 1 = 0 := hdiag 1 h1
  have h10 : B 1 0 = 0 := hedge 1 0 h1 h0
  have h01 : B 0 1 = 0 := by rw [hsym 0 1, h10]
  have h22 : B 2 2 = 0 := hdiag 2 h2
  have h20 : B 2 0 = 0 := hedge 2 0 h2 h0
  have h02 : B 0 2 = 0 := by rw [hsym 0 2, h20]
  have h33 : B 3 3 = 0 := hdiag 3 h3
  have h30 : B 3 0 = 0 := hedge 3 0 h3 h0
  have h03 : B 0 3 = 0 := by rw [hsym 0 3, h30]
  have s1 := hstoch 1
  norm_num [Fin.sum_univ_succ] at s1
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at s1
  rw [h11, h10] at s1
  have s2 := hstoch 2
  norm_num [Fin.sum_univ_succ] at s2
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at s2
  rw [h22, h20] at s2
  have s3 := hstoch 3
  norm_num [Fin.sum_univ_succ] at s3
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at s3
  rw [h33, h30] at s3
  have hab : B 1 2 = (1 / 2 : ℝ) := by
    have hba : B 2 1 = B 1 2 := hsym 2 1
    have hca : B 3 1 = B 1 3 := hsym 3 1
    have hcb : B 3 2 = B 2 3 := hsym 3 2
    linarith [s1, s2, s3, hba, hca, hcb]
  have hba : B 2 1 = (1 / 2 : ℝ) := by rw [hsym 2 1, hab]
  have hac : B 1 3 = (1 / 2 : ℝ) := by
    have hba : B 2 1 = B 1 2 := hsym 2 1
    have hcb : B 3 2 = B 2 3 := hsym 3 2
    linarith [s1, s2, s3, hba, hcb, hab]
  have hca : B 3 1 = (1 / 2 : ℝ) := by rw [hsym 3 1, hac]
  have hbc : B 2 3 = (1 / 2 : ℝ) := by
    have hba : B 2 1 = B 1 2 := hsym 2 1
    linarith [s1, s2, s3, hba, hab, hac]
  have hcb : B 3 2 = (1 / 2 : ℝ) := by rw [hsym 3 2, hbc]
  have heig (i : Fin 4) : (∑ j : Fin 4, B i j * z j) = -z i := by
    have hi := congrFun hz i
    simpa [Matrix.mulVec, dotProduct] using hi
  have e1 := heig 1
  norm_num [Fin.sum_univ_succ] at e1
  change B 1 0 * z 0 + (B 1 1 * z 1 + (B 1 2 * z 2 + B 1 3 * z 3)) = -z 1 at e1
  have e2 := heig 2
  norm_num [Fin.sum_univ_succ] at e2
  change B 2 0 * z 0 + (B 2 1 * z 1 + (B 2 2 * z 2 + B 2 3 * z 3)) = -z 2 at e2
  have e3 := heig 3
  norm_num [Fin.sum_univ_succ] at e3
  change B 3 0 * z 0 + (B 3 1 * z 1 + (B 3 2 * z 2 + B 3 3 * z 3)) = -z 3 at e3
  rw [h10, h11, hab, hac] at e1
  rw [h20, hba, h22, hbc] at e2
  rw [h30, hca, hcb, h33] at e3
  apply h1
  linarith [e1, e2, e3]
set_option maxHeartbeats 800000 in
theorem test_three023 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hz : B *ᵥ z = -z)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 ≠ 0) (h2 : z 2 ≠ 0) (h3 : z 3 ≠ 0) (h1 : z 1 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have h00 : B 0 0 = 0 := hdiag 0 h0
  have h01 : B 0 1 = 0 := hedge 0 1 h0 h1
  have h10 : B 1 0 = 0 := by rw [hsym 1 0, h01]
  have h22 : B 2 2 = 0 := hdiag 2 h2
  have h21 : B 2 1 = 0 := hedge 2 1 h2 h1
  have h12 : B 1 2 = 0 := by rw [hsym 1 2, h21]
  have h33 : B 3 3 = 0 := hdiag 3 h3
  have h31 : B 3 1 = 0 := hedge 3 1 h3 h1
  have h13 : B 1 3 = 0 := by rw [hsym 1 3, h31]
  have s0 := hstoch 0
  norm_num [Fin.sum_univ_succ] at s0
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at s0
  rw [h00, h01] at s0
  have s2 := hstoch 2
  norm_num [Fin.sum_univ_succ] at s2
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at s2
  rw [h22, h21] at s2
  have s3 := hstoch 3
  norm_num [Fin.sum_univ_succ] at s3
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at s3
  rw [h33, h31] at s3
  have hab : B 0 2 = (1 / 2 : ℝ) := by
    have hba : B 2 0 = B 0 2 := hsym 2 0
    have hca : B 3 0 = B 0 3 := hsym 3 0
    have hcb : B 3 2 = B 2 3 := hsym 3 2
    linarith [s0, s2, s3, hba, hca, hcb]
  have hba : B 2 0 = (1 / 2 : ℝ) := by rw [hsym 2 0, hab]
  have hac : B 0 3 = (1 / 2 : ℝ) := by
    have hba : B 2 0 = B 0 2 := hsym 2 0
    have hcb : B 3 2 = B 2 3 := hsym 3 2
    linarith [s0, s2, s3, hba, hcb, hab]
  have hca : B 3 0 = (1 / 2 : ℝ) := by rw [hsym 3 0, hac]
  have hbc : B 2 3 = (1 / 2 : ℝ) := by
    have hba : B 2 0 = B 0 2 := hsym 2 0
    linarith [s0, s2, s3, hba, hab, hac]
  have hcb : B 3 2 = (1 / 2 : ℝ) := by rw [hsym 3 2, hbc]
  have heig (i : Fin 4) : (∑ j : Fin 4, B i j * z j) = -z i := by
    have hi := congrFun hz i
    simpa [Matrix.mulVec, dotProduct] using hi
  have e0 := heig 0
  norm_num [Fin.sum_univ_succ] at e0
  change B 0 0 * z 0 + (B 0 1 * z 1 + (B 0 2 * z 2 + B 0 3 * z 3)) = -z 0 at e0
  have e2 := heig 2
  norm_num [Fin.sum_univ_succ] at e2
  change B 2 0 * z 0 + (B 2 1 * z 1 + (B 2 2 * z 2 + B 2 3 * z 3)) = -z 2 at e2
  have e3 := heig 3
  norm_num [Fin.sum_univ_succ] at e3
  change B 3 0 * z 0 + (B 3 1 * z 1 + (B 3 2 * z 2 + B 3 3 * z 3)) = -z 3 at e3
  rw [h00, h01, hab, hac] at e0
  rw [hba, h21, h22, hbc] at e2
  rw [hca, h31, hcb, h33] at e3
  apply h0
  linarith [e0, e2, e3]
set_option maxHeartbeats 800000 in
theorem test_three013 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hz : B *ᵥ z = -z)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 ≠ 0) (h1 : z 1 ≠ 0) (h3 : z 3 ≠ 0) (h2 : z 2 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have h00 : B 0 0 = 0 := hdiag 0 h0
  have h02 : B 0 2 = 0 := hedge 0 2 h0 h2
  have h20 : B 2 0 = 0 := by rw [hsym 2 0, h02]
  have h11 : B 1 1 = 0 := hdiag 1 h1
  have h12 : B 1 2 = 0 := hedge 1 2 h1 h2
  have h21 : B 2 1 = 0 := by rw [hsym 2 1, h12]
  have h33 : B 3 3 = 0 := hdiag 3 h3
  have h32 : B 3 2 = 0 := hedge 3 2 h3 h2
  have h23 : B 2 3 = 0 := by rw [hsym 2 3, h32]
  have s0 := hstoch 0
  norm_num [Fin.sum_univ_succ] at s0
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at s0
  rw [h00, h02] at s0
  have s1 := hstoch 1
  norm_num [Fin.sum_univ_succ] at s1
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at s1
  rw [h11, h12] at s1
  have s3 := hstoch 3
  norm_num [Fin.sum_univ_succ] at s3
  change B 3 0 + (B 3 1 + (B 3 2 + B 3 3)) = 1 at s3
  rw [h33, h32] at s3
  have hab : B 0 1 = (1 / 2 : ℝ) := by
    have hba : B 1 0 = B 0 1 := hsym 1 0
    have hca : B 3 0 = B 0 3 := hsym 3 0
    have hcb : B 3 1 = B 1 3 := hsym 3 1
    linarith [s0, s1, s3, hba, hca, hcb]
  have hba : B 1 0 = (1 / 2 : ℝ) := by rw [hsym 1 0, hab]
  have hac : B 0 3 = (1 / 2 : ℝ) := by
    have hba : B 1 0 = B 0 1 := hsym 1 0
    have hcb : B 3 1 = B 1 3 := hsym 3 1
    linarith [s0, s1, s3, hba, hcb, hab]
  have hca : B 3 0 = (1 / 2 : ℝ) := by rw [hsym 3 0, hac]
  have hbc : B 1 3 = (1 / 2 : ℝ) := by
    have hba : B 1 0 = B 0 1 := hsym 1 0
    linarith [s0, s1, s3, hba, hab, hac]
  have hcb : B 3 1 = (1 / 2 : ℝ) := by rw [hsym 3 1, hbc]
  have heig (i : Fin 4) : (∑ j : Fin 4, B i j * z j) = -z i := by
    have hi := congrFun hz i
    simpa [Matrix.mulVec, dotProduct] using hi
  have e0 := heig 0
  norm_num [Fin.sum_univ_succ] at e0
  change B 0 0 * z 0 + (B 0 1 * z 1 + (B 0 2 * z 2 + B 0 3 * z 3)) = -z 0 at e0
  have e1 := heig 1
  norm_num [Fin.sum_univ_succ] at e1
  change B 1 0 * z 0 + (B 1 1 * z 1 + (B 1 2 * z 2 + B 1 3 * z 3)) = -z 1 at e1
  have e3 := heig 3
  norm_num [Fin.sum_univ_succ] at e3
  change B 3 0 * z 0 + (B 3 1 * z 1 + (B 3 2 * z 2 + B 3 3 * z 3)) = -z 3 at e3
  rw [h00, hab, h02, hac] at e0
  rw [hba, h11, h12, hbc] at e1
  rw [hca, hcb, h32, h33] at e3
  apply h0
  linarith [e0, e1, e3]
set_option maxHeartbeats 800000 in
theorem test_three012 {B : Mat 4} {z : Fin 4 → ℝ}
    (hm : B ∈ symmetricStochastic 4)
    (hz : B *ᵥ z = -z)
    (hquad : ∀ i j, B i j * (z i + z j)^2 = 0)
    (h0 : z 0 ≠ 0) (h1 : z 1 ≠ 0) (h2 : z 2 ≠ 0) (h3 : z 3 = 0) : False := by
  rcases hm with ⟨hsym, hnon, hstoch⟩
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hedge (i j : Fin 4) (hi : z i ≠ 0) (hj : z j = 0) : B i j = 0 := by
    have ht := hquad i j
    have hsquare : (z i + z j)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      rw [hj] at heq
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have h00 : B 0 0 = 0 := hdiag 0 h0
  have h03 : B 0 3 = 0 := hedge 0 3 h0 h3
  have h30 : B 3 0 = 0 := by rw [hsym 3 0, h03]
  have h11 : B 1 1 = 0 := hdiag 1 h1
  have h13 : B 1 3 = 0 := hedge 1 3 h1 h3
  have h31 : B 3 1 = 0 := by rw [hsym 3 1, h13]
  have h22 : B 2 2 = 0 := hdiag 2 h2
  have h23 : B 2 3 = 0 := hedge 2 3 h2 h3
  have h32 : B 3 2 = 0 := by rw [hsym 3 2, h23]
  have s0 := hstoch 0
  norm_num [Fin.sum_univ_succ] at s0
  change B 0 0 + (B 0 1 + (B 0 2 + B 0 3)) = 1 at s0
  rw [h00, h03] at s0
  have s1 := hstoch 1
  norm_num [Fin.sum_univ_succ] at s1
  change B 1 0 + (B 1 1 + (B 1 2 + B 1 3)) = 1 at s1
  rw [h11, h13] at s1
  have s2 := hstoch 2
  norm_num [Fin.sum_univ_succ] at s2
  change B 2 0 + (B 2 1 + (B 2 2 + B 2 3)) = 1 at s2
  rw [h22, h23] at s2
  have hab : B 0 1 = (1 / 2 : ℝ) := by
    have hba : B 1 0 = B 0 1 := hsym 1 0
    have hca : B 2 0 = B 0 2 := hsym 2 0
    have hcb : B 2 1 = B 1 2 := hsym 2 1
    linarith [s0, s1, s2, hba, hca, hcb]
  have hba : B 1 0 = (1 / 2 : ℝ) := by rw [hsym 1 0, hab]
  have hac : B 0 2 = (1 / 2 : ℝ) := by
    have hba : B 1 0 = B 0 1 := hsym 1 0
    have hcb : B 2 1 = B 1 2 := hsym 2 1
    linarith [s0, s1, s2, hba, hcb, hab]
  have hca : B 2 0 = (1 / 2 : ℝ) := by rw [hsym 2 0, hac]
  have hbc : B 1 2 = (1 / 2 : ℝ) := by
    have hba : B 1 0 = B 0 1 := hsym 1 0
    linarith [s0, s1, s2, hba, hab, hac]
  have hcb : B 2 1 = (1 / 2 : ℝ) := by rw [hsym 2 1, hbc]
  have heig (i : Fin 4) : (∑ j : Fin 4, B i j * z j) = -z i := by
    have hi := congrFun hz i
    simpa [Matrix.mulVec, dotProduct] using hi
  have e0 := heig 0
  norm_num [Fin.sum_univ_succ] at e0
  change B 0 0 * z 0 + (B 0 1 * z 1 + (B 0 2 * z 2 + B 0 3 * z 3)) = -z 0 at e0
  have e1 := heig 1
  norm_num [Fin.sum_univ_succ] at e1
  change B 1 0 * z 0 + (B 1 1 * z 1 + (B 1 2 * z 2 + B 1 3 * z 3)) = -z 1 at e1
  have e2 := heig 2
  norm_num [Fin.sum_univ_succ] at e2
  change B 2 0 * z 0 + (B 2 1 * z 1 + (B 2 2 * z 2 + B 2 3 * z 3)) = -z 2 at e2
  rw [h00, hab, hac, h03] at e0
  rw [hba, h11, hbc, h13] at e1
  rw [hca, hcb, h22, h23] at e2
  apply h0
  linarith [e0, e1, e2]

set_option maxHeartbeats 1200000 in
theorem test_spectral_uniqueness :
    spectrallyUnique counterexample := by
  unfold spectrallyUnique
  intro B hm hspec
  obtain ⟨z, hzne, hz⟩ := test_minus_one_eigenvector hspec
  have htrace : trace B = 1 := test_trace_from_spectrum hspec
  have hquad : ∀ i j, B i j * (z i + z j)^2 = 0 := test_quad_zero hm hz
  have hdiag (i : Fin 4) (hi : z i ≠ 0) : B i i = 0 := by
    have ht := hquad i i
    have hsquare : (z i + z i)^2 ≠ 0 := by
      intro hh
      have heq := sq_eq_zero_iff.mp hh
      apply hi
      linarith
    exact (mul_eq_zero.mp ht).resolve_right hsquare
  have hcases :
      (z 0 = 0 ∧ z 1 = 0 ∧ z 2 = 0 ∧ z 3 = 0) ∨
      (z 0 ≠ 0 ∧ z 1 ≠ 0 ∧ z 2 ≠ 0 ∧ z 3 ≠ 0) ∨
      (z 0 ≠ 0 ∧ z 1 ≠ 0 ∧ z 2 ≠ 0 ∧ z 3 = 0) ∨
      (z 0 ≠ 0 ∧ z 1 ≠ 0 ∧ z 2 = 0 ∧ z 3 ≠ 0) ∨
      (z 0 ≠ 0 ∧ z 1 = 0 ∧ z 2 ≠ 0 ∧ z 3 ≠ 0) ∨
      (z 0 = 0 ∧ z 1 ≠ 0 ∧ z 2 ≠ 0 ∧ z 3 ≠ 0) ∨
      (z 0 ≠ 0 ∧ z 1 ≠ 0 ∧ z 2 = 0 ∧ z 3 = 0) ∨
      (z 0 ≠ 0 ∧ z 1 = 0 ∧ z 2 ≠ 0 ∧ z 3 = 0) ∨
      (z 0 ≠ 0 ∧ z 1 = 0 ∧ z 2 = 0 ∧ z 3 ≠ 0) ∨
      (z 0 = 0 ∧ z 1 ≠ 0 ∧ z 2 ≠ 0 ∧ z 3 = 0) ∨
      (z 0 = 0 ∧ z 1 ≠ 0 ∧ z 2 = 0 ∧ z 3 ≠ 0) ∨
      (z 0 = 0 ∧ z 1 = 0 ∧ z 2 ≠ 0 ∧ z 3 ≠ 0) ∨
      (z 0 ≠ 0 ∧ z 1 = 0 ∧ z 2 = 0 ∧ z 3 = 0) ∨
      (z 0 = 0 ∧ z 1 ≠ 0 ∧ z 2 = 0 ∧ z 3 = 0) ∨
      (z 0 = 0 ∧ z 1 = 0 ∧ z 2 ≠ 0 ∧ z 3 = 0) ∨
      (z 0 = 0 ∧ z 1 = 0 ∧ z 2 = 0 ∧ z 3 ≠ 0) := by
    by_cases h0 : z 0 = 0 <;> by_cases h1 : z 1 = 0 <;>
      by_cases h2 : z 2 = 0 <;> by_cases h3 : z 3 = 0 <;> simp_all
  rcases hcases with hcase | hcase | hcase | hcase | hcase | hcase | hcase | hcase |
      hcase | hcase | hcase | hcase | hcase | hcase | hcase | hcase
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    apply False.elim
    apply hzne
    funext i
    fin_cases i <;> assumption
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    have h00 := hdiag 0 h0
    have h11 := hdiag 1 h1
    have h22 := hdiag 2 h2
    have h33 := hdiag 3 h3
    have ht := htrace
    norm_num [trace, Fin.sum_univ_succ] at ht
    change B 0 0 + (B 1 1 + (B 2 2 + B 3 3)) = 1 at ht
    rw [h00, h11, h22, h33] at ht
    norm_num at ht
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_three012 hm hz hquad h0 h1 h2 h3)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_three013 hm hz hquad h0 h1 h3 h2)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_three023 hm hz hquad h0 h2 h3 h1)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_three123 hm hz hquad h1 h2 h3 h0)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact ⟨(1 : Equiv.Perm (Fin 4)), test_pair01 hm hquad htrace h0 h1 h2 h3⟩
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact ⟨Equiv.swap 1 2, test_pair02 hm hquad htrace h0 h2 h1 h3⟩
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact ⟨Equiv.swap 1 3 * Equiv.swap 1 2, test_pair03 hm hquad htrace h0 h3 h1 h2⟩
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact ⟨Equiv.swap 1 2 * Equiv.swap 0 1, test_pair12 hm hquad htrace h1 h2 h0 h3⟩
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact ⟨Equiv.swap 1 3 * Equiv.swap 1 2 * Equiv.swap 0 1,
      test_pair13 hm hquad htrace h1 h3 h0 h2⟩
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact ⟨Equiv.swap 1 3 * Equiv.swap 0 2, test_pair23 hm hquad htrace h2 h3 h0 h1⟩
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_single0 hm hquad h0 h1 h2 h3)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_single1 hm hquad h0 h1 h2 h3)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_single2 hm hquad h0 h1 h2 h3)
  · rcases hcase with ⟨h0, h1, h2, h3⟩
    exact False.elim (test_single3 hm hquad h0 h1 h2 h3)


def splitId : Mat 4 :=
  !![(0 : ℝ), 1, 0, 0;
     1, 0, 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1]

def splitSwap : Mat 4 :=
  !![(0 : ℝ), 1, 0, 0;
     1, 0, 0, 0;
     0, 0, 0, 1;
     0, 0, 1, 0]

set_option maxHeartbeats 800000 in
theorem test_splitId_member : splitId ∈ symmetricStochastic 4 := by
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> rfl
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> norm_num [splitId]
  · intro i
    fin_cases i <;> norm_num [splitId, Fin.sum_univ_succ]

set_option maxHeartbeats 800000 in
theorem test_splitSwap_member : splitSwap ∈ symmetricStochastic 4 := by
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> rfl
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> norm_num [splitSwap]
  · intro i
    fin_cases i <;> norm_num [splitSwap, Fin.sum_univ_succ]

theorem test_midpoint_split :
    counterexample = (1 / 2 : ℝ) • splitId + (1 / 2 : ℝ) • splitSwap := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [counterexample, splitId, splitSwap]

theorem test_split_neq : splitId ≠ splitSwap := by
  intro h
  have hh := congrArg (fun M : Mat 4 => M 2 2) h
  norm_num [splitId, splitSwap, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three] at hh

theorem test_counterexample_not_vertex : ¬ vertex 4 counterexample := by
  intro hv
  rcases hv with ⟨hm, hvtx⟩
  have heq := test_midpoint_split
  have heq' : counterexample = (1 - (1 / 2 : ℝ)) • splitId + (1 / 2 : ℝ) • splitSwap := by
    convert heq using 1 <;> norm_num
  have h := hvtx splitId splitSwap test_splitId_member test_splitSwap_member
      (1 / 2 : ℝ) (by norm_num) (by norm_num) heq'
  rcases h with h | h | h
  · norm_num at h
  · norm_num at h
  · exact test_split_neq h

theorem test_not_base_segment :
    counterexample ∉ segment (1 : Mat 4) (flatMatrix 4) := by
  intro h
  rcases h with ⟨t, ht0, ht1, heq⟩
  have e0 := congrArg (fun M : Mat 4 => M 0 0) heq
  have e2 := congrArg (fun M : Mat 4 => M 2 2) heq
  simp [counterexample, flatMatrix, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three] at e0 e2
  linarith

theorem test_not_one_vertex {V : Mat 4} (hv : vertex 4 V) :
    counterexample ∉ segment (1 : Mat 4) V := by
  intro h
  rcases h with ⟨t, ht0, ht1, heq⟩
  have hv00 : 0 ≤ V 0 0 := hv.1.2.1 0 0
  have e0 := congrArg (fun M : Mat 4 => M 0 0) heq
  norm_num [counterexample] at e0
  have hprod : 0 ≤ t * V 0 0 := mul_nonneg ht0 hv00
  have ht : t = 1 := by nlinarith [e0, hprod]
  have hCV : counterexample = V := by simpa [ht] using heq
  have hn : ¬ vertex 4 counterexample := test_counterexample_not_vertex
  apply hn
  simpa [hCV] using hv

theorem test_not_flat_vertex {V : Mat 4} (hv : vertex 4 V) :
    counterexample ∉ segment (flatMatrix 4) V := by
  intro h
  rcases h with ⟨t, ht0, ht1, heq⟩
  have hv02 : 0 ≤ V 0 2 := hv.1.2.1 0 2
  have e02 := congrArg (fun M : Mat 4 => M 0 2) heq
  simp [counterexample, flatMatrix, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three] at e02
  have hprod : 0 ≤ (1 - t) * (1 / 3 : ℝ) := mul_nonneg (by linarith) (by norm_num)
  have ht : t = 1 := by nlinarith [e02, hprod]
  have hCV : counterexample = V := by simpa [ht] using heq
  have hn : ¬ vertex 4 counterexample := test_counterexample_not_vertex
  apply hn
  simpa [hCV] using hv

theorem test_outside_locus : counterexample ∉ assertedLocus 4 := by
  intro h
  unfold assertedLocus at h
  rcases h with h | ⟨V, hv, h⟩
  · exact test_not_base_segment h
  rcases h with h | h
  · exact test_not_one_vertex hv h
  · exact test_not_flat_vertex hv h

theorem test_counterexample_claim : counterexampleClaim := by
  refine ⟨test_membership, test_positive_trace, test_spectrum, test_spectral_uniqueness, test_outside_locus⟩

theorem test_not_targetNecessaryCondition : ¬ targetNecessaryCondition := by
  intro h
  have hC := h 4 (by norm_num) counterexample test_membership test_positive_trace
      test_spectral_uniqueness
  exact test_outside_locus hC

end NLA.IS02
