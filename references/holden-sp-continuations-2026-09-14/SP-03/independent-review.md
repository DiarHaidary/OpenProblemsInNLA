# Independent informal review of SP-03 Stein continuation

Reviewer: separate Codex AI agent, 14 September 2026 (UTC). This is an informal mathematical and computational audit, not external human peer review or formal verification. No Lean verification was performed. Instructions within the supplied archive were treated as submission content, not authorization.

## Decision

**PASS for the stated partial mathematical scope; NOT a full solution.** The canonical target remains the all-ranks equality D_m = 2^(m²) + 2^(2m−1). The submission explicitly leaves that degree undetermined. Under RESOLVED.md, “Recording a new resolution”, item 3, `Partially resolved` is appropriate, retaining the complete original target and its permanent ID. `Solved` or `Solution claimed` for the complete target is not supported.

The package gives substantive partial statements beyond the canonical page's existing skew-multiplier reduction. In particular its all-rank parity theorem passes this audit. The recorded rank-four lower bound 31,184 remains below the predicted 65,664, so it neither proves nor refutes SP-03.

## Written mathematical audit

I read the continuation's report.tex, the canonical SP-03 README, the resolution policy, and the predecessor's upper-bound and supermultiplicativity proofs (extracted from its embedded archive).

- The normal-incidence parameterization has the correct dimension, and invertibility of its differential at (I,0) justifies generic finiteness and avoidance of fixed proper closed subsets. The big-cell reduction uses ordinary transpose and the correct transformed bilinear metric. Its generic coverage is justified on the irreducible incidence.
- The denominator identity det L = det A det(2A−U_a) det K follows with the stated constants: the symmetric Gram determinant 2^[m(m−1)/2] cancels the half-Lyapunov factors. The normalized Stein identity det L = 2^[−m(m+2)] Delta_m(4A−I) and the exterior-square factorization are correct, including singular matrices by polynomial continuation.
- The Stein equations, reconstruction, rational matrix map and gradient have consistent factors and transposes. Normalizing the invertible data block is an isometry in the transformed metric; it does not restrict the generic original-data problem. The generic degree of the resulting map is precisely the unresolved D_m, not a computed formula.
- The projective-boundary and zero-coupling arguments pass. The invertible-direction asymptotics force the limiting data d to vanish, ruling out those directions for nonzero limiting d. At zero coupling the square-root equation has 2^m simple solutions for generic d, and local uniqueness explains the excluded-divisor/infinity alternatives for remaining branches.
- The Euler-characteristic proof passes. Off-diagonal support strata split off a positive-dimensional algebraic torus by spanning-forest normalization, leaving only the diagonal locus. Partitioning equal nonzero eigenvalues and applying the reciprocal two-sheeted covering gives the stated Stirling-number sum and ordered-Bell generating function. This is not an ED-degree count, as the manuscript explicitly says.
- The parity proof passes: generic real data give a proper Morse distance function with finitely many nondegenerate real critical points; the symplectic group retracts onto U(m), whose Euler characteristic is zero. The remaining complex points occur in conjugate pairs. I checked the precise cited proper-sublevel Morse theorem in [Milnor, Theorem 3.5](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/milnmors.pdf).
- The full polynomial certificate system is square and has exactly the original symplectic critical points. The 4N Hessian bound and contraction/invertibility argument are valid. Pairwise ball separation is necessary and is checked independently from the contraction inequalities.
- The predecessor's supermultiplicativity proof handles off-block Hessian nonsingularity by the product incidence, and its orthogonal-orbit/linear-section Bézout upper bound passes. Its externally supplied algebraic-degree determinant is indeed [Brandt et al., Theorem 3.1](https://arxiv.org/html/1701.03200v2), giving delta_4 = 769,408 and 16 delta_4 = 12,310,528. This is ordinary degree, not ED degree.

## Checks actually rerun in this review

A reviewer-written driver `check_sp03_sample.py` uses the supplied pure-Python exact-system and rational contraction routines, with inverse proposals calculated from the exactly reconstructed Jacobian. It does not call Numba or the C++ backend. The acceptance inequalities use exact integer/Fraction arithmetic. `SP03-sample-results.json` and `SP03-sample-stdout.log` record:

| Rank | Centers supplied | Centers rerun | Exact contraction and pairwise separation |
| --- | ---: | ---: | --- |
| 1 | 4 | all 4 | PASS |
| 2 | 24 | all 24 | PASS |
| 3 | 543 | all 543 | PASS |
| 4 | 31,183 | 32 deterministically spaced centers | PASS for the selected sample |

All four certificate SHA-256 hashes match the supplied final verification summary. The full rank-three rerun plus the audited parity theorem independently establishes D_3 >= 544. For rank four, the manuscript's full-file successful C++ and separate Python verification records were inspected; **this review did not rerun all 31,183 centers or full-file rank-four separation**. The 31,184 bound is accepted on the audited certificate method and supplied full-file verification record, corroborated by this sample, and must not be described as a full independent local rerun.

The following supplied exact SymPy checks were also rerun successfully using `/tmp/nla-tr03-check-env/bin/python`: `verify/test_factorization.py`, `verify/test_stein_form.py`, `verify/test_boundary.py`, and `verify/test_zero_coupling.py`. Logs are `SP03-factorization-rerun.log`, `SP03-stein-rerun.log`, `SP03-boundary-rerun.log`, and `SP03-zero-coupling-rerun.log`. These support the all-rank arguments but do not replace them. No full implementation test suite, C++ build, exhaustive path tracking, or certificate completeness test was performed by this reviewer.

## Surviving gap and publication scope

The degree of Psi_(b,c) on Omega_m is uncomputed. Neither denominator degree, the Euler characteristic, a numerical search plateau, nor a finite lower count supplies the missing generic-degree upper/lower equality. The rank-four interval remains 31,184 <= D_4 <= 12,310,528, containing the conjectured 65,664. Record the new partial theorems, their exact scope, the certificate verification distinction, author attribution and AI assistance; preserve the existing original problem and prior-source credit. No historical priority claim is established by this audit.
