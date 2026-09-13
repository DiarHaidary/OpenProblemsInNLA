# PR #195 — second independent cross-review of MI-27

**Verdict: PASS for the full coefficient-one inequality. No analytic or target-fidelity blocker found.**

Reviewed exact head `b190a7ca5580669ea98d12e23970581abbe6ae7c` at `/private/tmp/nla-audit-195`. Read the complete 587-line `references/holden-mi27-2026-09-12/solution.tex`, the canonical README, and its diff against original published base `5830ed4fb06da0659414a3deb2a40ad327aca052`. This cross-review independently checks the universal analytic argument rather than relying on the submitted PASS or root's provisional verdict. No numerical or PDF checks were repeated. No worktree or GitHub changes were made; the worktree was clean.

## Original target and actual conclusion

The canonical path remains `matrix-inequalities-and-norms/MI-27/README.md`, and the permanent ID remains MI-27. The original problem statement is unchanged, and the ID registry has no diff. Its quantifiers are retained: every positive integer n, arbitrary complex positive definite A and B with `tr(A+B)=1`, natural logarithm by spectral functional calculus, and the **full** Schatten trace norm. The result establishes exactly

\[
\|[B,\log(A+B)]\|_1\le -a\log a-b\log b,
\qquad a=\operatorname{tr}A,
\quad b=\operatorname{tr}B.
\]

There is no commuting, rank, dimension, spectral-gap, or minimum-eigenvalue assumption. The proof is a full universal upper bound, with a strictly positive definite order-two family proving optimality. It does not replace the requested coefficient one by an unspecified universal coefficient. The attribution to Sidney Holden and the credit for the earlier supplied sharpness/projection findings remain explicit.

## Critical analytic checks

### 1. The effect estimate has coefficient one with the stated norm

For `X >= 0` and `0 <= Q <= I`, `R=2Q-I` is a Hermitian contraction. Thus

\[
\|[X,Q]\|_1
\le \tfrac12(\|XR\|_1+\|RX\|_1)
\le \|X\|_1\|R\|_\infty
\le \operatorname{tr}X.
\]

The factor 1/2 is exactly canceled by the two product terms. This proves the estimate for full trace norm, with no trace-distance normalization silently introduced. The product inequalities hold for complex matrices without requiring X and R to commute.

### 2. The hockey-stick derivative survives zero crossings

Fix a finite gamma and let `M(t)=rho-gamma sigma_t`, where `sigma_t=exp(itH) sigma exp(-itH)`. The positive-part trace is the maximum of `tr(QM)` over effects. Consequently it is Lipschitz as a function of M in trace norm. Composing with the smooth finite-dimensional matrix path makes `f(t)=tr M(t)_+` absolutely continuous on every compact time interval. The initial local Lipschitz constant may depend on gamma; that does not affect this step.

At a point where f is differentiable, hold the maximizing positive spectral projection Q at that point fixed. The variational inequality for `t+u`, together with the expansion of M, gives a supporting derivative inequality for each sign of u. Dividing by positive and negative u gives opposite bounds, hence

\[
f'(t)=\operatorname{tr}(Q M'(t)).
\]

This works even if M has a zero eigenvalue at that time, whenever f itself is differentiable. It does not differentiate the spectral projection, require uniqueness of a maximizer, or assume a spectral gap. The exceptional nondifferentiability set is harmless because absolute continuity permits integration of the almost-everywhere bound.

### 3. Gamma cancels exactly

The chosen Q commutes with `rho-gamma sigma_t`, so `[rho,Q]=gamma[sigma_t,Q]`. Since `M'(t)=-i gamma[H,sigma_t]`, trace cyclicity gives

\[
f'(t)=-i\gamma\operatorname{tr}H[\sigma_t,Q]
      =-i\operatorname{tr}H[\rho,Q].
\]

The effect estimate with `tr rho=1` therefore gives `|f'(t)| <= ||H||_infinity`, uniformly in gamma and dimension. Integrating proves the claimed finite-time Lipschitz bound. For rotation of the first argument, simultaneous unitary invariance moves the rotation to the second argument with generator `-H`; the same bound applies. There is no reliance on independence, commutativity of the states, or gamma being bounded.

### 4. The imported identity is ordinary Umegaki entropy

Independently checked [Hirche–Tomamichel, arXiv:2306.12343v3](https://arxiv.org/html/2306.12343v3), Section 2.3, Corollary 2.3, equation (2.22). It identifies the ordinary Umegaki relative entropy, as defined in their equation (2.20), with the two hockey-stick integrals weighted by `1/gamma` and `1/gamma^2`. Their extended definition includes a scalar trace correction, but for states and gamma at least one that correction is zero. Thus it matches the manuscript's positive-part convention exactly. The identity concerns arbitrary finite-dimensional quantum states, not just commuting ones or a different quantum f-divergence.

Also checked [Frenkel, arXiv:2208.12194v4](https://arxiv.org/pdf/2208.12194v4), Theorem 6, in complex matrix spaces. Its general positive-matrix formula has the additive term `tr(rho-sigma)`, which vanishes for states. Its negative-part integral matches the manuscript. Recomputed the substitutions on `v>1` and `v<0`: they give respectively the forward weight `1/gamma` and the reverse weight `1/gamma^2`, with the reversed integration orientation handled correctly. The positive-definite states used in the main theorem satisfy the support hypotheses; no problematic infinite relative entropy is subtracted there.

### 5. The skew and Holevo kernels are algebraically and analytically valid

For `M=alpha rho+beta sigma`, the first part of the Umegaki representation vanishes once `v>=1/alpha`. Before that threshold, factoring the positive scalar `1-alpha v` from the Hermitian pencil and setting `gamma=beta v/(1-alpha v)` maps the interval from gamma=1 to infinity. The inverse substitution and its derivative give the first coefficient

\[
\frac{\beta^2}{\gamma(\beta+\alpha\gamma)^2}.
\]

The reverse term uses `v=alpha+beta gamma`, giving `beta^2/(alpha+beta gamma)^2`. These operations are on scalar multiples and linear combinations of the original Hermitian matrices; simultaneous diagonalization is never used.

Expanding the weighted entropy difference into its two skew relative entropies is valid by linearity of trace. Combining the two nonnegative coefficients of each hockey-stick divergence yields exactly

\[
\frac{ab}{\gamma(b+a\gamma)},
\qquad
\frac{ab}{\gamma(a+b\gamma)}.
\]

The respective integrals are `-a log a` and `-b log b`; the displayed antiderivative differentiates to the first kernel and has the claimed endpoint values. Both kernels are positive and integrable because a and b are strictly positive. Since the hockey-stick divergences lie between zero and one, the representation is absolutely convergent, and differences can be bounded by the integral of absolute differences. The auxiliary skew-kernel masses in the appendix also check out.

### 6. No unjustified differentiation under an improper integral

The argument first applies the uniform **finite-difference** bound to each integrand and integrates against kernels of finite mass. This proves the global finite-time entropy bound with coefficient `h(b)`. It only then differentiates the finite-dimensional entropy function at time zero. Consequently it does not require a common differentiability set for all gamma, interchange a derivative with an improper integral, or assert uniform smoothness of positive-part spectral projections.

### 7. Entropy differentiation and trace-norm duality close the exact target

The sum `S_t=A+exp(itH)B exp(-itH)` remains positive definite, so the trace functional `-tr(S_t log S_t)` is differentiable. Its derivative is `-tr(S'_0(log S+I))`; `tr S'_0=0` and `S'_0=i[H,B]` give

\[
\left.\frac{d}{dt}\mathsf S(S_t)\right|_{t=0}
=-i\operatorname{tr}H[B,\log S].
\]

This trace-derivative formula does not require `S'_0` to commute with S: diagonalizing S gives the formula from the diagonal entries of the Fréchet derivative. Taking the derivative of the established scalar Lipschitz inequality bounds this expression for every Hermitian H. The matrix `K=-i[B,log S]` is Hermitian. Choosing `H=sgn K`, zero on its kernel, gives `tr(HK)=tr|K|` and operator norm at most one. Multiplication by `-i` preserves singular values, so this is the full trace norm of the requested commutator. There is no missing factor two or restriction to real test matrices. The n=1 and zero-commutator cases are included.

## Sharpness and auxiliary reductions

The displayed order-two family has the middle congruence factor with eigenvalues `t^2` and `1-t^2`, both in (0,1). Hence both A and B satisfy the original strict definiteness assumptions for every `0<t<1/2`, rather than only in a singular limit. Its commutator has two equal singular values, giving the stated full trace norm. The asymptotics `d_t/t -> 1`, `b_t/(2t) -> 1`, and `h(b_t)/(2t log(1/t)) -> 1` establish a ratio tending to one; every proposed smaller constant therefore fails on an admissible finite positive t. Credit for the family is explicit.

The projection appendix does not supply an unproved premise to the main upper bound. Its regularization preserves a fixed strictly positive sum, and its converse is a convex combination over projections followed by concavity of binary entropy. The trace values of these projections are allowed to vary. It therefore avoids assuming that a fixed-trace effect slice has only projection extreme points.

## Disposition and limits

The proof supplies the full original universal coefficient-one statement and its sharpness. The analytic chain is complete after the accurately quoted published relative-entropy identity. This cross-review found no hidden regularity assumption, endpoint gap, normalization mismatch, or remaining optimization conjecture.

This is a mathematical cross-review, not a Lean proof, a new numerical certification, or a priority determination. The submitted verification suite and publication artifacts were not rerun at root's request. Accepting the mathematical result and retaining the original ID, target and credits are supported by this review.
