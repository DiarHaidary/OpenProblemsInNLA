# Audit of PRs #232 and #233

Both mathematical source reviews and the upstream CI authentication passed. The two previously solved problems gain Lean verification; the original targets, problem IDs and attributions are retained. Final combined-branch GitHub checks remain a separate merge gate, recorded in the integration PR.

| PR | Problem | Formalized result | Evidence |
| --- | --- | --- | --- |
| [232](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/232) | IE-05 | Exact order-eight counterexample to the universal orthogonal GEPP extremizer equality | [Independent review](pr-232-independent-review.md), [exact replay](ie05-exact-replay.json) |
| [233](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/233) | KE-04 | Full strict interval occupancy across block Lanczos iterations | [Independent review](pr-233-independent-review.md), [source boundaries](ke04-source-boundaries.json) |

The [upstream CI audit](upstream-ci.md) authenticated both actual GitHub runs, all 7,590 tracked inputs, 41 theorem exports and 166 standard-axiom reports, including default-kernel acceptance and actual Comparator, rejection and Linux sandbox controls. These execution checks supplement direct independent review of the definitions and complete proof source; contributor reports were not accepted as proof by themselves. These are Codex agent reviews and Lean checks, not external human peer review.

Both projects retain historical SourceCorrespondence.md files whose pending-proof wording is bound to their original input inventories. Integration clarifies their historical status on the canonical problem pages and regenerates both PDFs. All five resulting PDF pages were visually checked; [hashes and page counts](pdf-review.json) identify the reviewed artifacts. Every file inside both Lean packages remains byte-identical to its submitted head.

The [preservation audit](preservation.md) checks all 15,966 previous-main paths, all 217 permanent IDs, exact original targets and history, all 7,590 new authored files, both source-head ancestors, shared verification safeguards, and combined catalog counts. Its [rerunnable verifier](verify_preservation.py) accepts `--repo`, `--ref`, and `--output-prefix`. Subsequent integration commits append only audit evidence.

Validation passed all [77 repository tests](repository-tests.log) without skips, all 17 permanent-ID regressions, the 17- and 24-declaration manifests, and the GitHub mathematics formatter. The resulting catalog has 26 Lean verified, 75 Solved, 46 Open and 70 Partially resolved entries. The 116 open targets are unchanged.

The independent arithmetic and source-boundary scripts have only their filesystem input/output plumbing adapted for repository use. Run `python3 ie05-exact-replay.py --project /path/to/IE-05/lean --output /tmp/ie05-check.json`. For the frozen KE-04 source check, create a read-only checkout at `ecd7d63a22e40db0967a9cb8e785555a0fad6ca8`, then run `python3 ke04-source-boundaries.py --repo /path/to/that/checkout --output /tmp/ke04-check.json`. Neither script compiles Lean or substitutes for the actual CI kernel checks.

A [second independent preservation review](preservation-cross-review.md) passed: both complete Lean Git subtree objects are identical to their submitted revisions, and only the documented canonical clarification/PDF and combined-index changes modify the assembled source content.
