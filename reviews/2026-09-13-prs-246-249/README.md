# Independent integration audit: PRs #246, #247 and #249

Reviewed on 13 September 2026 against published main `752218e5417998b7f4d2aee9c447ca5d256fe530`. Separate reviewers read the mathematical proofs and actual certificate code, checked relevant primary theorem statements, reproduced the computations in disposable directories and inspected the PDFs. These are informal AI-assisted reviews. Only IE-16 receives a Lean-verified status, supported by separately authenticated kernel and Comparator execution.

| PR | Exact audited head | Accepted scope |
| --- | --- | --- |
| #246 | `a4e8ea57f9b010b85390845b4de902183b6d97ba` | IE-16: fifteen Lean exports establish the finite complex-polynomial counterexample and negate the original candidate inequality. Stronger informal amplification remains outside the formal scope. |
| #247 | `24212f477b26aad36a757e62998bd4974b24ac81` | RA-05: further even-power upper bounds and matching high-accuracy regime; the full joint classification remains open. |
| #249 | `9e11821e2e999afb1699272005a167da7ee42861` | IE-11 remains Open with supporting local certificates; IE-20 becomes Partially resolved; IE-27/IE-28 retain their explicitly limited partial results. |

Read [IE-16 review](pr246-ie16-review.md), [RA-05 review](pr247-ra05-review.md), [IE-11 review](pr249-ie11-review.md), [IE-20 review](pr249-ie20-review.md), [IE-27/IE-28 review](pr249-ie27-ie28-review.md), and [archive/attribution review](pr249-provenance.md). Companion scripts and fresh JSON/log evidence are retained here. Paths inside captured reports/scripts describe the original disposable review environment; reproduce with corresponding source checkouts and scratch paths, never over preserved archive payloads.

## Integration checks

The only content conflict was simultaneous insertion at the top of RESOLVED.md. Both new blocks and every previously published contribution were retained. The validator ran before catalog regeneration. All 77 repository tests passed without skips, all 217 immutable IDs and their canonical targets/context remain unchanged, the fifteen-result IE-16 manifest passed, and the canonical math formatter reported zero pages needing changes.

The exact-blob preservation audit checks all 667 added source files, all 24,070 published base paths, 3,143 prior reference files, all modified canonical files against their audited source head, the registry, and unchanged shared tools/workflows. Every source head is an ancestor of the combined merge. No submitted PDF, mathematical source, proof module or archive was edited. Markdown hard breaks, preserved diff snapshots and original CSV line endings are retained; ordinary git whitespace warnings on those payloads are not mathematical/source defects.

The merged catalog has 43 Open, 73 Partially resolved, 72 Solved and 29 Lean verified entries: 116 open targets and 217 permanent IDs. Difficulty/importance flags remain unchanged.

## Lean acceptance evidence

[Source-run authentication](ie16-source-ci-authentication.json) binds the actual GitHub PR run to its exact head and synthetic merge parents, all 346 tracked project inputs, fifteen matched exports and fifteen standard-axiom reports. It verifies real default-kernel acceptance/rejection controls, the Comparator regressions, pinned tool versions and Linux isolation evidence. The read-only authenticator is retained as [authenticate-ie16-ci.py](authenticate-ie16-ci.py).

Fresh integration CI and its exact final head/tree authentication are recorded in the integration PR body after the final commit, avoiding a subsequent evidence-only commit that would invalidate that checked head. Local reports and source-run receipts are not substituted for final integration CI.
