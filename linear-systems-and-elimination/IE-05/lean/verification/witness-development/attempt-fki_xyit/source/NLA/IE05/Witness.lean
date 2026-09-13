import NLA.IE05.IntegerQR
import NLA.IE05.LUTrajectory
import NLA.IE05.ExactCertificates

/-!
# IE-05: exact real witness and canonical QR identification

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
The formal_review_standards AI agent implemented these bridges after the
accepted statement gate. Integer certificates, actual QR uniqueness and actual
Schur trajectories are reused; no further numerical QR calculation is made.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.IE05._proved

theorem castIntegerMatrix_transpose {n : ℕ} (A : IntMat n) :
    castIntegerMatrix A.transpose = (castIntegerMatrix A).transpose := rfl

theorem castIntegerMatrix_mul {n : ℕ} (A B : IntMat n) :
    castIntegerMatrix (A * B) = castIntegerMatrix A * castIntegerMatrix B := by
  ext i j
  simp [castIntegerMatrix, Matrix.mul_apply, Int.cast_sum, Int.cast_mul]

theorem castIntegerMatrix_diagonal {n : ℕ} (d : Fin n → ℤ) :
    castIntegerMatrix (Matrix.diagonal d) = Matrix.diagonal (fun j => (d j : ℝ)) := by
  ext i j
  by_cases h : i = j <;> simp [castIntegerMatrix, Matrix.diagonal_apply, h]

theorem castIntegerMatrix_tailProduct {n : ℕ} (L T : IntMat n) (k : ℕ) :
    castIntegerMatrix (tailProduct L T k) =
      tailProduct (castIntegerMatrix L) (castIntegerMatrix T) k := by
  ext i j
  by_cases h : k ≤ i.val ∧ k ≤ j.val
  · simp only [castIntegerMatrix, tailProduct, if_pos h, Int.cast_sum]
    apply Finset.sum_congr rfl
    intro r _
    by_cases hr : k ≤ r.val <;> simp [hr]
  · simp [castIntegerMatrix, tailProduct, h]

theorem castIntegerMatrix_unitLower {n : ℕ} (L : IntMat n) (hL : UnitLower L) :
    UnitLower (castIntegerMatrix L) := by
  refine ⟨?_, ?_⟩
  · intro i
    simp [castIntegerMatrix, hL.1 i]
  · intro i j hij
    simp [castIntegerMatrix, hL.2 i j hij]

theorem castIntegerMatrix_upper {n : ℕ} (T : IntMat n) (hT : UpperTriangular T) :
    UpperTriangular (castIntegerMatrix T) := by
  intro i j hij
  simp [castIntegerMatrix, hT i j hij]

theorem castIntegerMatrix_lower_bound {n : ℕ} (L : IntMat n)
    (hL : ∀ i j, j < i → |L i j| ≤ 1) :
    ∀ i j, j < i → |castIntegerMatrix L i j| ≤ 1 := by
  intro i j hij
  change |(L i j : ℝ)| ≤ 1
  exact_mod_cast hL i j hij

/-- The original exact integer data, transferred through the genuine real cast. -/
theorem real_factor_certificates (b : Bool) :
    (castIntegerMatrix (integerH b)).transpose * castIntegerMatrix (integerH b) =
        Matrix.diagonal (fun j => (integerD b j : ℝ)) ∧
      castIntegerMatrix (integerH b) =
        castIntegerMatrix (integerLower b) * castIntegerMatrix (integerT b) ∧
      UnitLower (castIntegerMatrix (integerLower b)) ∧
      UpperTriangular (castIntegerMatrix (integerT b)) ∧
      (∀ i j, j < i → |castIntegerMatrix (integerLower b) i j| ≤ 1) ∧
      (∀ i, 0 < castIntegerMatrix (integerT b) i i) ∧
      (∀ j, 0 < (integerD b j : ℝ)) := by
  obtain ⟨hGram, hLU, hL, hT, hLb, hTp, hd⟩ := integer_factor_certificates b
  refine ⟨?_, ?_, castIntegerMatrix_unitLower _ hL,
    castIntegerMatrix_upper _ hT, castIntegerMatrix_lower_bound _ hLb, ?_, ?_⟩
  · simpa only [castIntegerMatrix_mul, castIntegerMatrix_transpose,
      castIntegerMatrix_diagonal] using congrArg (castIntegerMatrix (n := 8)) hGram
  · simpa only [castIntegerMatrix_mul] using
      congrArg (castIntegerMatrix (n := 8)) hLU
  · intro i
    change 0 < (integerT b i i : ℝ)
    exact_mod_cast hTp i
  · intro j
    exact_mod_cast hd j

theorem normalizedInteger_orthogonal (b : Bool) : Orthogonal (normalizedInteger b) := by
  obtain ⟨hGram, _, _, _, _, _, hd⟩ := real_factor_certificates b
  exact scaledColumns_orthogonal _ _ hd hGram

/-- Both integer constructions follow exactly the proved real scaled-LU trajectory. -/
theorem normalizedInteger_path_trajectory (b : Bool) :
    FirstAvailablePath (normalizedInteger b) (noSwapPath 8) ∧
      firstPath (normalizedInteger b) = noSwapPath 8 ∧
      ∀ k, k ≤ 8 → trajectory (normalizedInteger b) (noSwapPath 8) k =
        scaledColumns (castIntegerMatrix (tailProduct (integerLower b) (integerT b) k))
          (fun j => (integerD b j : ℝ)) := by
  obtain ⟨_, hLU, hL, hT, hLb, hTp, hd⟩ := real_factor_certificates b
  have h := scaledLU_trajectory (castIntegerMatrix (integerLower b))
    (castIntegerMatrix (integerT b)) (fun j => (integerD b j : ℝ)) hL hLb hT hTp hd
  simpa only [normalizedInteger, hLU, castIntegerMatrix_tailProduct] using h

/-- Exact scalar entries of all actual active and terminal states; useful for growth. -/
theorem normalizedInteger_trajectory_entry (b : Bool) (k : ℕ) (hk : k ≤ 8)
    (i j : Fin 8) :
    trajectory (normalizedInteger b) (noSwapPath 8) k i j =
      (tailProduct (integerLower b) (integerT b) k i j : ℝ) /
        Real.sqrt (integerD b j : ℝ) := by
  rw [(normalizedInteger_path_trajectory b).2.2 k hk]
  rfl

theorem normalizedInteger_firstGrowth (b : Bool) :
    firstGrowth (normalizedInteger b) = growth (normalizedInteger b) (noSwapPath 8) := by
  unfold firstGrowth
  rw [(normalizedInteger_path_trajectory b).2.1]

/-- The integer candidate's lower factor is the prescribed matrix, by its definition. -/
theorem integerLower_false_prescribed :
    castIntegerMatrix (integerLower false) = prescribedLower 8 := by
  ext i j
  by_cases hij : i = j
  · subst j; simp [castIntegerMatrix, integerLower, prescribedLower]
  · by_cases hji : j < i <;> simp [castIntegerMatrix, integerLower, prescribedLower, hij, hji]

/-- The exact reviewed canonical QR identification and actual path. -/
theorem canonical_integer_identification :
    candidateQ 8 = normalizedInteger false ∧
      firstPath (candidateQ 8) = noSwapPath 8 := by
  obtain ⟨hGram, hLU, _, hT, _, hTp, hd⟩ := real_factor_certificates false
  have hQ : candidateQ 8 = normalizedInteger false := by
    change normalizedQRQ (prescribedLower 8) =
      scaledColumns (castIntegerMatrix (integerH false)) (fun j => (integerD false j : ℝ))
    rw [← integerLower_false_prescribed]
    exact normalizedQRQ_of_gram_lu _ _ _ _ hd hGram hLU hT hTp
  refine ⟨hQ, ?_⟩
  rw [hQ]
  exact (normalizedInteger_path_trajectory false).2.1

/-- The genuine real witness and its prescribed path meet all frozen conditions. -/
theorem witness_orthogonal_path :
    Orthogonal witnessQ ∧ firstPath witnessQ = noSwapPath 8 ∧
      FirstAvailablePath witnessQ (noSwapPath 8) ∧
      AdmissiblePath witnessQ (noSwapPath 8) := by
  obtain ⟨hpath, hfirst, _⟩ := normalizedInteger_path_trajectory true
  exact ⟨normalizedInteger_orthogonal true, hfirst, hpath, fun k => (hpath k).1⟩

#assert_trust kernel castIntegerMatrix_mul
#print axioms castIntegerMatrix_mul
#assert_trust kernel castIntegerMatrix_tailProduct
#print axioms castIntegerMatrix_tailProduct
#assert_trust kernel castIntegerMatrix_lower_bound
#print axioms castIntegerMatrix_lower_bound
#assert_trust kernel real_factor_certificates
#print axioms real_factor_certificates
#assert_trust kernel normalizedInteger_orthogonal
#print axioms normalizedInteger_orthogonal
#assert_trust kernel normalizedInteger_path_trajectory
#print axioms normalizedInteger_path_trajectory
#assert_trust kernel normalizedInteger_trajectory_entry
#print axioms normalizedInteger_trajectory_entry
#assert_trust kernel normalizedInteger_firstGrowth
#print axioms normalizedInteger_firstGrowth
#assert_trust kernel integerLower_false_prescribed
#print axioms integerLower_false_prescribed
#assert_trust kernel canonical_integer_identification
#print axioms canonical_integer_identification
#assert_trust kernel witness_orthogonal_path
#print axioms witness_orthogonal_path
end NLA.IE05._proved
