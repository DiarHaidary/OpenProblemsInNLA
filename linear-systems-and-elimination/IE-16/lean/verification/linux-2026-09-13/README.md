# IE-16 authoritative Linux verification

The complete fifteen-export canonical proof at
`697a2a1d88337a6747aa5c82fb6e554d3ff1b356` passed [run 34774629327, job 103770408910](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34774629327/job/103770408910)
on actual non-root Ubuntu Linux. Lean’s default kernel accepted the exported
solution and Comparator accepted all fifteen approved statements. The
[raw Comparator log](operational-record/extracted/verify-20260913T182805Z-4150/comparator.log)
prints exactly `propext`, `Classical.choice` and `Quot.sound` for each theorem.

The target job itself ran both sandbox modes, four invalid-option controls,
three actual kernel replay controls, five Comparator regressions and negative
sorry/native fixtures. The separate shared checker-controls job was skipped
because shared tooling was unchanged. The target’s own controls passed.

Artifact `lean-IE-16`, ID `10322764134`, is 22,598 bytes, SHA-256
`1e1662ad25d3ea724277a840f9c4579c034cae08c9f6fce76bc08cd48795eefd`.
The original [ZIP](operational-record/artifact.zip), API receipts and raw logs
are preserved. `result.json` hashes all 281 candidate inputs. All hashes match
the immutable Git commit; the publication’s two changed metadata files must
map to exact archived candidate bytes. All mathematical input files remain
byte-identical to the accepted run.

The `operational-record` was collected and checked by the source implementer
`/root/is02_cleanup_referee`, an AI agent. Its log checks are not an independent
mathematical review. The separate [final acceptance](../../reviews/FINAL-ACCEPTANCE.json)
binds both independent final referee reports and the coordinator decision.

Lean is 4.33.1 with pinned LeanCert and Mathlib. The trusted pinned Mathlib
cache was used; no claim is made that every dependency was rebuilt from
source. No local macOS Lean/Lake or substitute sandbox run occurred during
this phase. These are AI-agent reviews, not human peer review or official
Tau Ceti endorsement.

From the problem’s `lean/` directory in a full repository checkout, run
`python3 verification/verify_publication.py` for offline source, receipt,
archive and reviewed-boundary integrity. This check does not run Lean.

For a fresh authoritative rerun on non-root Linux, with the prerequisites in
`tools/lean/HARNESS.md`, run from the clean committed repository root:

```sh
tools/lean/bootstrap.sh /tmp/nla-lean-tools
tools/lean/verify.sh linear-systems-and-elimination/IE-16/lean /tmp/nla-lean-tools
```

The completed run already supplies this evidence; no duplicate workflow is
required merely to reread these records.
