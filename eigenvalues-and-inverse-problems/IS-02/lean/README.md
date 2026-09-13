# IS-02 complete Lean formalization

This package verifies the complete negative resolution of IS-02. All nine
exports passed independent mathematical reviews and actual non-root Linux
Comparator, permitted-axiom and default-kernel checks. The
[Linux record](verification/linux-2026-09-13/README.md) retains the raw evidence
and independent operational audit. It proves the exact 4 by 4 counterexample, the
characteristic-polynomial/eigenvalue-multiset bridge for real symmetric
matrices, spectral uniqueness up to permutation, exclusion from the complete
vertex-segment locus, and the resulting negation of the universal target.

The original mathematical counterexample remains credited to Matthew J.
Colbrook, Department of Applied Mathematics and Theoretical Physics,
University of Cambridge. The formalization is by George Stepaniants, Department of
Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA.

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
two complete independent mathematical reviews and narrow cleanup checks have
approved the proof. The separate actual Linux Comparator, default-kernel and
permitted-axiom verification passed on the immutable revision recorded above.
Those Linux receipts identify the exact checked source; local checks alone
are not presented as Linux verification.

The statement approvals, source correspondence, pinned manifest, and exact
frozen hashes are retained in `reviews/` and `SOURCE_MAP.md`.

The complete final reports, preserved old-source records, exact cleanup
correspondence and current proof hashes are in `reviews/FINAL-ACCEPTANCE.json`.
Run `python3 verification/verify_publication.py` from a full repository checkout
to check the package inventory, immutable reviewed source, original Linux
inputs and retained receipts offline; that integrity check does not run Lean
or replace mathematical review.
