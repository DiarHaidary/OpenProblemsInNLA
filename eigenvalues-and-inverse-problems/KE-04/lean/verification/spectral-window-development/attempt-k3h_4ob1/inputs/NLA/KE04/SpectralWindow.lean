import NLA.KE04.Frames
import NLA.KE04.Spectral
import Lean.Elab.Tactic.Omega

/-!
# KE-04: basis independence and consecutive spectral windows

Original mathematical proof: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
AI-assisted proof implementation after the accepted complete statement gate.

The window counts distinct basis indices, retaining repeated eigenvalues.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators

namespace NLA.KE04._proved

theorem compression_basis_independent {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q R : Rect n m) (hQ : Q.transpose * Q = 1) (hR : R.transpose * R = 1)
    (hspan : columnSpace Q = columnSpace R) :
    (∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R := by
  let O : Mat m := Q.transpose * R
  have hrep : R = Q * O := by
    apply Matrix.toEuclideanLin.injective
    apply LinearMap.ext
    intro x
    change act R x = act (Q * (Q.transpose * R)) x
    rw [act_mul, act_mul, ← frameProjection_act]
    apply ((frameProjection_fixed_iff Q hQ _).mp ?_).symm
    rw [hspan, columnSpace_eq_range_act]
    exact ⟨x, rfl⟩
  have hO : O.transpose * O = 1 := by
    change (Q.transpose * R).transpose * O = 1
    rw [Matrix.transpose_mul, Matrix.transpose_transpose, Matrix.mul_assoc, ← hrep, hR]
  have hO' : O * O.transpose = 1 := Matrix.mul_eq_one_comm.mp hO
  have hsim : compression A R = O.transpose * compression A Q * O := by
    conv_lhs => rw [hrep]
    simp only [compression, Matrix.conjTranspose_eq_transpose_of_trivial,
      Matrix.transpose_mul, Matrix.mul_assoc]
  have hchar : (compression A Q).charpoly = (compression A R).charpoly := by
    rw [hsim, Matrix.charpoly_mul_comm, ← Matrix.mul_assoc, hO', Matrix.one_mul]
  refine ⟨⟨O, hO, hrep, hsim⟩, hchar, ?_⟩
  let hTQ := Matrix.isSymmetric_toEuclideanLin_iff.mpr
    (Matrix.isHermitian_conjTranspose_mul_mul Q hA)
  let hTR := Matrix.isSymmetric_toEuclideanLin_iff.mpr
    (Matrix.isHermitian_conjTranspose_mul_mul R hA)
  have hvalues := (hTQ.eigenvalues_eq_eigenvalues_iff finrank_euclideanSpace_fin hTR
    finrank_euclideanSpace_fin).mpr (by
      simpa only [Matrix.toEuclideanLin_eq_toLin_orthonormal, Matrix.charpoly_toLin] using hchar)
  funext r
  exact congrFun hvalues r.rev

/-- Nonpositive eigenvalues on an orthonormal family's span give a nonpositive form. -/
theorem orthonormal_span_form_nonpos {n q : ℕ} (M : Mat n)
    (v : Fin q → Vec n) (d : Fin q → ℝ) (hv : Orthonormal ℝ v)
    (heig : ∀ j, act M (v j) = d j • v j) (hd : ∀ j, d j ≤ 0)
    (x : Vec n) (hx : x ∈ Submodule.span ℝ (Set.range v)) : form M x ≤ 0 := by
  obtain ⟨c, rfl⟩ := Submodule.mem_span_range_iff_exists_fun.mp hx
  have hform : form M (∑ j, c j • v j) = ∑ j, (c j * c j) * d j := by
    simp only [form, map_sum, map_smul, heig, smul_smul]
    simpa [mul_assoc] using hv.inner_sum c (fun j => c j * d j) Finset.univ
  rw [hform]
  exact Finset.sum_nonpos fun j _ => mul_nonpos_of_nonneg_of_nonpos (mul_self_nonneg _) (hd j)

theorem spectral_window_subspace {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) (i p : ℕ) (hi : i + p < m) :
    ∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0 := by
  let M := compression A Q
  let hM : M.IsHermitian := Matrix.isHermitian_conjTranspose_mul_mul Q hA
  let B := orderedEigenbasis M hM
  let t : Fin (p + 1) → Fin m := fun j => ⟨i + j.val, by omega⟩
  have ht : Function.Injective t := by
    intro j k h
    apply Fin.ext
    have := congrArg Fin.val h
    dsimp [t] at this
    omega
  let w : Fin (p + 1) → Vec n := fun j => act Q (B (t j))
  have hw : Orthonormal ℝ w := by
    rw [orthonormal_iff_ite]
    intro j k
    change inner ℝ (act Q (B (t j))) (act Q (B (t k))) = _
    rw [inner_act_left, act_transpose_act Q hQ]
    exact (orthonormal_iff_ite.mp (B.orthonormal.comp t ht)) j k
  let a := ritzValueAt A hA Q i
  let b := ritzValueAt A hA Q (i + p)
  let d : Fin (p + 1) → ℝ := fun j =>
    (orderedEigenvalues M hM (t j) - a) * (orderedEigenvalues M hM (t j) - b)
  have hi0 : i < m := by omega
  have ha : a = orderedEigenvalues M hM ⟨i, hi0⟩ := by
    simp [a, ritzValueAt, eigenvalueAt, hi0, M]
  have hb : b = orderedEigenvalues M hM ⟨i + p, hi⟩ := by
    simp [b, ritzValueAt, eigenvalueAt, hi, M]
  have hd : ∀ j, d j ≤ 0 := by
    intro j
    apply mul_nonpos_of_nonneg_of_nonpos
    · apply sub_nonneg.mpr
      rw [ha]
      apply (orderedSpectrum_semantics M hM).1
      change i ≤ i + j.val
      omega
    · apply sub_nonpos.mpr
      rw [hb]
      apply (orderedSpectrum_semantics M hM).1
      change i + j.val ≤ i + p
      omega
  have heig (j : Fin (p + 1)) :
      act (compressedQuadratic A Q a b) (w j) = d j • w j := by
    change act (Q * quadraticMatrix M a b * Q.conjTranspose) (act Q (B (t j))) = _
    rw [act_mul, act_mul, Matrix.conjTranspose_eq_transpose_of_trivial,
      act_transpose_act Q hQ,
      quadratic_apply_eigenvector M a b _ _ ((orderedSpectrum_semantics M hM).2.1 (t j)),
      map_smul]
  refine ⟨Submodule.span ℝ (Set.range w), ?_, ?_, ?_⟩
  · apply Submodule.span_le.mpr
    rintro _ ⟨j, rfl⟩
    rw [columnSpace_eq_range_act]
    exact ⟨B (t j), rfl⟩
  · simpa using Submodule.finrank_span_eq_card hw.linearIndependent
  · exact orthonormal_span_form_nonpos (compressedQuadratic A Q a b) w d hw heig hd

#assert_trust kernel compression_basis_independent
#assert_trust kernel orthonormal_span_form_nonpos
#assert_trust kernel spectral_window_subspace
#print axioms compression_basis_independent
#print axioms orthonormal_span_form_nonpos
#print axioms spectral_window_subspace

end NLA.KE04._proved
