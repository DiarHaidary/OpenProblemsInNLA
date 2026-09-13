/-
NR-03 modular public export assembly.

The proof declarations are defined in the bounded modules imported below.
The ten trust checks are retained for the eventual authoritative harness; this
diagnostic source is not itself a verification result.
-/
import NLA.NR03.Rank
import LeanCert.Tactic.Verification

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
set_option leancert.trust "kernel"
open scoped BigOperators Matrix
noncomputable section

/- Remote diagnostics: all public Comparator exports are checked only when
   an authoritative remote harness executes this file. -/
#assert_trust kernel NLA.NR03.cMatrix_nonnegative
#print axioms NLA.NR03.cMatrix_nonnegative
#assert_trust kernel NLA.NR03.boolVec_seven_card
#print axioms NLA.NR03.boolVec_seven_card
#assert_trust kernel NLA.NR03.nonnegative_rank_attained_minimal
#print axioms NLA.NR03.nonnegative_rank_attained_minimal
#assert_trust kernel NLA.NR03.rank_le_of_factorization
#print axioms NLA.NR03.rank_le_of_factorization
#assert_trust kernel NLA.NR03.scaled_certificate_gives_factorization
#print axioms NLA.NR03.scaled_certificate_gives_factorization
#assert_trust kernel NLA.NR03.witness_scaled_certificate
#print axioms NLA.NR03.witness_scaled_certificate
#assert_trust kernel NLA.NR03.witness_factorization
#print axioms NLA.NR03.witness_factorization
#assert_trust kernel NLA.NR03.witness_rank_upper_bound
#print axioms NLA.NR03.witness_rank_upper_bound
#assert_trust kernel NLA.NR03.witness_not_full_rank
#print axioms NLA.NR03.witness_not_full_rank
#assert_trust kernel NLA.NR03.not_targetStatement
#print axioms NLA.NR03.not_targetStatement
