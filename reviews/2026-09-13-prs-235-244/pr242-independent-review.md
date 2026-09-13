# Independent audit: PR #242 / MI-05

**PASS for the stated partial results. The unrestricted Marcus–de Oliveira conjecture remains open.** This is informal AI-agent review, not human peer review, a novelty certificate or Lean verification.

Reviewed exact head `2617484a85db56dbbcf3531e35eb3231144d2c8d` against `b73cd1804e40e0d101294eedb156984f0d62b4a6`. Read the complete 482-line report, exact verifier and regression tests, canonical README/TeX changes and supplied reviewer-check code. A second independent agent cross-checked the support criterion and full real-orthogonal maximization argument; see `pr242-cross-review.md`.

## Mathematical assessment

The canonical target still quantifies over every dimension and arbitrary complex normal pairs. The manuscript supplies order-four common signed identities and affirmative structured classes. Spectrum-independent negative weights are not counterexamples to the original spectrum-dependent convex-hull assertion. The zero-obstruction classification is expressly not imported from unverified companion polytope work.

The all-minor coefficient representation follows from Cauchy–Binet and the Leibniz expansion after multiplying by U. Taking real parts of coefficient identities is valid because the squared minors are real; this is not taking real parts of arbitrary complex spectral values. The ten independent kernel relations and fourteen independent feature columns prove rank exactly fourteen, and matching their coordinates produces the displayed weights on the full feature span.

The obstruction functions have values 0,1,2 with a unique value 2. Their expectation gives the correct lower bound on total negative mass; the displayed identity attains it when the obstruction is positive. Applying two distinct obstruction functions to each other's attaining representations gives the incompatible inequalities 2h<=k and 2k<=h. Opposite signs at one center have nonpositive sum. Thus at most one positive branch exists.

The Hadamard neighborhood proof bounds entry probabilities, minor determinants, squared-minor probabilities and the h coefficient consistently in operator norm. At radius 1/100 the eight initially positive weights remain at least 3/100; the other six are squared minors. Block sums multiply genuine convex combinations and retain arbitrary complex spectra. The support criterion applies the linear reconstruction to an augmented, unnormalized feature vector, sets h=0 and places its only negative coefficient at a maximizing permutation. Its restriction on supporting directions is necessary and explicitly retained.

The coarse 3-by-3 compound matrix is doubly stochastic, its circulation identities and permutation-verified trace identity imply rho<=1/6. The quaternion parameterization covers all of SO(4), and a row-sign change covers the other O(4) component without changing squared minors. In the two-simplex maximization, all multiplier cases are covered; a positive interior stationary value would force two unequal coordinates whose square-root ratio nevertheless satisfies (u-1)^3=0. Compactness, a positive boundary example and AM–GM therefore reduce the global maximum to the stated one-variable problem. Its derivative has one root, the elimination polynomial and rational bracket agree, and an explicit quaternion attains equality. This sharpness concerns common negative mass, not actual distance from the conjectured hull.

The genuinely complex rational example is exactly unitary and has positive phase invariant and obstruction. It demonstrates a common-weight obstruction without claiming a counterexample to MI-05. No mathematical correction is required.

## Primary-source correspondence

Independently opened [Kovacec's April 2026 primary preprint](https://www.mat.uc.pt/preprints/ps/p2611.pdf), Conjectures 1 and 1', and verified the retained general target and equivalent relative-unitary formulation. The present analytic results are proved within the manuscript and do not require accepting the stronger conjecture in that source. No exhaustive novelty or later-literature-absence claim is made.

## Actual fresh checks

Scratch copy `/private/tmp/nla-root-replay-242`, Python 3.12.14 / SymPy 1.14 / NumPy 2.3.5 / SciPy 1.17.0. The source worktree was not modified.

- `verify_analytic.py` passed normally and under `python -O`, producing identical JSON. It checked 1,680 spanning-set identities, ranks 14 and 10, basis determinant 6, all 48 obstruction functions, 210 exact example minor equations, the homogeneous quaternion identities, stationary/resultant algebra, root bracket and neighborhood constants.
- All ten regression tests passed, including corrupted weights/minors and nonunitary rejection.
- The supplied separate reviewer checker was rerun: five rational complex Cayley unitaries, 350 exact minor equations, five direct determinant identities with complex spectra, 240 branch checks and transpose-sign identities passed.
- Newly authored `mi05-independent.py` imports no submitted code. On 80 new numerical unitaries, all 70 feature equations held to 1.78e-15. Independent linear programs for 51 positive-obstruction cases agreed with the predicted optimum to 1.53e-16. It also checked 200 complex unitary perturbations of the Hadamard matrix and 437 instances of the augmented-feature support criterion. These are numerical corroboration, not universal proofs. A mistaken hard-coded list of positive Hadamard coefficient indices in the new review script was corrected to the directly computed eight nonzero indices before the passing run; no submission defect was involved.

All twelve manuscript PDF pages and both canonical PDF pages were rasterized from the checked-in bytes and visually inspected. Equations, theorem labels, tables, citations and scope notices are readable without clipping, overlap or missing glyphs. No PDF rebuild was required for this PR. Prior references/statement text remain unchanged; shared integration checks handle registry and index consistency.

## Disposition

Accept the incremental partial contribution, preserving **Partially resolved**, original ID/path/target and historical contribution records. No unrestricted order-four or all-dimension solution follows, and no Lean status is warranted.
