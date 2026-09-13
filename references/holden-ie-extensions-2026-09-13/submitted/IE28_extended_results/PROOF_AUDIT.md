# Proof audit and exact scope

## Target

For each n >= 2 and 0 < c_1 < ... < c_n <= 1, find one fixed real positive diagonal D satisfying (I - D^{-1}A)^n = 0. The archive does NOT establish this for all n and all nodes.

## Claim dependency map

| Claim | Proof | Computational dependency | Scope limitation |
|---|---|---|---|
| Inverse similarity and polynomial characterizations | Section 1, direct interpolation and matrix algebra | None | Algebraic reductions alone do not prove positivity/existence |
| Every two-stage node set | Section 2.1, explicit formula and two eigenvalue invariants | None | n = 2 |
| Every three-stage node set | Section 2.2, determinant normalization and exact endpoint trace signs | None | n = 3; the spectral sufficiency argument is not valid at higher n |
| Scaled Laguerre nodes, every n | Theorem 3.2, companion representation and Laguerre orthogonality | None | Special node family; also characterizes scalar diagonals |
| Polynomial extension through collisions | Section 4, alternant divisibility and divided differences | None | The original singular collocation matrix is not evaluated at repeated nodes |
| Confluent determinant formula | Lemma 5.1, augmented determinant and triangular Taylor recursion | None | Identity of determinants, not only a comparison of zero sets |
| Negative-a_1 seed and invertible Jacobian | Lemma 5.2, formal degree counting and finite recursion | None | Unique negative-a_1 CONFLUENT seed, not globally unique positive diagonal |
| Every n, all sufficiently clustered nodes | Theorem 5.3, real-analytic implicit function theorem and positivity by continuity | None | Neighborhood depends on n; no global continuation conclusion |
| Negative t^11 coefficient | Proposition 6.1 | `cluster/certify_seed.py` and exact dyadic interval operations in `certification/verify.py` | Finite computer-assisted algebraic sign proof |
| Nonnegative-coefficient ansatz impossible near n=11 confluence | Theorem 6.2, compactness and confluence, using Proposition 6.1 | Above sign certificate only | Auxiliary ansatz is excluded; original IE-28 is NOT disproved |
| Twelve certified assertions | Theorem 7.1 plus certificate JSON files | `certification/verify.py` | Six points and six specified node boxes only; uniqueness only inside diagonal box |
| n=8,11,15 continuation outputs | Section 8.1 | mpmath numerical computation | Not exact certificates, not an all-node proof |

## Deliberately avoided logical shortcuts

The proofs do not equate nilpotence of A-D with nilpotence of I-D^{-1}A. They do not replace the diagonal by a triangular matrix or a sweep-dependent family. They do not infer a positive real solution from a theorem over an algebraically closed field. They do not extend the three-stage invariant count to general n. They do not infer exact nilpotence by rounding computed eigenvalues or by reporting a small matrix-power residual.

The all-stage local proof neither assumes that the Taylor coefficients of its eigenpolynomial are nonnegative nor assumes all its nonzero roots lie on the negative real axis. The eleven-stage obstruction explains why that distinction matters.

## Verification trust boundary

For the twelve local certificates, the numerical generator only proposes rational center and preconditioner entries. The exact verifier recomputes every principal-minor enclosure, residual enclosure, Jacobian enclosure, and contraction inequality independently of the generator.

For the seed sign, the bracket for (11!)^(1/11) is certified by integer eleventh powers. Every subsequent operation encloses the exact algebraic seed recursion. The printed approximate upper bound is not used in acceptance. The final short decimal inequalities in the PDF are exact rational inequalities checked by the program.

The independent regression tests compare interval operations against exact rational arithmetic and determinants; compare determinant identities symbolically; check the triangular Jacobian formally in several dimensions; and reject deliberately corrupted certificates. Regression tests supplement, rather than replace, the analytical proofs.

These are human-readable mathematical arguments and auditable integer calculations, not formal proofs verified in Lean, Coq, or another proof assistant. No independent expert review has been obtained.
