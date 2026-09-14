# New exact certificate format

## Coefficient field and trace coordinates

The field is Q(s), with s = i sqrt(3). A pair `(a,b)` represents `a + b s`. Multiplication is `(a,b)(c,d) = (ac-3bd, ad+bc)` and conjugation is `(a,b)* = (a,-b)`.

The four projection letters are P1, P2, Q1, Q2. Words reduce by orthogonality within a family, idempotence, and trace cyclicity. The four singleton normalized traces are 1/3. Reduced words of length at most eight yield 109 real trace coordinates after reversal/conjugation pairing and singleton substitution. The coordinate list is fixed in `local_rank_witness.json`.

Hermitian Gram coordinates are: a real diagonal entry; an off-diagonal real entry and its conjugate; or an off-diagonal `s` entry and its conjugate. For a bilinear trace `z`, these contribute `z`, `2 Re(z)`, and `-6 Im_s(z)`, respectively.

## Modular rank witness

`local_rank_witness.json` stores the prime 1000003, 107 coefficient columns, 107 rows, the full trace-coordinate list, and determinant residue 308373. A column descriptor is `[block,u,v,type]`, with type `diag`, `real`, or `s`.

`rank_witness.py` uses the fixed integer kernel columns from the prior certificate. It multiplies the ordinary Gram localizer by 169, and uses the integer numerator of each localizing polynomial, clearing the denominator 169 in D*D. The only remaining coefficient denominator is the singleton trace denominator 3, invertible modulo the checked prime. The recomputed minor is nonzero.

## Integer rank witness

`exact_minor.py` computes the same entries without modular reduction and additionally clears the singleton denominator 3. Its matrix is 507 times the unscaled coefficient minor. Fraction-free Bareiss elimination checks exact divisibility at every step.

The fixed integer determinant in `exact_minor_witness.json` is

    -2^1740 * 3^342 * 5^14 * 7 * 13^215 * 59.

It has 939 decimal digits. The checker verifies this factorization and agreement with the modular result. The integer witness includes a SHA-256 binding to the modular witness's row and column choices.

The rank upper bound is not inferred from a numerical singular-value tolerance. The manuscript proves it from the model moment and an independent flat-tangent moment. `local_geometry.py` verifies the supporting exact kernel and tangent identities, including a nonzero moment derivative of -1/48.

## Local geometry

The weighted rational representation uses `Rbar = I - 2 * 1 * w^T`, `w=(5/8,1/4,1/8)`, and adjoint `X^dagger = W^-1 X* W`, `W=diag(w)`. The checker verifies the active-face rank, moment rank, the exact positive stationary density, the complete local evaluation kernels, and the universally normalized degree-one polynomial q.

The nine anti-Hermitian tangent directions and the explicit nongauge flat direction are given in the manuscript and in `local_geometry.py`.

## Quantitative constant

`quantitative_rigidity.py` expresses four fixed degree-at-most-three relation polynomials in the exact degree-four kernel. It recomputes a positive lower bound on the prior congruence Gram matrix, a universal local trace bound, four rational relation constants, and upward-rounded square roots. The resulting integer constant is 2705974.

The verification JSON preserves all rational constants. The bound concerns normalized Hilbert–Schmidt distance; the residual is measured in operator norm.
