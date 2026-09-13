import NLA.IE05.Witness
import NLA.IE05.GrowthBounds

/-!
# IE-05: the exact strict growth comparison

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted formalization after the independently approved statement gate.

Only the frozen integer certificates are used. The witness needs one final
pivot lower bound; the candidate needs its active-entry upper bounds. Square
roots are manipulated symbolically, with no interval computation.
-/

set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05._proved

theorem integerD_real_pos (b : Bool) (j : Fin 8) : 0 < (integerD b j : ℝ) :=
  (real_factor_certificates b).2.2.2.2.2.2 j

theorem witness_entryMax_upper : entryMax witnessQ ≤ 63 / Real.sqrt 5272 := by
  apply entryMax_le_from_entries _ _ (by positivity)
  intro i j
  change |(integerH true i j : ℝ) / Real.sqrt (integerD true j : ℝ)| ≤ _
  apply abs_div_sqrt_le (integerD_real_pos true j) (by norm_num) (by norm_num)
  norm_num only [show (63 : ℝ) ^ 2 = 3969 by norm_num]
  exact_mod_cast integer_entry_certificates.1 i j

theorem witness_final_pivot :
    trajectory witnessQ (noSwapPath 8) 7 7 7 = Real.sqrt 5272 := by
  obtain ⟨_, hD, _, _, _, hT⟩ := integer_entry_certificates
  change trajectory (normalizedInteger true) (noSwapPath 8) 7 7 7 = _
  rw [normalizedInteger_trajectory_entry true 7 (by norm_num), hT, hD]
  norm_num only [Int.cast_ofNat]
  apply (div_eq_iff (ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 5272)))).mpr
  nlinarith only [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5272)]

theorem witness_peak_lower : Real.sqrt 5272 ≤ peakMax witnessQ (noSwapPath 8) := by
  have h := abs_le_activeMax_proved (trajectory witnessQ (noSwapPath 8) 7) 7
    (7 : Fin 8) (7 : Fin 8) (by norm_num) (by norm_num)
  rw [witness_final_pivot, abs_of_nonneg (Real.sqrt_nonneg _)] at h
  exact h.trans (activeMax_le_peakMax_proved witnessQ (noSwapPath 8) (7 : Fin 8))

theorem witness_growth_lower : (5272 : ℝ) / 63 ≤ firstGrowth witnessQ := by
  have hE := (gepp_growth_bound_proved (by norm_num) witnessQ (noSwapPath 8)
    witness_orthogonal_path.2.2.2).1
  unfold firstGrowth
  rw [witness_orthogonal_path.2.1]
  change (5272 : ℝ) / 63 ≤ peakMax witnessQ (noSwapPath 8) / entryMax witnessQ
  apply (le_div_iff₀ hE).mpr
  calc
    (5272 : ℝ) / 63 * entryMax witnessQ ≤ (5272 : ℝ) / 63 * (63 / Real.sqrt 5272) :=
      mul_le_mul_of_nonneg_left witness_entryMax_upper (by positivity)
    _ = Real.sqrt 5272 := by
      have h := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5272)
      field_simp [ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 5272))]
      nlinarith only [h]
    _ ≤ peakMax witnessQ (noSwapPath 8) := witness_peak_lower

theorem candidate_entryMax_lower :
    51 / Real.sqrt 3286 ≤ entryMax (candidateQ 8) := by
  rw [canonical_integer_identification.1]
  have h := abs_le_entryMax_proved (normalizedInteger false) (2 : Fin 8) (2 : Fin 8)
  change |(integerH false 2 2 : ℝ) / Real.sqrt (integerD false 2 : ℝ)| ≤ _ at h
  rw [integer_entry_certificates.2.2.1, integer_entry_certificates.2.2.2.1] at h
  norm_num only [Int.cast_ofNat] at h
  rwa [abs_of_nonneg (by positivity)] at h

theorem candidate_peak_upper :
    peakMax (normalizedInteger false) (noSwapPath 8) ≤ Real.sqrt 5462 := by
  apply peakMax_le_proved _ _ _ (Real.sqrt_nonneg _)
  intro k
  apply activeMax_le_proved _ _ _ (Real.sqrt_nonneg _)
  intro i j hi hj
  rw [normalizedInteger_trajectory_entry false k.val (Nat.le_of_lt k.isLt)]
  apply abs_div_sqrt_le_sqrt (integerD_real_pos false j) (by norm_num)
  exact_mod_cast integer_entry_certificates.2.2.2.2.1 k i j hi hj

theorem candidate_growth_nonneg : 0 ≤ firstGrowth (candidateQ 8) :=
  growth_nonneg _ _

theorem candidate_growth_upper :
    firstGrowth (candidateQ 8) ≤ Real.sqrt 5462 / (51 / Real.sqrt 3286) := by
  have hsmall : (0 : ℝ) < 51 / Real.sqrt 3286 := by positivity
  have hE : 0 < entryMax (candidateQ 8) := hsmall.trans_le candidate_entryMax_lower
  have hpeak : peakMax (candidateQ 8) (noSwapPath 8) ≤ Real.sqrt 5462 := by
    rw [canonical_integer_identification.1]
    exact candidate_peak_upper
  unfold firstGrowth
  rw [canonical_integer_identification.2]
  change peakMax (candidateQ 8) (noSwapPath 8) / entryMax (candidateQ 8) ≤ _
  exact (div_le_div_of_nonneg_right hpeak hE.le).trans
    (div_le_div_of_nonneg_left (Real.sqrt_nonneg _) hsmall candidate_entryMax_lower)

theorem candidate_growth_sq_upper :
    (firstGrowth (candidateQ 8)) ^ 2 ≤ (17948132 : ℝ) / 2601 := by
  have h := (sq_le_sq₀ candidate_growth_nonneg (by positivity)).mpr candidate_growth_upper
  have he : (Real.sqrt 5462 / (51 / Real.sqrt 3286)) ^ 2 =
      (17948132 : ℝ) / 2601 := by
    rw [div_pow, div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5462),
      Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3286)]
    norm_num
  exact he ▸ h

theorem bounded_growth_data :
    entryMax witnessQ ≤ 63 / Real.sqrt 5272 ∧
      (5272 : ℝ) / 63 ≤ firstGrowth witnessQ ∧
      51 / Real.sqrt 3286 ≤ entryMax (candidateQ 8) ∧
      0 ≤ firstGrowth (candidateQ 8) ∧
      (firstGrowth (candidateQ 8)) ^ 2 ≤ (17948132 : ℝ) / 2601 :=
  ⟨witness_entryMax_upper, witness_growth_lower, candidate_entryMax_lower,
    candidate_growth_nonneg, candidate_growth_sq_upper⟩

theorem witness_strict_growth :
    firstGrowth (candidateQ 8) < firstGrowth witnessQ := by
  have hsq := candidate_growth_sq_upper
  have hgap := numerical_gap_positive
  have hw := witness_growth_lower
  have hsmall : firstGrowth (candidateQ 8) < (5272 : ℝ) / 63 := by
    nlinarith only [hsq, hgap.1, hgap.2, candidate_growth_nonneg]
  exact hsmall.trans_le hw

theorem supremum_strict_gap :
    firstGrowth (candidateQ 8) < orthogonalGrowthSup 8 := by
  have hmem : firstGrowth witnessQ ∈ orthogonalGrowthSet 8 := by
    refine ⟨witnessQ, witness_orthogonal_path.1, noSwapPath 8,
      witness_orthogonal_path.2.2.2, ?_⟩
    unfold firstGrowth
    rw [witness_orthogonal_path.2.1]
  have hsup : firstGrowth witnessQ ≤ orthogonalGrowthSup 8 :=
    le_csSup (orthogonalGrowthSet_bounded_proved 8 (by norm_num)).2.1 hmem
  exact witness_strict_growth.trans_le hsup

theorem orthogonalExtremizerConjecture : ¬ OrthogonalExtremizerConjecture := by
  intro h
  have he := h 8 (by norm_num)
  have hg := supremum_strict_gap
  rw [he] at hg
  exact (lt_irrefl _ hg)

#print axioms witness_entryMax_upper
#assert_trust kernel witness_entryMax_upper
#print axioms witness_final_pivot
#assert_trust kernel witness_final_pivot
#print axioms witness_peak_lower
#assert_trust kernel witness_peak_lower
#print axioms witness_growth_lower
#assert_trust kernel witness_growth_lower
#print axioms candidate_entryMax_lower
#assert_trust kernel candidate_entryMax_lower
#print axioms candidate_peak_upper
#assert_trust kernel candidate_peak_upper
#print axioms candidate_growth_upper
#assert_trust kernel candidate_growth_upper
#print axioms candidate_growth_sq_upper
#assert_trust kernel candidate_growth_sq_upper
#print axioms bounded_growth_data
#assert_trust kernel bounded_growth_data
#print axioms witness_strict_growth
#assert_trust kernel witness_strict_growth
#print axioms supremum_strict_gap
#assert_trust kernel supremum_strict_gap
#print axioms orthogonalExtremizerConjecture
#assert_trust kernel orthogonalExtremizerConjecture

end NLA.IE05._proved
