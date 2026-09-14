# Proof audit and scope register

## Overall assessment

This package is **PARTIAL** for the unrestricted RA-14 problem. The manuscript presents proofs of a matching bound for a restricted, explicitly defined algorithm class; a shifted singular-Wishart posterior; and an averaged rank-one upper bound on that shifted law. No all-adaptive transition theorem is asserted. The unrestricted bounds from the preceding v5 manuscript are inherited without strengthening.

These are unreviewed mathematical research arguments. The audit identifies the load-bearing steps, checks their model and probability qualifiers, and records what the accompanying computations do and do not test. It does not replace independent review, and no proof-assistant certificate is supplied.

## 1. Model separation

There are three distinct quantifier patterns.

**Unrestricted RA-14.** Every individual product with either A or A^T costs one query. The next real vector can be any measurable function of previous replies and independent randomness. Success must hold with probability at least 0.99 for every fixed matrix. The least worst-case budget is q_sp.

**Definition 2.1.** The physical initial width is deterministic and chosen before the input is queried. Every round costs the entire width, vectors must lie in the initial span plus preceding-round replies, and there is no within-round adaptation. Outputs need not lie in that span. The least worst-case budget within this class is q_fb. This is a restriction of, not a reformulation of, RA-14.

**Theorem 11.2.** The success probability averages over one explicitly specified shifted-Wishart input law and a Gaussian starting vector. This is not a pointwise guarantee over all input matrices. The algorithm does use actual oracle queries and does not receive hidden eigenvalues or eigenvectors.

The report, README, comparison, claim inventory, and status record preserve these distinctions. In particular q_sp <= q_fb, so a lower bound on q_fb does not by itself lower-bound q_sp.

## 2. Weighted graph criterion — Lemma 3.1

The leading eigenvalue is repeated k times and is strictly larger than the target residual threshold. This forces the leading block of any successful k-frame to be nonsingular. Writing its range as the graph [I;F], one tests all perpendicular vectors (-F^T y,y), not just individual eigenvectors. The resulting condition is

```
(a^2-tau^2) F F^T <= tau^2 I - D_tail^2.
```

Both sides are positive definite where inverted. The equivalent weighted singular-value condition implies the cone inequality for **every** vector in the output range. Its converse is also established. There is no assumption that a spectral approximation already has a constant unweighted principal-angle overlap: the explicit three-dimensional counterexample shows why that would fail at small accuracy.

The new component tests check the exact graph construction, the residual comparison, and matrix/vector versions of the cone. Floating-point agreement is not the proof of the equivalence.

## 3. Weighted Chebyshev interpolation — Lemma 4.1

The nodes are the d+1 distinct Chebyshev extrema. The cardinal signs, half endpoint weights, and normalization are written explicitly. The identity for the denominator J uses the nodal polynomial (z^2-1) U_(d-1)(z), including the d=1 endpoint case.

Two different lower bounds on J are used: the endpoint bound of order 1/s^2 and the hyperbolic bound of order d/s. Applying each to the appropriate term gives the weighted mass bound 10 s H_d T_d(1+2 epsilon). The extra factor s is material; dropping the residual weights would lose the desired finite-dimensional behavior.

The inequalities hold on the whole stated continuous parameter domain. The high-precision tests include accuracies too small for a floating-point matrix to distinguish 1, 1+epsilon, and 1+2 epsilon. The implementation separates such scalar tests from matrix diagnostics and rejects unrepresentable spikes rather than silently testing a different matrix.

## 4. Reciprocal Gaussian Gram estimate — Lemma 5.1

The claim requires m >= 8B. Each Gaussian tail block therefore has full column rank almost surely. The proof uses a t^2-net only for t <= 1/50 and separately bounds the operator-norm exception. Integration of the small-singular-value tail gives the finite expectation 3000/m. No asymptotic Wishart limit and no unexplained high-probability inverse bound are imported.

The numerical reciprocal-Gram experiment estimates the expectation on 12 finite shapes. Its observed means are far below the sufficient constant, but they are not estimates of a sharp universal constant and do not certify the small-ball tail for every shape.

## 5. Primitive no-cone theorem — Theorem 6.1

The explicit multiplicities are

```
m_j = 8B + ceil((n-k) w_j / 2),
```

with all leftover dimensions allocated to the node 1. The dimension hypothesis pays for every floor, ceiling, node, and Gaussian column rank. It ensures exactly n total eigenvalues, k leading eigenvalues, and sigma_(k+1)=1.

The matrix Cauchy-Schwarz inequality is applied simultaneously to all vector polynomials of degree at most d. Coefficients may even depend on all sampled Gaussian entries for this primitive statement. The random inverse-Gram sum has a proved expectation; Markov's inequality is used once for this sum, rather than union-bounding separate bad events at every node. Intersecting it with the leading-block norm event has probability above 0.749, more than the stated 0.74.

The quantitative sufficient condition gives a top-to-weighted-tail squared ratio at most 0.24 s^2, strictly below the necessary value Delta >= 2 s^2. A zero tail implies a polynomial vanishing at d+1 distinct nodes and hence the zero vector. This handles the possible zero-denominator case, rather than dividing by it.

The 72 numerical whole-prefix trials do **not** meet the conservative sufficient constant condition. They test the linear algebra on practical spectra; 42 exclude the cone numerically and 30 do not. Both outcomes are retained. None is represented as an instantiation of the theorem's universal threshold.

## 6. Arbitrary outputs — Lemmas 7.1 and 7.2

A lower bound for vectors in a Krylov space alone would not cover an output chosen outside that space. The report supplies a separate conditional-rotation argument.

For a fixed initial block, the group fixing that block is compact. The Haar-conjugated prior is invariant, and the full-prefix map is equivariant. Averaging a regular conditional probability kernel over this **fixed** group produces an equivariant version. A transformation fixing the observed prefix therefore preserves its conditional input law. This avoids assuming independence of the input and the adaptively observed space.

The output's component perpendicular to the observed space is factored into a frame and a coefficient matrix. Replacing that frame by an independent uniform frame preserves its Gram matrix and preserves the conditional average success probability. At most k independent Gaussian starting directions realize this comparison. The resulting output belongs to an enlarged prefix space.

This is a probability comparison, not an uncharged oracle operation by the original algorithm. The additional starting directions are used once for the final output. The statement does not authorize a fresh direction at every original query without a corresponding enlargement and cost analysis.

The augmented initial space is independent of the matrix. Its orientation in the eigenbasis of a Haar input is uniform. A Gaussian matrix spans the same distribution of subspaces; the proof uses equality of subspace distributions, not equality of the original arbitrary initial block and a Gaussian block entry by entry. Rank-deficient initial blocks can only be helped by completing their span.

## 7. All-parameter restricted lower bound — Section 8

A Haar rank-k projector proves that an initial width below min(k,n-k) cannot solve the rank-promise cases within the stated class, no matter how many rounds are performed. Both dimensions of the still-unknown residual subspace must be positive; this is why the minimum includes n-k.

For k>n/2 the unrestricted rank lower bound already gives the required linear lower scale. For smaller k, a valid deterministic width has b>=k. If n/b <= exp(48), the fact that at least one fully charged round is needed supplies the weak constant exp(-48). Otherwise the selected integer depth is

```
floor(min((n/b)/288, log(n/b)/(16 sqrt(epsilon)))).
```

Both primitive hypotheses are verified with B=b+k. The continuous threshold inequality is checked by its value at log(n/b)=48 and a negative derivative beyond that point. The floor loses at most a factor of two because its argument is already greater than two. Monotonicity of u log(en/u) transfers the physical-width expression to the target rank k.

The hard spectrum may depend on the fixed width b, but not on the algorithm's random seed. A single hard law covering randomized width mixtures is not supplied. The theorem therefore does not silently include randomized or changing widths.

## 8. Restricted upper bound — Section 9 and Appendix B

The two Gaussian stages of the preceding upper-bound construction are concatenated into one initial block of width 256(2k+1). Every power of M=A^T A is computed using two full rounds, so each individual product is charged. The width and exact-column fallback are selected before seeing the input.

The full prefix supplies the first stage's compressed matrix and the second stage's polynomial images and their compression. The latter uses H^2 Omega to form HQ after Q=orth(H Omega); no uncharged application of H is assumed. The final extraction uses top **right singular vectors** of Q^T H, not algebraic Ritz vectors of a potentially indefinite polynomial.

The scale c=sigma_(k+1)(A)^2 is not known for free. Appendix B proves its Ritz estimate, handles c=0 separately, supplies the two Gaussian probability events, and transfers the polynomial residual through a scalar functional-calculus inequality. The final rate is 24000 rather than 12000 solely because the whole physical block is charged in every round. The earlier unrestricted upper bound remains unchanged.

## 9. Shifted posterior — Theorem 10.1

The negative determinant tilt (pdet H)^((1-k)/2) is finite because it converts the positive Gram density to determinant exponent zero. This statement holds for every target rank, not only rank one. Conditioning the positive spectrum above h then translates a positive definite matrix density proportional to exp(-tr S/2).

Under adaptive Schur conditioning the pseudodeterminant factors into det J, the residual pseudodeterminant, and a kernel-graph determinant. The query vectors are predictable conditional on earlier replies; Gaussian completion applies inductively. The change of measure is on the full input distribution followed by conditioning, not a claim that adaptive queries are independent of the matrix.

The explicit posterior requires **J > h I** and t<n-k. Schur inertia gives the translated positive residual block on precisely this domain. The shorting identity gives the angular density factor, including its sign and the transcript-dependent trace normalization. At the empty transcript the formulas use empty J and B and reduce to the original uniform kernel and shifted positive block.

Corollary 10.2 computes the conditional pivot distribution. It does not prove a useful bound on the first-exit time. An ill-conditioned transcript close to the wall cannot be handled by assuming a transcript-independent norm bound for its posterior matrices. The rank-one algorithm in the following section shows that a linear transition stopping obstruction for this whole averaged ensemble would be false.

## 10. Resolvent and distribution-specific algorithm — Section 11

The Gaussian integration-by-parts identity is an **expectation identity**. Its underlying divergence is pointwise, but its expectation is equated to the Gaussian inner product only after integration. The real Gaussian rectangular dimensions are r by r+1; the N-r-1 coefficient therefore cancels exactly. Nonnegative terms and Jensen give the resolvent upper bound. A separate matrix-cone translation proves the exact exponential law of the smallest eigenvalue.

The algorithm knows the specified input law and its h=400 n epsilon normalization, but not the realized eigenvalues. It uses exact recovery on the designated branches and otherwise one Gaussian vector with a three-term Chebyshev recurrence. There is one charged A product per polynomial degree.

The proof controls four events: the Gaussian matrix norm, its smallest eigenvalue, a weighted residual sum, and the starting vector's leading component. The weighted residual estimate uses the resolvent expectation. The analysis threshold is shown to be below (1+epsilon) times the **true** sigma_2(A); it is not simply compared with an externally selected tail endpoint. The exceptional probabilities sum to less than 0.002 on the polynomial branch.

The final query estimate includes the ceiling, the small-y exact branch, and the degree>=n branch. Its guarantee averages over the stated law and the start. No conclusion about a universal all-input F-rate algorithm follows. At the transition it does rigorously rule out using this particular averaged law as a witness for an Omega(n) lower bound.

## 11. Prior dependencies and unresolved claim

Appendix A reproduces the unrestricted Gaussian rank lower bound. Appendix B reproduces the upper-bound certificates. The v5 finite-accuracy lower bound still depends on its explicitly imported Rudelson-Vershynin least-singular-value theorem. Its complete unmodified proof and source record are in the preserved archive; this continuation does not optimize its constants or claim independent publication status.

The remaining global interval at k=1 and epsilon=(log n/n)^2 is still

```
Omega(n log log n/log n) <= q_sp <= n.
```

The published adaptive-to-Krylov simulation has quadratic-sized granted information. Inserting its sizes into the new primitive theorem requires dimension of order q^2; it does not reach a near-linear q. A same-cost transfer, an unrestricted F-rate algorithm, or a different matching pair is still missing. No statement in the package removes this gap.

## 12. What the tests certify

The recorded 110 passing tests check finite identities, inequalities, query counters, and implementation branches. The sampled cone, posterior, and resolvent cases are diagnostic rather than universal certificates. All countervailing diagnostic outcomes are retained, including the initial resolvent small-sample discrepancy and a separately seeded fixed-size holdout. The unchanged prior test suites are rerun without altering their assertions.

The manifest verifies file bytes, not authorship, mathematical correctness, or independent review. A reviewer should prioritize the conditional-rotation kernel construction, the all-polynomial no-cone argument, the shifted posterior's support and normalization, and the averaged-versus-pointwise distinction before relying on the new conclusions.
