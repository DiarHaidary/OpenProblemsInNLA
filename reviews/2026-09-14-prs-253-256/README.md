# Maintainer audit of PRs 253-256

14 September 2026. All four exact PR revisions pass the current independent informal audit, with the integration corrections listed below. This is AI-assisted mathematical review, not external human peer review or formal verification. No Lean verification is claimed for any new result.

| PR | Reviewed source head | Accepted outcome |
| --- | --- | --- |
| [253](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/253) | `43183e8254d121aa4b365fdd34643cc4c91d8503` | RA-05 Solved; TR-03, RA-11, SP-10, RA-14 retain partial scopes |
| [254](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/254) | `0ea258baa0bde427540dfb64fee7dfff95e6498c` | Five limited results accepted; original statuses retained |
| [255](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/255) | `ecc57b82bbcb33aa37dd403530669f74bdf2ec30` | SP-03 Partially resolved; SP-07 Open; SP-09 Partially resolved |
| [256](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/256) | `b84772b48cd26a2e763ecc52a6243e8f0c34681f` | Verified NM-01 reference with precise scope context |

Published comparison base: `deb549fa9ddd6b119e6c59016f268237e645dfa2`. Exact source commits are retained as ancestors, preserving contributor attribution. Final CI and publication receipts are recorded on the integration pull request to avoid changing a checked commit merely to add its own receipt.

## Independent mathematical findings

- [RA-05 full review](pr253-ra05-review.md): both complete proof parts and primary dependencies support the full even/non-even classification, with arbitrary rank and dimension, nonnegative original-row weights and every allowed accuracy. The additional proposal is false. Fresh optional high-precision diagnostics and corrupted-certificate controls also pass. This supports Solved, not Lean verified.
- [Other PR253 targets](pr253-other-review.md), with a second [RA-14 adaptive-coupling review](pr253-ra14-adaptive-supplement.md): all four limited claims pass; no unrestricted target is closed.
- [PR254 review](pr254-review.md): all five advertised scopes pass, including the complete ten-case polygon refutation replay through four checker implementations. The MI-20 publication correction is sound and now consistently disclosed.
- [PR255 review](pr255-review.md): all 31,183 stored rank-four SP-03 centers were freshly checked with exact contraction and full-file separation, as were all lower-rank centers. This strengthens the submitted audit's sampled replay. The resulting degree lower bounds are not completeness claims. SP-07's stationary quotient is not a finite normal-matrix lower bound; SP-09's first-order estimate remains at fixed amplification.
- [PR256 reference review](pr256-review.md): the early NMF/VolMin discussion motivates the canonical decision question without stating that exact promise formulation.

The submitted historical reports remain untouched and accurately describe what their reviewers did. This dated maintainer record adds the new checks, including the full SP-03 replay and previously unavailable optional RA-05/SP-10 checks. Finite assertion totals are bookkeeping, not a measure of theorem completeness. Primary imports, omitted historical claims and computational limitations are identified in each report.

## Integration corrections and preservation

Both SP-07 notices are retained, and its canonical TeX/PDF is regenerated from their union. MI-20's reference README now explicitly discloses the conjugation correction already present in its publication report; the original ZIP is unchanged. NM-01 keeps the new citation with a concise paraphrase and a statement of its broader scope; its canonical TeX/PDF is synchronized. The renderer removes only obsolete forced reference-page breaks for RA-11, RA-14, SP-07, SP-14 and NM-01. All source manuscripts and certificate payloads are unchanged.

Catalog regeneration combines the two status transitions: **42 Open, 73 Partially resolved, 72 Solved, 30 Lean verified**, totaling **217 permanent IDs and 115 open targets**. Difficulty and importance flags are unchanged and consistent with the retained targets. Existing solved/partial history is retained in RESOLVED.md.

[Exact preservation](preservation.json) and the [independent integration review](integration-independent-review.md) confirm all 24,984 previously published paths, all 3,464 previous reference files, every canonical mathematical target and prior credit, and all 612 source-added paths survive. One source-added prose file (MI-20's reference README) has the disclosed correction; all other added blobs are exact. The registry is unchanged. No Lean project, workflow, checker or test safeguard is changed. The preserved-tree receipt is tied to the content integration commit; later changes only add this audit bundle.

## Checks and reproduction

Permanent-ID validation preceded catalog generation; all 17 ID safeguard tests pass. All **77 repository tests**, including renderer, status, selection and proof-harness gates, pass after the final layout correction. Global math formatting passes. A full diff against the published base reports Markdown hard-break spaces and whitespace in retained submission/evidence files; these are preserved to keep the source payloads and raw evidence exact. The working tree is clean. [Lean project selection](lean-selection.json) is empty, correctly reflecting the absence of formalization changes. Detailed mathematical replays are linked above; original checker code remains in the exact source packages.

All relevant publication and canonical PDF pages were rasterized and visually inspected by the assigned reviewers. [Final root PDF hashes and QA](root-pdf-qa.json) cover the combined and edited outputs; other reports include their own QA evidence. NM-01's initial mostly empty page was corrected and the final two-page version rechecked.

The small evidence folders retain fresh raw outputs, reviewer-written checks and source hashes. Raw logs retain their actual disposable execution paths. Reproduction uses scratch copies of the immutable source packages, with path adjustment as documented in the reports. Do not run scripts that overwrite diagnostics directly in the published source snapshots. `verify_preservation.py --repo /path/to/repository --ref HEAD --out /tmp/preservation.json` can recheck the integration, including after publication.

`EVIDENCE-SHA256.json` covers every file in this audit directory except itself. No scratch archive copies, compiled checkers or PDF rasterizations are committed.
