# Independent audit of PR #233 — KE-04

Date: 13 September 2026. Reviewer: independent Codex agent `/root/review_ke04_233`.

**Mathematical and statement-fidelity verdict: PASS.** The complete formalization proves the retained KE-04 target, including its largest-full-iteration convention, through a stronger arbitrary-full-prefix theorem. No mathematical blocker was found. Acceptance still requires the separately assigned authentication of actual CI, Comparator, kernel and sandbox evidence. This report does not claim a new local compilation or substitute the contributor's historical reviews for an independent review.

Reviewed source head: `ecd7d63a22e40db0967a9cb8e785555a0fad6ca8`.
Published base: `50838e37dd793830e2cecd1055cfc7e0349490f1`.
Read-only checkout: `/private/tmp/nla-audit-233`.

## Scope actually inspected

I read every line of the actual proof import closure: `Solution.lean`, and all ten `NLA/KE04/` modules, totaling 1,440 lines. I also read all 170 lines of the independent `Challenge.lean`, the complete retained Colbrook manuscript `solution.md`, the canonical README and its diff, the new RESOLVED entry, comparator configuration, complete formalization manifest and source correspondence, and the current-phase and historical-context portions of the project README. The mathematical reasoning below was derived from the actual source, without treating supplied referee conclusions as proof.

The companion `nla-pr233-source-boundary-check.py` and JSON record exact source hashes and independently verify the project import graph, all 24 source-level contract signatures, restricted comparator configuration, absence of proof placeholders/custom axioms/native-decision constructs, unchanged original target and manuscript files, and the historical correspondence bindings. This source-level check is complementary to the separately reviewed compiled Comparator and kernel results.

## Original target and semantic fidelity

The original-problem section of the canonical README is byte-identical to the published base. The complete retained `solution.md`, `solution.tex`, and `solution.pdf` are also unchanged. I checked the original conjecture directly in [Šimonová and Tichý, §2.1](https://arxiv.org/html/2507.16484v1): its open intervals, block-width offset, iteration bounds, and largest-full-dimension convention agree with the formal target. This review concerns that exact-arithmetic conjecture, not a finite-precision assertion elsewhere in the paper.

`Vec`, `Rect`, `Mat`, `act`, `column`, `krylov`, `FullColumnRank`, and `FullBlockDimension` are ordinary Mathlib Euclidean spaces, real matrices, actual matrix action, generated column spans, independence and finite dimension. None embeds interval occupancy, PSD implications or an annihilation exclusion as an input assumption. `IsKrylovBasis` requires exactly orthonormal columns and the correct column space. There is no compatibility requirement between the independently quantified `Qk` and `Qj`.

The final `BlockLanczosConjecture` universally quantifies all natural dimensions, real symmetric matrices, full-column-rank blocks, maximal full iteration, allowed iteration pairs and interval indices. `IterationOccupancy` uses `1 ≤ k < j ≤ s`, `1 ≤ i ≤ (k-1)p`, and a genuine `Fin (j*p)` eigenvalue witness strictly between the earlier endpoints. The separately proved arithmetic contract guarantees both natural endpoint indices `i-1` and `i+p-1` are in range. Consequently the total helper's out-of-range zero branch is unreachable in the target. It also derives `k ≥ 2` and `p > 0` from the admissible interval index, properly handling the empty cases. Positive width appears only where necessary for existence of a greatest full iteration; the stronger theorem remains valid at zero dimensions through its empty index ranges.

I inspected the pinned Mathlib [self-adjoint spectral API](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/InnerProductSpace/Spectrum.lean), including definitions and proofs of the eigenvalue ordering, matched eigenbasis, characteristic-root multiset identity and ordered-spectrum equality criterion. The project correctly reverses both eigenvalues and the matching basis. Distinct basis indices, rather than distinct eigenvalues, define its spectral window, so algebraic multiplicity is retained. The actual PSD bridge and zero-form/kernel theorem also match their uses in the pinned [positive-operator](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/InnerProductSpace/Positive.lean) and [matrix-order](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/Matrix/Order.lean) sources; neither requires positive definiteness or an invertible matrix.

## Complete proof audit

The proof is a faithful exact-algebra implementation of the three-part Colbrook argument. Its contradiction first derives endpoint order from the actual ordered spectrum. Assuming no later eigenvalue lies in the open interval makes `(Tj-aI)(Tj-bI)` PSD by explicit diagonalization in its actual orthonormal eigenbasis. The earlier `p+1` consecutive indexed eigenvectors give an orthonormal family of dimension `p+1`, with nonpositive quadratic form even when eigenvalues repeat or the proposed endpoints coincide. The submodule dimension formula and full-prefix dimensions then supply a nonzero vector in that window and `K_(k-1)`.

The transport implementation distinguishes the two identities the proof needs. On `K_(k-1)`, both compressions give the same quadratic form because `x` and `Ax` lie in each space. It does not assert the generally invalid equality between the earlier squared compression and `A²`. Only for the later compression does it use `A²x ∈ K_(k+1) ⊆ K_j` to identify the actual quadratic vector action. The ambient representative is `Q q(QᵀAQ) Qᵀ`, the subspace quadratic extended by zero; it is not the polynomial of an ambient zero-extended first compression. PSD plus the nonpositive form yields a zero form and then a genuine kernel equation, including singular PSD.

Full-rank nonannihilation is proved, not assumed. Coefficients in the actual block-power map admit zero extension and a degree shift. Injectivity from full block dimension forces a shift equal to a scalar multiple of zero extension to have all coefficients zero, by backward induction starting at the last block. Thus a vector in `K_ell` cannot be an eigenvector when full dimension holds at `ell+1`. Applying this successively to `y=(A-bI)x ∈ K_k` and `x ∈ K_(k-1)` excludes `(A-aI)(A-bI)x=0` using full dimension through `k+1`. This exact affine-factor argument is a valid replacement for the informal highest-coefficient presentation, including `a=b`.

The assembly obtains each needed full dimension from the single full-prefix premise and `k+1 ≤ j ≤ s`. It obtains the final contradiction without assuming endpoint separation. `fullPrefix_implies_canonical` then uses the full-dimension component of `LastFullBlockIteration` to prove exactly the original target. Ignoring the redundant starting-block rank hypothesis within the stronger proof strengthens the argument and does not change its published contract.

## Coverage of all 24 exported declarations

All names below have prefix `NLA.KE04.`. Each implementation signature matches its Challenge signature exactly after removal of comments and normalization of whitespace. Every export has explicit kernel-trust and axiom-report commands.

| Export | Independent coverage |
| --- | --- |
| `real_matrix_semantics` | Real transpose/Hermitian equivalence, ordinary coordinate matrix action and orthonormal columns. |
| `krylov_range_semantics` | Actual block-column span equals the finite coefficient-map range; coefficient expansion and cardinality dimension bound. |
| `krylov_nesting_and_shift` | Empty prefix, inclusion of degree sets and one multiplication of every actual column. |
| `fullBlockDimension_iff_independent` | Finite-span dimension equals indexed cardinality exactly when independent; first prefix recovers V. |
| `fullBlockDimension_prefix` | Independence restricts along an injective degree embedding; genuine coefficient-map injectivity follows. |
| `lastFullBlockIteration_exists` | Positive width bounds all full indices by n; the nonempty finite set has a greatest element. |
| `krylovBasis_exists` | A standard orthonormal basis of the actual finite-dimensional submodule gives a matrix of the exact required size. |
| `frameProjection_semantics` | Hermitian idempotence, fixed-space equivalence and orthogonality of projection error. |
| `compression_semantics` | True symmetric `QᵀAQ` and representation of projected matrix action on its subspace. |
| `orderedSpectrum_semantics` | Increasing ordering, matching eigenvector equations, complete root multiset and valid indexing. |
| `compression_basis_independent` | Explicit `O=QᵀR`, orthogonal similarity, characteristic-polynomial equality and identical ordered eigenvalues. |
| `interval_index_validity` | All permitted one-based endpoint indices are valid; empty low-width/low-iteration cases handled. |
| `quadratic_semantics` | Actual monic degree-two polynomial, matrix polynomial evaluation and exact expansion. |
| `spectral_gap_quadratic_psd` | Sign on every later eigenvalue and diagonal PSD transport; coincident endpoints included. |
| `spectral_window_subspace` | Exactly p+1 independent indexed eigenvectors, inclusion in the frame range and nonpositive form. |
| `krylov_intersection_nonzero` | Dimension of sum/intersection and the preceding-prefix codimension p yield a nonzero vector. |
| `psd_zero_form_iff_kernel` | Correct Euclidean translation of the actual semidefinite matrix theorem, without invertibility. |
| `compressedQuadratic_semantics` | True coordinate quadratic-form identity and PSD preservation by congruence. |
| `quadratic_forms_agree` | Form equality through common x and Ax membership; no invalid early A² substitution. |
| `later_quadratic_identity` | Later space contains x, Ax and A²x, giving the full quadratic vector identity. |
| `fullRank_quadratic_nonannihilation` | Injective coefficient shifts and successive affine factors rule out annihilation for all a,b. |
| `strictIntervalOccupancy` | Complete contradiction assembled for every admissible input under a full-prefix premise. |
| `fullPrefix_implies_canonical` | Exact reduction to the published maximal-s convention. |
| `blockLanczosConjecture` | Complete retained original target, through the proved stronger result. |

## Proof boundary and attribution

The actual Solution import graph reaches only the ten implementation/definition modules and their Mathlib/Lean/LeanCert imports. It never imports Challenge or any historical source snapshots, test inputs, referee inspections, other problem formalizations or manuscript-generation machinery. Challenge itself imports only Definitions. Its 24 intentional holes occur in that separate reference environment; there are none in the actual proof closure. No custom axiom, native decision, unsafe implementation, syntax replacement or fabricated semantic object was found in the local proof sources. Comparator permits exactly `propext`, `Classical.choice`, and `Quot.sound`, and lists no replaceable definitions.

The new canonical prose clearly credits George Stepaniants for formalization, Matthew J. Colbrook for the original mathematical proof, and D. Šimonová/P. Tichý for the conjecture. AI assistance is disclosed, and agent reviews are not described as external human peer review. Scope is the complete exact-arithmetic KE-04 problem; there is no separate finite-precision or novelty claim.

## Canonical publication and historical-document clarification

I rendered and visually inspected all three pages of the submitted canonical `problem.pdf` with the PDF skill. Its SHA-256 is `88c3b7449e63d5b66a676552dbf5aa917502db61d5ccf628d9460c4cfc62be22`. Status, authorship, equations, strict inequalities, reference links and reproduction commands are legible, with no clipping, overlapping text or missing glyphs. The original statement and reference sections are complete. The proof-manuscript PDF is unchanged from the published base and was not newly re-rendered in this audit.

One editorial clarification is recommended and has been communicated to the coordinator: the canonical link to `SourceCorrespondence.md` should explicitly identify it as a historical statement-stage record. That document intentionally retains statements that proof implementation and later gates were pending at its original stage. Its exact SHA-256 `399f28847f52a6c5ff309a25b9501c0c6d4bd5a76892de2f5adaa9c25fe80a00` is independently bound in `DRAFT-INVENTORY.json`, the statement freeze and proof freeze, and matches three retained statement-referee input copies. Its bytes should therefore remain unchanged. The current Lean project README already distinguishes historical and current phases.

Suggested canonical wording: “See the [historical statement-stage source correspondence](lean/SourceCorrespondence.md) and [completed proof map](lean/PROOF-MAP.md). The correspondence preserves the original review boundary; the verification evidence below records the completed proof.” A resulting regenerated canonical PDF should receive a fresh visual check. This documentation distinction does not undermine the complete proof or its statement fidelity.

No mathematical or source-boundary blockers remain. Final merge is conditional on the coordinator's separately authenticated execution evidence, final publication checks and exact-head guard.
