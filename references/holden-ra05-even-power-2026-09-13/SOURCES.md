# Sources and dependency map

Web sources checked September 13, 2026 by reading public websites. No GitHub
plugin was used. URLs identify the specific mathematical statements used.

## Original target and status

- Canonical RA-05:
  https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/randomized-and-low-rank-approximation/RA-05/README.md
  Original-row nonnegative model; every rank-at-most-k subspace; arbitrary input
  rank; fixed real p>2; joint-size target, with no runtime requirement.
- Status guidelines and partial-results archive:
  https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/RESOLVED.md
- Prior quartic informal audit:
  https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/references/holden-ra05-quartic-2026-09-13/verification/independent-review.md
  This concerns only the preceding quartic package, not the new extension.

## Imported mathematical statements

1. Honghao Lin, Vahab Mirrokni, David P. Woodruff,
   *Nearly Optimal Strong Coresets for ell_p Subspace Approximation*,
   arXiv:2608.26047v2, August 27, 2026.
   https://arxiv.org/html/2608.26047v2
   Theorem 1.2: baseline nonnegative row reduction with size
   C_p k^(p/2) epsilon^-2 log^(p+5)(C_p k/(epsilon delta)).
   Failure probability is fixed; positive success probability proves existence.
   Used as one upper branch and preliminary reduction, not as a proof of the
   improved second branch.

2. Thomas Rothvoss, *Constructive Discrepancy Minimization for Convex Sets*,
   arXiv:1404.0339v4, 2016.
   https://arxiv.org/pdf/1404.0339
   Lemma 9, printed page 8: coefficient subspace, Gaussian-measure condition,
   arbitrary fractional starting center, constant saturation fraction.
   The displayed lemma was checked from a page screenshot as well as text.

3. Joel A. Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*,
   arXiv:1004.4389v7.
   https://arxiv.org/html/1004.4389v7
   Theorem 1.5: rectangular Gaussian series with both left and right variance.
   Coefficient-projection contraction and anisotropic normalization are proved
   in the new manuscript rather than silently assumed.

4. Adam W. Marcus, Daniel A. Spielman, Nikhil Srivastava,
   *Interlacing Families III: Sharper Restricted Invertibility Estimates*,
   arXiv:1712.07766.
   https://arxiv.org/html/1712.07766
   Theorem 1.1 states the Spielman--Srivastava stable-rank column-selection bound.
   Used only to select actual input columns after spectral truncation.

## Earlier conversation work

The untouched prior ZIP is included under `prior_work/`. Its nested manuscripts
contain the earlier all-exponent lower bounds, all-accuracy construction,
rank-restricted even-power classification, and unrestricted quartic theorem.
The new upper proof is given in full and does not assume an earlier unreviewed
upper theorem. Section 10 explicitly cites an earlier lower bound for a gap
comparison only. No novelty or priority certification is claimed.
