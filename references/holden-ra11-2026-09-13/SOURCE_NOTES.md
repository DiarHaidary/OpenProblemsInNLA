# Public-source audit

Access date: 13 September 2026. Public web pages, raw repository text, arXiv HTML,
and the arXiv PDF were read. No GitHub plugin was used. These notes are an audit
of source scope, not a claim that all subsequent literature was exhaustively
searched. Third-party papers are not redistributed in this ZIP.

## 1. Exact RA-11 statement

https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/randomized-and-low-rank-approximation/RA-11/README.md

The fetched statement has local dimensions n,q >= 2, 0 < epsilon < 1/2,
arbitrary real PSD matrices, adaptive full-vector responses, and arbitrary
finite exact arithmetic. It expressly has no condition-number bound and no
restriction to Hutchinson estimators. Its displayed status is Open, with a
last-check field of 2026-09-10. That source status is not an assessment of the
new arguments in this package.

## 2. Meyer–Swartworth–Woodruff

“Understanding the Kronecker Matrix-Vector Complexity of Linear Algebra.”
ICML 2025; PMLR 267, 43909–43933.

https://arxiv.org/html/2502.08029v2
https://arxiv.org/pdf/2502.08029v2
https://proceedings.mlr.press/v267/meyer25a.html

Definition 1 specifies the full-vector oracle. Theorem 7 is explicitly about
conditioned vector-matrix-vector queries and is not a lower bound for the
unrestricted full-vector trace target. Conjecture 23, in Section 6, concerns
orthogonal projection onto the span of polynomially many fixed product
vectors. Its statement was checked in the PDF on printed page 13 (zero-based
page 12). The package's n=2 construction contradicts that universal conjecture
as written in arXiv v2, not the stated conditioned theorems.

Section 6 asks for tight trace-estimation bounds and points to possible
Hutch++-type improvements. Nothing in that discussion licenses treating the
conjecture as a proved lower bound.

## 3. Meyer–Avron

“Hutchinson's Estimator is Bad at Kronecker-Trace-Estimation.”
SIMAX 47 (2026), 353–387; online manuscript arXiv:2309.04952v2.

https://arxiv.org/html/2309.04952v2
https://arxiv.org/abs/2309.04952
https://doi.org/10.1137/24M1720895

The estimator-specific real and complex fourth-moment rates do not characterize
all adaptive algorithms. Section 1.2.3 and Section 6 discuss a sqrt(k)/epsilon
lower scale for an RMSE/standard-deviation accuracy criterion using independent
Wishart factors. The manuscript here uses the same type of prior but supplies
an additional log-concave anti-concentration proof for fixed success probability.

Section 7 and Theorem 47 give a kd+1-query product-factor recovery construction.
The package's normalization-and-shift identity supplies parallel access, with
n total calls for PSD factors of order n. The source also notes that rank-one
PSD trace can be recovered in one full-vector query; that particular observation
is not claimed as new here.

## 4. Hutch++

Meyer, Cameron Musco, Christopher Musco, and Woodruff,
“Hutch++: Optimal Stochastic Trace Estimation.” SOSA 2021.

https://arxiv.org/abs/2010.09649

The paper introduces ordinary full-matvec trace estimation with O(1/epsilon)
queries. The package rederives a Gaussian variant with explicit constants,
unbiasedness, nonnegativity, and scale-equivariance so that it can be multiplied
across independent factor estimates.

## 5. Log-concavity

Saumard and Wellner, “Log-concavity and strong log-concavity: a review.”
Statistics Surveys 8 (2014), 45–114.

https://arxiv.org/abs/1404.5886

Used for preservation of log-concavity under convolution (a consequence of
Prékopa's theorem). The log-density calculation, variance lower bound, and
one-dimensional density-height estimate used in this package are provided
explicitly in the manuscript.
