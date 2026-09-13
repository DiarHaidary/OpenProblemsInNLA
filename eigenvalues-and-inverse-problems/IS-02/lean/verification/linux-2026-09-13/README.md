# IS-02 authoritative Linux verification

The complete nine-export proof passed the actual non-root Ubuntu checker at
commit `522f091b9f0d39d4846f5939bcafc1549ba16a55`:
[run 34766178560, target job 103747466088](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34766178560/job/103747466088).
The run and target job both succeeded. The [independent operational review](independent-audit/OPERATIONAL-REVIEW.md)
accepted the exact result and all 119 committed input hashes.

The sandbox probe, three kernel-replay controls, five Comparator regressions,
negative sorry/native fixtures, separate Challenge/Solution builds, nine formal
statement comparisons and default-kernel acceptance passed. Every public
export's actual Linux axiom report is exactly `propext`, `Classical.choice`
and `Quot.sound`. The separate checker-controls workflow job was skipped
because shared tools were unchanged; the target job ran all project-side
controls itself. Harmless proof linter warnings are retained.

Artifact `lean-IS-02`, ID `10320941744`, has SHA-256
`27171071d0a2087eaa63cfac39d95529f7037e7c007084852b01fae72d2afeca`.
The [original ZIP](independent-audit/lean-IS-02-artifact.zip), API receipts,
raw logs and extraction record are preserved. Lean is 4.33.1, with pinned
LeanCert and Mathlib dependencies. The trusted Mathlib cache was used;
no claim is made that every dependency was rebuilt from source.

From this problem's `lean/` directory in a full repository checkout, run
`python3 verification/verify_publication.py` with the shared metadata
requirements installed. It checks the current package, immutable reviewed
mathematical boundary, original verified inputs, archive and receipts without
network access or running Lean. Three changed metadata files have explicit
immutable candidate snapshots; all original mathematical inputs remain
unchanged in the live project. This is an offline integrity check, separate
from mathematical proof verification.

To rerun authoritative verification from a clean committed checkout on a
non-root Linux host with the prerequisites in `tools/lean/HARNESS.md`, run:

```sh
tools/lean/bootstrap.sh /tmp/nla-lean-tools
tools/lean/verify.sh eigenvalues-and-inverse-problems/IS-02/lean /tmp/nla-lean-tools
```

Two independent statement reviews preceded proof implementation; two complete
independent mathematical reviews and narrow cleanup reviews passed. AI
assistance and independent AI-agent review are disclosed. These records are
not external human peer review or official Tau Ceti endorsement.
