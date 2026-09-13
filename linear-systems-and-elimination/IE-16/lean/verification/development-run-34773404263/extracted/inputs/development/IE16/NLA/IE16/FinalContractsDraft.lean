/-
  Source-only finite-family and universal-negation contracts for IE-16.

  The subset geometry module is expected to export the two exact named
  helpers used below.  This file contains only order-theoretic finite-family
  plumbing and the final rational/π comparisons; it introduces no extra
  hypotheses into the public statements.
-/
import NLA.IE16.FullMinimumDraft
import NLA.IE16.SubsetGeometryDraft
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Tactic

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical ComplexConjugate
noncomputable section

namespace NLA.IE16

lemma subsetFamily_nonempty_draft :
    (subsetFamily explicitL 4).Nonempty := by
  have hcard : 5 ≤ explicitL.card := by
    rw [explicitL_card]
    norm_num
  obtain ⟨S, hsub, hScard⟩ := Finset.exists_subset_card_eq hcard
  refine ⟨S, ?_⟩
  simp only [subsetFamily, Finset.mem_filter, Finset.mem_powerset]
  exact ⟨hsub, by simpa using hScard⟩

lemma five_point_minimum_pos_draft {S : Finset ℂ}
    (hS : S ∈ subsetFamily explicitL 4) : 0 < M S 4 := by
  have hmem : S ∈ explicitL.powerset.filter (fun T => T.card = 4 + 1) := by
    simpa [subsetFamily] using hS
  have hfilter := Finset.mem_filter.mp hmem
  have hsub : S ⊆ explicitL := Finset.mem_powerset.mp hfilter.1
  have hcard : S.card = 5 := by simpa using hfilter.2
  have hnonempty : S.Nonempty := by
    have hcardpos : 0 < S.card := by omega
    exact Finset.card_pos.mp hcardpos
  have hnz : ∀ z ∈ S, z ≠ 0 := by
    intro z hz
    exact explicitL_admissible.2 z (hsub hz)
  have hM := every_five_point_subset_minimum_isLeast S hS
  have hL := lagrange_isLeast hcard hnonempty hnz
  have heq : M S 4 = (lagrangeSum S)⁻¹ := hM.unique hL
  rw [heq]
  exact inv_pos.mpr (lagrangeSum_pos hnonempty hnz)

lemma subset_max_upper_draft :
    subsetMax explicitL 4 < subsetUpperBound := by
  unfold subsetMax
  rw [dif_pos subsetFamily_nonempty_draft]
  apply (Finset.sup'_lt_iff subsetFamily_nonempty_draft).mpr
  intro S hS
  exact every_five_point_subset_upper S hS

lemma subset_max_positive_draft : 0 < subsetMax explicitL 4 := by
  unfold subsetMax
  rw [dif_pos subsetFamily_nonempty_draft]
  obtain ⟨S, hS⟩ := subsetFamily_nonempty_draft
  exact (five_point_minimum_pos_draft hS).trans_le
    (Finset.le_sup' (fun T : Finset ℂ => M T 4) hS)

lemma ratio_lower_bound_draft :
    ratioLowerBound < M explicitL 4 / subsetMax explicitL 4 := by
  have hBpos : 0 < subsetMax explicitL 4 := subset_max_positive_draft
  have hBupper : subsetMax explicitL 4 < subsetUpperBound :=
    subset_max_upper_draft
  apply (lt_div_iff₀ hBpos).2
  calc
    ratioLowerBound * subsetMax explicitL 4 <
        ratioLowerBound * subsetUpperBound := by
      exact mul_lt_mul_of_pos_left hBupper (by
        norm_num [ratioLowerBound])
    _ = fullLowerBound := by
      norm_num [ratioLowerBound, subsetUpperBound, fullLowerBound]
    _ < M explicitL 4 := full_lower_bound_draft

lemma ratio_exceeds_candidate_draft :
    (4 / Real.pi) < ratioLowerBound := by
  have hpi : (40 / 13 : ℝ) < Real.pi := by
    calc
      (40 / 13 : ℝ) < 3.14 := by norm_num
      _ < Real.pi := Real.pi_gt_d2
  unfold ratioLowerBound
  apply (div_lt_iff₀ Real.pi_pos).2
  nlinarith [hpi]

theorem counterexample_draft : ExplicitCertificate := by
  refine ⟨explicitL_card, explicitL_admissible, witness_feasible,
    full_minimum_exact_draft, full_minimum_isLeast_draft,
    full_lower_bound_draft, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro S hS
    exact every_five_point_subset_upper S hS
  · intro S hS
    exact every_five_point_subset_minimum_isLeast S hS
  · exact subset_max_upper_draft
  · exact subset_max_positive_draft
  · exact ratio_lower_bound_draft
  · exact ratio_exceeds_candidate_draft

theorem not_IE16Conjecture_draft : ¬ IE16Conjecture := by
  intro hconj
  have hineq := hconj 9 (by norm_num) explicitL explicitL_admissible
    4 (by norm_num) (by norm_num)
  have hratio :
      (4 / Real.pi) < M explicitL 4 / subsetMax explicitL 4 :=
    ratio_exceeds_candidate_draft.trans ratio_lower_bound_draft
  have hprod :
      (4 / Real.pi) * subsetMax explicitL 4 < M explicitL 4 :=
    (lt_div_iff₀ subset_max_positive_draft).mp hratio
  exact (not_lt_of_ge hineq) hprod

end NLA.IE16
