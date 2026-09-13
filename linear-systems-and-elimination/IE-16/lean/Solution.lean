/-
Complete proof exports for the frozen IE-16 statement boundary.

Original mathematics: Sidney Holden. Formalization: George Stepaniants,
Department of Computing and Mathematical Sciences, California Institute of
Technology, Pasadena, California, USA, with AI-agent assistance. The module
imports the numerical and subset contracts and aliases the remaining
internal declarations to the exact public names required by Challenge.
-/
import NLA.IE16.Numeric
import NLA.IE16.SubsetGeometryDraft
import NLA.IE16.FullMinimumDraft
import NLA.IE16.FinalContractsDraft
import LeanCert.Tactic.Verification

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical
noncomputable section

namespace NLA.IE16

/- The first four public contracts are supplied by Numeric, and the next two
   subset contracts by SubsetGeometryDraft. They are intentionally not
   redeclared here, so Comparator sees one declaration per frozen name. -/

theorem full_minimum_exact : M explicitL 4 = exactFullMinimum := by
  exact full_minimum_exact_draft

theorem full_minimum_isLeast :
    IsLeast (feasibleValues explicitL 4) (M explicitL 4) := by
  exact full_minimum_isLeast_draft

theorem full_lower_bound : fullLowerBound < M explicitL 4 := by
  exact full_lower_bound_draft

theorem subset_max_upper : subsetMax explicitL 4 < subsetUpperBound := by
  exact subset_max_upper_draft

theorem subset_max_positive : 0 < subsetMax explicitL 4 := by
  exact subset_max_positive_draft

theorem ratio_lower_bound :
    ratioLowerBound < M explicitL 4 / subsetMax explicitL 4 := by
  exact ratio_lower_bound_draft

theorem ratio_exceeds_candidate : (4 / Real.pi) < ratioLowerBound := by
  exact ratio_exceeds_candidate_draft

theorem counterexample : ExplicitCertificate := by
  exact counterexample_draft

theorem not_IE16Conjecture : ¬ IE16Conjecture := by
  exact not_IE16Conjecture_draft

#assert_trust kernel explicitL_card
#print axioms explicitL_card
#assert_trust kernel explicitL_admissible
#print axioms explicitL_admissible
#assert_trust kernel witness_feasible
#print axioms witness_feasible
#assert_trust kernel witness_objective
#print axioms witness_objective
#assert_trust kernel full_minimum_exact
#print axioms full_minimum_exact
#assert_trust kernel full_minimum_isLeast
#print axioms full_minimum_isLeast
#assert_trust kernel full_lower_bound
#print axioms full_lower_bound
#assert_trust kernel every_five_point_subset_upper
#print axioms every_five_point_subset_upper
#assert_trust kernel every_five_point_subset_minimum_isLeast
#print axioms every_five_point_subset_minimum_isLeast
#assert_trust kernel subset_max_upper
#print axioms subset_max_upper
#assert_trust kernel subset_max_positive
#print axioms subset_max_positive
#assert_trust kernel ratio_lower_bound
#print axioms ratio_lower_bound
#assert_trust kernel ratio_exceeds_candidate
#print axioms ratio_exceeds_candidate
#assert_trust kernel counterexample
#print axioms counterexample
#assert_trust kernel not_IE16Conjecture
#print axioms not_IE16Conjecture

end NLA.IE16
