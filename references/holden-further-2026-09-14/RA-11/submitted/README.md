# RA-11 — Round 4: probability-sensitive bounds and diagonal correction

**Status: PARTIAL. This package is not a complete solution of RA-11.**

The new write-up proves two general upper bounds for arbitrary real PSD matrices accessible only through full responses to real product-vector queries. The first improves the exponential dependence on tensor order at fixed accuracy; the second gives a simple, nonadaptive O(sqrt(n^q)/epsilon) bound with bounded-bit probes. Neither is a matching unrestricted minimax characterization.

Start with `manuscript/ra11_probability_diagonal.md`. It contains complete proofs of the new claims, an exact accounting of oracle calls, a finite-randomness reduction, a restricted-estimator lower bound, and the remaining gap. `PROOF_SCOPE.md` separates new theorems, inherited claims, numerical diagnostics, and missing results.

## New bounds

For 1 < p <= 2, put

    C(n,p) = n^p Gamma(p+1) Gamma(n) / Gamma(n+p).

An ideal complex-spherical empirical estimator, implemented through real queries, uses at most

    (q+1) ceil[(6 C(n,p)^q / epsilon^p)^(1/(p-1))]

queries and succeeds with probability at least 2/3. A bounded-fair-bit version exists with at most twice the sample count. No unstructured oracle input is needed.

For fixed n and fixed epsilon, its exponential rate in q is

    D_n = log(n) + 1 - H_n.

At n=2 this is D_2 = log(2) - 1/2, giving base 2/sqrt(e), rather than the earlier variance-bound base 4/3. The rate D_n is sharp for this particular empirical-average family, NOT for the RA-11 oracle problem.

A separate two-stage diagonal estimator proves

    Q(n,q,epsilon) <= min{n^q, 2 ceil[sqrt(6 n^q)/epsilon]}.

When n^q is a power of two, replace 6 by 3. All inputs can be fixed before any response, and all randomness in this estimator uses a deterministically bounded number of fair bits.

## Reproduce

Python 3.10+ is sufficient for the exact checks. NumPy is required for numerical diagnostics.

    python code/exact_checks.py
    python code/numerical_checks.py

The numerical code is not a floating-point stability theorem. The large-q empirical-average experiment works with an analytically equivalent scalar distribution; it does not allocate an exponentially large matrix. Diagnostic experiments do not replace the proofs.

The `results` folder records the execution status of the bundled scripts. Original available archives/PDFs are copied to `prior_work` without modification; their presence is provenance, not an independent verification of every inherited proof. See `prior_work/CONTENTS.json` for exactly which files were available.

No repository status or remote file was changed.
