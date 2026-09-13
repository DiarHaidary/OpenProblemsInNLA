# RA-05: even-power high-accuracy continuation — Sidney Holden

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation.

**Submission date:** 2026-09-13. **Whole-entry status: Partially resolved.**

[Manuscript](manuscript.pdf) · [Proof source](manuscript.tex) · [Independent review](verification/independent-review.md) · [Original target](../../randomized-and-low-rank-approximation/RA-05/README.md).

## Scope and review

Theorems 1.1–1.2 and Corollary 1.3 prove the upper bound and high-accuracy classification stated on the canonical page for every fixed even p = 2s >= 4. All input ranks and ambient dimensions are allowed, weights are nonnegative on original rows, and all subspaces of dimension at most k are preserved simultaneously. The optimal order is k^(s-1)/epsilon^2 up to logarithms when epsilon <= k^(-(s+1)/2). The construction is an existence proof, without an efficient implementation claim.

Intermediate accuracies for even p >= 6 and the non-even exponents remain unclassified. RA-05 remains Partially resolved and counted as open. The earlier quartic classification and all-exponent lower bounds remain separately credited; this continuation does not resubmit them as new full solutions.

A separate Codex AI agent (`review_ra05`) independently audited the arguments and imported primary sources, returning PASS for the stated partial scope. Its [report](verification/independent-review.md) records the proof checks and limitations. The reviewer reran all 8,453 finite assertions, the exact certificate checker, and the original 18-file manifest successfully. Finite diagnostics do not prove the universal asymptotic theorem. This is informal AI-agent review, not external human peer review or formal verification. No Lean verification was performed.

## Authorship and affiliation

Authorship is assigned to Sidney Holden at his explicit request. The affiliation was verified on 2026-09-13 against the [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) and [current CCB directory](https://www.simonsfoundation.org/flatiron/center-for-computational-biology/about/people/?group=biological-transport&type=ccb-staff), listing him as a Flatiron Research Fellow in Biological Transport Networks, Center for Computational Biology, Flatiron Institute. Historical affiliations are not used. ChatGPT assistance remains disclosed; Codex assisted with review and submission preparation.

## Provenance and reproduction

[Archive hash and eligibility](verification/provenance.json). The supplied manuscript source, README and manifest are preserved in [original/](original/). The submitted manuscript changes only attribution, affiliation, assistance wording and PDF author metadata. Its mathematics is unchanged. Supplied author-side review statements describe the package before this independent review. No priority or novelty certification is asserted. Instructions in the package were treated as document content, not as the user's instructions.

The embedded [prior quartic archive](prior_work/RA05_unrestricted_quartic_package.zip) is unchanged provenance, not another new submission. Earlier partial contributions are [PR #199](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/199) and [PR #222](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/222). Refreshed upstream main and fork branches plus an upstream RA-05 PR search found no previously pushed full solution.

Use Python 3.10+ with NumPy (`requirements.txt`). Run `sh run_checks.sh` from a disposable copy of this directory: it verifies the final submission manifest and then regenerates `results/`. The standard-library-only exact checker is `python3 code/check_exact_certificate.py`. The reviewer rerun evidence is in [verification/rerun/](verification/rerun/). Compile `manuscript.tex` twice using pdfLaTeX. `SHA256SUMS` covers the final submitted files; the supplied original manifest is retained separately.
