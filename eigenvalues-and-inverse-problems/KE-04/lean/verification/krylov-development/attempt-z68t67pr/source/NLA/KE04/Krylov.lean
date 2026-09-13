import NLA.KE04.Definitions
import Mathlib.LinearAlgebra.Dimension.OrzechProperty
import Mathlib.Data.Nat.Find
import LeanCert.Tactic.Verification

/-!
# Exact block Krylov range, rank and prefix dimensions

These lemmas supply the algebraic prerequisites of Matthew J. Colbrook's KE-04
argument: the actual block-power coefficient map, its full-rank prefixes and
the existence of the last full iteration at positive block width.

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA,
with substantial AI assistance.
-/

noncomputable section
open scoped BigOperators

namespace NLA.KE04._proved

/-- Matrix action on a column is the corresponding column of the product. -/
theorem act_column_mul {n m p : ℕ} (M : Rect n m) (N : Rect m p) (c : Fin p) :
    act M (column N c) = column (M * N) c := by
  -- In coordinates both sides are the same finite matrix-product sum.
  ext i
  rfl

/-- The true block coefficient map has exactly the Krylov space as its range. -/
theorem krylov_eq_range {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    krylov A V ell = LinearMap.range (krylovCombination A V ell) := by
  simpa [krylov, krylovCombination] using
    (Fintype.range_linearCombination ℝ (krylovColumns A V ell)).symm

/-- The actual Krylov span has at most as many dimensions as indexed columns. -/
theorem krylov_finrank_le {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    Module.finrank ℝ (krylov A V ell) ≤ ell * p := by
  simpa [krylov, Set.finrank] using
    (finrank_range_le_card (R := ℝ) (krylovColumns A V ell))

/-- Exact coefficient expansion and dimension bound for every block prefix. -/
theorem krylov_range_semantics {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    krylov A V ell = LinearMap.range (krylovCombination A V ell) ∧
      (∀ x, x ∈ krylov A V ell ↔ ∃ c : Fin ell × Fin p → ℝ,
        x = ∑ rc, c rc • column (A ^ rc.1.val * V) rc.2) ∧
      Module.finrank ℝ (krylov A V ell) ≤ ell * p := by
  refine ⟨krylov_eq_range A V ell, ?_, krylov_finrank_le A V ell⟩
  intro x
  rw [krylov_eq_range]
  constructor
  · rintro ⟨c, hc⟩
    exact ⟨c, by simpa [krylovCombination, Fintype.linearCombination_apply,
      krylovColumns] using hc.symm⟩
  · rintro ⟨c, hc⟩
    exact ⟨c, by simpa [krylovCombination, Fintype.linearCombination_apply,
      krylovColumns] using hc.symm⟩

/-- Inclusion of degree index sets induces inclusion of their actual spans. -/
theorem krylov_mono {n p : ℕ} (A : Mat n) (V : Rect n p) :
    Monotone (krylov A V) := by
  intro ell s h
  apply Submodule.span_mono
  rintro x ⟨⟨r, c⟩, rfl⟩
  exact ⟨(Fin.castLE h r, c), rfl⟩

/-- One multiplication shifts every block power into the next actual prefix. -/
theorem act_mem_krylov_succ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) (x : Vec n) (hx : x ∈ krylov A V ell) :
    act A x ∈ krylov A V (ell + 1) := by
  induction hx using Submodule.span_induction with
  | mem x hx =>
      rcases hx with ⟨⟨r, c⟩, rfl⟩
      rw [krylovColumns, act_column_mul]
      apply Submodule.subset_span
      refine ⟨(r.succ, c), ?_⟩
      simp [krylovColumns, pow_succ', Matrix.mul_assoc]
  | zero => simp
  | add x y hx hy hix hiy =>
      simpa using (krylov A V (ell + 1)).add_mem hix hiy
  | smul a x hx hix =>
      simpa using (krylov A V (ell + 1)).smul_mem a hix

/-- The empty prefix, nesting and shift all follow from the actual powers. -/
theorem krylov_nesting_and_shift {n p : ℕ} (A : Mat n) (V : Rect n p) :
    krylov A V 0 = ⊥ ∧ Monotone (krylov A V) ∧
      ∀ ell x, x ∈ krylov A V ell → act A x ∈ krylov A V (ell + 1) := by
  refine ⟨?_, krylov_mono A V, act_mem_krylov_succ A V⟩
  simp [krylov]

/-- The full finite span dimension is equivalent to independence of its columns. -/
theorem fullBlockDimension_iff_columns {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) :
    FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell) := by
  simpa [FullBlockDimension, krylov, Set.finrank, eq_comm] using
    (linearIndependent_iff_card_eq_finrank_span (R := ℝ)
      (b := krylovColumns A V ell)).symm

/-- At iteration one the degree index is a singleton and the columns are V. -/
theorem fullColumnRank_iff_first {n p : ℕ} (A : Mat n) (V : Rect n p) :
    FullColumnRank V ↔ FullBlockDimension A V 1 := by
  rw [fullBlockDimension_iff_columns]
  constructor
  · intro hV
    have hsnd : Function.Injective (Prod.snd : Fin 1 × Fin p → Fin p) := by
      intro x y h
      exact Prod.ext (Subsingleton.elim _ _) h
    simpa [krylovColumns, FullColumnRank, Function.comp_def] using
      hV.comp Prod.snd hsnd
  · intro hV
    have hpair : Function.Injective (fun c : Fin p => ((0 : Fin 1), c)) := by
      intro x y h
      exact congrArg Prod.snd h
    simpa [krylovColumns, FullColumnRank, Function.comp_def] using
      hV.comp (fun c : Fin p => ((0 : Fin 1), c)) hpair

/-- Both original rank interpretations use genuine column independence. -/
theorem fullBlockDimension_iff_independent {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) :
    (FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell)) ∧
      (FullColumnRank V ↔ FullBlockDimension A V 1) :=
  ⟨fullBlockDimension_iff_columns A V ell, fullColumnRank_iff_first A V⟩

/-- Independence restricts to earlier degree indices, without a trajectory premise. -/
theorem fullBlockDimension_prefix {n p : ℕ} (A : Mat n) (V : Rect n p)
    (s : ℕ) (hs : FullBlockDimension A V s) :
    ∀ ell, ell ≤ s → FullBlockDimension A V ell ∧
      Function.Injective (krylovCombination A V ell) := by
  intro ell h
  let embed : Fin ell × Fin p → Fin s × Fin p := fun rc => (Fin.castLE h rc.1, rc.2)
  have hinj : Function.Injective embed := by
    intro x y hxy
    apply Prod.ext
    · apply Fin.ext
      exact congrArg (fun z : Fin s × Fin p => z.1.val) hxy
    · exact congrArg Prod.snd hxy
  have hli : LinearIndependent ℝ (krylovColumns A V ell) := by
    simpa [embed, krylovColumns, Function.comp_def] using
      ((fullBlockDimension_iff_columns A V s).mp hs).comp embed hinj
  exact ⟨(fullBlockDimension_iff_columns A V ell).mpr hli,
    (linearIndependent_iff_injective_fintypeLinearCombination.mp hli)⟩

/-- Full block dimension bounds the number of independent columns by n. -/
theorem fullBlockDimension_mul_le {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) (hfull : FullBlockDimension A V ell) : ell * p ≤ n := by
  calc
    ell * p = Module.finrank ℝ (krylov A V ell) := hfull.symm
    _ ≤ Module.finrank ℝ (Vec n) := Submodule.finrank_le _
    _ = n := finrank_euclideanSpace_fin

/-- At positive block width every full iteration lies in the finite range 0..n. -/
theorem fullBlockDimension_index_le {n p : ℕ} (hp : 0 < p) (A : Mat n)
    (V : Rect n p) (ell : ℕ) (hfull : FullBlockDimension A V ell) : ell ≤ n := by
  have h : ell ≤ ell * p := by
    simpa using Nat.mul_le_mul_left ell (Nat.succ_le_iff.mpr hp)
  exact h.trans (fullBlockDimension_mul_le A V ell hfull)

/-- The finite nonempty set of full iterations has a greatest member. -/
theorem lastFullBlockIteration_exists {n p : ℕ} (hp : 0 < p)
    (A : Mat n) (V : Rect n p) (hV : FullColumnRank V) :
    ∃ s, 1 ≤ s ∧ LastFullBlockIteration A V s := by
  classical
  have h1 := (fullColumnRank_iff_first A V).mp hV
  have hn := fullBlockDimension_index_le hp A V 1 h1
  refine ⟨Nat.findGreatest (FullBlockDimension A V) n,
    Nat.le_findGreatest hn h1, Nat.findGreatest_spec hn h1, ?_⟩
  intro t ht
  exact Nat.le_findGreatest (fullBlockDimension_index_le hp A V t ht) ht

end NLA.KE04._proved

set_option leancert.trust "kernel"
#assert_trust kernel NLA.KE04._proved.act_column_mul
#print axioms NLA.KE04._proved.act_column_mul
#assert_trust kernel NLA.KE04._proved.krylov_eq_range
#print axioms NLA.KE04._proved.krylov_eq_range
#assert_trust kernel NLA.KE04._proved.krylov_finrank_le
#print axioms NLA.KE04._proved.krylov_finrank_le
#assert_trust kernel NLA.KE04._proved.krylov_range_semantics
#print axioms NLA.KE04._proved.krylov_range_semantics
#assert_trust kernel NLA.KE04._proved.krylov_mono
#print axioms NLA.KE04._proved.krylov_mono
#assert_trust kernel NLA.KE04._proved.act_mem_krylov_succ
#print axioms NLA.KE04._proved.act_mem_krylov_succ
#assert_trust kernel NLA.KE04._proved.krylov_nesting_and_shift
#print axioms NLA.KE04._proved.krylov_nesting_and_shift
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_iff_columns
#print axioms NLA.KE04._proved.fullBlockDimension_iff_columns
#assert_trust kernel NLA.KE04._proved.fullColumnRank_iff_first
#print axioms NLA.KE04._proved.fullColumnRank_iff_first
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_iff_independent
#print axioms NLA.KE04._proved.fullBlockDimension_iff_independent
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_prefix
#print axioms NLA.KE04._proved.fullBlockDimension_prefix
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_mul_le
#print axioms NLA.KE04._proved.fullBlockDimension_mul_le
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_index_le
#print axioms NLA.KE04._proved.fullBlockDimension_index_le
#assert_trust kernel NLA.KE04._proved.lastFullBlockIteration_exists
#print axioms NLA.KE04._proved.lastFullBlockIteration_exists
