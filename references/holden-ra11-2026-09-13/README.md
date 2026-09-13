# RA-11 partial-results submission — Sidney Holden

**Author:** Sidney Holden. **Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.

Verified on 13 September 2026 against the [official Simons Foundation staff profile](https://www.simonsfoundation.org/people/sidney-holden/) and [Biological Transport Networks staff directory](https://www.simonsfoundation.org/flatiron/center-for-computational-biology/about/people/?group=biological-transport&type=ccb-staff), which identify Holden as a Flatiron Research Fellow. The institution is not asserted to endorse this submission.

[Manuscript PDF](manuscript/ra11_partial_results.pdf) · [TeX](manuscript/ra11_partial_results.tex) · [Independent review](independent-review.md) · [Original package guide](PACKAGE-README.md) · [Scope](STATUS.md).

The submission gives partial results for the retained RA-11 target. It does not determine the unrestricted adaptive minimax complexity for arbitrary PSD matrices in all parameter regimes. The matched tensor-product result requires a promise on the unknown matrix. The projection counterexample concerns a source conjecture, not a negative resolution of RA-11.

A separate Codex AI agent performed the linked informal mathematical audit. AI assistance in preparation is disclosed in the manuscript; no external human peer review, formal verification, or novelty certification is asserted. No Lean verification was performed.

## Provenance and duplicate screening

The user supplied `RA11_research_package.zip`; all original file hashes were verified before editing. `ORIGINAL-MANIFEST.sha256` records the supplied files, not the edited deliverables. The original package's internal-review wording is historical. The authored manuscript changes attribution and review disclosure only; mathematical claims are unchanged. `MANIFEST.sha256` records the final package.

Fresh upstream main and fork branches were fetched on 13 September 2026. RA-11 remains Open upstream; all-branch commit-title search and the latest 250 upstream pull-request titles found no prior RA-11 full-solution submission. This package addresses only RA-11. It preserves the existing ID, canonical path, target, ratings and source credit.

## Reproduction

Run `python tests/exact_checks.py` and `OPENBLAS_NUM_THREADS=1 python tests/numerical_checks.py` with NumPy and SymPy installed. Run `bash build.sh` with pdfLaTeX installed. Submitted results are retained under `results/`; independent rerun evidence is saved in [verification/](verification/) and described in the review. Finite checks support the audit but do not prove the quantified bounds.
