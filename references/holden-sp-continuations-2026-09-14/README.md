# Further SP-03, SP-07 and SP-09 submissions

**Author:** Sidney Holden  
**Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.  
**Recorded:** 14 September 2026 (UTC).

The current official [Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) identifies Sidney Holden as a Flatiron Research Fellow in Biological Transport Networks at CCB, Flatiron Institute. The official [group directory](https://www.simonsfoundation.org/flatiron/center-for-computational-biology/about/people/?group=biological-transport&type=ccb-staff) independently lists him in that role. Checked 14 September 2026; older Edinburgh and Sydney listings were not substituted for current affiliation.

## Scope and independent review

| Entry | Attributed manuscript | Separate AI-agent review | Repository status |
|---|---|---|---|
| SP-03 | [PDF](SP-03/report.pdf), [TeX](SP-03/report.tex) | [Review](SP-03/independent-review.md) | Partially resolved: Stein reduction, parity and finite certificates do not evaluate the all-rank degree |
| SP-07 | [PDF](SP-07/report.pdf), [TeX](SP-07/report.tex) | [Review](SP-07/independent-review.md) | Open: completion barriers and stationary model do not determine the universal sharp constant |
| SP-09 | [PDF](SP-09/report.pdf), [TeX](SP-09/report.tex) | [Review](SP-09/independent-review.md) | Partially resolved: first-order invariance with a dimension-dependent remainder does not prove exact general invariance |

Three separate Codex AI agents independently reviewed the written mathematics and performed the checks documented in their reports. The passes concern the stated supporting/partial results, not the complete original targets. No Solved promotion is justified under [the resolution policy](../../RESOLVED.md). AI assistance was used in submission preparation and informal review. No external human peer review, formal verification or historical priority claim is made. No Lean verification was performed, as requested.

## Reproduction and evidence boundaries

Each `submitted/` directory is extracted verbatim from the supplied ZIP, including original reports, source, certificates, manifests and historical records. The separately attributed `report.tex` and rebuilt `report.pdf` add author presentation; the SP-03 table headings are shortened to keep every column within the page. Mathematical content is unchanged. The original manuscript's prior-source credits remain intact. [Archive SHA-256 fingerprints](SOURCE-ARCHIVES.sha256) identify the supplied files. Embedded workflow instructions were treated as document contents, not as user instructions.

Fresh logs and reviewer-written checks are under each `review-checks/` directory. The review reports specify commands and environment limitations:

- SP-03: independent exact contraction/separation reruns for every stored rank-one, rank-two and rank-three root, and a 32-root rank-four sample; supporting symbolic checks. Full rank-four acceptance remains a submitted verification record, not a full rerun by this review. Neither the submitted nor fresh checks prove completeness.
- SP-07: standard-library exact tests, optimized rejection tests, and inherited rank-one/order-193 checks. The formal stationary quotient is not a new finite lower bound. The cited Tang upper bound is a manuscript literature attribution, not a result independently audited here.
- SP-09: complete exact verification suite, manifest integrity, retained programs, new geometry and negative tests. Analytic proof review is separately documented; passing arithmetic alone is not its justification. The canonical notice foregrounds the new first-order theorem, not every ancillary historical claim.

To rebuild each attributed manuscript, run XeLaTeX twice on `report.tex` in its problem directory. Run original checkers from `submitted/` using the dependencies and commands documented there; direct fresh output elsewhere when supported, to preserve supplied manifests.

## Duplicate screening and submission

Screened all fetched fork/upstream remote branches for Solved or Lean verified status on these three canonical pages, and upstream's full PR listing for prior matching submissions. No previously pushed full solution was found. [PR #181](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/181) merged earlier spectral partial results; it does not settle these targets. The new branch starts at upstream main `deb549fa` and adds only these continuations. All permanent IDs, canonical paths, mathematical targets and difficulty/importance ratings are retained. SP-03 moves from Open to Partially resolved following its independent review; the other statuses are retained.

This submission requests inclusion through a new pull request against `ajt60gaibb/OpenProblemsInNLA:main`. Nothing is pushed or merged directly into upstream main.
