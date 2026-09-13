# KE-04: prospective statement track

This is a coordinator's source-reading note, not a Lean statement approval,
proof implementation, eligibility audit, or formal verification claim.

At upstream base `5830ed4fb06da0659414a3deb2a40ad327aca052`, the canonical path
is `eigenvalues-and-inverse-problems/KE-04/README.md`, status Solved. The complete
canonical target and `solution.md` were read. The original resolution belongs
to Matthew J. Colbrook, Department of Applied Mathematics and Theoretical
Physics, University of Cambridge. Any future formalization must retain that
credit and separately credit George Stepaniants with his approved Caltech
department affiliation. No claim about a new formalization PR search is made.

The complete target uses a real symmetric matrix A, a full-column-rank starting
block V of width p, actual block Krylov spaces K_l, full dimension through s,
arbitrary orthonormal bases of those spaces, and all their ordered Ritz values
with multiplicity. For every 1 <= k < j <= s and 1 <= i <= (k-1)p, the open
interval between the i-th and (i+p)-th Ritz values at k must contain a Ritz
value at j. The case of equal proposed endpoints must also be excluded by the
proof; spectral simplicity and positive endpoint width cannot be hypotheses.

The manuscript has a finite-dimensional exact route with no interval work:

1. Under the negation, q(t)=(t-a)(t-b) is nonnegative on the later spectrum.
2. The p+1 dimensional span of the earlier eigenvectors from i through i+p
   intersects K_(k-1) nontrivially, because its codimension inside K_k is p.
3. On a vector in that intersection, the two quadratic forms agree, since
   both compressed operators equal A there. Positive semidefiniteness then
   forces q(H_j)x=0, and the Krylov inclusions imply q(A)x=0.
4. Full column independence through degree k excludes this monic degree-two
   annihilation of a nonzero vector in K_(k-1).

Prospective statement obligations must include the genuine spaces and spectra,
compression self-adjointness and basis independence, dimension/intersection
bridge, spectral quadratic-form positivity and zero implication, degree-two
compression identity, and full-rank nonannihilation. None may be assumed as an
informal-literature axiom. Actual pinned Mathlib APIs remain to be inspected.
LeanCert kernel trust auditing can be used without an artificial numerical
certificate. Two independent statement reviews are required before proof work.

This is a promising additional algebraic track after capacity becomes available;
RA-20 and IE-05 retain priority. A first read attempted a guessed category path
and failed; the permanent registry then supplied the correct path above.
