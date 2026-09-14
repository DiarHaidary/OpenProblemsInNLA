# Further submissions by Sidney Holden

**Author:** Sidney Holden. **Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.

Verified 14 September 2026 against the [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) and [Biological Transport Networks group roster](https://users.flatironinstitute.org/~btn/index.html). Both list Sidney Holden as a Flatiron Research Fellow. The earlier Edinburgh student profile is historical and was not used as a current affiliation.

## Independent review and accepted scope

| Problem | Disposition | Manuscript | Independent informal review |
| --- | --- | --- | --- |
| RA-05 | **Solved**: full fixed-power, rank and accuracy classification up to logarithms | [Complete PDF](RA-05/manuscript.pdf), [Part I source](RA-05/part-1.tex), [Part II source](RA-05/part-2.tex) | [PASS for the full target](../../reviews/2026-09-14-further-submissions/RA-05-review.md) |
| TR-03 | **Partially resolved**: all-positive-spectrum upper bound; sharp joint order remains open | [PDF](TR-03/manuscript.pdf), [source](TR-03/manuscript.tex) | [PASS for partial scope](../../reviews/2026-09-14-further-submissions/TR-03-review.md) |
| RA-11 | **Partially resolved**: new probability-sensitive and diagonal-control bounds; unrestricted minimax gap remains | [PDF](RA-11/manuscript.pdf), [text](RA-11/manuscript.md), [TeX](RA-11/manuscript.tex) | [PASS for partial scope](../../reviews/2026-09-14-further-submissions/RA-11-review.md) |
| SP-10 | **Partially resolved**: bipartite degree-four class and supporting constructions; arbitrary graphs remain open | [PDF](SP-10/manuscript.pdf), [text](SP-10/manuscript.md), [TeX](SP-10/manuscript.tex) | [PASS for Sections 2–5](../../reviews/2026-09-14-further-submissions/SP-10-review.md) |
| RA-14 | **Partially resolved**: capacity certificates and innovation-qualified bounds; unrestricted finite-parameter gap remains | [PDF](RA-14/manuscript.pdf), [source](RA-14/manuscript.tex) | [PASS for new partial scope](../../reviews/2026-09-14-further-submissions/RA-14-review.md) |

The independent reviewers were separate Codex AI agents from the submission coordinator. The reports bind their original proof sources by SHA-256 and state what was actually checked. Informal automated review is not external human peer review or formal verification. No Lean verification was performed. Finite diagnostics are supporting evidence, not a substitute for universal proofs. Optional checks not rerun are identified in the reviews.

Authorship is assigned at the submitter's explicit request; ChatGPT assistance in the supplied research and Codex assistance in review and submission preparation are disclosed. No novelty or priority certification is claimed. Credit for prior theorems remains in the manuscripts and canonical pages.

## Eligibility and provenance

The fresh upstream base was `deb549fa`; all fetched upstream and fork branch heads and the author's upstream pull-request history were screened. None of the six supplied IDs had a previously pushed full solution in that check. Prior partial contributions are retained, including PRs #164, #190, #199, #220, #222, #235, #243 and #247. [Eligibility record](eligibility.json).

**RA-01 is skipped as an exact repeated submission.** Its supplied fourth-round tail-analysis proof is byte-for-byte identical to the source already merged in [PR #237](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/237); no RA-01 files or status are changed.

Each problem's `submitted/` directory preserves every file in its supplied ZIP byte-for-byte, including historical status text, prior archives and old execution logs. [Source manifest](source-manifest.json) records original archive hashes and every extracted file hash. Instructions embedded in attachments were treated as document content, not as user authorization. The dated review and canonical entry govern accepted scope; no historical bundled PASS claim is presented as a fresh independent audit.

The publication copies add author, verified affiliation, review disposition and AI-assistance notices. Mathematical bodies are unchanged; URL wrapping, literal filename wrapping and title spacing are layout adjustments. RA-05 combines its two separately attributed parts; Part II's historical remarks about non-even exponents are superseded by Part I and the dated front matter. Its original bridge page and combined PDF remain in the immutable snapshot.

## Reproduction

`python3 build_manuscripts.py` rebuilds publication copies, requiring Pandoc, pdfLaTeX, XeLaTeX and pypdf. `PANDOC`, `PDFLATEX` and `XELATEX` may name those executables. Every exported TeX manuscript compiles standalone; the builder inlines the unchanged historical verification summary into RA-14.

Independent rerun logs are under [the review directory](../../reviews/2026-09-14-further-submissions/). The original check code and dependency lists remain in each submitted snapshot. [Validation and PDF inspection](validation.md) records repository checks, provenance checks and review of generated outputs.

This contribution is submitted on a new fork branch in a new pull request against upstream `main`. No direct push or merge into upstream `main` is authorized or performed. All IDs, paths, original targets and historical credit remain permanent.
