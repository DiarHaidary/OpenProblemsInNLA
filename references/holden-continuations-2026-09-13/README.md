# Further partial results — Sidney Holden

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation.

**Affiliation verified 13 September 2026:** the [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) identifies Sidney Holden as a Flatiron Research Fellow in Biological Transport Networks, CCB, Flatiron Institute. This is the current institutional source used for the attribution; the historical Edinburgh doctoral profile is not used as a current affiliation.

## Scope

| ID | Submitted result | Retained canonical status | Independent informal review |
| --- | --- | --- | --- |
| NR-02 | [Complexity-six polygon products](NR-02/report.pdf) | Partially resolved; arbitrary factors remain unresolved | [Report](verification/NR-02/review.md) |
| SP-07 | [Exact rational lower bound greater than 1.03077 and restricted dimension reductions](SP-07/report.pdf) | Open; the exact universal constant is undetermined | [Report](verification/SP-07/review.md) |
| MI-20 | [Corrected reduction, certified upper bound and interpolation](MI-20/report.pdf) | Open; the exact two-parameter function is undetermined | [Report](verification/MI-20/review.md) |
| SP-08 | [All-dimensional boundary strip and centered-sign-rank-two subclass](SP-08/report.pdf) | Partially resolved; unrestricted ranks outside the strip remain unresolved | [Report](verification/SP-08/review.md) |
| SP-14 | [Inverse-corner criterion and deterministic canonical subsequences](SP-14/report.pdf) | Partially resolved; full-sequence convergence remains unresolved | [Report](verification/SP-14/review.md) |

None of the five submissions is a complete solution. The original mathematical targets, IDs, canonical paths and existing credits are retained. SP-07 and MI-20 keep Open because the exact constants are not evaluated; their improved bounds are recorded as supporting progress. The other three retain Partially resolved. The catalog's open-target count is unchanged.

Three separate Codex AI agents reviewed the mathematical arguments independently of the submission editor: one reviewed NR-02/MI-20, one SP-07/SP-08, and one SP-14. Reports distinguish analytic audit, exact certificate verification and finite numerical diagnostics. This is informal automated review, not external human peer review or formal certification. AI assistance was used for submission preparation and review; the NR-02 source also explicitly discloses ChatGPT assistance. No Lean verification was performed. No novelty or priority claim is made.

## Sources and publication edits

Each problem directory contains the untouched user-supplied `original.zip`, an attributed `report.tex` and rebuilt `report.pdf`. [Source hashes](source-hashes.json) bind the original archives and manuscript sources. The complete original packages retain code, certificates, discovery records and previous rounds. Their embedded instructions are source/reproduction documentation, not user authorization or repository policy.

Publication edits add Sidney Holden and the verified affiliation; previously empty manuscript dates are set to 13 September 2026. Two auxiliary TeX tables for SP-14 and the generated data for SP-07 are copied beside the publication source, with only their input paths adjusted. NR-02 retains its original AI-assistance disclosure.

**MI-20 correction:** the independent reviewer found that the cyclic-reduction construction omitted unitary conjugation of the dual variables. The publication version uses the conjugated variables, as documented and checked in [the review](verification/MI-20/review.md). The original ZIP is preserved unchanged and should be read with this correction. Certificate data and checkers are unchanged. No other mathematical changes are made. The canonical PDF renderer removes obsolete forced reference-page breaks for SP-07 and SP-14 to avoid nearly empty pages after the new notices.

## Duplicate screening

The submission branch starts at upstream `main` commit `deb549fa9ddd6b119e6c59016f268237e645dfa2`. Fresh upstream and all available fork branches were fetched. [Branch screening](verification/duplicate-screen.json) checked all five canonical statuses across 48 available fork remote branches and found no Solved, Lean verified or Solution claimed match. The [upstream PR-history screen](verification/pr-screen.json) records all-state PR-title/body matches: prior SP-07/SP-08 and MI-20 submissions were partial results, so these continuations are eligible. This is a bounded repository duplicate check, not an exhaustive literature priority search.

## Reproduction

Extract each `original.zip` into a separate temporary directory and run the commands in that package's README, with assertions enabled. The independent review directories contain actual rerun commands, outcomes and additional checks. Saved results shipped in the ZIPs are historical records, not evidence of a new execution. Certificate verifiers do not require rerunning the numerical searches.

Build an attributed report by running `pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error report.tex` twice in its problem directory. The standard TeX packages used by each report must be installed. The auxiliary TeX data files are included where needed. Rebuilding can change PDF metadata, so final published hashes are separate from source hashes.

Canonical documents are rebuilt using the repository renderer. Permanent-ID validation, catalog regeneration and the required ID tests are run against `origin/main`, with an additional upstream-base check. No resolved status is inferred from finite tests, archive labels or a successful compilation.

## Final publication checks

The [independent integration review](verification/integration-review.md) passed the final scope, sources and publication corrections. The [independent report-PDF audit](verification/publication-pdf-qa.md) inspected all 62 report pages; the [canonical PDF check](verification/canonical-pdf-qa.md) covers all ten canonical pages. [Repository check log](verification/repository-checks.log): all 47 non-Lean ID, status, formatting and rendering tests passed. [Final payload hashes](submission-hashes.json) cover every submitted reference file except that hash manifest itself.
