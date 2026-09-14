---
title: "RA-11: probability-sensitive product probes and diagonal correction"
author: Sidney Holden
date: 14 September 2026
---

**Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.

**Submission disposition:** Partially resolved. Theorems 2.1 and 2.2 and Corollary 2.3 pass for the new upper bounds and estimator-specific rate. The unrestricted joint minimax characterization remains open.

[Independent informal AI-agent review](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/reviews/2026-09-14-further-submissions/RA-11-review.md). ChatGPT assistance is disclosed. No Lean verification, external human peer review or formal verification is claimed. This dated notice supersedes historical statements about pending review; inherited claims are accepted only within the linked review scope.


**Research continuation — round 4. Status: partial, not a full solution.**

## Abstract

We consider relative trace estimation of an arbitrary real positive-semidefinite matrix of order N=n^q, when an oracle returns the full matrix-vector response only on real product inputs. Two new upper bounds are established. A fractional-moment analysis of product-spherical empirical averaging improves the fixed-accuracy exponential rate from log(2n/(n+1)) to D_n=log n+1-H_n. The rate D_n is sharp for that empirical-average estimator, but not a minimax lower bound for the full oracle. Separately, a two-stage diagonal-control estimator has variance at most 2N||M||_F^2/(ms) after m training queries and s coordinate corrections, giving O(sqrt(N)/epsilon) queries with finite-bit, nonadaptive real inputs. Both results hold for every PSD input. The remaining unrestricted lower/upper gap is stated explicitly.

## 1. Model and relationship to the previous packages

Fix integers n,q >= 2 and 0 < epsilon < 1/2. The unknown real symmetric matrix M has order N=n^q and satisfies M >= 0. One oracle call supplies real vectors v_1,...,v_q in R^n and returns the entire vector

    M(v_1 tensor ... tensor v_q).

The matrix M itself need not factor. Define Q(n,q,epsilon) as the minimum worst-case number of calls needed by a randomized algorithm that, for every fixed M, returns T with

    P(|T - tr M| <= epsilon tr M) >= 2/3.

Finite exact computation is uncharged; no query-conditioning bound is imposed. These are the model requirements used in the preceding manuscripts and in the repository's RA-11 statement [R1]. All new proofs below concern this stronger full-vector oracle, not a conditioned scalar oracle.

Write tau=tr M. When tau=0, PSD implies M=0 and the estimators below return zero exactly.

The previous packages [R2--R4] report, among other results, the retained lower bound

    Q >= (1/80000) max_{1<=b<=q} min{n^b, sqrt(floor(q/b))/epsilon}.

They also give fixed-q optimality and several upper bounds. Those results are inherited, not newly proved here. This manuscript supplies proofs of its own new upper bounds from elementary calculations and explicitly distinguishes them from the inherited assertions.

## 2. Main results

For 1 < p <= 2 define

    C(n,p) = n^p Gamma(p+1) Gamma(n) / Gamma(n+p).

Equivalently, with t=p-1,

    C(n,1+t) = n^t product_{k=2}^n k/(k+t).

### Theorem 2.1 — fractional-moment upper bound

For any 1 < p <= 2, an ideal complex-spherical estimator can be implemented with real product queries using

    (q+1) ceil[(6 C(n,p)^q / epsilon^p)^(1/(p-1))]

calls, and its success probability is at least 2/3 for every real PSD M. A version with a deterministically finite number of fair random bits exists with no more than twice the number of samples in this display. In either case the query list can be fixed before responses are observed. The exact basis bound N may always be used instead.

The ideal formulation uses continuous random probes, as is customary in exact-real oracle analysis. Section 6 gives the finite-bit reduction; it does not assume floating-point Gaussian simulation is exact.

### Theorem 2.2 — diagonal-control upper bound

There is an explicit bounded-fair-bit, nonadaptive algorithm with

    Q(n,q,epsilon) <= min{N, 2 ceil[sqrt(6N)/epsilon]}.

When N is a power of two, the constant 6 can be replaced by 3. Only real Rademacher-product inputs and real coordinate-product inputs are used. This construction does not use interpolation, Gaussian sampling, or a low-rank approximation subroutine.

### Corollary 2.3 — fixed-accuracy rate of the new first branch

Put

    D_n = log n + 1 - H_n,
    V_n = sum_{k=2}^n 1/k^2,
    A = log(6/epsilon).

If q V_n >= 2A, the ideal sample count in Theorem 2.1 is at most

    ceil[epsilon^(-1) exp(q D_n + sqrt(2 q V_n A))].

The finite-bit version uses at most twice this sample count. Each sample costs q+1 real queries. In particular, at n=2 and epsilon=1/4, for q>=26,

    Q(2,q,1/4)
      <= min{2^q,
             2(q+1) ceil[4 exp((log 2 - 1/2)q
                                   + sqrt((q/2)log 24))]}.

Thus the fixed-accuracy exponential base of this upper branch is 2/sqrt(e), approximately 1.21306. This is strictly below 4/3, the base supplied by the preceding complex-spherical variance calculation. It is still an exponential upper bound, and it does not match the known unrestricted lower scale.

## 3. Convex-order reduction to a scalar product distribution

Let z_j be independent and uniform on the complex sphere of radius sqrt(n), and set z=z_1 tensor ... tensor z_q. Let W=nB, where B has the Beta(1,n-1) distribution. Then EW=1. Define P_q=product_{j=1}^q W_j for independent copies W_j.

Recall that X is dominated by Y in convex order when E phi(X)<=E phi(Y) for every convex function for which the expectations exist, and EX=EY.

### Lemma 3.1 — one local factor

For any unit u in C^n, |u* z_1|^2 has law W. If A>=0 and tr A=1, then z_1* A z_1 is dominated by W in convex order.

Proof. Unitary invariance gives the first assertion. Diagonalize A=sum_r lambda_r u_r u_r*, where lambda_r>=0 and sum lambda_r=1. Pointwise Jensen gives

    phi(sum_r lambda_r |u_r* z_1|^2)
       <= sum_r lambda_r phi(|u_r* z_1|^2).

Take expectations. Every summand on the right has the W distribution. Isotropy supplies equality of means. QED.

### Theorem 3.2 — all-PSD convex-order domination

For every Hermitian PSD M with positive trace tau,

    (z* M z)/tau  is dominated by  P_q in convex order.

Proof. Induct on q, including arbitrary PSD matrices in the induction statement. For a rank-one matrix uu* with ||u||=1, condition on the first q-1 factors. The contraction against these factors is a vector a in C^n. The conditional quadratic response has law ||a||^2 W, with W independent of the conditioning variables: this follows from local unitary invariance, including the case a=0. The quantity ||a||^2 is a product-probe quadratic form of the PSD partial trace of uu*, on q-1 modes, with trace one. By induction it is convex-order dominated by P_{q-1}. Multiplication by an independent nonnegative W preserves this order, since x -> E phi(Wx) is convex. This proves the assertion for rank one. For general trace-one M, use its spectral decomposition and the same pointwise Jensen argument as in Lemma 3.1. Rescaling handles tau. QED.

Two consequences should not be confused. First,

    E(z* M z)^p <= tau^p C(n,p)^q

for p>=1. Second, replacing independent copies one at a time shows that the empirical average of normalized responses is convex-order dominated by the empirical average of independent P_q variables. This gives bounds for convex losses, but it does not say that every tail probability is maximized by a rank-one input.

The moment formula follows directly from the beta integral:

    EW^p = n^p (n-1) integral_0^1 b^p(1-b)^(n-2) db
          = C(n,p).

No assumption about a tensor-product factorization of M was made.

## 4. Bounded-probability analysis and real-query accounting

### Lemma 4.1 — an elementary mean bound

Let X_1,...,X_m be independent nonnegative identically distributed variables with mean mu and finite p-th moment, 1<p<=2. Then

    E |m^(-1) sum_i X_i - mu|^p <= 2 E X_1^p / m^(p-1).

Proof. Introduce independent copies X_i'. Jensen bounds the centered sum's p-th moment by that of sum_i(X_i-X_i'). The independent differences are symmetric, so independent random signs may be inserted without changing their joint distribution. Conditional on the differences d_i, the sign average is bounded by

    E_sign |sum_i sign_i d_i|^p
       <= (sum_i d_i^2)^(p/2)
       <= sum_i |d_i|^p.

The first inequality is monotonicity of moments from p to 2; the second uses p<=2. For nonnegative a,b, |a-b|^p<=a^p+b^p. Taking expectations and dividing by m^p proves the claim. QED.

Apply this lemma with X=z* M z. Theorem 3.2 and Markov's inequality give

    P(|mean X - tau| > epsilon tau)
       <= 2 C(n,p)^q / (m^(p-1) epsilon^p).

The sample count in Theorem 2.1 makes the right side at most 1/3.

### Lemma 4.2 — real simulation of a complex product response

For arbitrary complex factors g_j=a_j+i b_j, consider the vector polynomial

    v(t) = tensor_{j=1}^q (a_j+t b_j).

Its degree is at most q. Query Mv(t) at q+1 distinct real values, for example 0,1,...,q, and interpolate its value at t=i. This returns M(g_1 tensor ... tensor g_q) using only real product inputs.

Explicitly, the weight for node j is

    ell_j(i)= product_{0<=h<=q, h!=j} (i-h)/(j-h).

These weights are Gaussian rational. There are finitely many exact arithmetic operations, although floating-point interpolation can be badly conditioned.

To sample a spherical probe without taking a square root in unknown-data arithmetic, draw nonzero complex Gaussian factors g_j and query their raw product. If g= tensor_j g_j, return

    [product_j n/(g_j* g_j)] (g* M g).

This equals z* M z for the associated normalized spherical factors. All normalizing weights are real scalar divisions. The same raw-query implementation applies to the finite-support construction in Section 6.

The query list is nonadaptive: all factors and interpolation nodes are selected before any oracle response.

## 5. The exponential rate and its exact scope

Let t=p-1. A useful exact identity is

    f_n(t) := log C(n,1+t)
             = t log n - sum_{k=2}^n log(1+t/k).

Hence

    f_n'(0)=D_n,
    f_n''(t)=sum_{k=2}^n 1/(k+t)^2 <= V_n.

Taylor's theorem with an integral remainder gives

    f_n(t) <= D_n t + (V_n/2)t^2,  0<=t<=1.

The logarithm of the unrounded ideal sample count is at most

    q D_n + log(1/epsilon) + A/t + (q V_n/2)t,
    A=log(6/epsilon).

When sqrt(2A/(qV_n))<=1, choose this value of t to obtain Corollary 2.3. Otherwise choose t=1; the original formula of Theorem 2.1 remains valid at every parameter value.

### Theorem 5.1 — sharp rate for empirical averaging, not for Q

Fix n and 0<epsilon<1. Consider ideal spherical empirical averaging with m_q independent probes. If

    limsup_{q->infinity} (log m_q)/q < D_n,

then on a trace-one rank-one product matrix its empirical mean converges to zero in probability. Conversely, for any fixed r>D_n, taking m_q=ceil(exp(rq)) makes the empirical mean converge to one in probability uniformly over all trace-one PSD matrices of order n^q.

Proof of the converse. Since f_n(t)/t tends to D_n as t decreases to zero, choose a fixed t>0 with f_n(t)/t<r. The bound in Section 4 then tends to zero for each fixed epsilon, uniformly over M.

Proof of the lower statement. For a rank-one product matrix, a normalized response has exactly the P_q distribution. Tilt the local law of W by the density W, which is a probability density because EW=1. Under this tilted law,

    E_tilt log W = E[W log W] = D_n.

Its log moment is integrable. For any a<D_n, the law of large numbers therefore gives

    E[P_q 1{log P_q <= aq}]
       = P_tilt(sum_j log W_j <= aq) -> 0.

Choose a strictly between the assumed upper exponential rate of m_q and D_n. A union bound and Markov's inequality give

    P(any sampled P_q > exp(aq)) <= m_q exp(-aq) -> 0.

On the complementary event, the empirical mean equals the average of the truncated samples. That truncated average has expectation tending to zero by the preceding tilted identity, and thus tends to zero in probability. QED.

This theorem is an estimator-specific obstruction. It is emphatically NOT an exponential lower bound for RA-11. If M=uu^T and a query x satisfies u^T x != 0, then with y=Mx,

    M = yy^T/(x^T y),
    tr M = ||y||^2/(x^T y).

A generic continuous product x has nonzero overlap almost surely with any fixed nonzero u. Thus one full-vector query recovers the very rank-one example used in the empirical-average lower bound. Confusing these two oracle statements would invalidate a claimed complete solution.

For n=2 one may also write W=2U with U uniform on [0,1]. Then

    log P_q = q log 2 - G_q,

where G_q is Gamma with shape q and rate 1. Under the size-biased law its rate is 2. These formulas allow scalar experiments at moderately large q without constructing a 2^q-by-2^q matrix. Such experiments concern the empirical estimator only.

## 6. Bounded-fair-bit reduction for the fractional-moment bound

This section establishes existence of a finite exact implementation with at most a factor two in sample count. It is separate from the floating-point Gaussian diagnostic code.

### Lemma 6.1 — finite isotropic angular approximation

For fixed n, p in (1,2], and delta>0, there is a finite dyadic-probability distribution on nonzero Gaussian-rational raw vectors g in C^n such that the formal normalized vector z=sqrt(n)g/||g|| satisfies

    E zz* = I,
    ||z||^2 = n,
    sup_{||u||=1} E|u* z|^(2p) <= C(n,p)+delta.

It can be sampled using a deterministically bounded number of fair bits. Raw query inputs and normalization squared weights require no square roots.

Proof. Approximate a real standard Gaussian by a symmetric finite distribution on nonzero rational half-grid points, with dyadic probabilities. Let its support grow and mesh and probability error decrease. Take 2n independent coordinates with that distribution, grouping them into n complex coordinates. Every resulting raw vector is nonzero. The distributions converge weakly to a nondegenerate complex Gaussian. After normalization, their angular distributions converge weakly to complex Haar measure, because normalization is continuous away from zero and the limiting Gaussian has no atom at zero.

The finite laws are invariant under complex-coordinate permutations and multiplication of any coordinate by i: real and imaginary coordinates have the same symmetric law. These symmetries force the covariance of z to be a scalar identity, and its deterministic squared norm n makes the scalar one. This is exact, not approximate isotropy.

On the compact unit sphere, the functions z -> |u* z|^(2p), indexed by unit u, are uniformly bounded and equicontinuous. A finite net in u and weak convergence imply uniform convergence of their expectations. A sufficiently fine law therefore gives the required moment bound. The finite laws can be chosen effectively: Gaussian tail bounds, rational mesh bounds away from the origin, and rational approximations to the one-dimensional bin probabilities give explicit finite error certificates. Symmetric dyadic masses are used in pairs, and the remaining mass is assigned symmetrically. Each coordinate draw then uses a fixed number of bits. QED.

For completeness, an elementary modulus suffices for the constructive assertion. Outside an event where ||G||<a or a coordinate exceeds a chosen truncation radius R, a coordinate rounding error at most h changes the normalized direction by at most 2sqrt(2n)h/a. On the unit sphere the directional moment function has Lipschitz constant at most 2p n^p. The exceptional probability is bounded by (sqrt(2/pi)a)^(2n)+4n exp(-R^2/2), plus the total variation error in the finite scalar probabilities. Choose a small rational a, an integer R, a rational h, and dyadic probability precision in that order. These bounds tend to zero and can be compared to any positive rational tolerance. This is finite preparatory computation; it need not be efficient.

### Lemma 6.2 — tensorizing a local moment bound

If local probes are isotropic and satisfy E|u* z_j|^(2p)<=h||u||^(2p), then for q independent factors and every PSD M,

    E(z* M z)^p <= h^q (tr M)^p.

Proof. For a vector u with slices u_i, condition on one factor and apply its moment bound. Minkowski's inequality in L_p gives

    [E(sum_i |u_i* z_remaining|^2)^p]^(1/p)
       <= sum_i [E|u_i* z_remaining|^(2p)]^(1/p).

Induction proves the vector bound h^q||u||^(2p); a spectral decomposition and Minkowski give the PSD bound. QED.

Let t=p-1 and choose the finite law so that its local moment h obeys

    h <= C(n,p) exp[t log(2)/q].

Then h^q <= 2^t C(n,p)^q. Doubling the ideal number of samples compensates for this factor in the denominator m^t of the probability bound. Isotropy keeps the estimator exactly unbiased. This proves the finite-bit part of Theorem 2.1. The complex factors are implemented by Lemma 4.2 using raw Gaussian-rational vectors.

The finite law may be very large. This result makes no claim of practical bit complexity, and the package does not include a certified generator for that law.

## 7. A two-stage diagonal estimator

The following proof is independent of the spherical analysis.

### 7.1 Training from full-vector responses

For each training query draw independent local Rademacher vectors r_1,...,r_q in {-1,+1}^n and set x=r_1 tensor ... tensor r_q. Then x_i^2=1 and E x_i x_j=delta_ij. Query y=Mx and form the entire vector

    a(x)_i = x_i y_i.

Let d_i=M_ii and let a be the average of m independent such vectors.

### Lemma 7.1 — simultaneous diagonal moment identity

    E a = d,
    E ||a-d||_2^2 = [||M||_F^2 - sum_i M_ii^2]/m.

Proof. For one sample,

    a(x)_i-d_i = sum_{j!=i} M_ij x_i x_j.

Isotropy proves the mean identity. Since x_i^2=1, the squared error has expectation sum_{j!=i} M_ij^2; no fourth-moment independence assumption is needed. Sum over i and use independence of training samples. QED.

The full-vector response is crucial: one call supplies all N training estimates. This does not charge N separate scalar queries.

### 7.2 Finite-bit coordinate corrections

Choose a probability distribution p_i>0 on the N coordinate indices, independently of the training stage. Draw s independent indices I_l. Each e_{I_l} is itself a product of local coordinate vectors. Query M e_{I_l} to obtain d_{I_l}, and return

    T = sum_i a_i + (1/s) sum_{l=1}^s (d_{I_l}-a_{I_l})/p_{I_l}.

Conditional on a, this estimator has mean tau. Its conditional variance is

    (1/s) [sum_i (d_i-a_i)^2/p_i - (sum_i(d_i-a_i))^2]
      <= (max_i 1/p_i)/s * ||d-a||_2^2.

Since the conditional mean is exactly tau, there is no extra variance term from the random training sum. Lemma 7.1 proves

    Var T <= (max_i 1/p_i)/(ms) * ||M||_F^2.

PSD gives ||M||_F<=tr M, so the relative variance is bounded by (max_i 1/p_i)/(ms).

Uniform sampling gives max_i 1/p_i=N. For a bounded-bit rule valid for every N, let B=ceil(log_2 N), draw U uniformly from {0,...,2^B-1}, and set I=U mod N. Its exact probability is

    p_i = [floor(2^B/N) + 1{i < (2^B mod N)}]/2^B,
    i=0,...,N-1.

It satisfies p_i>=1/(2N), uses exactly B bits, and has a known rational probability for the correction weight. When N is a power of two it is exactly uniform.

Taking m=s=ceil(sqrt(6N)/epsilon) gives relative variance at most epsilon^2/3. Chebyshev proves success probability at least 2/3. For a power-of-two N take m=s=ceil(sqrt(3N)/epsilon). Use the cheaper exact basis sweep whenever its N calls are fewer. This proves Theorem 2.2.

All random factors and coordinate indices can be drawn in advance. The query choice does not depend on a, y, or any other response. Arithmetic and memory can be O(Nm) or larger, but these are not charged in RA-11.

### 7.3 A regime in which the diagonal branch improves the preceding envelope

Take n=2 and epsilon_q=(9/10)^q. Up to universal constants and polynomial factors, the previous displayed upper envelope in this conversation gives

    [(4/3)/(9/10)^2]^q = (400/243)^q,

whose base is approximately 1.64609; this branch is below the exact 2^q bound. The earlier linear-accuracy hierarchy has base greater than 2 in this binary case and does not improve that comparison.

The new diagonal estimator gives

    O[(sqrt(2)/(9/10))^q]
      = O[(10sqrt(2)/9)^q],

with base approximately 1.57135. The ratio of the new base to the old is 27sqrt(2)/40<1 (squaring reduces this to 1458<1600). This is an asymptotic comparison of proved query counts, not a claim that an exponential-size matrix experiment was run.

## 8. What is and is not resolved

The new upper envelope is the minimum of the previously reported bounds, the diagonal bound of Theorem 2.2, and the infimum of Theorem 2.1 over p in (1,2]. The finite-bit version is available with at most a factor two in sample count.

At n=2 and epsilon=1/4, the previously retained blocking lower bound has scale

    Omega(sqrt(q/log q)),

whereas the new upper bound has scale

    exp[(log 2 - 1/2)q + O(sqrt q)] times a polynomial in q.

This improves the previous exponential upper rate but leaves an exponential-versus-polynomial gap. Theorem 5.1 does not close it: its lower bound is only for an empirical-average estimator, and its hard rank-one example is easy for the full-vector oracle.

Accordingly, this package does not determine Q to universal constant factors jointly in n,q,epsilon and is not a full solution of RA-11. The missing statement is a matching unrestricted lower bound, a substantially stronger unrestricted upper bound, or another characterization closing the gap. No repository status has been changed.

## 9. Reproducibility and limitations

`code/exact_checks.py` checks exact rational diagonal identities, coordinate correction identities, and Gaussian-rational real interpolation on finite examples. These calculations catch algebraic/implementation mistakes but are not formal proofs of the general theorems.

`code/numerical_checks.py` runs finite diagonal-estimator experiments and scalar Gamma-law diagnostics for the empirical-average estimator. The latter do not use a giant matrix and must not be described as full-oracle lower-bound experiments. Query hashes check nonadaptivity of the diagonal implementation at fixed random seeds. The numerical script records its actual parameter choices, query counts, and failures.

Floating-point linear algebra, interpolation, and random variate routines are not exact arithmetic. The finite-support fractional-moment theorem is a constructive existence argument; a fully certified discretization implementation is not supplied. No floating-point stability guarantee, efficient runtime theorem, independent mathematical review, or proof-assistant certification is claimed.

## References and provenance

[R1] RA-11 repository statement, OpenProblemsInNLA, randomized-and-low-rank-approximation/RA-11/README.md. Public source: <https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/randomized-and-low-rank-approximation/RA-11/README.md> . See the local source snapshot and retrieval metadata when available.

[R2] Prior conversation manuscript, `ra11_partial_results.pdf`, round 1. Source of the reported blocking lower bound and the original real-query interpolation construction in this research sequence.

[R3] Prior conversation manuscript, `ra11_linear_accuracy.pdf`, round 2. Reported fixed-tensor-order optimality for arbitrary PSD inputs and the first general linear-accuracy hierarchy.

[R4] Prior conversation manuscript, `ra11_superset_controls.pdf`, round 3. Reported superset-specific controls and the improved linear-accuracy upper bound. This package does not assert an independent re-verification of all inherited proofs.

The new arguments are written out above. No claim is made that their ingredients, such as importance-sampling entropy rates or diagonal control variates, are new to all literature.
