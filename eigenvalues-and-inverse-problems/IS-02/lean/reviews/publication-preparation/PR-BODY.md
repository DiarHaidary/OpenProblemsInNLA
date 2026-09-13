## Change

Add the complete IS-02 Lean formalization and promote the existing entry from `Solved` to `Lean verified`. The original problem ID, path, mathematical target and informal manuscript remain unchanged.

Formalization: **George Stepaniants**, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. The original mathematical resolution remains credited to **Matthew J. Colbrook**, Department of Applied Mathematics and Theoretical Physics, University of Cambridge.

## Mathematical evidence

The source is *Theorem IS-02, Sections 1–2* of the retained complete manuscript. `NLA.IS02.counterexample_claim` proves the order-four witness is spectrally unique among every real symmetric stochastic competitor and lies outside all three original segment families with genuine vertices. `NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq` preserves eigenvalue multiplicities. `NLA.IS02.not_targetNecessaryCondition` negates the complete universal target; no case remains open in the original truth question.

The [immutable proof revision](https://github.com/sgstepaniants/OpenProblemsInNLA/tree/522f091b9f0d39d4846f5939bcafc1549ba16a55/eigenvalues-and-inverse-problems/IS-02/lean) pins Lean 4.33.1, LeanCert `621a43d7cf21f87872392a01e874f2f1dbddc926`, and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. Two independent statement reviews preceded implementation; two independent complete mathematical reviews and narrow cleanup reviews passed. AI assistance and agent review are disclosed; no human peer review or Tau Ceti endorsement is claimed.

All nine statements passed [actual non-root Ubuntu verification](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34766178560/job/103747466088), including Comparator, default-kernel replay, sandbox probes, three kernel controls, five Comparator regressions and negative axiom controls. Every export's actual Linux transitive axiom report contains exactly `propext`, `Classical.choice`, and `Quot.sound`. The raw ZIP, API receipts, logs and independent operational audit are retained under `lean/verification/linux-2026-09-13/`. All 119 original input hashes remain checkable; the three changed metadata files have exact immutable candidate snapshots.

Reproduce authoritative checking from a clean committed checkout on non-root Linux using `tools/lean/bootstrap.sh /tmp/nla-lean-tools`, then `tools/lean/verify.sh eigenvalues-and-inverse-problems/IS-02/lean /tmp/nla-lean-tools`, with the prerequisites in `tools/lean/HARNESS.md`. For offline integrity checking, run `python3 verification/verify_publication.py` from the problem's `lean/` directory with `tools/lean/requirements.txt` installed. The Linux run uses the pinned trusted Mathlib cache; it does not claim to rebuild every dependency from source.

## Documents checked

Updated and inspected the canonical README, standalone TeX and two-page PDF, Lean guide, `formalization.yaml`, Linux evidence guide, existing `RESOLVED.md` entry and regenerated indexes. The original target and informal `solution.md`, `solution.tex` and `solution.pdf` remain byte-identical. The PDF was visually reviewed on both pages after two page-break-only layout corrections. Permanent-ID validation, all 17 numbering tests, manifest/coverage checks and offline publication integrity checks pass. Shared Lean tools and the permanent registry are unchanged.

Please merge this complete per-problem formalization into `main`.
