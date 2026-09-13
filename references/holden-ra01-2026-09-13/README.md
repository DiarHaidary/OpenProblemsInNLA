# RA-01: tail-envelope guarantees and a clock obstruction

**Author:** Sidney Holden.  
**Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.  
**Submission date:** 13 September 2026.  
**Disposition:** Independently audited partial results; unrestricted RA-01 remains open.

[Attributed manuscript](report.pdf) · [Editable source](report.tex) · [Independent review](independent-review.md) · [Retained canonical problem](../../randomized-and-low-rank-approximation/RA-01/README.md).

## Result and policy comparison

Theorems 4.1, 5.1 and 6.1 establish the original expected relative trace-error guarantee at the requested pivot count under half-geometric, inverse-square and fixed summable power tail envelopes, respectively. Their constants are 3, 4 and an explicit finite constant depending only on the fixed exponent. Tail indices start after the target rank and the scale is the first tail eigenvalue. The original complex Hermitian model, adaptive residual-diagonal pivot probabilities, arbitrary head spread, all tolerances, zero-tail termination and dimension cap are retained.

The unrestricted-spectrum target is neither proved nor refuted. Theorem 7.1 disproves only an auxiliary continuous-time count bound with unit tail coefficient; Proposition 8.1 exposes saturation of a determinant upper comparison. Under [the repository policy](../../RESOLVED.md#recording-a-new-resolution), this warrants **Partially resolved**, retaining the general target in the open count, not Solved. Earlier nested packages, including their claimed universal lower bound, are provenance rather than newly accepted resolutions.

## Authorship and affiliation

Sidney Holden is credited at the submitting user's express request. On 13 September 2026, the [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) identified Sidney Holden as a Flatiron Research Fellow in Biological Transport Networks at the Center for Computational Biology, Flatiron Institute. The [official current staff directory](https://www.simonsfoundation.org/flatiron/about/people/page/3/?type=42) corroborated that role. These current institutional sources support the affiliation above; the older Edinburgh student profile was not used as a current affiliation.

AI assistance was used for the independent mathematical audit and submission preparation. The audit was performed by a separate Codex agent, identified in its report. It is informal automated review, not external human peer review, proof-assistant verification, or a certificate of historical novelty. No Lean verification was performed.

Credit for the RPCholesky algorithm, determinant-path method, spectral coefficient techniques and classical product identity remains with the sources cited in the manuscript and [submitted source audit](submitted/SOURCE_AUDIT.md), including Chen, Epperly, Tropp, Webber, Divan and Gilles.

## Review and reproduction

The [independent audit](independent-review.md) passed the stated partial results and examined the general analytic proofs, not just finite tests. The reviewer verified all 18 manifest entries before regeneration and reran all 8,500 exact rational checks on eight matrix cases. A separate submission-agent rerun passed both real and complex order-11 exhaustive floating cases and 1,200 Monte Carlo trajectories over six cases. The optional floating program required the bundled NumPy runtime. These finite checks support only their finite calculations.

Preserve the supplied snapshot when reproducing: copy `submitted/` to a temporary directory and run there:

```sh
python3 code/verify_manifest.py
python3 code/verify_exact.py
OPENBLAS_NUM_THREADS=1 python3 code/verify_floating.py
```

The last command needs NumPy. The fresh [exact results](verification/exact_results.json) and [floating results](verification/floating_results.json) are separate from the original evidence. Timing fields change on rerun. Build the attributed report with two runs of `pdflatex report.tex` from this directory. [Build output](verification/report-build.log) and [publication checks](verification/publication-checks.json) document the submission preparation.

## Provenance and duplicate screening

All 19 files in `RA01_round4_tail_analysis.zip` are retained byte-for-byte under [submitted/](submitted/README.md), including its original manuscript, code, logs, manifest and nested previous-round ZIP. The original archive SHA-256 is `fa0165507c6a18a21509b5cfa28a977fa7980374880eda034748b63e2215af89`. The authored report adds Sidney Holden, the verified affiliation, date and PDF author metadata, and updates the abstract and Section 9 to distinguish the original delivery state from the completed informal audit and repository submission. Sections 1–8 and the bibliography are byte-identical to the independently reviewed original. Statements about lack of review in the preserved snapshot describe its historical delivery state.

Current upstream main was `b73cd1804e40e0d101294eedb156984f0d62b4a6` when the new branch was created. All 57 fetched origin/upstream branch heads retain RA-01 as Open; an all-history commit-message search found no RA-01 submission. Authenticated all-state upstream PR and issue searches for RA-01 and the fork's PR search found no previously pushed full RA-01 solution. Matches concerning RA-02/RA-03 explicitly address different same-rank targets. This is a bounded public/repository screening, not a claim about inaccessible work or all literature.

The current Epperly and Divan-Gilles primary manuscripts linked in the source audit were opened during preparation; this submission preserves their attribution and makes no priority claim. The permanent RA-01 ID, canonical path, original mathematical statement, references and prior audit are unchanged. The new pull request is directed to upstream `main` for maintainer review.
