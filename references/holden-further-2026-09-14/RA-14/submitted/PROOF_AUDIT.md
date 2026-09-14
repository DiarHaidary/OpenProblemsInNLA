# Proof audit and scope register

## Overall status

PARTIAL for unrestricted RA-14. The archive develops new mathematical reductions and conditional lower bounds but leaves the global transition interval unchanged. Earlier generated proofs are treated as unreviewed dependencies, not established literature. A previous numerical completion percentage is not evidence and is not used.

## 1. The deterministic minimum-energy criterion

The leading excess Gamma and tail margin E must both be strictly positive definite. Testing every vector perpendicular to a graph gives the exact residual criterion. The minimizer of L^T G L under T L=I is a Loewner-order minimizer: cross terms vanish for every feasible difference. Minimizing each column separately without checking cross terms would not establish the matrix statement.

For nonsingular G, the capacity is T G^{-1} T^T. A successful graph exists exactly when this matrix dominates Gamma. For singular G, directions in T ker(G) have zero tail cost and must not be discarded. Projecting off those directions gives C_R=R^T T G^dagger T^T R and the exact condition C_R >= R^T Gamma R. The source gives a simultaneous linear minimizer and proves its feasibility.

These formulas use hidden spectral coordinates for analysis. They are not claimed to be computable by a zero-query RA-14 algorithm.

## 2. Independent Gaussian node formula

At exactly d+1 distinct tail nodes, degree-d polynomial evaluation is invertible. The nodal values are independent coefficient variables. This makes the weighted-tail Gram block diagonal and yields the exact capacity G_top [sum ell_j(a)^2 e_j (G_j^T G_j)^{-1}] G_top^T.

The formula assumes full column rank at each node. Its expectation requires m_j>B+1, not merely m_j>=B. The exact inverse-Gram moment is derived from a chi-squared Schur complement. Off-diagonal integrability is checked before using sign invariance.

Success implies trace capacity >= k Delta. The first-moment probability bound is for existence of a whole rank-k successful output, not the stronger absence of every nonzero cone vector. It remains uniform over coefficients chosen after all the Gaussian entries are revealed.

## 3. Integer spectrum construction

The multiplicities are B+2+ceil((n-k)w_j/2), with leftover dimensions assigned to the node 1. The condition 2(B+3)(d+1)<=n-k pays for the integer rounding and the reciprocal-Gram moment. The endpoint ensures sigma_(k+1)=1 exactly.

The weighted interpolation estimate is reproduced from v6, including endpoints, degree one, the two distinct lower bounds on its normalization, and the continuous epsilon domain. The finite probability bound is 100 B/(n-k) log^2(ed) exp(4 d sqrt(epsilon)). The tradeoff uses a stronger condition with coefficient 400 to make this at most one quarter.

## 4. Adaptive conditional invariance

The prior is a Haar-conjugated fixed spectrum. For a fixed original algorithmic seed, the conditional input law after an adaptive transcript is invariant under transformations fixing every query and response. The proof uses induction and an averaged regular conditional probability kernel under a compact stabilizer group. It does not assume that adaptive queries are independent of the input.

Measurable orthonormal completions supply a measurable representation of history-dependent stabilizers. Assertions are needed almost surely in the transcript, not at every zero-probability transcript value.

## 5. Linear-size unrestricted reduction

For the actual queries V and replies AV, the output comparison uses X=[V,AV,G_k], with at most 2q+k columns. The independent Gaussian G_k replaces only the external part of the final output under conditional rotation. There are no extra products with A and no innovation restriction in this reduction.

The resulting capacity matrix is adaptively dependent on A. Its distribution is NOT the independent-node Gaussian law. Proving a suitable probability bound for this actual linear-size capacity is the missing all-adaptive step; the report does not claim to have proved it.

## 6. Innovation-count lifting

An innovation is defined relative to the span of previous queries and responses, not relative to a list of all random vectors the algorithm might generate. The simulator maintains an orthogonal coordinate map and preserves every earlier query-response pair. A Householder map sends a newly requested external direction to the projection of a fresh independent Gaussian. The map fixes the known span, so the conditional virtual input law is unchanged.

Each simulated query uses exactly one original matrix-vector product. At most h Gaussians enter queries, and at most k more replace the final external output frame. Their images are not obtained for free. The actual simulator is then enlarged to a degree-q prefix with h+k starts only for analysis.

The safe degree is q, not q/(h+k). The statement does not grant that every vector in the full prefix was learned with q products. This distinction is essential.

## 7. Innovation probability tradeoff

The hard spectrum depends only on the specified n,k,epsilon,q,h, not on a realized random seed or adaptive path. Algorithms exceeding h innovations are truncated before the next such query. This preserves the original success event intersected with the event of at most h innovations. The first-moment bound applies to the truncated algorithm, giving probability at most 1/4.

A pointwise 0.99 guarantee then forces more than h innovations with probability at least 0.74 on this hard law. It does not force a contradiction for an unrestricted algorithm, which may innovate on every query.

The bounded-innovation corollary assumes R=(n-k)/(h+k+3)>=exp(16). The continuous numerical threshold is checked at 16 and by a negative derivative thereafter. No n-cap is added to a lower bound outside its hypotheses. The matching linear statement at rank one and fixed h>=1 uses a separately proved invariant block-Krylov exact algorithm. It costs at most 2n products and at most k innovations, with every independent basis vector processed once. The unrestricted exact-column algorithm is not silently transferred to the restricted class.

## 8. Full-prefix saturation

When a tail node has m_j<B, its Gaussian block has a nontrivial coefficient nullspace. At d+1 nodes, interpolation makes these nullspaces independently usable. Their sum has generic dimension min(B,sum(B-m_j)_+), and the leading Gaussian maps it to min(k,B,sum deficits) pure leading directions.

For B>=k and (d+1)B>=n, this contains the entire exact leading space. Thus a whole-prefix exclusion is false in that saturation regime for this nodal construction. It does not follow that the original q-query algorithm knows an exact output. The actual transcript has far fewer independent feature columns.

## 9. Exact finite rank certificate

The supplied 12-dimensional example has q=3 actual products, seven columns in the actual-query/output enlargement, and sixteen columns in the full prefix. Nonzero integer minors certify actual full rank and tail rank both seven, and full-prefix rank twelve. The actual enlargement therefore contains no pure leading vector, whereas the prefix is the entire ambient space.

The certificate is verified using rational elimination and exact integer determinants. It illustrates an information-enlargement error; it is not itself a probabilistic lower bound or an approximate-residual impossibility theorem.

## 10. Tests and artifact checks

The new suite checks finite identities, exact-formula implementations, integer allocation, scalar bounds, and transcript consistency. Gaussian capacity diagnostics retain successful and unsuccessful space-containment outcomes. Their probabilities are not treated as certified universal estimates.

The simulated rotation tests check algebra, not conditional-law equality. The exact minor certificate verifies a specific rank statement, not all-adaptive query complexity. Earlier suites are preserved but are not claimed as rerun. The manifest verifies file bytes, not mathematical correctness, novelty, or authorship.

## Remaining mathematical gap

At k=1 and epsilon=(log n/n)^2 the inherited interval remains Omega(n log log n/log n) to n. The new exact linear-size reduction states the missing target cleanly, but its adaptive capacity distribution has not been bounded. Therefore unrestricted RA-14 remains unresolved by this archive.
