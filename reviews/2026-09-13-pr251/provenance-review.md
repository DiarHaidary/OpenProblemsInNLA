# PR #251 independent provenance and statement-correspondence review

**Verdict: no actionable finding in this audit's scope.** Reviewed PR head `589ec79798ee42adc7a7160a376c67252280a121` read-only at `/private/tmp/nla-audit-251`, against published base `752218e5417998b7f4d2aee9c447ca5d256fe530`. The accepted proof snapshot is `f664d07e82aaa60bc9c78dd1946e763168c5c530`. The current proof and frozen statement/configuration bytes agree with that snapshot. This is a source/provenance, metadata, target/credit and PDF review; the coordinating reviewer separately owns live GitHub evidence authentication/integration, and two other reviewers own full Lean proof/math and finite-certificate replay.

## Independent reproductions

The scratch-only [audit script](/private/tmp/nla-pr-251-provenance.py) completed successfully with `/private/tmp/nla-lean-audit-python/bin/python`; its complete machine-readable result is [provenance JSON](/private/tmp/nla-pr-251-provenance.json). It reads committed Git blobs directly, rather than accepting agreement between submitted manifests as sufficient evidence.

| Check | Independently observed result |
| --- | --- |
| Historical canonical verification inputs | All 113 SHA-256 values recomputed from `f664d07…` agree with both the input-binding record and raw result JSON. |
| Complete current package | All 170 inventory entries match; adding the deliberately self-excluded inventory file gives exactly the complete 171-file tracked Git set, with no omitted or extra tracked package file. |
| Active proof graph | Independently following project imports from `Solution.lean` yields exactly the manifest's 58 modules. All lengths/hashes match, and every module is byte-identical to the accepted proof snapshot. |
| Frozen boundary | Definitions, Challenge, Comparator configuration, Lake project, dependency manifest and toolchain all match their hashes and accepted proof bytes. |
| Mathematical source map | All seven source rows match both recorded Git blob IDs and SHA-256 at immutable source base `50838e37dd793830e2cecd1055cfc7e0349490f1`. |
| Metadata | YAML validates against the pinned v0.4 schema; schema SHA-256 `25ff6b25ca4511635aff4443cf20480c15e59dddf19591c730950b442ea54fce` matches. All ten dependency revision pins, ten exported declarations and both final-review hashes agree with their underlying files. Lean toolchain is `leanprover/lean4:v4.33.1`. |
| Copied raw evidence | All 30 evidence-manifest files match. All 13 ZIP payloads are byte-identical to their extracted counterparts, with no absolute/traversal/drive paths, symlinks or duplicates. |
| Publication receipt | All three canonical document hashes and 84 source/boundary bindings match the present files. |

Within the historical 113 input paths, the only changes between accepted proof and PR head are `ACTIVE-MODULE-MANIFEST.json`, `README.md`, `SOURCE_MAP.md`, `formalization.yaml` and `reviews/proof-candidate-hashes.json`. These are the disclosed documentation/metadata transition. There is no subsequent change to accepted Lean proof source, boundary, toolchain, dependency lock or Comparator configuration. The 113 historical inputs and 171 current tracked files are different inventories for explicitly different snapshots; neither count indicates missing verification inputs.

After reading `verification/linux-2026-09-13/check_evidence.py`, I also ran it read-only with Python `-B`. It passed its checks of the retained run/job/artifact, 113 bindings, ten dependency checkouts, ten exports, standard axioms, default kernel, Comparator, sandbox and rejection markers. This reproduces offline evidence consistency; it does not itself execute Lean or authenticate GitHub's servers.

## Historical claims checked against Git

The coordinator fetched immutable historical objects `3b3eb8f3fa384e4b3bf640d48bca87cf40db9565` and `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`. The historical-development comparison is therefore completed, not left as a receipt-only assumption.

- Every one of the 58 active modules in canonical package `523c5aeaddd8bf7c2dc01afb053bb0dea8811335` is byte-identical to its development source at `3b3eb8f3…`.
- The actual development diff `fe4140cc…` to `3b3eb8f3…` contains exactly the seven disclosed overlay paths. Their added/modified classifications match `certificate-bridge/INTEGRATION-PATHS.json`. All seven source hashes and all five copied package payload hashes match actual Git/file bytes.
- Current source differs from that development graph only in `NLA/NR03/Rank.lean`. Removing the single inserted line `change (0 : ℝ) ≤ (W i k : ℝ)` exactly recreates the old `523c5a…` Rank blob. Both old/new hashes and the retained repair diff hash match. The remaining 57 modules are unchanged.

The [source map](/private/tmp/nla-audit-251/nonnegative-and-positive-factorizations/NR-03/lean/SOURCE_MAP.md:37) correctly separates the six-module bridge diagnostic, the earlier failed Rank compilation and complete canonical acceptance. The terminal record identifies run `34785341662`, job `103799711659`, artifact `10326896988` and proof snapshot `f664d07…`. Artifact SHA-256 is `91f80abcbbb0f10fbf614ab259fbf5121a8dabd5c600969a260e3b8b2c8e267c`; raw result SHA-256 is `e7bd039fb9e4dcc7f46a4930b9f4dc2eb79a9977a80c0cbb4299d8edcb4eb0ed`. Pending/statement-only descriptions inside earlier frozen records describe those earlier stages; the current package explicitly identifies its final acceptance. Branch publication counts are likewise historical snapshot counts, not a claim about the later integrated main branch.

## Original target, boundary and credit

The canonical README from `## Context and notation` onward is byte-identical to the published base; the original mathematical target and source references remain intact. The complete Colbrook historical partial-result block is also byte-identical. `problem_ids.json` is byte-identical, retains all 217 ID/path pairs and preserves `NR-03` at its canonical path. The diff contains no changes to the shared Lean verifier, its workflow, schema or ID safeguards.

The [definitions](/private/tmp/nla-audit-251/nonnegative-and-positive-factorizations/NR-03/lean/NLA/NR03/Definitions.lean:23) use all Boolean vectors `Fin n → Bool`, real dot products and the real square `(1 - boolDot a b)^2`. Real nonnegative factors and their actual minimum width are represented explicitly. The totalized no-factorization branch is disclosed; the Challenge contracts require existence for the general minimum semantics, and the claimed counterexample supplies a factorization. The target remains `∀ n, 3 ≤ n → nonnegativeRank (cMatrix n) = 2 ^ n`. Positive integer denominators and the complete entrywise identity remain explicit certificate obligations.

The full Challenge file was read and all ten named contracts compared with the disclosed scope. `Challenge.lean` is deliberately outside the independently reconstructed active Solution import closure. Its statement placeholders are therefore not imported proof premises. Supplementary `CertificateData.lean` is outside that closure as documented. Semantic discharge of the contracts and the guarded-natural-subtraction bridge are assigned to the independent proof reviewers.

The [canonical verification block](/private/tmp/nla-audit-251/nonnegative-and-positive-factorizations/NR-03/README.md:43) distinguishes the complete negative answer obtained at `n=7` from determining exact rank 127 or the smallest counterexample dimension. Holden's stronger informal general bound is preserved without claiming it was all formalized here. Sidney Holden receives mathematical counterexample credit, George Stepaniants receives formalization credit, and Matthew J. Colbrook's earlier partial result remains separately credited with its original affiliation. AI assistance and the informal nature of the agent reviews are disclosed; no external human review or official Tau Ceti endorsement is claimed.

## PDF inspection and limits

The only changed PDF is the three-page [canonical problem PDF](/private/tmp/nla-audit-251/nonnegative-and-positive-factorizations/NR-03/problem.pdf). Following the PDF skill's read-only rendering workflow, I rasterized all pages with Poppler and inspected each page individually. The images are retained as [page 1](/private/tmp/nla251-raster/problem-1.png), [page 2](/private/tmp/nla251-raster/problem-2.png) and [page 3](/private/tmp/nla251-raster/problem-3.png). All are legible; the original formula, new Lean scope, citations and credit render without missing symbols, clipping or overlapping text. No PDF was rebuilt. The unchanged Holden proof sources are covered by exact source-map checks.

No source checkout or GitHub mutation was made by this reviewer; final `git status --short` was clean. No Lean compiler run, new CI dispatch, external authentication or full independent proof-body verdict is claimed in this report. Those complementary checks belong to the coordinating review. Within this audit's stated scope, no unresolved provenance blocker remains.
