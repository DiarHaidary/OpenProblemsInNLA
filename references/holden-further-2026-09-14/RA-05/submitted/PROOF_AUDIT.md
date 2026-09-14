# Author-side proof audit

This is an internal audit, not independent verification.

## Non-even proof chain

1. **Core selection (Part I, Lemma 3.1).** The kernel is the absolute `p`-power kernel, not the derivative kernel from earlier packages. It is symmetric with diagonal one; no positive-semidefiniteness is assumed. Gaussian moments bound the expected squared Frobenius distance from identity. A projection to its stable spectral interval, followed by restricted invertibility, selects original columns. Projection is removed before any query is interpreted.

2. **Integral and sign (Lemmas 4.1–4.2).** The cosine Taylor remainder is globally one-signed, proved by second-derivative induction. Its integral is absolutely convergent and nonzero for `2q < p < 2q+2`. The middle Walsh degree exceeds `p`, annihilating every subtracted polynomial. Both trigonometric powers are even because `h` is a multiple of four; the spectral integral has no cancellation. Constants degenerate at even exponents as they should.

3. **Noise column selection (Lemma 4.3).** The normalized middle-layer projection has rank `binomial(h,h/2)`. Restricted invertibility is applied with a quarter of this rank and then undone via projection contraction. The final columns are original normalized cube vectors. Their least singular value is for the entire selected coefficient space, not merely a subspace of weights.

4. **Tensor error identity (Proposition 5.1).** The complete error matrix is exactly `G Delta F^T`. No per-group query can be chosen independently and then silently added. Both least-singular-value bounds hold for arbitrary coefficient matrices, so every omitted row costs one in `||Delta||_F^2`. The support argument works for signed weights in this construction.

5. **Rank accounting.** A tensor test is a normal in `R^(rh)` and defines a fitted hyperplane of dimension `rh-1`. It is padded only when `rh <= k+1`. The final hyperplanes have dimension exactly `k`. The zero-subspace query is permitted because the model allows dimension at most `k`.

6. **All parameter ranges (Section 7).** The maximal admissible multiple-of-four `h` exists for small enough accuracy and is logarithmic in inverse accuracy. Its next failed value gives a lower bound on the number of noise columns. Large enough `k` admits the tensor construction. If `k = O_p(log(1/epsilon))`, the explicit `k/epsilon^2` block lower bound loses only a permitted logarithmic factor against `k^(p/2)/epsilon^2`. Bounded-away-from-zero accuracies use the constant-accuracy core lower bound. All constants remain fixed with `p`.

7. **Positivity boundary.** The tensor support theorem permits signed weights; the auxiliary all-rank block construction and constant-accuracy own-row argument use positivity. The final theorem concerns nonnegative original-row weights, exactly as requested.

8. **Upper and lower are different kinds of arguments.** The non-even upper bound is the explicitly imported general row-coreset theorem. This completion does not derive an upper bound from numerical lower-bound examples.

## Included even-power proof

Part II is reproduced in full. Its proof was read and the new structured Gaussian mechanism was checked against its role in the mixed-term estimate. The adapted parameter norm is positive because the head rows span their space. Polynomial norming is applied to a `k^2`-dimensional parameter space, with fixed degree. The full vectorized Gaussian covariance and the separate left matrix variance are both used. Protecting an output Hilbert-space direction costs one scalar equation, not an entire matrix column.

The fixed-feature variances use the pre-round positive measure. Temporary inner partial-coloring centers are not assumed to satisfy a new invariant. Outer fractional exceptions are frozen nonnegatively; full copies double; geometric sums control the total error. Input rank is separated from fitted-subspace rank. The general upper theorem, Rothvoss Lemma 9, Tropp Theorem 1.5, and restricted invertibility remain explicitly imported dependencies.

This reading and the separate finite rerun are not an independent proof audit.

## Attribution

The Boolean absolute-power matrix and its middle Walsh spectrum are established mechanisms in Li–Wang–Woodruff, Section 3.1. The present proof gives an elementary version of that estimate and tensors the selected Boolean family with a bounded-cost core to obtain the joint support bound. It does not claim to have discovered the Fourier mechanism or certify priority for the amplification.

## Exact certificate boundary

The cubic certificate is stronger than a single bad coreset example: its rational spectral inequalities prove a universal finite support bound for every real reweighting preserving 3,072 specified tests. Its matrices are explicitly listed or reproducibly defined, and the selected Gram lower bound is verified by rational LDL factorization. The direct violating candidate is an additional check of Euclidean projector costs.

The certificate does not prove the infinite family of core existence statements, select every asymptotic restricted-invertibility subset, or formalize either complete theorem.
