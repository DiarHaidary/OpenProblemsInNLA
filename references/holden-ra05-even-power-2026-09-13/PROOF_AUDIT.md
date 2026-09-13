# Author-side proof audit

This is a dependency and failure-mode audit, not independent verification.

## Exact target

The main upper theorem treats all ambient dimensions and arbitrary input rank.
A compressed original projector is a positive contraction of rank at most k;
its cost is the same on the row span. The argument controls all such contractions.
The high-accuracy lower construction uses dimension k+1+N but query dimension k.
Its auxiliary dimension is not silently charged to the query rank.

## Normalizations

The optimal head has nonzero optimum when input rank exceeds k. Scale the tail
2s-moment to one so every query cost is at least one. Lewis normalization is only
inside the head, and is undone through linear-form/Gaussian-averaging identities.
No projected or synthetic rows are returned.

The two densities are deliberately distinct. omega controls tail norms after
row scaling; pi includes omega and all relevant tensor leverage distributions.
Every tensor feature includes sqrt(omega). Products therefore reconstruct the
original row cost with factor omega, while rounding coefficients are eta*x/pi.
All feature metrics and both densities remain fixed.

## Complete monomial partition

The expansion (A+2X+r^2-R)^s has indices a+b+c+d=s.

1. b=c=0, a>=1: weighted radial head polynomial, controlled by spectral truncation.
2. a>=1, b+c>0: protected E_l--F_jt operator factorization.
3. a=0, b>=2: balanced two-feature matrix bound.
4. a=0, b=1, c=0: vector bound.
5. a=0, b=1, c>=1: anisotropic matrix bound.
6. a=b=0: recombined pure tail, controlled by Gaussian Lipschitz comparison.

This partition is exhaustive. The pure-tail constant is exactly preserved.
No higher mixed term is discarded as an unquantified remainder.

## Operator-valued queries

For the protected family choose l=min(2a,s), nu=l mod 2,
 h=floor(l/2), e=a-ceil(l/2), j=2a+b-l, t=b+2c.
The left/right maps have a common vector output when nu=1. Their error is
tr(L Z J^T), bounded by ||Z||op ||L||F ||J||F. Claiming a scalar rank-one query
here would be false in general. The degree and norm identities are proved and
numerically checked, including p=6 and p=10 odd-degree cases.

j+c<=s-1 and l<=s give the protected exponent (3s-1)/2. The proof does not
replace this with s+1/2 for s>2. That unjustified improvement would overstate
the result and hide part of the surviving gap.

## Gaussian restrictions and dimensions

All exact constraints act by coefficient-space projection. Left variance,
right variance, vector second moment, and scalar increment metrics contract.
Tropp is applied in an independent orthonormal basis of the constrained space,
not to correlated coordinates treated as independent.

Protecting q right directions costs D_l*q scalar constraints. Budgets are divided
among the finitely many s-dependent families. Head eigendirection constraints
can change on each partial step; the protected mixed right spaces remain fixed
for the whole outer round. All variances inside a round use domination by its
pre-round positive measure, not an unproved invariant at each fractional center.

The pure-tail class uses an s-Lipschitz scalar map and Frobenius rank bound sqrt(k).
A direct high-order tail-tensor norm would introduce an incorrect extra rank loss.
The one-cross family uses a fixed full-round right covariance plus a ridge;
its query-specific quadratic form is uniformly bounded by the exact trace state.

## Positive rounding

Rothvoss's arbitrary-center subspace lemma is required: remaining fractional
coordinates are generally not centered at zero. At each outer round, fractional
exceptions are frozen positively, zero entries are deleted, and full positive
entries double. Exact total-density mass implies active counts halve.

The entire evolving measure, including frozen entries, is used in every matrix
state. No pointwise domination by the original input is asserted. Exact scalar
states and a covariance-error induction supply the needed bounds instead.
Executed masses satisfy geometric prefix bounds, yielding the stated error and
support sums. The preliminary coreset reduction removes log(original n) and
log(original d), while preserving original row indices after weight composition.

## Lower-bound dependencies

The lower proof re-establishes the smoothed random core, its moment estimate,
and spectral truncation. It imports only the stated restricted-invertibility
theorem for selecting columns. Polynomial derivative extraction uses genuine
fixed-rank queries and requires an even exponent. Small ranks are covered by
an explicit nonnegative block construction; the signed extension is asserted
only for the large-rank core family.

## Checks versus proofs

The 8,453 finite assertions include repeated index/degree bookkeeping and are
not 8,453 independent checks of the theorem. Feature checks test identities and
norm bounds on finite data, not the asymptotic oracle construction. Random
finite feature inputs are not asserted to have optimal heads. The separate
12-row integer example does have a globally optimal head, proved via covariance
and Jensen. The finite certificate does not establish the general support theorem.
