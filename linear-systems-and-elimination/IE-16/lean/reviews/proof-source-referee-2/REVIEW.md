# IE-16 second independent source referee

Reviewer: `/root/nr03_independent_referee`, OpenAI Codex **AI agent**, 13
September 2026. I authored none of the reviewed IE-16 proof. This review was
performed independently of the other full-proof referee's conclusions. It
applies `docs/lean/REVIEW.md`, the repository's Tau Ceti adaptation, and is
neither external human peer review nor an official Tau Ceti service run.

**Mathematical/source verdict: favorable; no mathematical defect found.
Implementation verdict: changes required, with formal acceptance withheld.**
The exact candidate has documented compilation failures. Subsequent compiler
repairs and their resulting source require a separate recheck; this report
does not approve unreviewed later bytes.

The immutable reviewed commit is
`28bdf9e85541764b6a5cb2debd647b9cebaea21f`, under `development/IE16`.
`Solution.lean` SHA-256 is
`dea94208561e823f1b76f831b4a8c5c5f419e9214c2b0a10ec5d4abc8612f69c`.
All ten proof-path files, configurations, source inputs and inspected logs
have exact hashes in `INPUT-HASHES.json`.

## Target, scope and minimum semantics

I read every proof-path module, Definitions, all fifteen Challenge contracts,
numerical targets, implementation plans, comparator configuration, metadata,
both amended statement reports and statement acceptance. I also read the
complete canonical README and all 600 lines of Holden's retained TeX
manuscript, including its alternative positive-weight proof. The canonical
README, complete manuscript and retained certificate were independently
matched to actual Git bytes at upstream commit
`b73cd1804e40e0d101294eedb156984f0d62b4a6`.

Definitions, Challenge, Comparator and YAML match the accepted hashes. The
numerical-target change consists of precisely the two expressly permitted
wording corrections, with its original accepted bytes preserved. No
mathematical definition or public contract was weakened.

The target still quantifies every `n ≥ 3`, every finite set of n distinct
nonzero **complex** points, and every `1 ≤ k ≤ n - 2`, with actual `Real.pi`
and the original factor `4/π`. `Poly` is `Polynomial ℂ`; feasibility permits
every complex polynomial of degree at most k with actual evaluation `p(0)=1`.
The zero-polynomial `natDegree` convention creates no extra feasible input.
The unused L parameter of `feasible` is harmless: normalization and degree
are independent of the evaluation set.

`maxModulus` is the finite maximum of the actual complex norms. `M` is the
infimum over all feasible objective values, not the value of a selected
polynomial. `FullMinimumDraft` proves an explicit member and a lower bound
against every feasible polynomial, then uses `IsLeast.csInf_eq`. `Minimax`
does the same for every five-point subset. Thus the actual minima required
by the original problem are both attained and globally minimal at every set
used in this counterexample. No general all-input compactness theorem is
needed for this negative resolution.

`subsetFamily` contains every powerset member of cardinality five. The final
proof establishes that this family is nonempty and each member has strictly
positive M, then proves positivity of its actual finite maximum. Empty-set
totalizations and division by zero cannot account for the ratio. At n=9,
k=4 all original range conditions hold. The last proof derives a direct
contradiction to the original inequality, with no assumed certificate,
optimality, subset bound, ratio or negated conclusion. The stronger
amplification theorem and matrix-level GMRES witness are outside the formal
claims; the nine-point example already negates the entire original assertion.

## Full-set proof path

The nine nodes are exactly `omega^a + (1/1000)*omega^b` for a,b in `Fin 3`,
with `omega = -1/2 + (sqrt 3/2)i`. The injectivity and nonzero obligations
prevent collapsing the image to fewer points. The witness is the source's
normalized cubic, which is allowed at degree four.

Numeric supplies positive diagonal/off-diagonal weights corresponding to
Holden's `H/(9D)` and `Q/(9D)`, total weight one, constant witness modulus,
and all four complex moments for powers 1 through 4. `weighted_cross_zero`
expands an arbitrary complex polynomial of degree at most four with zero
constant term. Therefore the moment vanishing applies to every difference
`p - witnessPolynomial`, not merely to real coefficients or cubic residuals.
`weighted_minimum_lower_indexed` combines the complex square-norm identity,
nonnegative remainder, and weighted maximum bound. This proves the full
lower bound matching the feasible witness's objective. The indexed route is
valid even without injectivity; injectivity is separately required and proved
for the original nine-point cardinality.

## Every subset and the 109/146 estimates

The generic Lagrange argument uses Mathlib's basis polynomials, with
`b_z = ell_z(0)` and `A = sum |b_z|`. Every b_z is nonzero because nodes are
distinct and exclude zero. Interpolating `(abs(b_z)/A)*b_z⁻¹` yields value one
at zero, degree at most four, and node norm `1/A`. Interpolation of any other
feasible p and the triangle inequality give the matching lower bound. The
phase choice agrees with the manuscript's conjugate expression.

`labels_image` and `labels_card` recover every actual S contained in
`explicitL`, using the injective map from all nine labels. The finite
`occupancy_disjunction` ranges over every finite subset of the grid, with
only the cardinality-five condition. It does not read a certificate table.
The two alternatives are valid: at least four selected points have one
same-cluster companion, or at least three have two companions.

The exact geometric constants are l=999/1000, q=13/7500 and r=2603/1500.
Reverse triangle inequality gives the node lower bound; root distances and
triangle inequality give the near/far bounds. The Lagrange denominator is
split into an actual chosen companion subset and its complement, with all
four positive factors retained. The strict rational margins
`109*q*r^3 < l^4` and `146*q^2*r^2 < l^4` give coefficients strictly above
109 or 146. The complete nonnegative sum is therefore above 436 or 438,
both greater than 10000/23. Taking its positive reciprocal proves the strict
bound on every subset, and finite supremum gives the bound on `subsetMax`.

The final chain uses `M > 299/100000`, `0 < B < 23/10000`, and
`(13/10)*(23/10000)=299/100000` to obtain M/B>13/10.
Mathlib's `pi_gt_d2` implies 4/π<13/10. Every strictness and denominator
condition needed in the final conversion is present.

My independent standard-library Python audit used exact arithmetic in
Q(omega), without executing or importing the author's verifier. It checked
all nine distinct/nonzero nodes, nine constant residual norm squares,
positive weights summing to one, all four exact complex moments and all
81 point-distance pairs. It checked all 126 subsets, obtaining profile
counts 81/27/18, and matched all 630 Lagrange coefficient squared norms to
the retained certificate. Integer-square-root enclosures independently
reproduced every retained 60-digit sum interval and corresponding subset
minimum interval. All product margins and the ratio bound passed. This is
source-level evidence, not a Lean proof oracle; see `AUDIT-RESULT.json`.

## Actual failures and required recheck

All reviewed project source files match the input copies retained for remote
development run **34771972369**. I inspected its module results and raw
Numeric/Minimax stdout/stderr. Definitions and LeanCert Verification returned
zero; Numeric and Minimax returned one. Every subsequent proof module,
including Solution, was skipped. The result explicitly records
`authoritative_verification: false` and `comparator_executed: false`.

The frozen source therefore needs these implementation repairs:

1. `Minimax.lean:27,96,145` uses the rejected `sum ... in S` binder syntax.
   Its source also fails at `:45` when applying `sum_pos'` to the wrapped
   `lagrangeSum` goal, and at `:72` when rewriting absolute value while the
   goal still contains a real norm. Repair these syntax/unfolding/norm-API
   mismatches and recompile the same statements.
2. `Numeric.lean:56` exceeds the heartbeat limit in the injectivity proof,
   causing a downstream unknown-constant error. The squared witness-norm
   proof at `:99` leaves higher powers of sqrt(3) unreduced, and the weight
   sum/moment reductions at `:144,158` exceed recursion depth. The numerical
   statements pass the independent exact audit, but their current Lean proof
   scripts do not establish them. Use the root relation or explicit algebraic
   power normalization to keep the computations bounded.
3. The skipped `WeightedDraft.lean` contains the same obsolete finite-sum
   binder syntax throughout. This is an additional visible source issue
   that the failed dependency prevented the run from reaching. Its locations
   are recorded in `AUDIT-RESULT.json`; correct or eliminate those unused
   duplicate bridges before attempting downstream compilation.

These errors require implementation changes, not weaker hypotheses or a
smaller target. Successful later development compilation alone would still
leave authoritative kernel replay and sandboxed Comparator verification.

## Reuse, API, documentation, trust and limits

I searched and inspected the actual pinned Mathlib Lagrange interpolation,
polynomial-degree/evaluation, finite-supremum, `IsLeast.csInf_eq`, complex
square-norm and π-bound sources. `API-INPUTS.json` records exact hashes and
excerpts. The interpolation and order APIs fit the argument. The five-point
minimax lemmas could later generalize to `card=k+1`, but their present
specialization is sufficient and honest. The indexed weight bridge is broadly
reusable. The unused unindexed weight argument substantially duplicates it;
consolidating that code and reusing `Complex.normSq_add` would simplify
maintenance. Those are quality suggestions, not mathematical obstructions.

The rational geometric margins efficiently replace repeated irrational
calculations over the 126 subsets; the only subset enumeration left for Lean
is pure nine-label combinatorics. The finite arithmetic scripts need the
resource repairs already demonstrated by the remote run.

Holden's mathematical authorship and Stepaniants's distinct formalization
credit, Caltech affiliation and AI assistance are retained. No email or human
endorsement is added. Schiffer/Forsythe are labeled organizational precedents
and supply no imported mathematical theorem. This review reuses the protocol
and retained Forsythe replay-example inspection from my prior NR-03 review;
it is not a new audit of those complete external projects.

The development README honestly excludes authoritative acceptance, and the
old statement metadata is explicitly retained as context. Before publishing
a final package, update that metadata and stale statement-stage prose to the
actual completed source and evidence, including the Section 6 weighted proof
route now used instead of group averaging. Solution's phrase “independently
proved” should not imply successful elaboration or an independent referee's
proof: these are candidate proof modules until their gates pass.

The proof-path source scan found no placeholder, custom axiom, native
evaluation or unsafe override, and no import of Challenge. All fifteen
exports have kernel-trust and axiom diagnostic commands. Comparator permits
only `propext`, `Classical.choice` and `Quot.sound`. Those source safeguards
do not establish a transitive closure for skipped modules.

I ran no local Lean/Lake process, download, cache action, Git mutation or proof
edit. No successful Solution elaboration, transitive axiom audit, default
kernel replay or sandboxed Linux Comparator result was inspected or claimed.
This report covers scope, correctness, quality, reuse, generality, API,
naming/placement, documentation and attribution for exactly the frozen source.
