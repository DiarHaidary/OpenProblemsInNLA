# Proposed RA-18 research update

No repository changes have been made. This note is suggested wording for consideration after mathematical review, not a claim of acceptance or publication.

## Overall status

Keep the overall entry **Partially resolved**. The main real Goreinov–Tyrtyshnikov–Zamarashkin conjecture is not resolved by this package.

## Proposed addition to the complex-extension section

An explicit recursive construction refutes the proposed existence of a constant independent of both dimensions. Let `omega=exp(2*pi*i/3)`, `a=(1,1,1)^T/sqrt(3)`, and `c=(1,omega,omega^2)^T/sqrt(3)`. Starting from `U_0=(1,1)^T/sqrt(2)`, set

\[
U_{k+1}=[U_k\otimes a\quad I_{2\cdot3^k}\otimes c].
\]

Then `U_k` is a complex `(2*3^k) x 3^k` isometry with equal row norms. Every nonsingular square row submatrix satisfies

\[
\|U_{k,I}^{-1}\|_2^2\ge(3\cdot4^k+1)/2.
\]

Thus `t_C(3^k,2*3^k)/sqrt(2*3^k)` is unbounded. The construction also has an exact scalar spectral recurrence and gives a dimension-dependent lower bound

\[
t_C(r,n)\ge\sqrt{3/32}\,\sqrt n\,
\min(r,n-r)^{\log_3 2-1/2}.
\]

This settles the proposed dimension-independent complex extension negatively, subject to review of the attached proof. It does not determine the optimal complex growth rate.

## Proposed addition to the real special cases

Using the real two-column theorem and weighted orthogonal-complement duality, the real `sqrt(n)` selection bound holds for Parseval frames whose nonzero rows occupy at most `r+2` distinct one-dimensional subspaces. The proof allows arbitrary row lengths and multiplicities within each direction group.

Neither assertion should be described as a proof of the unrestricted real conjecture. The attachment is a proof submission, not an independently reviewed publication.
