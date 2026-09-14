# Proof-critical distinctions checked in this round

This is a self-audit of the written argument, not an independent peer review.

The active density has ordinary trace one on a two-dimensional singular space. The map used in the lower bound is its matrix-valued partial trace, not a normalized full trace. This preserves an operator inequality in the repetition coordinate and is essential for noncommuting blocks.

The quadratic coefficient must include the Schur-complement term. The unreduced value 19/2080 is not the coefficient used in the proof; the verified reduced value is 1/52.

The initial quantitative rigidity estimate only gives O(sqrt(t)) distance from the equality orbit. The transverse coordinate is improved to O(t) using the rank-three face map and the positive-density one-sided bound. Without this improvement, discarding transverse quadratic terms would be unjustified.

The only remaining nongauge flat coordinate is a single Hermitian matrix T. Its pure quadratic contribution is exactly Q(X_*) tensor T^2. Other coefficient matrices are not assumed to commute with T; mixed terms are bounded in operator norm by O(t^(3/2)).

The first-order upper witness corrects the entire active matrix, not only its trace. Surjectivity of the lifted face map onto the kernel of the partial-trace map supplies that correction.

The Horn theorem is used for zero-sum Hermitian triples and then glued along partial sums. The source's block integrals are multiplied by the target dimension to obtain block averages. This does not give a direct Horn proof for the full normal-matrix residual.

All dimensions and directions are fixed before taking the perturbation limit. The proof does not establish constants uniform in amplification size and does not exchange those limits.

Numerical witnesses are labeled as upper bounds. The retained n=7, k=2 comparison is exactly the tensor repetition of the best retained base witness to numerical precision; it is not evidence of a strict amplification gain.
