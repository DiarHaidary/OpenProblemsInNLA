# Exact status and unresolved cases

## Original problem

RA-05 asks for optimal joint rank/accuracy dependence, up to logarithms, for
all fixed real p>2, arbitrary input rank, nonnegative weights on original rows,
and all query subspaces of dimension at most k.

## New resolved subtarget

For every even p=2s>=4 and epsilon<=k^(-(s+1)/2), the unrestricted size is
Theta-tilde_s(k^(s-1)/epsilon^2). The constants depend only on fixed s.
This is a joint-rank statement, not an accuracy exponent with rank fixed.

The new all-accuracy upper bound is
O_s((k^((3s-1)/2)/epsilon+k^(s-1)/epsilon^2) log^5(2k/epsilon)).
The baseline O_s(k^s/epsilon^2 log^(2s+5)(2k/epsilon)) is separately imported
from Lin--Mirrokni--Woodruff, Theorem 1.2.

## Mathematical gaps

At p=6 and epsilon=k^-1, the available lower bound k^(9/2) still falls short
of the upper bound k^5, up to logarithms. At epsilon=k^-3/2 the bounds are k^5
and k^(11/2). Thus not every even-power accuracy regime is classified.

No argument here justifies a non-even-power extension. Uniform polynomial
approximation would need both relative-error and degree-dependent rank control;
neither may be omitted.

## Evidence level

The new proof has an author-side structural audit and reproducible finite
checks only. The public repository's informal audit of the preceding quartic
package does not audit this new extension. No external human peer review,
independent new audit, Lean/formal certificate, or novelty certification is claimed.

## Proposed repository treatment

Further PARTIAL progress, subject to review. Do not mark the whole entry SOLVED,
and do not present this as a complete SOLUTION CLAIMED submission.
No repository files were changed in preparing this archive.
