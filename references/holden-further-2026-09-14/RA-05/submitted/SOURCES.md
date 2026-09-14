# Primary sources and exact dependency scope

Accessed via public web pages, not a GitHub plugin, on September 13, 2026. URLs are included here for reproducibility. Published status, historical priority, and independent verification of the new manuscript are not inferred from these references.

## Original target

OpenProblemsInNLA, RA-05: Sharp joint rank and accuracy dependence for strong l_p subspace coresets.

https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/randomized-and-low-rank-approximation/RA-05

https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/randomized-and-low-rank-approximation/RA-05/README.md

The request concerns nonnegative original-row weights, every fitted linear subspace of dimension at most k, all fixed real p > 2, and all accuracies in (0,1/2). Constants may depend only on p. No running-time target is imposed.

## General upper bound — imported

H. Lin, V. Mirrokni, D. P. Woodruff. *Nearly Optimal Strong Coresets for l_p Subspace Approximation*. arXiv:2608.26047v2, August 27, 2026.

https://arxiv.org/html/2608.26047v2

**Theorem 1.2** supplies the nonnegative strong-row upper bound `C_p k^(p/2) epsilon^(-2) log^(p+5)(C_p k/(epsilon delta))`. Fixing delta=1/4 gives existence. It is the matching non-even upper bound and is also a preliminary reduction used in Part II. The new lower bound is not attributed to this source.

## Boolean spectrum — direct antecedent, estimate reproved

Y. Li, R. Wang, D. P. Woodruff. *Tight Bounds for the Subspace Sketch Problem with Applications*. arXiv:1904.05543v3; SIAM Journal on Computing 50(4), 2021.

https://arxiv.org/abs/1904.05543

https://arxiv.org/pdf/1904.05543

**Section 3.1, Lemmas 3.1–3.3 and Corollary 3.4** analyze the middle Walsh spectrum of the Boolean absolute-power matrix. **Theorem 6.1** concerns sampling-based embeddings. The new manuscript explicitly credits this mechanism and reproves its needed spectral estimate. The tensor support proof is direct; it does not interpret a bit-complexity statement as a weight-support statement.

## Restricted invertibility — imported twice in Part I

A. W. Marcus, D. A. Spielman, N. Srivastava. *Interlacing Families III: Sharper Restricted Invertibility Estimates*. arXiv:1712.07766.

https://arxiv.org/html/1712.07766

**Theorem 1.1** states the Spielman–Srivastava stable-rank bound. Used to select core columns and selected Boolean columns. No unit-column assumption is imposed, and the unprojected original columns have at least the projected least singular value.

## Additional structural inputs in the included even proof

T. Rothvoss. *Constructive Discrepancy Minimization for Convex Sets*. arXiv:1404.0339v4.

https://arxiv.org/pdf/1404.0339

**Lemma 9** allows an arbitrary starting point and a coefficient subspace. Its displayed parameters were also checked in the rendered page: delta=(3/2) xi log_2(1/xi), with saturation xi/2. Only an absolute-constant consequence is used.

J. A. Tropp. *User-Friendly Tail Bounds for Sums of Random Matrices*. arXiv:1004.4389v7.

https://arxiv.org/html/1004.4389v7

**Theorem 1.5**, rectangular Gaussian series. The covariance projection and structured Gaussian norming consequences used by Part II are proved in that part rather than attributed wholesale to Tropp.

## Included proof, not external verification

The preceding *Sharp unrestricted even-power row coresets* manuscript is reproduced unchanged as Part II, with source and original archive. Its local Theorem 1.1 is the even half of the combined theorem. Historical references in that document to a remaining non-even gap are addressed by the new Part I, not erased.

## Repository evidence levels

https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/RESOLVED.md

A primary manuscript claiming the complete target without independent verification is “Solution claimed.” A mathematical gap is not the same as pending verification. This package claims no remaining parameter gap, but does not claim external acceptance or formal checking.
