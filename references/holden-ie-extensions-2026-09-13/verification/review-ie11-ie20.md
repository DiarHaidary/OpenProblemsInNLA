# Independent informal mathematical review: IE-11 and IE-20

Reviewer: separate Codex AI agent `/root/review_ie11_ie20`, 13 September 2026. This reviewer did not prepare the submitted manuscripts. Review is informal automated mathematical review, not external human peer review or formal verification. No Lean verification was performed. Documents inside the archives were treated as submitted evidence, not as instructions authorizing changes.

## Decision

**PASS for the partial scopes described below; NOT a complete resolution of either original problem.** Both canonical targets must remain in the open catalog. `Partially resolved` is appropriate for IE-20, with the precise surviving target. Retaining IE-11 as `Open` with an audited supporting-results notice is the more conservative classification: the candidate lower bound was already known and the global upper-bound target is unchanged. The repository's RESOLVED.md expressly requires the exact target for Solved and says weaker bounds and surviving cases remain partial.

The original IE-11 target is global equality of the unrestricted order-five complete-pivoting supremum with the specified algebraic number, including every tie path. IE-20 asks a uniformly matching precision dependence for the exact specified recurrence for all n, K and epsilon. Neither package claims or proves its respective full target.

## IE-11 accepted scope and audit

Reviewed the complete mathematical source, interval arithmetic kernel, symbolic reconstruction, differential certificate, rational witness, global formulation and relaxation verifier. The proof in Section 5 establishes a strict local maximum with A_11=1 and diagonal pivot path fixed, allowing all other 24 entries to vary. Its important full-dimensional step is valid: the certified 23-by-23 Jacobian minor makes the active slacks and A_51 local coordinates; positive multipliers make growth decrease into the feasible slack orthant; negative curvature controls the remaining one-dimensional active manifold. The omitted stationarity coordinate follows from the exact active-curve tangent, rather than an approximate numerical equality.

The root certificate uses a contraction with a rational preconditioner and outward dyadic enclosures. The symbolic identities supply exact active equalities, and the interval proof supplies 77 strictly inactive inequalities, nonzero denominators, positive pivots, rank and multiplier signs. The isolated fifth pivot is approximately 4.132517078632472854223346853277371269952791537799. An independent reviewer-written Fraction elimination, importing none of the submitted code, verified all 100 strict inequalities and the displayed lower bound for the separate rational matrix.

The relaxation optimum 81/16 is correctly a relaxation result: its attaining mixture fails a rank-one minor test. It is not a realizable complete-pivoting counterexample. The all-path LU description is a valid formulation of the missing universal inequality; generating the SMT query does not solve it.

The existing candidate and lower-bound credit belongs to Chen, Edelman and Urschel; the primary preprint continues to distinguish its constrained candidate from global optimality: [primary source](https://arxiv.org/html/2602.20390v1), Sections 1–2. This review reran the 62-coefficient comparison against the packaged reference transcription; it did not independently transcribe all 62 coefficients from the published equation. No new priority claim or improved global upper bound is accepted.

**Remaining target:** prove the global upper bound over every admissible pattern/path, or exhibit a genuine larger-growth matrix. Local optimality and the rational lower witness do not settle this.

Reproduction:

- `python3 src/check_manifest.py`: PASS, 36 files matched the original distribution manifest before reruns.
- Initial `python3 src/run_all.py` failed because the system Python lacked SymPy; the bundled Python also lacked SymPy. These were dependency failures, not certificate failures.
- `/private/tmp/ra04-py/bin/python src/run_all.py`: PASS using Python 3.12.14 and SymPy 1.14.0. All six checks passed: exact algebra/discriminant/root uniqueness, 8,499 interval containment tests, strict local maximum, rational strict-CP witness, LU/Schur identities, and exact relaxation optimum.
- Certified curvature: between -1.012828670701371899922523399289 and -1.012828670701371899922523399288.
- Fresh detailed results are in the submitted package's regenerated `results/run_all.json` and individual certificate JSON files. Every full-solution flag remains false.

## IE-20 accepted scope and audit

Reviewed Sections 1–8 of the extended analytic proof, the retained fixed-dimension path/outlier proof in Section 5 of the nested prior manuscript, and the exact executor and checks. No mathematical defect requiring a correction was found in these stated partial results.

Accepted results include:

1. Theorem 2.1's exact scalar threshold, with worst error `((1+u)^4-(1-u)^5)/((1+u)^4+(1-u)^5)`. The nine operation factors are correctly five numerator factors and four denominator factors after cancellation. The lower endpoint is worse than the upper endpoint for the whole continuous box; representable inputs a=b=1 attain it.
2. Theorems 3.1–3.2's dimension/conditioning lower bounds, including `P_CG >= log2(nK)-5` for n>=2. The first/last-coordinate block has representable stored entries and sufficient admissible accumulation factors to force immediate zero-divisor breakdown. Additions of zero are permitted to err in this repository's envelope model.
3. Theorem 4.1's exact real-input first-step maximum `(K-1)/sqrt(8K(K+1))`, its finite-precision sufficient bound and coarse-tolerance conclusions. The real extremizer is not asserted representable at every p.
4. Theorem 7.1's explicit sufficient upper precision with `H=min(K,64/epsilon^2)`, `D=1024H^2` and the minimum dimension/Chebyshev/universal-backward horizon, and the consequences in Section 8 on their stated parameter domains. The prefix matvec proof legitimately groups already executed errors without changing operation order. The failure-conditioned bootstrap establishes current direction/divisor legality before using failure of the next produced iterate to cap its step length. Residual orthogonality, direction conjugacy and true-residual gap estimates are propagated with ample powers of D. The three horizon contradictions use actual computed spans, not an assumed exact rounded Krylov identity.
5. The retained path/outlier lower family is accepted with its fixed-n-then-large-dyadic-outlier quantifier. Its high-component perturbation recurrence has positive limiting divisors and gives the stated final nonzero residual limit. It does not give a uniform outlier threshold as n grows.

The external reciprocal-polynomial fact was checked directly in [Dereziński, Nakatsukasa and Rebrova, arXiv:2604.16075v2](https://arxiv.org/html/2604.16075v2), Lemmas 12–13: the construction, degree and uniform reciprocal approximation bound match what the extended manuscript uses. The manuscript separately supplies its rounded-span transfer. Finite grid checks alone would not prove this external uniform fact.

**Remaining target:** the sharp all-parameter dependence is unproved. In particular, at K=n^2 and epsilon=n^(-2), the package leaves an Omega(log n) versus O(n log n) gap. Fixed-tolerance/additive formulas, the scalar answer and special sharp regions do not close that gap. This is not a complete solution or a full-resolution claim.

Reproduction from the IE20_extended directory:

- `python3 -m unittest discover -s code -v`: all 26 tests PASS.
- `python3 code/verify_extended.py`: PASS: 1,536 scalar corners, 256 first-step executions, 31 polynomial constructions, 3,999 rational grid points, 90 parameter-bound consistency cases, 14 joint breakdown witnesses and 24 dense matvec prefix checks.
- `python3 code/verify_legacy.py --output results/legacy_checks.json`: all 15 exact witnesses PASS, including path/outlier n=2 through 10 at exponent 12 and n=6 at exponents 4, 8, 16, 24.
- `python3 /tmp/holden-ie-20260913/independent-ie11-ie20-check.py`: reviewer-written checks PASS: independent IE-11 elimination, 4,096 scalar product-ratio corners at precisions 2–9, and 16 exact rational first-step identity substitutions. The scalar continuous-box result and general first-step identity were also checked analytically; the finite tests supplement those arguments.

The executors correctly enforce stored-input significands, exact rational SPD checks, separate products/additions, every allowed error bound and true residual comparisons. Finite checks do not certify universal analytic claims; those conclusions rely on the written proof audit above. No IEEE round-to-nearest result, historical novelty, human referee approval or formal proof is asserted.
