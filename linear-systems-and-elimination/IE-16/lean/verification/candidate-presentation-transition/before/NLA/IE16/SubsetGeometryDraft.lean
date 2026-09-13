/- Source-only bridge from the actual nine complex points to the shared
subset bounds. All five-point subsets are retained. The original analytic
counterexample is due to Sidney Holden; formalization by George Stepaniants,
Department of Computing and Mathematical Sciences, Caltech, with AI assistance.
Remote compilation and final verification are still required.
-/
import NLA.IE16.Numeric
import NLA.IE16.SubsetBoundsDraft

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators
noncomputable section

namespace NLA.IE16.SubsetBounds

def point (ab : Grid) : ℂ := clusterPoint ab.1 ab.2

lemma point_injective : Function.Injective point := by
  change Function.Injective (fun ab : Fin 3 × Fin 3 => clusterPoint ab.1 ab.2)
  exact clusterPoint_injective

lemma omega_norm_one : ‖omega‖ = 1 := by
  have hs : ‖omega‖ ^ 2 = (1 : ℝ) := by
    rw [Complex.sq_norm]
    norm_num [omega, Complex.normSq_apply, Real.sq_sqrt] <;>
      ring_nf <;> norm_num [Real.sq_sqrt]
  nlinarith [norm_nonneg omega]

lemma epsilon_norm : ‖epsilon‖ = (1 / 1000 : ℝ) := by
  norm_num [epsilon, norm_div]

lemma root_distance_sq_le_three (a c : Fin 3) :
    ‖omega ^ a.val - omega ^ c.val‖ ^ 2 ≤ (3 : ℝ) := by
  have ho : omega ^ 2 = -omega - 1 := by
    linear_combination omega_sq_add_omega_add_one
  fin_cases a <;> fin_cases c <;>
    norm_num only [Fin.reduceFinMk, pow_zero, pow_one, ho] <;>
    rw [Complex.sq_norm] <;>
    norm_num [omega, Complex.normSq_apply, Real.sq_sqrt] <;>
    ring_nf <;> norm_num [Real.sq_sqrt]

lemma root_distance_upper (a c : Fin 3) :
    ‖omega ^ a.val - omega ^ c.val‖ ≤ (26 / 15 : ℝ) := by
  have hs := root_distance_sq_le_three a c
  have hn := norm_nonneg (omega ^ a.val - omega ^ c.val)
  nlinarith

lemma point_modulus_lower (ab : Grid) : pointLower ≤ ‖point ab‖ := by
  have htriangle : ‖omega ^ ab.1.val‖ ≤
      ‖point ab‖ + ‖epsilon * omega ^ ab.2.val‖ := by
    calc
      ‖omega ^ ab.1.val‖ = ‖point ab - epsilon * omega ^ ab.2.val‖ := by
        congr 1
        simp [point, clusterPoint]
      _ ≤ ‖point ab‖ + ‖epsilon * omega ^ ab.2.val‖ := norm_sub_le _ _
  rw [norm_pow, omega_norm_one, one_pow, norm_mul, epsilon_norm,
    norm_pow, omega_norm_one, one_pow, mul_one] at htriangle
  norm_num [pointLower] at htriangle ⊢
  linarith

lemma same_cluster_distance (ab cd : Grid) (hfirst : ab.1 = cd.1) :
    ‖point ab - point cd‖ ≤ nearUpper := by
  have he : point ab - point cd =
      epsilon * (omega ^ ab.2.val - omega ^ cd.2.val) := by
    simp only [point, clusterPoint, hfirst]
    ring
  rw [he, norm_mul, epsilon_norm]
  calc
    (1 / 1000 : ℝ) * ‖omega ^ ab.2.val - omega ^ cd.2.val‖ ≤
        (1 / 1000 : ℝ) * (26 / 15) :=
      mul_le_mul_of_nonneg_left (root_distance_upper ab.2 cd.2) (by norm_num)
    _ = nearUpper := by norm_num [nearUpper]

lemma any_point_distance (ab cd : Grid) :
    ‖point ab - point cd‖ ≤ farUpper := by
  have he : point ab - point cd =
      (omega ^ ab.1.val - omega ^ cd.1.val) +
        epsilon * (omega ^ ab.2.val - omega ^ cd.2.val) := by
    simp only [point, clusterPoint]
    ring
  have hsmall : ‖epsilon * (omega ^ ab.2.val - omega ^ cd.2.val)‖ ≤
      (2 / 1000 : ℝ) := by
    rw [norm_mul, epsilon_norm]
    calc
      (1 / 1000 : ℝ) * ‖omega ^ ab.2.val - omega ^ cd.2.val‖ ≤
          (1 / 1000 : ℝ) * (‖omega ^ ab.2.val‖ + ‖omega ^ cd.2.val‖) :=
        mul_le_mul_of_nonneg_left (norm_sub_le _ _) (by norm_num)
      _ = 2 / 1000 := by simp [norm_pow, omega_norm_one]; norm_num
  rw [he]
  calc
    ‖(omega ^ ab.1.val - omega ^ cd.1.val) +
        epsilon * (omega ^ ab.2.val - omega ^ cd.2.val)‖ ≤
      ‖omega ^ ab.1.val - omega ^ cd.1.val‖ +
        ‖epsilon * (omega ^ ab.2.val - omega ^ cd.2.val)‖ := norm_add_le _ _
    _ ≤ (26 / 15 : ℝ) + 2 / 1000 :=
      add_le_add (root_distance_upper ab.1 cd.1) hsmall
    _ = farUpper := by norm_num [farUpper]

def labels (S : Finset ℂ) : Finset Grid := by
  classical
  exact Finset.univ.filter (fun ab => point ab ∈ S)

lemma mem_labels {S : Finset ℂ} {ab : Grid} :
    ab ∈ labels S ↔ point ab ∈ S := by
  classical
  simp [labels]

lemma labels_image {S : Finset ℂ} (hS : S ⊆ explicitL) :
    (labels S).image point = S := by
  classical
  ext z
  constructor
  · intro hz
    rcases Finset.mem_image.mp hz with ⟨ab, hab, rfl⟩
    exact mem_labels.mp hab
  · intro hz
    rcases Finset.mem_image.mp (hS hz) with ⟨ab, hab, he⟩
    refine Finset.mem_image.mpr ⟨ab, ?_, ?_⟩
    · apply mem_labels.mpr
      change clusterPoint ab.1 ab.2 ∈ S
      rw [he]
      exact hz
    · exact he

lemma labels_card {S : Finset ℂ} (hS : S ⊆ explicitL) :
    (labels S).card = S.card := by
  classical
  have h := Finset.card_image_of_injective (labels S) point_injective
  rw [labels_image hS] at h
  exact h.symm

lemma lagrange_sum_labels {S : Finset ℂ} (hS : S ⊆ explicitL) :
    lagrangeSum S = ∑ ab ∈ labels S, ‖lagrangeBasisAtZero S (point ab)‖ := by
  classical
  calc
    lagrangeSum S = ∑ z ∈ (labels S).image point, ‖lagrangeBasisAtZero S z‖ := by
      rw [labels_image hS]
      rfl
    _ = ∑ ab ∈ labels S, ‖lagrangeBasisAtZero S (point ab)‖ :=
      Finset.sum_image (fun ab _ cd _ he => point_injective he)

lemma label_coefficient_gt {S : Finset ℂ} {ab : Grid} {h : ℕ} {c : ℝ}
    (hS : S ⊆ explicitL) (hcard : S.card = 5) (hab : ab ∈ labels S)
    (hcount : h ≤ companionCount (labels S) ab)
    (hc : 0 ≤ c)
    (hmargin : c * (nearUpper ^ h * farUpper ^ (4 - h)) < pointLower ^ 4) :
    c < ‖lagrangeBasisAtZero S (point ab)‖ := by
  classical
  obtain ⟨K, hK, hKcard⟩ := Finset.exists_subset_card_eq hcount
  let H := K.image point
  have hHcard : H.card = h := by
    change (K.image point).card = h
    rw [Finset.card_image_of_injective K point_injective, hKcard]
  have hH : H ⊆ S.erase (point ab) := by
    intro z hz
    rcases Finset.mem_image.mp hz with ⟨cd, hcd, rfl⟩
    have hmem := (Finset.mem_filter.mp (hK hcd)).1
    refine Finset.mem_erase.mpr ⟨?_, ?_⟩
    · intro he
      exact (Finset.mem_erase.mp hmem).1 (point_injective he)
    · exact mem_labels.mp (Finset.mem_erase.mp hmem).2
  apply coefficient_gt_of_close_subset hcard (mem_labels.mp hab) ?_
    hH hHcard ?_ ?_ hc hmargin
  · intro z hz
    rcases Finset.mem_image.mp (hS hz) with ⟨cd, hcd, rfl⟩
    exact point_modulus_lower cd
  · intro z hz
    rcases Finset.mem_image.mp hz with ⟨cd, hcd, rfl⟩
    have hfirst := (Finset.mem_filter.mp (hK hcd)).2
    exact same_cluster_distance ab cd hfirst.symm
  · intro z hz
    rcases Finset.mem_image.mp (hS (Finset.mem_of_mem_erase hz)) with
      ⟨cd, hcd, rfl⟩
    exact any_point_distance ab cd

lemma lagrange_sum_large {S : Finset ℂ}
    (hS : S ⊆ explicitL) (hcard : S.card = 5) :
    (10000 / 23 : ℝ) < lagrangeSum S := by
  classical
  have hlabels : (labels S).card = 5 := (labels_card hS).trans hcard
  rw [lagrange_sum_labels hS]
  rcases occupancy_disjunction (labels S) hlabels with hpairs | htriples
  · have hs := sum_gt_from_many_terms
      (S := labels S)
      (T := (labels S).filter (fun ab => 1 ≤ companionCount (labels S) ab))
      (f := fun ab => ‖lagrangeBasisAtZero S (point ab)‖)
      (n := 4) (c := 109) (Finset.filter_subset _ _) (by decide) hpairs
      (by norm_num)
      (by
        intro ab hab
        rcases Finset.mem_filter.mp hab with ⟨hab, hcount⟩
        apply label_coefficient_gt hS hcard hab hcount (by norm_num)
        simpa only [pow_one, Nat.reduceSub, mul_assoc] using rational_pair_margin)
      (fun ab _ => norm_nonneg _)
    norm_num at hs
    exact lt_trans (by norm_num : (10000 / 23 : ℝ) < 436) hs
  · have hs := sum_gt_from_many_terms
      (S := labels S)
      (T := (labels S).filter (fun ab => 2 ≤ companionCount (labels S) ab))
      (f := fun ab => ‖lagrangeBasisAtZero S (point ab)‖)
      (n := 3) (c := 146) (Finset.filter_subset _ _) (by decide) htriples
      (by norm_num)
      (by
        intro ab hab
        rcases Finset.mem_filter.mp hab with ⟨hab, hcount⟩
        apply label_coefficient_gt hS hcard hab hcount (by norm_num)
        simpa only [Nat.reduceSub, mul_assoc] using rational_triple_margin)
      (fun ab _ => norm_nonneg _)
    norm_num at hs
    exact lt_trans (by norm_num : (10000 / 23 : ℝ) < 438) hs

end NLA.IE16.SubsetBounds

namespace NLA.IE16

theorem every_five_point_subset_upper (S : Finset ℂ)
    (hS : S ∈ subsetFamily explicitL 4) : M S 4 < subsetUpperBound := by
  classical
  have hsub : S ⊆ explicitL :=
    Finset.mem_powerset.mp (Finset.mem_filter.mp hS).1
  have hcard : S.card = 5 := by
    simpa using (Finset.mem_filter.mp hS).2
  have hne : S.Nonempty := Finset.card_pos.mp (by omega)
  have hnz : ∀ z ∈ S, z ≠ 0 := fun z hz => explicitL_admissible.2 z (hsub hz)
  have hmin := lagrange_isLeast hcard hne hnz
  have hM : M S 4 = (lagrangeSum S)⁻¹ := hmin.csInf_eq
  have hlarge := SubsetBounds.lagrange_sum_large hsub hcard
  have hpos : 0 < lagrangeSum S := lagrangeSum_pos hne hnz
  rw [hM]
  apply (inv_lt_iff_one_lt_mul₀ hpos).mpr
  norm_num [subsetUpperBound] at hlarge ⊢
  nlinarith

theorem every_five_point_subset_minimum_isLeast (S : Finset ℂ)
    (hS : S ∈ subsetFamily explicitL 4) :
    IsLeast (feasibleValues S 4) (M S 4) := by
  classical
  have hsub : S ⊆ explicitL :=
    Finset.mem_powerset.mp (Finset.mem_filter.mp hS).1
  have hcard : S.card = 5 := by
    simpa using (Finset.mem_filter.mp hS).2
  have hne : S.Nonempty := Finset.card_pos.mp (by omega)
  have hnz : ∀ z ∈ S, z ≠ 0 := fun z hz => explicitL_admissible.2 z (hsub hz)
  have hmin := lagrange_isLeast hcard hne hnz
  have hM : M S 4 = (lagrangeSum S)⁻¹ := hmin.csInf_eq
  rw [hM]
  exact hmin

end NLA.IE16
