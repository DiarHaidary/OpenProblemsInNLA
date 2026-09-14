# Independent integration review: PRs #253--#256

Reviewed the combined workspace `/private/tmp/nla-integration-253-256` on 14 September 2026 against published base `deb549fa9ddd6b119e6c59016f268237e645dfa2`. Review began at merge head `f1bf1af1108c8a0dccf59ca74f1a3c24dcbf9c14` with the disclosed renderer/NM-01 layout changes, and the final verification snapshot is the clean committed head **`ee0971c7492a55c641181081cb73175156236ff2`**. The reviewer made no changes to the integration worktree and no GitHub mutations.

**Verdict: no actionable integration mismatch identified.** This is an independent check of target/credit preservation, merged notices, the two disclosed editorial corrections and renderer scope. Full archived-blob preservation, proof-specific audits, PDF regeneration/layout and final CI authentication remain the coordinator's responsibilities.

## Exact source ancestry and target preservation

Confirmed that all four reviewed source heads are ancestors of the integration history:

- #253: `43183e8254d121aa4b365fdd34643cc4c91d8503`
- #254: `0ea258baa0bde427540dfb64fee7dfff95e6498c`
- #255: `ecc57b82bbcb33aa37dd403530669f74bdf2ec30`
- #256: `b84772b48cd26a2e763ecc52a6243e8f0c34681f`

Read the canonical diffs and independently checked all **217 registered canonical README pages** against the published base. Every prior nonempty line except the intentionally updated Status and Last checked metadata survives in its original order. Thus the original mathematical statements, assumptions, quantifiers, previous contributions, references and author credit remain intact, including on all 13 changed canonical pages. The append-only ID registry is unchanged.

All **13 newly added source canonical sections** are preserved as complete exact text from their source PRs. In particular, SP-07 retains both separate contributions:

- PR #254's seven-dimensional normal-pair certificate giving `C_normal>1.03077`, with its restricted reductions and explicit Open status;
- PR #255's odd-polygon completion barriers and stationary two-line model, including the statement that the quotient near 1.0373054 is not a finite normal-matrix lower bound.

The earlier SP-07 subclass result and original sharp-constant target also remain intact. No conflict resolution silently discarded either source contribution.

Every prior nonempty RESOLVED.md line remains in order, and every newly added source resolution section remains present. The historical RA-05 partial notices are retained with the new notice expressly superseding their remaining-gap claims.

## Source notices and scoped editorial changes

Compared all **27 source-added or source-modified reference README files** with their original PR heads. Every one is identical in the integration except the explicitly intended MI-20 disclosure correction. That correction now accurately explains that the publication report also repairs an omitted unitary conjugation in its cyclic-reduction construction, while the original ZIP preserves the submitted version. It no longer makes the misleading statement that the publication mathematics was unchanged. The attribution and review/provenance links remain intact.

The NM-01 addition preserves Nicolas Gillis's proposed Fu--Huang--Sidiropoulos--Ma bibliographic reference, DOI, journal coordinates and authorship credit. The original long quotation is replaced by a short paraphrase with an accepted-manuscript link and §VIII locator. The added qualification makes clear that the earlier discussion concerns solvability under additional practical assumptions and does not state the repository's exact rational-input SSC promise problem. The existing precise target and Gillis reference remain unchanged. This is a scoped bibliographic/contextual edit; no new equivalence or solved claim is introduced.

## Renderer and verification boundary

Parsed both the published-base and integrated `tools/render_problems.py` with Python's AST. After deleting the following five entries from the base's forced-reference-page-break set, the ASTs are identical:

`NM-01`, `RA-11`, `RA-14`, `SP-07`, `SP-14`.

Thus the renderer modification changes only those forced page breaks; it does not change mathematics conversion, reference parsing, other problem layout rules or output generation semantics.

No Lean source/project, shared Lean checker, workflow, permanent-ID validator or permanent-ID test file changes are present. `git diff --check` passes. These read-only checks do not replace the coordinator's required full test suite or final remote checks.

The final canonical count independently recomputed from the registry is:

- 42 Open
- 73 Partially resolved
- 72 Solved
- 30 Lean verified

This is 217 retained IDs, 115 targets still open and 102 entries outside that count, agreeing with README.md and CATALOG.md. The two status transitions are RA-05 from Partially resolved to Solved and SP-03 from Open to Partially resolved. No additional source notice has been promoted beyond its audited scope.

Machine-readable snapshot: `integration-independent-checks.json` beside this report. The worktree was clean at that snapshot. If later substantive edits change a target, scope notice or renderer behavior, they require renewed review; adding audit records alone does not alter these conclusions.
