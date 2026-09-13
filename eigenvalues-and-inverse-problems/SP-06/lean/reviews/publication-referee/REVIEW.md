# SP-06 final publication referee report

**Reviewer:** OpenAI Codex agent `/root/lean_ie15_next` (AI agent; independent of the SP-06 proof author).
**Date:** 13 September 2026
**Candidate:** `/tmp/nla-lean-sp06-worktree`, branch `codex/lean-sp06-jordan-curve`
**Verified proof commit:** `3122d69460b0ed6dda3ea00dfaa899f93411ce2f`

## Verdict

**PASS — publication promotion ready.** I found no substantive defect in target preservation, proof/source correspondence, attribution, privacy, package metadata, retained Linux evidence, or generated publication files. This is an independent publication review; it does not commit, push, open, or merge a pull request.

## Evidence reviewed

- The rendered `Problem statement` section is whitespace-normalized identical to HEAD, and the current PDF text matches the coordinator's rendered snapshot byte-for-byte. The PDF's status/date/evidence additions explain the binary change; the mathematical target is preserved.
- `solution.md`, `solution.tex`, and `solution.pdf` are byte-identical to HEAD. The six proof modules and all pinned project inputs are unchanged from the verified proof commit. `SOURCE_MAP.md` reproduces its four canonical source hashes from upstream commit `50838e37dd793830e2cecd1055cfc7e0349490f1`.
- `problem_ids.json` is unchanged (SHA-256 `d7f9925a483d40030ef266917bc8e413dac6d45530ad5515da506ffe9583e763`) and still maps SP-06 to `eigenvalues-and-inverse-problems/SP-06/README.md`. Catalog, category index, root summary, SP-06 README, and `RESOLVED.md` consistently show the promotion and 74 solved / 27 Lean-verified counts.
- Publication-facing material names **George Stepaniants**, Department of Computing and Mathematical Sciences, California Institute of Technology, and preserves Matthew J. Colbrook's original mathematical credit and Cambridge affiliation. No George/Stepaniants contact email is published.
- Running the complete offline publication checker with `/tmp/nla-lean-formalization/venv/bin/python` passed: schema and Comparator coverage (20 declarations), package inventory (96 files), and SP-06 publication integrity (61 original inputs, 20 exports, original ZIP, successful Linux receipts). No Lean compiler or Lake command was run during this review.
- The candidate mapping preserves exactly three changed metadata files and binds all 61 original verified input hashes. `formalization.yaml` records zero sorries, 20 main results, the complete target, pinned LeanCert/Mathlib, two statement reviews, two final mathematical reviews, and the successful Linux evidence.
- The retained Linux run `34765629739` / job `103745998196` completed successfully on the verified commit and reports `comparator-accepted`. The corrected operational report has SHA-256 `8be74df4c72817a96377c3b68d89a4fce78aaa298304470f64df88fa1ebf9d5c` and distinguishes LeanCert `621a43d7cf21f87872392a01e874f2f1dbddc926` from the Forsythe harness revision `8d1b0c0545a77b40245e84705aa7d273e6c81e62`. Its artifact ZIP is SHA-256 `fac2ebe5f81ec421a7b478fcbd1a11768887b8678ad5d166adac3a1402aece6c` with 13 safe entries; raw sandbox, kernel, Comparator, regression, and negative-fixture markers match.
- The rendered problem PDF has three pages. I reviewed the retained page renderings; root's publication record also records all-page visual inspection and no clipping/overflow.

## Nonblocking records

`NUMERICAL_TARGETS.md` keeps its original statement-stage heading, and `reviews/FINAL-ACCEPTANCE.json` keeps the pre-Linux phase text saying Linux/Comparator were pending. These are retained historical receipts; live README/YAML/Linux evidence and indexes state the completed status. The two trailing spaces reported by `git diff --check` are intentional Markdown hard-breaks on the added status/date lines.

## Recommendation

Approve the SP-06 promotion. The coordinator may commit the reviewed promotion files, push the branch, and open the individual upstream pull request.
