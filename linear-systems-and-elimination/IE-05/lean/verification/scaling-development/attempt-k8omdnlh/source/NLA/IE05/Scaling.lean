import NLA.IE05.Definitions
import LeanCert.Tactic.Verification

/-!
# IE-05: orthogonality from exact diagonal Gram data

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted formalization of the approved statement boundary.
-/

set_option leancert.trust "kernel"

noncomputable section
open scoped BigOperators

namespace NLA.IE05._proved

/-- Positive column normalization of a diagonal Gram identity is orthogonal.
Only one generic scalar square-root identity is needed; no entrywise numerical
square roots or interval comparisons are computed. -/
theorem scaledColumns_orthogonal {n : ℕ} (H : Mat n) (d : Fin n → ℝ)
    (hd : ∀ j, 0 < d j) (hH : H.transpose * H = Matrix.diagonal d) :
    Orthogonal (scaledColumns H d) := by
  classical
  unfold Orthogonal
  ext i j
  change (∑ k : Fin n, (H k i / Real.sqrt (d i)) *
    (H k j / Real.sqrt (d j))) = if i = j then 1 else 0
  have hentry : (∑ k : Fin n, H k i * H k j) = Matrix.diagonal d i j := by
    simpa only [Matrix.mul_apply, Matrix.transpose_apply] using
      congrArg (fun M : Mat n => M i j) hH
  rw [show (∑ k : Fin n, (H k i / Real.sqrt (d i)) *
      (H k j / Real.sqrt (d j))) =
      (∑ k : Fin n, H k i * H k j) / (Real.sqrt (d i) * Real.sqrt (d j)) by
    simp_rw [div_mul_div_comm]
    rw [Finset.sum_div]]
  rw [hentry]
  by_cases hij : i = j
  · subst j
    simp only [Matrix.diagonal_apply, ↓reduceIte]
    rw [← pow_two, Real.sq_sqrt (hd i).le, div_self (ne_of_gt (hd i))]
  · simp [Matrix.diagonal_apply, hij]

#print axioms scaledColumns_orthogonal
#assert_trust kernel scaledColumns_orthogonal

end NLA.IE05._proved
