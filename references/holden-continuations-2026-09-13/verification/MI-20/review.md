# Independent informal audit: MI-20 round four

Reviewer: independent Codex AI agent `/root/review_nr_mi`, separate from the submission integrator. Date: 2026-09-13 (America/New_York).

Verdict: PASS for the main upper/lower enclosure, positive power-system characterization, order constraints and interpolation argument **after the explicit cyclic-reduction correction below is applied**. The submitted proof as written has that local gap. This is an informal AI-agent audit, not formal verification or external human peer review. No Lean was run. No historical novelty claim was checked.

Retain MI-20 **Open**: the exact sharp function C_p(m), including sharpness at p=4/3,m=2, remains undetermined. Bounds and an equivalent unevaluated supremum do not resolve the canonical target.

## Required correction and its independent verification

In the proof of “Exact cyclic reduction,” the submission chooses L_l=S_tilde^(1/2) U^l but then sets T_l=m^(-2/q) R_tilde^2. Since a_l=U^(-l) S_tilde U^l, that constant choice does not produce the pinching claimed in the next sentence. The correct choice is

    T_l = m^(-2/q) U^(-l) R_tilde^2 U^l.

Its Schatten t-power constraint is unchanged by unitary conjugation. Writing E for block pinching, direct multiplication now gives

    sum_l a_l = m E(S_tilde),
    sum_l a_l^(1/2) T_l a_l^(1/2)
      = m^(1-2/q) E(S_tilde^(1/2) R_tilde^2 S_tilde^(1/2)).

For each coordinate projection P_j the block fidelity equals the trace norm of R_tilde S_tilde^(1/2) P_j S_tilde^(1/2), which is ||R X_j||_1 by the isometric dilation identity. Thus fidelity is m^(1-1/q) sum_j ||R X_j||_1; the denominator m^(1/p) cancels. This repairs the reverse cyclic inequality without changing any theorem or certificate. Acceptance in this report refers to that corrected proof.

## Mathematical audit

The positive-dual unitary maximization follows from Schatten duality and polar decomposition. The inner fidelity problem has a unique minimizer: strict convexity of tr(AK^-1), convexity of the block Schatten norm, and the two coercive boundaries suffice. Its first-order equation constructs a feasible maximizing dual tuple, so no unjustified minimax exchange is needed.

At a fixed-order normalized maximizer, support compression makes A positive definite. A rank-one perturbation in a singular block's kernel increases the numerator to first order, while its p-power constraint increases by epsilon^p. The unique-inner-minimizer envelope derivative is valid locally; hence every block is positive definite. I checked the factors and exponents in the Lagrange equations, the ordered matrix power identity, both directions of reconstruction, and the scaling giving (Lambda/2^(2kappa-1))^(1/(2kappa)).

The sum constraints use operator Jensen only in its valid power ranges and order-preserving maps of degree strictly between zero and one. The individual-root proof uses Loewner–Heinz for kappa<=2 and the correctly parameterized Furuta inequality for kappa>2. I verified the cited Theorem F(ii), including its parameter condition, at https://files.ele-math.com/articles/mia-01-10.pdf .

The cubic certificate uses ordered trace words, cyclic invariance and reversal only. Realification justifies this model for complex Hermitian matrices. Each localizing matrix is a Hilbert–Schmidt Gram matrix with two positive weights, so its pairing with a positive coefficient matrix is nonnegative. I read the model and interval acceptance code and checked that the same cubic multipliers are shared between endpoints. Their affine combination therefore excludes every Lambda in the interval, not merely its endpoints. The inherited eight-stage cap is recomputed before the interval certificate is accepted. Taking a supremum over orders justifies a non-strict final upper bound even though each finite-order maximizer lies strictly below the excluded endpoint.

The interpolation proof explicitly computes the sum of the boundary moduli of its analytic family; it does not incorrectly treat that denominator as a linear norm. Its exponents agree at p=4/3 and the endpoint p=2. The endpoint source, https://arxiv.org/html/2608.17565 , proves the sharp quadratic formula used for the initial cap. I checked the exact lower-certificate argument's row-norm contraction bound, polar-factor perturbation bound and integer-power comparison, distinguishing fixed-moduli upper endpoints from universal upper bounds.

## Reproduction

Ran unmodified supplied standard-library verifiers, with output directed outside the supplied package:

    python3 -B -S code/check_hashes.py
    python3 -B -S code/verify_all.py
    python3 -B -S code/test_exact.py

Integrity passed for all 53 files. The eight-stage inherited chain and new interval certificate passed; the latter checks 184 identities and 44 rational positive-definite Gram matrices. All 27 tests passed, including corruption controls and literal noncommuting-matrix checks. Logs: hashes.log, verify_all.json, test_exact.log. The code is read-only for these calls; original files were preserved.

Recommended canonical summary after correction: “An independently audited continuation proves 1.018371575 < C_(4/3)(2) <= (861/800)^(1/4), with corresponding interpolation bounds and a positive power-system characterization. The upper and lower bounds do not match; the full sharp function remains Open.” Link both the corrected manuscript and this audit, preserving the original submission separately and documenting the correction.

## Publication correction record

Applied only to the publication report.tex; the extracted original is unchanged.

Original snippet: `T_\ell=m^{-2/q}\widetilde R^2.`

Corrected snippet: `T_\ell=m^{-2/q}U^{-\ell}\widetilde R^2U^\ell.`

Original snippet SHA-256: `b2bf2efaca9beac70296ed44a221f3a7feb193d90c7c5bad22f1da25823f3f73`

Corrected snippet SHA-256: `482e092a8421ef260cc0916e7ba8314ea3c6764d2eb0463c9861ae7e7914d14b`

Publication TeX before correction SHA-256: `56d61a5c904121fa5cd23681c166e289cbcf3ed62164953ced4ead8a94d1747a`

Publication TeX after correction SHA-256: `785d79d7f9ffe54e08a0c27dbd883ca64e58284049983da9c9366fe5611ee78a`

The independently checked algebra above establishes the corrected reverse reduction. With this applied, the stated limited-scope verdict is PASS.
