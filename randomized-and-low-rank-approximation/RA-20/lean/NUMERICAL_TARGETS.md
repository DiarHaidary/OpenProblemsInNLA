# RA-20: mathematical contracts fixed before proof implementation

All scalar and matrix coordinates in the target are **complex**. No claim is
restricted to real data. The natural-number notation for the four formulas is
used only under the original ranges `n >= 3`, `1 <= s <= 4`, `s <= n`, where the
displayed subtractions have their ordinary nonnegative values.

The full target says that for each such `(n,s)`, outside a proper algebraic
exceptional set of symmetric data, the actual smooth-locus critical set has
cardinality `3(n-1)-2`, `9(n-2)-2`, `27(n-3)+4`, or `81(n-4)+28` respectively.
The definition keeps all four cases. Its negation will use the allowed case
`n=s=3`, whose claimed value is exactly four.

1. **Actual matrix variety.** For every `a,b,c in C`, the hollow symmetric matrix
   `[[0,a,b],[a,0,c],[b,c,0]]` has determinant `2abc`, and belongs to the original
   rank-at-most-two, three-diagonal-zero variety exactly when `abc=0`. Every
   matrix in that variety has this unique coordinate form.
2. **Reduced coordinate ring.** Establish a coordinate-preserving algebra
   isomorphism from the quotient by **all** polynomials vanishing on the actual
   matrix variety to `C[a,b,c]/(abc)`. Coordinate values, including all nine
   original matrix entries, are fixed in the statement.
3. **Genuine smooth locus.** A matrix is in Mathlib's algebraic smooth locus of
   the reduced coordinate ring exactly when it has the hollow form and exactly
   one coordinate is zero. In particular, every intersection of two planes is
   excluded even if its matrix rank is two. This equivalence must be proved;
   it is not built into the definition.
4. **Actual Zariski tangent equations.** At every `abc=0` point, including
   singular points, tangent directions are hollow symmetric matrices with
   `bc*Z12 + ac*Z13 + ab*Z23 = 0`. The tangent definition annihilates the full
   vanishing ideal, not just the three-coordinate determinant polynomial.
5. **Full-distance derivative.** For every order, matrix point and direction,
   the actual complex derivative is `2 sum_ij (Xij-Uij) Zij`.
6. **Restricted metric.** For arbitrary symmetric data, the actual full-entry
   objective becomes `sum_i Uii^2 + 2[(a-U12)^2+(b-U13)^2+(c-U23)^2]`.
7. **All generic critical points.** For every symmetric `U` with
   `alpha*beta*gamma != 0`, where `(alpha,beta,gamma)=(U12,U13,U23)`, the complete
   actual smooth critical set consists of the three pairwise distinct points
   `(0,beta,gamma)`, `(alpha,0,gamma)`, `(alpha,beta,0)`.
8. **Nondegeneracy.** In each plane chart, the actual second complex derivative
   is the bilinear form `4 sum_i h_i v_i`. Its kernel is zero. Thus the source's
   Hessian `4I_2` and simple-critical-point assertion are explicitly supported.
9. **True genericity.** Every nonempty principal open set in the full space of
   symmetric three-by-three data intersects `alpha*beta*gamma != 0`. This is
   needed to rule out a different, allegedly generic count of four; the source's
   single generic set cannot simply be substituted into an unknown exceptional
   polynomial without a proof of intersection.
10. **Generic count three.** Prove the actual cardinal count three on a nonempty
    principal open set. Infinite critical sets cannot satisfy a finite cardinal
    equality accidentally.
11. **No generic count four.** The actual generic-count definition cannot have
    value four in this same case.
12. **Complete negative answer.** Negate the original all-parameter,
    four-formula conjecture without an extra matrix, spectrum, smoothness,
    genericity, critical-count, or algebraic representation premise.

The source's optional rational data matrix is
`U=[[1,1,2],[1,2,3],[2,3,3]]`. Its candidate coordinate triples are `(0,2,3)`,
`(1,0,3)`, `(1,2,0)`, with full-Frobenius squared distances `16,22,32` and
restricted Hessian determinant `16`. These values, the generic determinant and
distance polynomial identities, and the gradient/Hessian coefficients are
independently reconstructed by `verification/reconstruct.py`. This Python
diagnostic is not the proof of genericity, the algebraic smooth locus, the
cardinal equality, or the full target. It is not submitted as a Lean certificate.

No interval size, eigensolver, numerical integration, approximate root, or
floating-point test is needed. The proof plan is exact ring/localization algebra,
actual derivatives and finite cardinal arguments. LeanCert will audit kernel
trust. A numerical singleton would be artificial and is deliberately absent.

Remaining substantive route: smooth coordinate-plane points can be obtained by
localization and elimination; nonsmooth intersections can be excluded using
square-zero lifting obstructions in truncated polynomial rings. Those are
unproved implementation plans only. No Challenge hole is authorized to become
an assumption or custom axiom.
