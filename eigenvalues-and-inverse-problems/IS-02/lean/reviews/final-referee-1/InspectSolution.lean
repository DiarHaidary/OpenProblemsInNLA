import Solution
set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true
#print NLA.IS02.Mat
#print axioms NLA.IS02.Mat
#print NLA.IS02.symmetric
#print axioms NLA.IS02.symmetric
#print NLA.IS02.entrywiseNonnegative
#print axioms NLA.IS02.entrywiseNonnegative
#print NLA.IS02.stochastic
#print axioms NLA.IS02.stochastic
#print NLA.IS02.symmetricStochastic
#print axioms NLA.IS02.symmetricStochastic
#print NLA.IS02.trace
#print axioms NLA.IS02.trace
#print NLA.IS02.permute
#print axioms NLA.IS02.permute
#print NLA.IS02.permutationSimilar
#print axioms NLA.IS02.permutationSimilar
#print NLA.IS02.sameSpectrum
#print axioms NLA.IS02.sameSpectrum
#print NLA.IS02.realEigenvalueMultiset
#print axioms NLA.IS02.realEigenvalueMultiset
#print NLA.IS02.spectrallyUnique
#print axioms NLA.IS02.spectrallyUnique
#print NLA.IS02.segment
#print axioms NLA.IS02.segment
#print NLA.IS02.vertex
#print axioms NLA.IS02.vertex
#print NLA.IS02.flatMatrix
#print axioms NLA.IS02.flatMatrix
#print NLA.IS02.assertedLocus
#print axioms NLA.IS02.assertedLocus
#print NLA.IS02.counterexample
#print axioms NLA.IS02.counterexample
#print NLA.IS02.targetNecessaryCondition
#print axioms NLA.IS02.targetNecessaryCondition
#print NLA.IS02.counterexampleClaim
#print axioms NLA.IS02.counterexampleClaim
#check NLA.IS02.test_membership
#assert_trust kernel NLA.IS02.test_membership
#print axioms NLA.IS02.test_membership
#check NLA.IS02.test_trace
#assert_trust kernel NLA.IS02.test_trace
#print axioms NLA.IS02.test_trace
#check NLA.IS02.test_positive_trace
#assert_trust kernel NLA.IS02.test_positive_trace
#print axioms NLA.IS02.test_positive_trace
#check NLA.IS02.test_spectrum
#assert_trust kernel NLA.IS02.test_spectrum
#print axioms NLA.IS02.test_spectrum
#check NLA.IS02.custom_to_hermitian
#assert_trust kernel NLA.IS02.custom_to_hermitian
#print axioms NLA.IS02.custom_to_hermitian
#check NLA.IS02.test_spectrum_bridge
#assert_trust kernel NLA.IS02.test_spectrum_bridge
#print axioms NLA.IS02.test_spectrum_bridge
#check NLA.IS02.test_trace_from_spectrum
#assert_trust kernel NLA.IS02.test_trace_from_spectrum
#print axioms NLA.IS02.test_trace_from_spectrum
#check NLA.IS02.test_minus_one_root
#assert_trust kernel NLA.IS02.test_minus_one_root
#print axioms NLA.IS02.test_minus_one_root
#check NLA.IS02.test_minus_one_eigenvector
#assert_trust kernel NLA.IS02.test_minus_one_eigenvector
#print axioms NLA.IS02.test_minus_one_eigenvector
#check NLA.IS02.test_quad_zero
#assert_trust kernel NLA.IS02.test_quad_zero
#print axioms NLA.IS02.test_quad_zero
#check NLA.IS02.test_pair01
#assert_trust kernel NLA.IS02.test_pair01
#print axioms NLA.IS02.test_pair01
#check NLA.IS02.test_pair02
#assert_trust kernel NLA.IS02.test_pair02
#print axioms NLA.IS02.test_pair02
#check NLA.IS02.test_pair03
#assert_trust kernel NLA.IS02.test_pair03
#print axioms NLA.IS02.test_pair03
#check NLA.IS02.test_pair12
#assert_trust kernel NLA.IS02.test_pair12
#print axioms NLA.IS02.test_pair12
#check NLA.IS02.test_pair13
#assert_trust kernel NLA.IS02.test_pair13
#print axioms NLA.IS02.test_pair13
#check NLA.IS02.test_pair23
#assert_trust kernel NLA.IS02.test_pair23
#print axioms NLA.IS02.test_pair23
#check NLA.IS02.test_single0
#assert_trust kernel NLA.IS02.test_single0
#print axioms NLA.IS02.test_single0
#check NLA.IS02.test_single1
#assert_trust kernel NLA.IS02.test_single1
#print axioms NLA.IS02.test_single1
#check NLA.IS02.test_single2
#assert_trust kernel NLA.IS02.test_single2
#print axioms NLA.IS02.test_single2
#check NLA.IS02.test_single3
#assert_trust kernel NLA.IS02.test_single3
#print axioms NLA.IS02.test_single3
#check NLA.IS02.test_three123
#assert_trust kernel NLA.IS02.test_three123
#print axioms NLA.IS02.test_three123
#check NLA.IS02.test_three023
#assert_trust kernel NLA.IS02.test_three023
#print axioms NLA.IS02.test_three023
#check NLA.IS02.test_three013
#assert_trust kernel NLA.IS02.test_three013
#print axioms NLA.IS02.test_three013
#check NLA.IS02.test_three012
#assert_trust kernel NLA.IS02.test_three012
#print axioms NLA.IS02.test_three012
#check NLA.IS02.test_spectral_uniqueness
#assert_trust kernel NLA.IS02.test_spectral_uniqueness
#print axioms NLA.IS02.test_spectral_uniqueness
#check NLA.IS02.splitId
#assert_trust kernel NLA.IS02.splitId
#print axioms NLA.IS02.splitId
#check NLA.IS02.splitSwap
#assert_trust kernel NLA.IS02.splitSwap
#print axioms NLA.IS02.splitSwap
#check NLA.IS02.test_splitId_member
#assert_trust kernel NLA.IS02.test_splitId_member
#print axioms NLA.IS02.test_splitId_member
#check NLA.IS02.test_splitSwap_member
#assert_trust kernel NLA.IS02.test_splitSwap_member
#print axioms NLA.IS02.test_splitSwap_member
#check NLA.IS02.test_midpoint_split
#assert_trust kernel NLA.IS02.test_midpoint_split
#print axioms NLA.IS02.test_midpoint_split
#check NLA.IS02.test_split_neq
#assert_trust kernel NLA.IS02.test_split_neq
#print axioms NLA.IS02.test_split_neq
#check NLA.IS02.test_counterexample_not_vertex
#assert_trust kernel NLA.IS02.test_counterexample_not_vertex
#print axioms NLA.IS02.test_counterexample_not_vertex
#check NLA.IS02.test_not_base_segment
#assert_trust kernel NLA.IS02.test_not_base_segment
#print axioms NLA.IS02.test_not_base_segment
#check NLA.IS02.test_not_one_vertex
#assert_trust kernel NLA.IS02.test_not_one_vertex
#print axioms NLA.IS02.test_not_one_vertex
#check NLA.IS02.test_not_flat_vertex
#assert_trust kernel NLA.IS02.test_not_flat_vertex
#print axioms NLA.IS02.test_not_flat_vertex
#check NLA.IS02.test_outside_locus
#assert_trust kernel NLA.IS02.test_outside_locus
#print axioms NLA.IS02.test_outside_locus
#check NLA.IS02.test_counterexample_claim
#assert_trust kernel NLA.IS02.test_counterexample_claim
#print axioms NLA.IS02.test_counterexample_claim
#check NLA.IS02.test_not_targetNecessaryCondition
#assert_trust kernel NLA.IS02.test_not_targetNecessaryCondition
#print axioms NLA.IS02.test_not_targetNecessaryCondition
#check NLA.IS02.counterexample_symmetric_nonnegative_stochastic
#assert_trust kernel NLA.IS02.counterexample_symmetric_nonnegative_stochastic
#print axioms NLA.IS02.counterexample_symmetric_nonnegative_stochastic
#check NLA.IS02.counterexample_trace
#assert_trust kernel NLA.IS02.counterexample_trace
#print axioms NLA.IS02.counterexample_trace
#check NLA.IS02.counterexample_positive_trace
#assert_trust kernel NLA.IS02.counterexample_positive_trace
#print axioms NLA.IS02.counterexample_positive_trace
#check NLA.IS02.counterexample_spectrum
#assert_trust kernel NLA.IS02.counterexample_spectrum
#print axioms NLA.IS02.counterexample_spectrum
#check NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq
#assert_trust kernel NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq
#print axioms NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq
#check NLA.IS02.counterexample_spectral_uniqueness
#assert_trust kernel NLA.IS02.counterexample_spectral_uniqueness
#print axioms NLA.IS02.counterexample_spectral_uniqueness
#check NLA.IS02.counterexample_outside_locus
#assert_trust kernel NLA.IS02.counterexample_outside_locus
#print axioms NLA.IS02.counterexample_outside_locus
#check NLA.IS02.counterexample_claim
#assert_trust kernel NLA.IS02.counterexample_claim
#print axioms NLA.IS02.counterexample_claim
#check NLA.IS02.not_targetNecessaryCondition
#assert_trust kernel NLA.IS02.not_targetNecessaryCondition
#print axioms NLA.IS02.not_targetNecessaryCondition
