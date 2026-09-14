# Independent audit of PR #255

**Verdict: PASS for the stated partial/supporting scope. No mathematical merge blocker found.**

Reviewed source head: `ecc57b82bbcb33aa37dd403530669f74bdf2ec30`. Published comparison base: `deb549fa9ddd6b119e6c59016f268237e645dfa2`. Source worktree: `/private/tmp/nla-audit-255`. Review date: 14 September 2026. Reviewer: a separate Codex agent assigned to this PR, not the submitting reviewers. This is an informal mathematical and computational review, not external human peer review or a proof-assistant verification. No Lean verification was performed.

The three permanent IDs, canonical paths, and original mathematical targets are preserved. The proposed statuses are appropriate: **SP-03 Partially resolved; SP-07 Open; SP-09 Partially resolved.** No complete target is solved by this PR. The difficulty and impact ratings remain consistent with the unresolved targets.

## SP-03: Stein normal form, parity, and finite lower certificates

I read the entire new manuscript and the predecessor's regular reduction, degree upper bound, and supermultiplicativity arguments. The new all-rank statements pass direct mathematical review:

- The normal incidence has dimension `(2m)^2`. Its derivative at `(I,0)` is invertible because the real tangent and Frobenius normal spaces are complementary. This justifies generic finiteness, reduced fibers, and generic avoidance of the proper bad loci. The big-cell and denominator exclusions have an explicit good incidence point; they do not silently omit generic critical points.
- In the denominator factorization, the symmetric Gram determinant contributes `2^(m(m-1)/2)`, exactly canceling the factors from the half-Lyapunov operator. Thus `det L = det A det(2A-U_a) det K` has the displayed constant. Polynomial continuation includes singular matrices. The normalized Stein identity has factor `2^(-m(m+2))`; the exterior-square factors and transpose conventions are consistent.
- Left normalization of the invertible data block is an isometry for the transformed bilinear metric. The normalized data family retains generic degree, rather than restricting the original problem to an exceptional data set. The two Stein equations, reconstruction, inverse-transpose square, and gradient factor `1/4` agree.
- The projective-boundary argument correctly uses invertibility of the limiting congruence operator to force `d_nu -> 0` along an invertible direction at infinity. At zero coupling the matrix-square equation has exactly `2^m` simple regular roots for generic `d`; the other branches must reach the excluded divisor or singular infinity. This does not imply conservation of degree in the special fiber.
- The Euler-characteristic calculation stratifies by off-diagonal support, splits off a torus using a spanning forest, and reduces to diagonal tuples. Grouping equal nonzero values and the reciprocal double cover gives the stated Stirling sum. It is expressly not an ED-degree computation.
- The parity argument is valid for every positive rank: real generic data give finitely many nondegenerate critical points of a proper distance function; its real critical count has the parity of the Euler characteristic. The polar deformation retract onto `U(m)` and its free central-circle action give Euler characteristic zero. Nonreal complex critical points come in conjugate pairs. I checked the needed proper-sublevel formulation against [Milnor, Theorem 3.5](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/milnmors.pdf).
- The predecessor's upper bound uses a special linear section with bounded total component degree, then `m` quadratic stationarity equations transverse at the critical points. Its off-block Hessian argument establishes supermultiplicativity on the product incidence. The imported ordinary-degree determinant is exactly [Brandt et al., Theorem 3.1](https://arxiv.org/html/1701.03200v2); `delta_4=769408` and `16 delta_4=12310528`. This ordinary degree is not an ED degree.

The full denominator-free polynomial system has precisely the symplectic ED critical points. I checked its tangent-orthogonality interpretation and the global second-derivative bound `4N`. The exact contraction inequalities prove existence, uniqueness in each ball, and simplicity; distinctness must be checked separately.

**This review reran every stored center at all four ranks**, improving on the submitted independent review's 32-center rank-four sample:

| Rank | Stored centers | Fresh exact contraction checks | Exact full-file separation |
|---|---:|---:|---|
| 1 | 4 | 4 passed | passed |
| 2 | 24 | 24 passed | passed |
| 3 | 543 | 543 passed | passed |
| 4 | 31,183 | 31,183 passed | passed |

The rank-four pass took approximately 265 seconds. Its certificate SHA-256 is `2126da41dabc9e2bf92993dba888bc855c45ab9178177feb3e65a79d383c7768`. Fresh reports retain all radius exponents. A reviewer-written second separation check sorted exact `Fraction` intervals in the first real coordinate and checked all adjacent gaps, independently of the supplied sweep routine. All 31,182 rank-four adjacent gaps are strictly positive. Thus no sampled or submitted-only acceptance is needed for the rank-four count in this review.

The reviewer driver obtains untrusted floating inverse proposals from the exactly reconstructed Jacobian, then calls the inspected Python integer/Fraction contraction implementation. It does not import Numba or call the C++ backend. The C++ implementation was read but was not built or rerun; Numba and Boost headers are unavailable in this review environment. The report therefore does **not** claim two fresh full arithmetic implementations. All certificate acceptance decisions in the actual replay were exact.

Further checks passed: independent SymPy construction of all 120 equations, all 5,664 Jacobian entries through rank four, and the quadratic Hessian bounds; supplied factorization, Stein, boundary, zero-coupling, and selection suites; 156 reviewer-written corruption checks over 52 valid centers, rejecting a large center perturbation, zero inverse, and negated inverse; four duplicate/touching/separation boundary cases. Symbolic finite checks supplement the all-rank arguments rather than replacing them.

The fresh count and audited parity theorem establish **`D_3 >= 544` and `D_4 >= 31184`**, without claiming a new stored 544th or 31,184th center. There is no completeness certificate and no evaluation of the generic degree in all ranks. The target prediction `D_4=65664` lies inside the remaining interval. Recording this as partial progress is justified; a Solved promotion is not.

## SP-07: completion barriers and the stationary model

I read all new Sections 1–9 and the exact-quadrature appendix. The new arguments pass with their explicit scope restrictions:

- The defect-space compression preserves the selected block and cannot increase the anticommutator norm. Adding zero defect coordinates handles endpoint eigenvalues. Averaging is legitimate in the stated relaxation because the complementary matrix is arbitrary; the attaining broken shift is not normal. Pinching to the positive and negative reflection spaces yields the two edge weights, and their elementary inequality gives the claimed exact completion norm.
- The odd alternating-sum lower bound and attaining angles agree. The direct-sum orbit dilation produces an orthonormal selected basis inside reducing eigenspaces; its overlap is circulant and fixes the constant vector. The arbitrary-overlap obstruction requires a selected compression eigenvalue `+1` or `-1`, and the dimension-intersection argument supplies that eigenvalue for the specified Hall witness in dimension `2p-1`. This is not a universal constant-one bound for the completed pair's full matching distance.
- The compressed-optimum formulas yield different limiting quotients for different denominators. They do not transfer a compressed bound to a normal completion.
- The periodic Lipschitz multiplier preserves `H^1`; reflection cancels the unbounded derivative. The Pauli singular-value formula gives the bounded multiplier norm. The reciprocal-speed integral proves the phase lower bound even for nonmonotone paths, diverges at the endpoint, decreases strictly, and is attained by the positive ODE solution. Fixed-sum strict convexity and endpoint signs prove the height balance; the uniform integral estimate proves the limiting quotient. No certified global optimizer over both parameters is obtained.
- The explicit cross-channel bijection computes the actual countable matching distance. Its ratio is strictly below one. Hence the formal number near `1.0373054` is **not a finite normal-matrix lower bound** and does not improve the inherited finite endpoint.

I inspected the rational quadrature implementation: the tangent-half-angle quartic, exact integrated binomial polynomials, absolute tail bound, outward square roots, cell accumulation, and Machin-series enclosure correspond to the written proof. Fresh exact checks passed for all 500 odd orders from 3 to 1001, the specified formal interval, ten current exact/rejection test methods normally and under `-O`, the retained rank-one arithmetic certificate and its nine tests, and the inherited order-193 certificate by both congruence diagonal dominance and interval LDL.

For order 193, I also inspected the exact constructor and both positivity implementations. Rational spectral recursion proves the active pair-sum identities; the selected Hall set and explicit matching prove distance exactly 2. The contractive Gram-inverse enclosure establishes a genuine rational orthogonal reflection; the norm error budget transfers the strict slack to that exact reflection. The fresh replay confirms norm `< 19281027/10000000`, hence ratio `> 20000000/19281027`. The two positivity methods share the spectrum/reflection enclosure code; they are not wholly independent constructors.

[Tang's primary manuscript](https://arxiv.org/html/2609.09177v1), introduction and Section 3, does explicitly report the classical universal upper bound `2.9038872828` and leaves the sharp constant open. That verifies the continuation's literature attribution. Tang's new result is a dimension-dependent truncation inequality, not a new dimension-free constant; this review does not re-prove the older Fourier-analysis bound. Likewise, the retained rank-one arithmetic replay is not a fresh full written audit of every nested historical reduction or fixed-rank theorem. None is needed to validate the new completion and stationary-model arguments.

PR #254's distinct SP-07 continuation should remain alongside this one. Neither continuation determines the unrestricted sharp constant. **Keep Open.**

## SP-09: first-order independent splitting

I read the complete new proof, the retained reference trace certificate and equality argument, and the quantitative rigidity proof actually imported by the new result. The primary Horn input was checked directly in [Bercovici–Collins–Dykema–Li–Timotin, Theorem 0.2](https://arxiv.org/html/0805.4817v1). Its block integrals become averages after multiplying the output matrices by the smaller dimension. Reversing the ordered spectrum under negation and gluing triples along unitarily equivalent partial sums gives the claimed cancellation for finite lists of independent Hermitian orbits. This does not deamplify the coupled normal residual itself.

The reference lower certificate is dimension independent: it uses projection relations and trace cyclicity, without rank-one identities. Strictly positive Gram blocks and the distinguished polynomial of normalized trace one rule out a smaller norm. At equality the entire degree-four relation kernel forces a unital representation of `M_3`, giving exactly the block-gauge orbit. The quantitative estimate follows from four controlled relations and polar alignment, consistently using the same normalized Hilbert–Schmidt norm. This supplies the initial operator-norm `O(sqrt(t))` estimate at fixed dimension.

The new finite geometry, tensor lifting, and analytic rate argument are consistent. The scalar face has rank 3, the gauge rank is 5, and a one-dimensional nongauge flat direction remains. Tensoring with Hermitian coefficient matrices gives the full skew-Hermitian space and `range L_r = kernel Phi_r`. The positive density controls a one-sided face bound without assuming commutativity. The finite-dimensional slice removes the gauge with a bounded inverse at fixed dimension.

At a true perturbed minimizer the Schur complement has the **positive correction `13/23`**. Its one-sided estimate improves the transverse coordinate from `O(sqrt(t))` to `O(t)` before any quadratic terms are discarded. Mixed terms then have order `t^(3/2)`, and the remaining flat term has positive partial trace `T^2/52`. The upper construction solves the entire active correction through `range L_r`; the fixed lower spectral gap makes off-diagonal effects quadratic even though the top eigenvalue is multiple. This proves the stated lower/upper expansion and right derivative. Horn cancellation then gives the nonnegative squared amplification gain `O(t^(3/2))` for **fixed** repetition, amplification, and directions.

The full exact suite passed with optimization enabled: 208 top-level and 163 retained manifest entries, all eight retained exact programs (including the universal trace identity, equality kernel, local geometry, modular and integer minors, and rigidity constant), the new exact finite geometry, and all nine new corruptions. The fresh finite geometry reports curvature `1/52`; the unreduced value `19/2080` is correctly not substituted for it. Numerical feasible-witness demonstrations were not needed or rerun. This audit does not separately accept every ancillary theorem in the historical archive, especially the entire open-neighborhood certificate transport theorem; the imported reference distance, equality, and stability statements used here were examined directly.

**Keep Partially resolved.** Exact equality at nonzero perturbation, uniformity in amplification, and the original universal reverse inequality remain unproved.

## Integrity, presentation, and reproducibility

All 101 SP-03, 44 SP-07, and 208 SP-09 submitted-manifest hashes matched in the immutable source worktree. Attributed TeX differs from submitted TeX only by author/affiliation presentation and shorter SP-03 table headings; the exact diffs are retained. All 44 pages of the three canonical PDFs (2, 2, and 3 pages) and attributed manuscripts (14, 12, and 11 pages) were rendered and visually inspected. No clipping, broken glyphs, overlapping content, or unreadable tables were found. No PDF edits were made. The source worktree remains clean.

Fresh evidence is under `pr255/evidence/`. Scratch source copies and PDF rasterizations are deliberately excluded from that small evidence bundle. The retained executed reviewer drivers use the disclosed `/private/tmp/nla-review-253-256/pr255/` layout; create scratch copies of each immutable submitted directory there to repeat them. Main commands were:

```text
/private/tmp/nla-batch-python/bin/python pr255/check_sp03_all.py
/private/tmp/nla-batch-python/bin/python pr255/check_sp03_controls.py
# From scratch/sp03, normally (assertions enabled):
python verify/test_factorization.py
python verify/test_stein_form.py
python verify/test_boundary.py
python verify/test_zero_coupling.py
python verify/test_polynomial_system.py
python verify/test_selection.py
# From scratch/sp07:
python -S verify_all.py --prior --output /outside/source/sp07-full-checks.json
# From scratch/sp09:
python -O verify_all.py --report-dir /outside/source/sp09-exact
```

Environment: Python 3.12.14, NumPy 2.3.5, SymPy 1.14.0 on macOS; standard-library arithmetic for SP-07. Full repository validation, final combined catalog/PDF consistency, GitHub checks, and exact-head merge guards belong to the coordinating audit. This report's acceptance is for the exact source head above.
