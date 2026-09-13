import NLA.KE04.SpectralWindow
import NLA.KE04.Transport
import NLA.KE04.Intersection
import NLA.KE04.Nonannihilation

/-!
# KE-04: complete strict interval occupancy

Original mathematical proof: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA,
with substantial AI assistance after the accepted complete statement gate.

The contradiction uses the actual later positive semidefinite quadratic, the
earlier consecutive eigenvector window, and the nonzero Krylov intersection.
No compatibility of the independently chosen frames or endpoint separation is
assumed.
-/

set_option leancert.trust "kernel"
noncomputable section

namespace NLA.KE04._proved

/-- A genuinely positive semidefinite real matrix has nonnegative Euclidean form. -/
theorem psd_form_nonneg {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m) :
    0 ≤ form M x := by
  exact (Matrix.isPositive_toEuclideanLin_iff.mpr hM).inner_nonneg_right x

theorem strictIntervalOccupancy : FullPrefixBlockLanczosClaim := by
  intro n p A hA V _hV s hs k j hk hkj hjs Qk Qj hQk hQj i hi hu
  obtain ⟨hk2, _hp, hia, hib⟩ := interval_index_validity k p i hk hi hu
  let a := ritzValueAt A hA Qk (i - 1)
  let b := ritzValueAt A hA Qk (i + p - 1)
  have hidx : i - 1 + p = i + p - 1 := by omega
  have hab : a ≤ b := by
    have hmon := (orderedSpectrum_semantics (compression A Qk)
      (Matrix.isHermitian_conjTranspose_mul_mul Qk hA)).1
    have horder : (⟨i - 1, hia⟩ : Fin (k * p)) ≤ ⟨i + p - 1, hib⟩ := by
      change i - 1 ≤ i + p - 1
      omega
    simpa only [a, b, ritzValueAt, eigenvalueAt, dif_pos hia, dif_pos hib] using hmon horder
  by_contra hno
  have hgap : ∀ r, ¬ (a < ritzValues A hA Qj r ∧ ritzValues A hA Qj r < b) := by
    intro r hr
    exact hno ⟨r, hr⟩
  have hsmall : (quadraticMatrix (compression A Qj) a b).PosSemidef :=
    spectral_gap_quadratic_psd (compression A Qj)
      (Matrix.isHermitian_conjTranspose_mul_mul Qj hA) a b hab hgap
  have hpsd : (compressedQuadratic A Qj a b).PosSemidef :=
    (compressedQuadratic_semantics A Qj a b).2 hsmall
  obtain ⟨E, hE, hdim, hform⟩ :=
    spectral_window_subspace A hA Qk hQk.1 (i - 1) p (by omega)
  have hEk : E ≤ krylov A V k := by
    rw [← hQk.2]
    exact hE
  have hfullk := (fullBlockDimension_prefix A V s hs k (by omega)).1
  have hprev := (fullBlockDimension_prefix A V s hs (k - 1) (by omega)).1
  obtain ⟨x, hne, hxE, hx⟩ := krylov_intersection_nonzero A V k hk hfullk hprev E hEk hdim
  have hle : form (compressedQuadratic A Qk a b) x ≤ 0 := by
    simpa only [a, b, hidx] using hform x hxE
  rw [quadratic_forms_agree A hA V k j hk hkj Qk Qj hQk hQj x hx a b] at hle
  have hzero : form (compressedQuadratic A Qj a b) x = 0 :=
    le_antisymm hle (psd_form_nonneg _ hpsd x)
  have hkernel := (psd_zero_form_iff_kernel _ hpsd x).mp hzero
  rw [later_quadratic_identity A V k j hk hkj Qj hQj x hx a b] at hkernel
  have hfullnext := (fullBlockDimension_prefix A V s hs (k + 1) (by omega)).1
  exact fullRank_quadratic_nonannihilation A V k hk2 hfullnext x hx hne a b hkernel

theorem blockLanczosConjecture : BlockLanczosConjecture :=
  fullPrefix_implies_canonical strictIntervalOccupancy

#assert_trust kernel psd_form_nonneg
#assert_trust kernel strictIntervalOccupancy
#assert_trust kernel blockLanczosConjecture
#print axioms psd_form_nonneg
#print axioms strictIntervalOccupancy
#print axioms blockLanczosConjecture

end NLA.KE04._proved
