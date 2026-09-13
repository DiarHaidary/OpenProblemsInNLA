# IS-02 Lean formalization

This package contains a complete proof candidate for the frozen IS-02
statement boundary. It proves the exact 4 by 4 counterexample, the
characteristic-polynomial/eigenvalue-multiset bridge for real symmetric
matrices, spectral uniqueness up to permutation, exclusion from the complete
vertex-segment locus, and the resulting negation of the universal target.

The canonical problem and its mathematical solution remain credited to Matthew
J. Colbrook. The formalization is by George Stepaniants, Department of
Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA. George's email is intentionally omitted.

`Definitions.lean` and `Challenge.lean` preserve the independently reviewed
statement boundary. `Solution.lean` proves the same nine declarations in a
separate module and does not import `Challenge.lean`. The implementation uses
only exact rational matrix identities and finite algebra; `norm_num`, `ring`
and `linarith` discharge the identities, while LeanCert audits the resulting
declarations in kernel-trust mode. No numerical interval certificate is
needed. `Solution.lean` imports LeanCert's verification command, sets kernel
trust, and performs explicit `#assert_trust kernel` checks.

The local proof-stage direct Lean check passed with the pinned Lean 4.33.1 and
pre-existing dependency artifacts; set `IS02_DEP_ROOT` to the existing
`.lake/packages` directory and see
[`verification/proof-typecheck.md`](verification/proof-typecheck.md) and
[`verification/proof-typecheck.sh`](verification/proof-typecheck.sh). The
script checks all ten manifest revisions and clean tracked dependency trees,
then preserves raw commands and results in its fresh private prefix. The
authoritative Linux Comparator run, independent final proof reviews, and
catalog promotion remain pending. This package does not itself change the
canonical problem status.

The statement approvals, source correspondence, pinned manifest, and exact
frozen hashes are retained in `reviews/` and `SOURCE_MAP.md`.
