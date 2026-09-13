import NLA.RA20.Count
import NLA.RA20.Differential

/-!
# RA-20 completed proof assembly

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
Original negative resolution: the repository's Codex automated maintainer audit;
conjecture: Kubjas, Sodomaco and Tsigaridas.

The imported proofs establish the genuine reduced coordinate ring, algebraic
smooth locus, entire-ideal tangent space, full complex Frobenius derivatives,
critical-set exhaustion, generic-open intersection and actual cardinal count.
The final count refutes the complete original four-formula conjecture at n=s=3.
No reference Challenge or admitted declaration is imported. This proof is exact
symbolic algebra and calculus; LeanCert audits kernel trust without an artificial
numerical interval certificate.
-/

set_option leancert.trust "kernel"

#assert_trust kernel NLA.RA20.hollow_variety_semantics_proved
#print axioms NLA.RA20.hollow_variety_semantics_proved
#assert_trust kernel NLA.RA20.reduced_coordinate_ring_proved
#print axioms NLA.RA20.reduced_coordinate_ring_proved
#assert_trust kernel NLA.RA20.algebraic_smooth_locus_proved
#print axioms NLA.RA20.algebraic_smooth_locus_proved
#assert_trust kernel NLA.RA20.algebraic_tangent_space_proved
#print axioms NLA.RA20.algebraic_tangent_space_proved
#assert_trust kernel NLA.RA20.full_frobenius_differential_proved
#print axioms NLA.RA20.full_frobenius_differential_proved
#assert_trust kernel NLA.RA20.hollow_distance_semantics_proved
#print axioms NLA.RA20.hollow_distance_semantics_proved
#assert_trust kernel NLA.RA20.generic_critical_locus_proved
#print axioms NLA.RA20.generic_critical_locus_proved
#assert_trust kernel NLA.RA20.component_hessians_proved
#print axioms NLA.RA20.component_hessians_proved
#assert_trust kernel NLA.RA20.generic_data_intersection_proved
#print axioms NLA.RA20.generic_data_intersection_proved
#assert_trust kernel NLA.RA20.generic_count_three_proved
#print axioms NLA.RA20.generic_count_three_proved
#assert_trust kernel NLA.RA20.generic_count_not_four_proved
#print axioms NLA.RA20.generic_count_not_four_proved
#assert_trust kernel NLA.RA20.not_criticalCountConjecture_proved
#print axioms NLA.RA20.not_criticalCountConjecture_proved
