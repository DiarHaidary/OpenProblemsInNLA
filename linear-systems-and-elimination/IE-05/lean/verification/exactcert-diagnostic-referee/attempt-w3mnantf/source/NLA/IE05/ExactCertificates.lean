import NLA.IE05.Definitions
import Mathlib.Tactic.NormNum
import LeanCert.Tactic.Verification

/-!
# IE-05: reduced exact integer and rational certificates

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted formalization of the independently approved numerical statements.

Only the required integer Gram/LU identities, 64 witness input inequalities,
204 active candidate inequalities and one positive rational gap are computed.
There is no square-root evaluation, interval subdivision or native-execution axiom.
-/

set_option leancert.trust "kernel"
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

namespace NLA.IE05._proved

theorem integer_factor_certificates :
    ∀ b : Bool,
      (integerH b).transpose * integerH b = Matrix.diagonal (integerD b) ∧
      integerH b = integerLower b * integerT b ∧
      UnitLower (integerLower b) ∧ UpperTriangular (integerT b) ∧
      (∀ i j, j < i → |integerLower b i j| ≤ 1) ∧
      (∀ i, 0 < integerT b i i) ∧ (∀ j, 0 < integerD b j) := by
  intro b
  cases b
  all_goals
    dsimp only [UnitLower, UpperTriangular, integerLower, integerH, integerD, integerT]
    decide +kernel

theorem integer_entry_certificates :
    (∀ i j : Fin 8, 5272 * (integerH true i j) ^ 2 ≤ 3969 * integerD true j) ∧
    integerD true 7 = 5272 ∧
    integerH false 2 2 = 51 ∧ integerD false 2 = 3286 ∧
    (∀ k i j : Fin 8, k ≤ i → k ≤ j →
      (tailProduct (integerLower false) (integerT false) k.val i j) ^ 2 ≤
        5462 * integerD false j) ∧
    tailProduct (integerLower true) (integerT true) 7 7 7 = 5272 := by
  decide +kernel

theorem numerical_gap_positive :
    ((5272 : ℝ) / 63) ^ 2 - (17948132 : ℝ) / 2601 =
      (117335164 : ℝ) / 1147041 ∧
      0 < (117335164 : ℝ) / 1147041 := by
  norm_num

#print axioms integer_factor_certificates
#assert_trust kernel integer_factor_certificates
#print axioms integer_entry_certificates
#assert_trust kernel integer_entry_certificates
#print axioms numerical_gap_positive
#assert_trust kernel numerical_gap_positive

end NLA.IE05._proved
