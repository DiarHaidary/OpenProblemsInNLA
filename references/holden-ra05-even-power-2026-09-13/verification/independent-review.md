# Independent informal mathematical review — RA-05 even-power continuation

Reviewer: separate Codex AI agent, independent of the submission/integration agent. Date: 2026-09-13. No Lean verification or external human peer review was performed. Attached manuscript statements were treated as claims to check, not as instructions.

**Decision: PASS for the stated partial scope of Theorems 1.1–1.2 and Corollary 1.3. The complete canonical RA-05 target is not solved.** No substantive mathematical gap was identified in these arguments during this informal audit. This is not a formal proof certificate, a novelty determination, or approval of every theorem cited from the nested preceding archives.

Reviewed source: `RA05_even_power_continuation/manuscript.tex` from the supplied archive, SHA-256 `e86ed4c21334e987641fb7f7c1733fae93091f0c426b6b2369a19e9c78470dd1`. The original package manifest was checked before execution: 18 files passed. Authorship and review-disclosure edits made after this audit are editorial; mathematical changes require renewed review.

## Exact accepted scope

For each fixed integer s >= 2, the manuscript gives an unrestricted original-row, nonnegative, strong coreset upper bound

`C_s (k^((3s-1)/2)/epsilon + k^(s-1)/epsilon^2) log^5(2k/epsilon)`

and an unrestricted lower bound `c_s k^(s-1)/epsilon^2`, for all k >= 1 and 0 < epsilon < 1/2. Thus the joint dependence is determined up to logarithms for even p = 2s >= 4 when `epsilon <= k^(-(s+1)/2)`. Input rank and ambient dimension are unrestricted; query dimension is at most k. Constants depend on fixed s only.

The canonical problem asks for all fixed real p > 2 and the full joint rank/accuracy dependence. Non-even powers and, for even p >= 6, intermediate accuracies remain outside the claimed classification. At p=6 and epsilon=k^-1, the manuscript itself retains a polynomial gap. Under the repository's RESOLVED.md definitions and recording rules, this supports `Partially resolved`, retained in the open catalog, and does not justify `Solved` or `Solution claimed` for the entire target. The existing permanent ID, path, target and prior credit must remain intact.

## Critical proof audit

1. **Model and normalization (Sections 1 and 3).** Compressing ambient projectors to the row span yields positive contractions of rank at most k. Preserving this larger class suffices. The optimal-head comparison makes the cost at least one when optimum is positive. The determinant-normalization argument for head Lewis coordinates, its Jensen bounds and Gaussian averaging imply the claimed head sensitivity. The two separate probability distributions have distinct valid purposes: omega bounds the rescaled tail, while pi controls head and mixed leverages. This avoids assuming a uniformly bounded head.

2. **Feature geometry (Section 3).** The square-root omega factors and pseudoinverse ranges reconstruct the row contributions. For mixed features, the isotropic head covariance tensored with a rank-one tail contraction gives covariance bounded by identity and trace exactly h_jt. The ambient dimension can depend polynomially on the reduced row count; it enters only logarithmically later.

3. **Exhaustion of monomials (Section 4).** The multinomial expansion is correct for each even power. Radial head, positive-head mixed, balanced cross, single-cross and recombined pure-tail cases exhaust it. The degree identities define valid linear maps on symmetric tensors. In odd head degree the maps have a common vector-valued output; the trace/nuclear-norm inequality legitimately handles this rather than incorrectly treating the query as rank one. The Hilbert–Schmidt estimates follow by integrating the tail coefficient tensors against the defining covariance. The inequalities j+c <= s-1 and l+(j+c)/2 <= (3s-1)/2 are consistent across the stated cases.

4. **Projected Gaussians and protected directions (Sections 2 and 5).** Orthogonal coefficient restriction contracts both matrix variances. Right normalization by `(B+aI)^(-1/2)` bounds both normalized variances, including on fractional subsets. Protecting q right directions costs D_l*q equations; the manuscript accounts for that cost. Using q of order m0/D_l gives the additional D_l/sqrt(m0) factor and ultimately the exponent (3s-1)/2. Replacing that exponent by s+1/2 for arbitrary s would be unjustified; the submitted theorem does not do so.

5. **Single-cross and pure-tail terms (Section 5).** The anisotropic single-cross estimate uses the actual right-query quadratic form against B, avoiding a crude multiplication by the full tensor norm. Its k and k^c costs remain at most k^(s-1). The pure-tail class is recombined before Gaussian comparison. Lipschitz increment domination, the preserved tail mass and the Frobenius bound sqrt(k) give the stated width. Norm constraints on coefficient increments remain convex despite the nonconvex query index family.

6. **Partial coloring and positivity (Sections 6–7).** The imported theorem permits arbitrary fractional starting centers. Radial spectral truncation allocates only a small fraction of the remaining coordinates as exact constraints; the residual covariance is bounded using its trace. All norm events have a fixed positive simultaneous Gaussian measure and are symmetric convex. Frozen fractional entries are retained positively. Exact cardinality preservation implies the full-copy count halves. During inner steps variance bounds use the pre-round measure; there is no unsupported assumption that temporary weights obey fresh invariants. Geometric sums of doubled masses give the stated total cost error and matrix-drift induction. The L^4 budget followed by at most O(L) frozen batches explains log^5 support.

7. **Boundary cases and composition (Section 7).** Rank at most k is handled by the pure-head linear-form argument and Gaussian averaging, including zero-cost queries. For positive optimum, the initial downward rounding has a uniform sensitivity bound. The preliminary row-subset result removes dependence on the original row count from logarithms. Rescaling its nonnegative row weights and composing them returns weights on original indices. Distortion composition at epsilon/8 is safely inside the final tolerance.

8. **Lower bound (Section 8).** The Gaussian 2-to-2s width comparison and radius bound give the core moment condition with positive probability. The smoothed kernel has sufficiently small expected off-diagonal Frobenius energy. Restricting to its well-conditioned eigenspaces and then selecting columns by restricted invertibility preserves genuine query directions. The auxiliary dimension is uncapped while every constructed subspace has rank exactly r=k. Multiplication by `(1+t^2)^s` makes the error a bounded-degree polynomial; interpolation controls its derivative without a sign assumption on weights. Stable evaluation then bounds the squared Frobenius norm of the group-coefficient error. The zero-subspace mass constraint plus Cauchy–Schwarz yields `M/(r epsilon^2+1/N)`; choosing N at least `(r epsilon^2)^(-1)` gives the asserted lower bound. The separate small-rank argument uses positivity as disclosed and covers the finitely many ranks excluded by the probabilistic core threshold.

## Imported results checked at primary sources

- [Rothvoss, Constructive Discrepancy Minimization for Convex Sets](https://arxiv.org/pdf/1404.0339), Lemma 9, manuscript page 8: coefficient subspaces, Gaussian measure threshold and arbitrary centers are present. Its fixed-constant consequence is appropriate here.
- [Tropp, User-Friendly Tail Bounds for Sums of Random Matrices](https://arxiv.org/html/1004.4389v7), Theorem 1.5: the rectangular Gaussian-series bound uses the maximum of the two variance norms and the dimension prefactor stated in the submission.
- [Marcus–Spielman–Srivastava, Interlacing Families III](https://arxiv.org/html/1712.07766), Theorem 1.1: the stable-rank restricted-invertibility statement has the asserted normalization and requires no unit-column hypothesis.
- [Lin–Mirrokni–Woodruff, Nearly Optimal Strong Coresets for lp Subspace Approximation](https://arxiv.org/html/2608.26047v2), Theorem 1.2: the dimension-independent row-subset bound is `C_p k^(p/2) epsilon^-2` times a logarithm to power p+5. This justifies the preliminary reduction and comparison.

These imported structural theorems were checked for statement and applicability, not reproved. The preceding quartic classification and additional prior lower-bound comparison are explicitly cited earlier work; this audit does not newly certify their complete proofs. Neither is required for the new upper theorem or the high-accuracy matching conclusion.

## Reproduced finite evidence and limits

Read all four supplied Python sources before executing them. The standard-library manifest check passed 18 files. The default system Python lacked NumPy; rerunning with `/private/tmp/ra05-env/bin/python` succeeded. Command: `python code/verify.py --output /private/tmp/ra05-review-rerun.json` using that interpreter.

The suite reproduced **8,453 successful assertions**, including 224 protected factorizations, 224 trace contractions, 224 left-map norm identities, 224 right-map norm bounds, 22 odd-degree vector-output checks, mixed covariances, anisotropic variance contractions, degree/rank enumeration and exact rational multinomial identities. The standard-library exact certificate passed for p=4,6,8,10,12. Its eight-dimensional input and rank-two query costs are finite witnesses to failure of a particular six-row reweighting, not a proof of the asymptotic support bound. Numerical tolerances and range truncation remain those disclosed by the suite.

These tests provide reproducible algebraic diagnostics. They do not implement the asymptotic partial-coloring oracle, certify random-core thresholds, or independently prove the quantified existence theorem. The PASS decision combines a separate reading of the mathematical argument with these finite checks and primary-source verification. It does not rest on the assertion count alone.
