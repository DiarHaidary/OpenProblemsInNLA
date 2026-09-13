import NLA.IE05.QR

/-!
# IE-05: identifying a normalized QR factor from exact Gram and LU data

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted implementation after the accepted statement gate.

This generic bridge uses the already approved integer Gram and LU identities.
It introduces no additional entrywise numerical certificate.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators

namespace NLA.IE05._proved

theorem normalizedQRQ_of_gram_lu {n : ℕ} (L H T : Mat n) (d : Fin n → ℝ)
    (hd : ∀ j, 0 < d j) (hGram : H.transpose * H = Matrix.diagonal d)
    (hLU : H = L * T) (hT : UpperTriangular T) (hTp : ∀ i, 0 < T i i) :
    normalizedQRQ L = scaledColumns H d := by
  classical
  have htri : T.IsUpperTriangular := by
    intro i j hij
    exact hT i j hij
  have hdet : 0 < T.det := by
    rw [Matrix.det_of_isUpperTriangular _ htri]
    exact Finset.prod_pos (fun i _ => hTp i)
  have hunit : IsUnit T.det := isUnit_iff_ne_zero.mpr (ne_of_gt hdet)
  letI : Invertible T := Matrix.invertibleOfIsUnitDet T hunit
  have hInv : T⁻¹.IsUpperTriangular :=
    Matrix.blockTriangular_inv_of_blockTriangular htri
  have hInvPos : ∀ i, 0 < (T⁻¹) i i := by
    intro i
    have hsum : (T * T⁻¹) i i = T i i * (T⁻¹) i i := by
      rw [Matrix.mul_apply, Finset.sum_eq_single i]
      · rfl
      · intro j _ hji
        rcases lt_or_gt_of_ne hji with hji | hij
        · rw [hT i j hji, zero_mul]
        · rw [hInv hij, mul_zero]
      · simp
    have heq := congrArg (fun M : Mat n => M i i) (Matrix.mul_nonsing_inv T hunit)
    rw [hsum, Matrix.one_apply_eq] at heq
    exact (mul_pos_iff_of_pos_left (hTp i)).mp (by rw [heq]; norm_num)
  have hRecover : H = scaledColumns H d * Matrix.diagonal (fun j => Real.sqrt (d j)) := by
    ext i j
    rw [Matrix.mul_diagonal]
    change H i j = (H i j / Real.sqrt (d j)) * Real.sqrt (d j)
    rw [div_mul_cancel₀ _ (ne_of_gt (Real.sqrt_pos.mpr (hd j)))]
  apply normalizedQRQ_eq_of_positiveQR
    (R := Matrix.diagonal (fun j => Real.sqrt (d j)) * T⁻¹)
  refine ⟨scaledColumns_orthogonal H d hd hGram, ?_, ?_, ?_⟩
  · calc
      L = (L * T) * T⁻¹ := by rw [Matrix.mul_assoc, Matrix.mul_nonsing_inv T hunit, Matrix.mul_one]
      _ = H * T⁻¹ := by rw [hLU]
      _ = (scaledColumns H d * Matrix.diagonal (fun j => Real.sqrt (d j))) * T⁻¹ := by
        rw [← hRecover]
      _ = _ := Matrix.mul_assoc _ _ _
  · intro i j hij
    rw [Matrix.diagonal_mul, hInv hij, mul_zero]
  · intro i
    rw [Matrix.diagonal_mul]
    exact mul_pos (Real.sqrt_pos.mpr (hd i)) (hInvPos i)

#print axioms normalizedQRQ_of_gram_lu
#assert_trust kernel normalizedQRQ_of_gram_lu

end NLA.IE05._proved
