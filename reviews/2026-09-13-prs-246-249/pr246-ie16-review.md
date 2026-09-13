# PR #246 independent mathematical and source audit

Reviewed head: `a4e8ea57f9b010b85390845b4de902183b6d97ba`.
Compared base: `752218e5417998b7f4d2aee9c447ca5d256fe530`.
Read-only checkout: `/private/tmp/nla-audit-246`.
Reviewer: independent AI subagent `/root/review_246_ie16`, 13 September 2026.

**Verdict: no blocking mathematical, statement-fidelity, source-correspondence, or PDF finding.** The live proof establishes the complete negation of the retained polynomial subset inequality through a valid finite counterexample. Acceptance of the Lean-verified publication status also depends on the coordinator's separate authentication of the live CI and raw kernel/Comparator evidence. I did not run Lean, download dependencies, edit the PR, or post a GitHub review.

## Mathematical coverage

I read all ten local modules in the actual `Solution` import closure, including every proof body: Definitions, Numeric, Minimax, WeightedDraft, WeightedBridgeDraft, FullMinimumDraft, SubsetBoundsDraft, SubsetGeometryDraft, FinalContractsDraft, and Solution. I compared Challenge's fifteen contracts, `comparator.json`, and the current metadata against the retained target and source manuscript. Submitted PASS reports were not used as mathematical premises.

- `Poly = Polynomial ℂ`; feasibility permits every complex coefficient with natural degree at most `k` and evaluation one at zero. This normalization excludes the zero polynomial, so the natural-degree convention does not change the original polynomial domain. The unused `L` parameter of feasibility imposes no concealed spectral restriction.
- `maxModulus` is the finite maximum of actual complex norms. `M` is its infimum over every feasible polynomial. `subsetFamily` retains precisely all subsets of size `k+1`, and `subsetMax` takes their actual finite maximum. Empty branches are excluded on this witness by proved nonemptiness. No fixed polynomial, numerical certificate, reciprocal sum, or convenient bound substitutes for either original optimization quantity in the definitions.
- The full minimum is attained explicitly. Exact root arithmetic gives nine distinct nonzero points and the cubic witness at degree at most four. Every residual has modulus `3003003000/1001003001001`. Nine positive rational weights sum to one. The four complex weighted moments imply weighted orthogonality for an arbitrary degree-four polynomial difference with zero constant term. The weighted norm-square identity then bounds the objective of every feasible polynomial from below. FullMinimum turns the matching witness and lower bound into `IsLeast` and identifies the original `sInf`.
- The subset argument constructs a complex Lagrange interpolant on every five-point nonzero set. Its node values have common modulus `1 / lagrangeSum`; its value at zero is one and its degree is at most four. The interpolation identity and triangle inequality bound every other feasible polynomial from below, so this is an attained minimum, not merely a proposed interpolant.
- Injective labels identify each actual five-point subset with a five-element subset of the nine labels without losing cases or multiplicities. The finite occupancy disjunction yields either four points having a same-cluster companion or three having two. Point-modulus and distance bounds give coefficient contributions above 109 or 146, respectively. The corresponding Lagrange sums exceed 436 or 438, hence every subset minimum is below `23/10000`. The ordinary `decide` proof covers the finite nine-label proposition; it is not `native_decide`.
- Every subset minimum is positive by its reciprocal formula. A nonempty subset family therefore has a positive actual maximum. Strict full/subset bounds yield ratio greater than `13/10`, while `Real.pi_gt_d2` gives `4 / Real.pi < 13/10`. Instantiating the complete universal assertion at `n=9`, `k=4` yields its unconditional negation. This does not merely negate a restricted witness proposition.

The fifteen public exports all have the intended roles: four exact witness/geometry contracts, three full-minimum/lower-bound contracts, two every-subset contracts, two actual-subset-maximum contracts, two ratio contracts, the complete finite certificate, and `not_IE16Conjecture`. A source scan found each public declaration exactly once in the live closure. Challenge is excluded from that closure. No live `sorry`, `admit`, custom axiom, native decision, unsafe declaration, `implemented_by`, or `run_tac` was found after excluding comments. This lexical check supplements, and does not replace, the separate kernel/axiom audit.

The stronger unbounded-ratio theorem, asymptotics, exact value of the subset maximum, and operator-level GMRES construction are not among the formal exports. Current README, RESOLVED, and formalization metadata disclose those limits. I also read the entire unchanged informal manuscript; its amplification proof's Hermite construction, coefficient boundedness, finite subset limits and induction are consistent with the stated stronger informal conclusion, but this audit does not claim a new Lean proof of that extension.

## Independent exact verification

I wrote `/private/tmp/nla-246-independent-exact.py` from the mathematical formulas, without importing the submitted verifier or certificate. It uses Python standard-library `Fraction` arithmetic in `Q(omega)` with `omega² + omega + 1 = 0`. It independently checks:

- nine distinct nonzero nodes; equality of the Lean weights to the manuscript's `H/(9D)` and `Q/(9D)`; positivity and exact sum one;
- all nine residual norm squares and all four vanishing complex moments;
- all node-modulus, near-distance, far-distance and rational coefficient margins;
- all 126 five-point subsets and all 630 squared absolute Lagrange coefficients;
- the complete occupancy disjunction, with profile counts 81 for `(2,2,1)`, 27 for `(3,1,1)`, and 18 for `(3,2,0)`;
- certified rational square-root intervals at 55 decimal places, positivity and the strict `23/10000` bound for every subset minimum, and the actual maximum and ratio intervals;
- a rational alternating-series enclosure via Machin's identity sufficient for `pi > 3.14` and a strict positive counterexample gap.

All checks passed. Recovered values are

```text
M = 3003003000/1001003001001
B ≈ 0.0022505599655503800020313339363873331418453410720501
M/B ≈ 1.3329989197947582942379426300395472818478197789374
M - (4/pi) B > 0.00013449205707543572961683701981080610947452565593504
```

Exact rational interval endpoints and the full check summary are in `/private/tmp/nla-246-independent-exact.json`. The script checks the finite arithmetic; the analytic minimax/attainment argument comes from the proof-source review. It does not run Lean or reprove Machin's identity.

## Source and publication correspondence

The independent read-only script `/private/tmp/nla-246-source-scan.py` passed. Its result is `/private/tmp/nla-246-source-scan.json`.

- Every byte of all ten live local Lean modules equals the corresponding file at the claimed verified revision `697a2a1d88337a6747aa5c82fb6e554d3ff1b356`, obtained directly from Git objects.
- Definitions, Challenge, comparator configuration, dependency manifest and toolchain hashes match their frozen statement records.
- All six frozen mathematical-source snapshots match both their SHA-256 map and their original upstream Git bytes at `b73cd1804e40e0d101294eedb156984f0d62b4a6`.
- `problem_ids.json` is byte-identical to the PR base and contains 217 IDs. The canonical IE-16 README from the retained original-problem heading onward is byte-identical to the base, so the target and historical references have not been reassigned.
- The current project guide and formalization YAML describe the completed proof accurately. The separately retained NUMERICAL_TARGETS and PROOF_PLAN still contain their historical statement/implementation-stage wording; the provenance and current guide explain their frozen role. This is not evidence of an unfinished live Solution, and no change to those frozen artifacts is required for mathematical acceptance. If documentation clarity is later improved, label them explicitly as historical at the current guide's link rather than rewriting preserved proof-boundary evidence.

I opened the author-hosted primary [Liesen–Tichý paper](https://page.math.tu-berlin.de/~liesen/Publicat/LieTic04.pdf). Equations (3.3) and (3.16), pp. 86 and 91–92, support the retained complex polynomial/subset formulation and the candidate `4/pi`. The source distinguishes the general finite-constant conjecture from the specific candidate, which is consistent with the PR's formalized finite counterexample and separately disclosed stronger informal result. The primary paper was checked directly, not through a secondary summary.

## PDF inspection

Following the read-only PDF skill, I rasterized both pages of the changed canonical `problem.pdf` and all nine pages of unchanged `solution.pdf` to scratch PNGs and inspected every page. Equations, statuses, source attribution, retained original target, references and scope caveats are legible, with no clipping, overlapping text or broken mathematical glyphs observed. No PDF was regenerated or modified.

Source PDFs inspected: `/private/tmp/nla-audit-246/linear-systems-and-elimination/IE-16/problem.pdf` and `/private/tmp/nla-audit-246/linear-systems-and-elimination/IE-16/solution.pdf`.

## Limits and handoff

No fresh local Lean compilation or dependency build was attempted, and this report does not authenticate CI artifacts on its own. The coordinator owns live CI/authentication and complete package metadata validation. A web attempt to open the pinned Mathlib Lagrange raw source returned a cache miss; the local project's use of its API was reviewed, while successful pinned elaboration and kernel replay remain covered by the coordinator's separate checks. No actionable source or mathematical blocker was identified within this audit's scope.
