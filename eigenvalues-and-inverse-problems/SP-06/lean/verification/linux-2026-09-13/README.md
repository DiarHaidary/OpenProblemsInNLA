# SP-06 authoritative Linux verification

The complete twenty-export proof passed the actual non-root Ubuntu checker at
commit `3122d69460b0ed6dda3ea00dfaa899f93411ce2f`:
[run 34765629739, target job 103745998196](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34765629739/job/103745998196).
The run and target job both succeeded. The [independent operational review](independent-audit/OPERATIONAL-REVIEW.md)
accepted the exact result and all 61 committed input hashes.

The actual sandbox probe, three kernel replay controls, five Comparator
regressions, negative sorry/native fixtures, fresh Challenge/Solution builds,
twenty formal statement comparisons and default-kernel acceptance passed.
Only `propext`, `Classical.choice` and `Quot.sound` were permitted. Separate
per-export axiom reports are retained with the local mathematical reviews;
the Linux result enforces the permitted closure. The separate checker-controls
workflow job was skipped because shared tools were unchanged; the target job
ran all project-side controls itself.

Artifact `lean-SP-06`, ID `10320127872`, has SHA-256
`fac2ebe5f81ec421a7b478fcbd1a11768887b8678ad5d166adac3a1402aece6c`.
The [original ZIP](independent-audit/lean-SP-06-artifact.zip), API receipts,
raw logs and extraction record are preserved. Lean is 4.33.1, with pinned
LeanCert and Mathlib dependencies; the trusted Mathlib cache was used.
No claim is made that every dependency was rebuilt from source.

From the problem's `lean/` directory in a full repository checkout, run
`python3 verification/verify_publication.py` with the shared metadata
requirements installed to check the complete current package, reviewed
mathematical boundary, original verified inputs, ZIP members and receipts.
It is an offline integrity check, separate from mathematical verification.
Three changed metadata files have explicit immutable candidate snapshots;
every original mathematical input remains unchanged in the live project.

To rerun authoritative verification from a clean committed checkout on a
non-root Linux host with the prerequisites in `tools/lean/HARNESS.md`, run:

```sh
tools/lean/bootstrap.sh /tmp/nla-lean-tools
tools/lean/verify.sh eigenvalues-and-inverse-problems/SP-06/lean /tmp/nla-lean-tools
```

AI assistance and independent AI-agent reviews are disclosed. These records
are not human peer review or official Tau Ceti endorsement.
