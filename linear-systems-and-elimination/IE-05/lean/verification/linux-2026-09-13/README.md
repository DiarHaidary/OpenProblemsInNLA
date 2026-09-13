# IE-05 authoritative Linux verification

This directory records the successful IE-05 target job from workflow
[34751393873, attempt 1](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34751393873/attempts/1)
at candidate revision `71cf72f9db2af0f01b5cfa7f18a69e28310eb52f`.
The target job was `103708463461`; it ran on Ubuntu 24.04 with Lean 4.33.1,
the default Lean kernel, the configured Comparator, and the real sandbox.

The extracted target artifact is retained under `artifacts/lean-IE-05/`.
The independent read-only operational audit is retained under
`independent-audit/`; its sealed report is
[`OPERATIONAL-REVIEW.md`](independent-audit/OPERATIONAL-REVIEW.md), and its
outer evidence seal is
[`EVIDENCE-MANIFEST.json`](independent-audit/EVIDENCE-MANIFEST.json).
Run `python3 independent-audit/verify.py` to check that seal without running
Lean or changing the candidate.

The target job accepted all 17 exports, reported only the standard axioms
`propext`, `Classical.choice`, and `Quot.sound`, and passed the default-kernel,
Comparator, native/sorry rejection, and sandbox controls. The independent
review verified the GitHub artifact digests, candidate input hashes, source
lock, and the retained historical inventories. The initial workflow's only
failures were unrelated elan-download HTTP 500 errors in MI-06 and RA-07;
the later authorized failed-job retry completed successfully, but is not used
as a substitute for the sealed attempt-1 target evidence.

This is a verification archive, not a new mathematical claim. The proof's
scope and two final mathematical reviews remain documented in the project
root and `reviews/`.
