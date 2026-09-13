import NLA.IE05.Pivot

/-!
# IE-05: actual partial-pivoting trajectory of positively scaled LU factors

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
Implementation by the formal_review_standards AI agent after the two accepted
statement reviews. The genuine Schur recurrence and tie rule are proved; no
trajectory, determinant, or admissibility assertion is assumed.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.IE05._proved

/-- The initial trailing product is the actual full matrix product. -/
theorem tailProduct_zero {n : ℕ} (L T : Mat n) : tailProduct L T 0 = L * T := by
  ext i j
  simp [tailProduct, Matrix.mul_apply]

/-- The padded trailing product at the terminal stage has no active coordinates. -/
theorem tailProduct_terminal {n : ℕ} (L T : Mat n) : tailProduct L T n = 0 := by
  ext i j
  simp [tailProduct, Nat.not_le.mpr i.isLt]

/-- The actual pivot row of a trailing product comes from the upper factor. -/
theorem tailProduct_pivot_row {n : ℕ} (L T : Mat n) (hL : UnitLower L)
    (k j : Fin n) (hj : k ≤ j) : tailProduct L T k.val k j = T k j := by
  unfold tailProduct
  rw [if_pos ⟨le_rfl, hj⟩]
  rw [Finset.sum_eq_single k]
  · simp [hL.1 k]
  · intro r _ hr
    by_cases hkr : k ≤ r
    · have hlt : k < r := lt_of_le_of_ne hkr (Ne.symm hr)
      simp [hkr, hL.2 k r hlt]
    · simp [hkr]
  · simp

/-- The actual pivot column factors as a lower multiplier times the upper pivot. -/
theorem tailProduct_pivot_column {n : ℕ} (L T : Mat n) (hT : UpperTriangular T)
    (k i : Fin n) (hi : k ≤ i) : tailProduct L T k.val i k = L i k * T k k := by
  unfold tailProduct
  rw [if_pos ⟨hi, le_rfl⟩]
  rw [Finset.sum_eq_single k]
  · simp
  · intro r _ hr
    by_cases hkr : k ≤ r
    · have hlt : k < r := lt_of_le_of_ne hkr (Ne.symm hr)
      simp [hkr, hT r k hlt]
    · simp [hkr]
  · simp

/-- Removing the first active factor gives exactly the next trailing product. -/
theorem tailProduct_split {n : ℕ} (L T : Mat n) (k i j : Fin n)
    (hi : k < i) (hj : k < j) :
    tailProduct L T k.val i j = L i k * T k j + tailProduct L T (k.val+1) i j := by
  unfold tailProduct
  rw [if_pos ⟨hi.le,hj.le⟩, if_pos ⟨hi,hj⟩]
  calc
    (∑ r : Fin n, if k.val ≤ r.val then L i r * T r j else 0) =
        ∑ r : Fin n, (if r = k then L i k * T k j else 0) +
          (if k.val+1 ≤ r.val then L i r * T r j else 0) := by
      apply Finset.sum_congr rfl
      intro r _
      by_cases hr : r = k
      · subst r; simp
      · have hiff : k.val ≤ r.val ↔ k.val+1 ≤ r.val := by
          have hne : r.val ≠ k.val := fun h => hr (Fin.ext h)
          omega
        by_cases hkr : k.val ≤ r.val
        · simp [hr,hkr,hiff.mp hkr]
        · have hs : ¬ k.val+1 ≤ r.val := fun hs => hkr (hiff.mpr hs)
          simp [hr,hkr,hs]
    _ = L i k * T k j + ∑ r : Fin n,
        if k.val+1 ≤ r.val then L i r * T r j else 0 := by
      rw [Finset.sum_add_distrib]
      simp

/-- A genuine no-swap Schur step cancels exactly the active LU contribution. -/
theorem scaled_tail_schur {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hT : UpperTriangular T)
    (hTp : ∀ i, 0 < T i i) (hd : ∀ j, 0 < d j) (k : Fin n) :
    schurStep (scaledColumns (tailProduct L T k.val) d) k k =
      scaledColumns (tailProduct L T (k.val+1)) d := by
  have hs : Real.sqrt (d k) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (hd k))
  have ht : T k k ≠ 0 := ne_of_gt (hTp k)
  ext i j
  by_cases hij : k < i ∧ k < j
  · have hcol := tailProduct_pivot_column L T hT k i hij.1.le
    have hrow := tailProduct_pivot_row L T hL k j hij.2.le
    have hkk := tailProduct_pivot_row L T hL k k le_rfl
    have hsplit := tailProduct_split L T k i j hij.1 hij.2
    have hratio : (L i k * T k k / Real.sqrt (d k)) /
        (T k k / Real.sqrt (d k)) = L i k := by
      field_simp
    simp only [schurStep, rowSwap, Equiv.swap_self, Equiv.refl_apply,
      hij, if_pos, scaledColumns]
    rw [hcol, hrow, hkk, hratio, hsplit]
    ring
  · have hinactive : ¬ (k.val+1 ≤ i.val ∧ k.val+1 ≤ j.val) := hij
    simp [schurStep, rowSwap, hij, scaledColumns, tailProduct, hinactive]

/-- The actual diagonal row is an admissible least-row pivot, including ties. -/
theorem scaled_tail_firstAvailable {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hLb : ∀ i j, j < i → |L i j| ≤ 1)
    (hT : UpperTriangular T) (hTp : ∀ i, 0 < T i i)
    (hd : ∀ j, 0 < d j) (k : Fin n) :
    FirstAvailablePivot (scaledColumns (tailProduct L T k.val) d) k k := by
  have hrow := tailProduct_pivot_row L T hL k k le_rfl
  have hpos : 0 < T k k / Real.sqrt (d k) := div_pos (hTp k) (Real.sqrt_pos.2 (hd k))
  refine ⟨⟨le_rfl, ?_, ?_⟩, ?_⟩
  · change tailProduct L T k.val k k / Real.sqrt (d k) ≠ 0
    rw [hrow]
    exact ne_of_gt hpos
  · intro i hi
    have hl : |L i k| ≤ 1 := by
      by_cases hik : i = k
      · subst i; simp [hL.1 k]
      · exact hLb i k (lt_of_le_of_ne hi (Ne.symm hik))
    change |tailProduct L T k.val i k / Real.sqrt (d k)| ≤
      |tailProduct L T k.val k k / Real.sqrt (d k)|
    rw [tailProduct_pivot_column L T hT k i hi, hrow]
    rw [mul_div_assoc, abs_mul, abs_of_pos hpos]
    simpa only [one_mul] using mul_le_mul_of_nonneg_right hl hpos.le
  · intro i hi _
    exact hi

/-- Exact scaled-LU trajectories for the prescribed path, including stage n. -/
theorem scaled_noSwap_trajectory {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hT : UpperTriangular T)
    (hTp : ∀ i, 0 < T i i) (hd : ∀ j, 0 < d j)
    (k : ℕ) (hk : k ≤ n) :
    trajectory (scaledColumns (L * T) d) (noSwapPath n) k =
      scaledColumns (tailProduct L T k) d := by
  induction k with
  | zero => simp [trajectory, tailProduct_zero]
  | succ k ih =>
    have hkn : k < n := by omega
    rw [trajectory, dif_pos hkn, ih (by omega)]
    exact scaled_tail_schur L T d hL hT hTp hd ⟨k,hkn⟩

/-- The exact reviewed generic LU-to-GEPP contract. -/
theorem scaledLU_trajectory {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hLb : ∀ i j, j < i → |L i j| ≤ 1)
    (hT : UpperTriangular T) (hTp : ∀ i, 0 < T i i) (hd : ∀ j, 0 < d j) :
    FirstAvailablePath (scaledColumns (L * T) d) (noSwapPath n) ∧
      firstPath (scaledColumns (L * T) d) = noSwapPath n ∧
      ∀ k, k ≤ n → trajectory (scaledColumns (L * T) d) (noSwapPath n) k =
        scaledColumns (tailProduct L T k) d := by
  have htraj := scaled_noSwap_trajectory L T d hL hT hTp hd
  have hp : FirstAvailablePath (scaledColumns (L * T) d) (noSwapPath n) := by
    intro k
    rw [htraj k.val (Nat.le_of_lt k.isLt)]
    exact scaled_tail_firstAvailable L T d hL hLb hT hTp hd k
  exact ⟨hp, (NLA.IE05.firstPath_eq_of_firstAvailable_proved _ _ hp).symm, htraj⟩

#assert_trust kernel tailProduct_zero
#print axioms tailProduct_zero
#assert_trust kernel tailProduct_terminal
#print axioms tailProduct_terminal
#assert_trust kernel tailProduct_pivot_row
#print axioms tailProduct_pivot_row
#assert_trust kernel tailProduct_pivot_column
#print axioms tailProduct_pivot_column
#assert_trust kernel tailProduct_split
#print axioms tailProduct_split
#assert_trust kernel scaled_tail_schur
#print axioms scaled_tail_schur
#assert_trust kernel scaled_tail_firstAvailable
#print axioms scaled_tail_firstAvailable
#assert_trust kernel scaled_noSwap_trajectory
#print axioms scaled_noSwap_trajectory
#assert_trust kernel scaledLU_trajectory
#print axioms scaledLU_trajectory
end NLA.IE05._proved
