# Independent integration review — five continuations

Reviewer: separate Codex AI agent `/root/review_sp07_sp08`, 14 September 2026 UTC. This bounded review checks integration against the five mathematical review reports; it does not repeat their certificate computations. **Verdict: PASS; no blocking integration issue found.** No Lean was run.

Reviewed worktree: `/tmp/nla-holden-continuations`, compared against upstream base `deb549fa9ddd6b119e6c59016f268237e645dfa2`.

## Scope and policy

All five new canonical notices and the submission README accurately reflect their independent reports. NR-02 explicitly accepts only the complexity-six polygon-product theorem and excludes the inherited all-polytopes corollary from independent-audit coverage. SP-07 reports a strict lower bound and restricted reductions, with no exact sharp constant. MI-20 reports a certified upper bound and interpolation after the disclosed cyclic-reduction correction. SP-08 preserves the crucial centered-sign rank hypothesis outside the unrestricted strip. SP-14 distinguishes an actual-eigenvalue canonical subsequence from full-sequence convergence.

The retained statuses agree with the review decisions: NR-02, SP-08 and SP-14 Partially resolved; SP-07 and MI-20 Open. No complete-solution status is asserted. The original problem statements, assumptions, prior-result notices, source credits, canonical paths and IDs remain intact. A programmatic comparison found that each canonical README differs from the upstream base only by the new continuation notice, Last checked metadata, and blank-line normalization.

## Attribution and source preservation

All five publication manuscripts explicitly attribute Sidney Holden and the same affiliation. The official institutional profile was independently reopened during this integration review: [Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) identifies him as a Flatiron Research Fellow in Biological Transport Networks, CCB, Flatiron Institute. It supports the affiliation used; the Edinburgh degree is historical background, not a current appointment. The publication's September 13 date is consistent with the user's local timezone.

All five retained original ZIP hashes match both `source-hashes.json` and the user-supplied files in Downloads. Every original manuscript source hash was independently checked against the corresponding ZIP member. Comparing each publication TeX with that original shows only the declared authorship/PDF-author additions, formerly blank dates, two SP-14 input-path changes, and the explicitly documented MI-20 mathematical correction. NR-02's ChatGPT-assistance disclosure is preserved. The three copied auxiliary TeX data files are byte-identical to their archived sources.

MI-20's corrected variable is exactly `T_\ell=m^{-2/q}U^{-\ell}\widetilde R^2U^\ell`, matching the independent review's repair. The publication file SHA-256 is `785d79d7f9ffe54e08a0c27dbd883ca64e58284049983da9c9366fe5611ee78a`, exactly the review's post-correction record. No other mathematical source edit was found.

## PDF layout adjustment

I also inspected the final diff of `tools/render_problems.py`: it removes only SP-07 and SP-14 from the ID set that inserts a forced page break before References. This is a narrowly scoped PDF-layout adjustment, with no mathematical or Markdown-content changes. Rebuild and visual QA remain the integrator's responsibility.

## Links and limits

All relative Markdown link targets in the five changed canonical READMEs and the submission README resolve to existing files. Every publication TeX input target exists. The notices link their own reports, reviews and the shared provenance/affiliation record.

This review does not independently rerun the duplicate branch/PR-history search, rebuild or visually inspect PDFs, repeat the other agents' mathematical certificate computations, or certify novelty. Those checks remain covered by their separately recorded evidence. No repository files were edited during this integration review.
