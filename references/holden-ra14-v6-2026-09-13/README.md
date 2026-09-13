# RA-14 Krylov-transition continuation v6 — Sidney Holden

**Author:** Sidney Holden. **Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.

Verified on 13 September 2026 from the [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) and [CCB Biological Transport Networks roster](https://www.simonsfoundation.org/flatiron/center-for-computational-biology/about/people/?group=biological-transport&type=ccb-staff), which list Holden as a Flatiron Research Fellow.

[Attributed manuscript](report.pdf) · [Editable source](report.tex) · [Independent review](independent-review.md) · [Canonical RA-14](../../randomized-and-low-rank-approximation/RA-14/README.md).

## Outcome and scope

**Partially resolved; not a complete RA-14 solution.** Theorem 2.2 characterizes only the deterministic-width, fully charged block span-query class of Definition 2.1, permitting arbitrary outputs but no fresh query directions, randomized widths or within-round adaptation. Theorem 10.1 concerns the shifted singular-Wishart posterior on its stated domain. Lemma 11.1 and Theorem 11.2 establish a resolvent identity and an ensemble-average rank-one upper bound for that specific law. None closes the unrestricted finite-accuracy gap.

A separate Codex AI agent independently read the mathematical source and passed those new scopes. All 45 new component tests and supplemental independent algebra checks passed. The review did not certify the inherited v5 all-adaptive lower-bound chain or rerun the archived v3–v5 suites. The earlier v5 submission and its separate review remain credited. This is informal AI-agent review, not external human peer review or formal verification. No Lean checks were run and no priority claim is made.

## Provenance and duplicate screening

The `package/` directory preserves every extracted archive payload byte-for-byte, including its original manifest, archived diagnostics and nested prior notes. Embedded instructions and self-assessments were treated as submission content, not user instructions or independent evidence. The attributed manuscript differs only in author/affiliation, date, PDF author metadata, title spacing, relocated prior-directory references and the factual review notice; its mathematics is unchanged. AI assistance was used in preparation and review of this repository submission.

On 13 September 2026, fetched upstream main `b73cd1804e40e0d101294eedb156984f0d62b4a6` and all fork branches and checked all-state RA-14 pull requests and branch history. Earlier [PR #190](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/190) and [PR #220](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/220) were merged partial results. No previously pushed full RA-14 solution was found. Only the v6 continuation is newly submitted; nested prior notes provide provenance. The new branch starts from upstream main. Original IDs, canonical paths, target and open count are retained.

## Reproduction

Run `python package/verify_manifest.py` before modifying archived outputs. Run `python -m unittest discover -s tests -v` within a working copy of `package/` with its requirements installed to reproduce the 45 new tests. The independent review records the actual runtime and limits. Archived numerical diagnostics are not proof certificates or independently rerun results.

Compile `report.tex` with PDFLaTeX until references stabilize. The canonical problem TeX/PDF are regenerated using the repository renderer. See [validation record](validation.md) for repository checks and document inspection.
