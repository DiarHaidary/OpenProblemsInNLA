/-
  Full-set minimum and infimum-attainment contracts.

  WeightedBridgeDraft.lean supplies the lower bound for every feasible
  polynomial. This module bridges that bound and the explicit witness to M
  and IsLeast. Internal suffixed names are exported under the exact public
  Challenge names by Solution.lean.
-/
import NLA.IE16.WeightedBridgeDraft
import Mathlib.Order.ConditionallyCompleteLattice.Basic
import Mathlib.Tactic

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical ComplexConjugate
noncomputable section

namespace NLA.IE16

lemma explicitL_nonempty_draft : explicitL.Nonempty := by
  rw [Finset.nonempty_iff_ne_empty]
  intro h
  have hc := explicitL_card
  rw [h] at hc
  simp at hc

theorem full_minimum_value_isLeast_draft :
    IsLeast (feasibleValues explicitL 4) exactFullMinimum := by
  refine ⟨?_, ?_⟩
  · exact ⟨witnessPolynomial, witness_feasible, witness_objective⟩
  · intro r hr
    rcases hr with ⟨p, hp, rfl⟩
    exact witness_full_lower hp

theorem full_minimum_exact_draft :
    M explicitL 4 = exactFullMinimum := by
  unfold M
  exact full_minimum_value_isLeast_draft.csInf_eq

theorem full_minimum_isLeast_draft :
    IsLeast (feasibleValues explicitL 4) (M explicitL 4) := by
  rw [full_minimum_exact_draft]
  exact full_minimum_value_isLeast_draft

theorem full_lower_bound_draft : fullLowerBound < M explicitL 4 := by
  rw [full_minimum_exact_draft]
  norm_num [fullLowerBound, exactFullMinimum]

end NLA.IE16
