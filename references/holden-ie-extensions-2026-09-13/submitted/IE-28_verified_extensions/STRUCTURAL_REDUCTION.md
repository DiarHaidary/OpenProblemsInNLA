# An exact structural reduction and a limitation of broader approaches

## 1. Definitions and equivalence

Let `0 < c_1 < ... < c_n`. Let `ell_j` be the degree-at-most-`n-1`
Lagrange cardinal polynomial at these nodes, and define

    Q_ij = integral from 0 to c_i of ell_j(t) dt.

Let `D = diag(d_1,...,d_n)` with every `d_i > 0`. The desired condition is
that `I - D^(-1) Q` be nilpotent. Since `Q` is invertible, this is equivalent
to

    det(lambda I - Q^(-1) D) = (lambda - 1)^n.

Indeed, nilpotence of `I - D^(-1) Q` is equivalent, by the characteristic
polynomial and Cayley-Hamilton theorem, to all eigenvalues of `D^(-1) Q`
being 1, with algebraic multiplicity `n`. Inversion preserves this assertion.
This equivalence does not presume diagonalizability.

## 2. A diagonal similarity with an explicit Cauchy matrix

Put

    w_i = 1 / product_{j != i}(c_i - c_j),
    T = diag(c_i / w_i).

Then

    T^(-1) Q^(-1) T = B,

where

    B_ii = 1/c_i + sum_{j != i} 1/(c_i - c_j),
    B_ij = 1/(c_i - c_j)  for i != j.

In particular, `B = diag(a_i) + K` with `K^T = -K`.

**Proof.** The polynomials

    L_j(t) = (t/c_j) ell_j(t)

are the cardinal basis for polynomials of degree at most `n` that vanish at
zero. Differentiation in their nodal-value coordinates has matrix `Q^(-1)`.
For `i != j`,

    L_j'(c_i) = (c_i/c_j) (w_j/w_i) / (c_i-c_j),

and

    L_i'(c_i) = 1/c_i + sum_{j != i} 1/(c_i-c_j).

Conjugation by `T` gives the displayed formula. Since `T` and `D` commute,
`Q^(-1)D` is similar to `BD`. Moreover, `BD` is similar to
`D^(1/2) B D^(1/2)`. Thus the diagonal-plus-skew structure is preserved
under the positive scaling. This is a reduction, not an existence proof.

## 3. Principal minors from derivatives of a Vandermonde determinant

Write

    V(c) = (product_i c_i) product_{i<j}(c_j-c_i).

For every subset `S` of the node indices,

    det(B[S,S]) = (partial_S V(c)) / V(c),

where `partial_S` differentiates once with respect to each coordinate in `S`.
Consequently,

    det(I - t B D)
      = sum_S (-t)^|S| (product_{i in S} d_i) partial_S V(c)/V(c).

**Proof.** Let `W_ik = c_i^k`, for `k=1,...,n`; then `det W = V(c)`.
Differentiating its row `i` gives the evaluation row for differentiation on
the same polynomial space. Replacing precisely the rows indexed by `S`
therefore multiplies `det W` by the principal minor `det(Q^(-1)[S,S])`.
Since the coordinate `c_i` occurs only in row `i`, the determinant of the
row-replaced matrix is also `partial_S V(c)`. Principal minors are unchanged
by diagonal similarity, proving the formula for `B`.

Two necessary equations, useful in exact computations, follow:

    sum_i a_i d_i = n,
    product_i d_i = (product_i c_i) / n!.

For the second, `det Q^(-1) = n! / product_i c_i`, directly from the same
polynomial evaluation matrices. These equations alone are insufficient when
`n > 2`; all characteristic coefficients must be imposed.

## 4. An exact counterexample to an overly broad auxiliary assertion

One might hope that positive diagonal entries, positive principal minors,
and a skew-symmetric off-diagonal part are enough to guarantee a positive
diagonal scaling with all eigenvalues equal to 1. They are not.

Consider the exact matrix

    B0 = [[ 1,  4,  4],
          [-4,  1,  4],
          [-4, -4,  1]].

Its symmetric part is the identity. Its order-one principal minors are 1,
its order-two principal minors are 17, and its determinant is 49. Hence all
of its principal minors are strictly positive.

Nevertheless, there is no positive diagonal `D` such that `B0 D` has
characteristic polynomial `(lambda-1)^3`.

**Proof.** Such a diagonal would necessarily satisfy

    d_1 + d_2 + d_3 = 3,
    17(d_1 d_2 + d_1 d_3 + d_2 d_3) = 3,
    49 d_1 d_2 d_3 = 1.

Apply arithmetic-geometric mean to the three positive numbers
`d_1 d_2`, `d_1 d_3`, and `d_2 d_3`. The last two equations would imply

    1/17^3 >= 1/49^2,

which is false because `17^3 = 4913 > 2401 = 49^2`. This contradiction
is exact and excludes every positive diagonal, not merely a numerical
parametrization.

**Scope of the counterexample.** `B0` is not asserted to arise from any
admissible collocation node set. In particular, equal nonzero off-diagonal
magnitudes in all three positions do not have the reciprocal-difference
structure of three ordered distinct real nodes. Therefore this example
is NOT a counterexample to IE-28. It only shows that a proof must use
additional structure beyond the matrix-class properties stated above.

## 5. Remaining gap

The reduction preserves the global difficulty: one still has to solve the
characteristic equations with `d_i > 0` for every admissible Cauchy-structured
matrix `B`. The local existence theorem in the recovered report and the
computational certificates do not settle that universal statement. No
completion of that step is claimed in this archive.
