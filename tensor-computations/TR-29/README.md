# TR-29 — Exact partially symmetric rank of products of generalized W tensors

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

**Difficulty:** challenging  
**Importance:** interesting to specialist  
**Status:** Partially resolved  
**Last checked:** 2026-09-13

**Rating rationale:** Matching constructive upper bounds by sharp lower bounds for arbitrary products requires substantial new decomposition arguments. The exact partially symmetric rank of this particular family chiefly interests specialists in tensor rank and multipartite entanglement.

## Partial resolution — the two-factor case k = 2, 13 September 2026

**Author:** Maximilian Behr. [Submission record](../../references/behr-tr29-2026-09-13/README.md).

[Theorem 1.1, proved in Sections 3–4](../../references/behr-tr29-2026-09-13/manuscript/TR29_two_factor_rank.pdf) settles every tuple with $`k=2`$:

```math
R(W_{d_1}\otimes W_{d_2})=2(d_1+d_2-2)\qquad\text{for all }d_1,d_2\ge2 .
```

The lower bound combines a peeling lemma — a point set supporting $`x^py\otimes u^qv`$ lies on no curve of bidegree $`(1,q)`$ or $`(p,1)`$, so its Hilbert function is maximal there — with the catalecticant–Sylvester inequality of Wang–Seigal applied to this unbalanced pair of bidegrees, where the catalecticant has rank four. The matching upper bound is Gałązka's decomposition (also Canino–Casarotti–Santarsiero, Theorem 1.1). Previously equality was known for $`d_1=2`$ or $`d_2=2`$, for $`(3,3)`$, and for $`(4,4)`$ in an unpublished 2021 note of Gałązka. Corollary 5.4 of the same manuscript also determines $`R(x^ay^b\otimes u^cv^d)=(a+1)(c+1)-(a-b)(c-d)`$ for all $`a\ge b\ge1`$, $`c\ge d\ge1`$.

**The case $`k\ge3`$ remains open** (for example $`R(W_3\otimes W_3\otimes W_3)`$, with upper bound 20), so the entry stays Partially resolved.

The argument passed two separate [independent AI-agent informal audits](../../references/behr-tr29-2026-09-13/verification/independent-review.md), with exact rational checks and exhaustive finite-field black-box searches that were rerun. AI assistance is disclosed; no external human peer review or formal verification is claimed. No Lean verification was performed.

## Problem statement

For an integer $`d\geq3`$, put

```math
W_d=\sum_{j=1}^{d}
e_1^{\otimes(j-1)}\otimes e_2\otimes
e_1^{\otimes(d-j)}\in\mathop{\mathrm{Sym}}\nolimits^d(\mathbb C^2).
```

Given any $`k\geq2`$ and $`d_1,\ldots,d_k\geq3`$, set
$`T_{\mathbf d}=W_{d_1}\otimes\cdots\otimes W_{d_k}`$.
Determine the exact smallest integer $`s`$ such that

```math
T_{\mathbf d}=\sum_{\ell=1}^{s}
(v_{1,\ell})^{\otimes d_1}\otimes\cdots\otimes
(v_{k,\ell})^{\otimes d_k},
\qquad v_{j,\ell}\in\mathbb C^2.
```

This minimum is the partially symmetric rank with the $`k`$ blocks of orders $`d_1,\ldots,d_k`$ fixed. It is not the border rank and not the rank obtained after grouping modes from different blocks. The harmless nonzero scalar relating the displayed $`W_d`$ to the polynomial $`x^{d-1}y`$ can be absorbed into a decomposition.

## Why it matters

These explicit tensors are benchmarks for the difference between exact, border, and symmetry-constrained tensor decompositions. They already demonstrate that decomposing two copies together can cost fewer terms than multiplying their individual ranks. Determining their exact ranks would quantify that saving beyond small examples.

## References and status check

1. A. Oneto and E. Ventura, *Ranks of tensors: geometry and applications*, [2025 survey](https://doi.org/10.1007/s40574-025-00472-9), Question 12, following Theorems 4.4–4.5.
2. E. Ballico, A. Bernardi, M. Christandl, and F. Gesmundo, *On the partially symmetric rank of tensor products of W-states and other symmetric tensors*, [arXiv:1803.01623](https://arxiv.org/abs/1803.01623), §§3–4; Rendiconti Lincei **30** (2019), 93–124.
3. S. Canino, A. Casarotti, and P. Santarsiero, *A new bound on the rank of tensor product of W-states*, [arXiv:2512.05828v1](https://arxiv.org/html/2512.05828v1), Theorem 1.1 and its following discussion.

### Status check — 2026-09-10

Checked the 2025 source question and Canino–Casarotti–Santarsiero v1, Theorem 1.1 and the ensuing sharpness discussion, with targeted W-product-rank searches through 2026. The December 2025 paper gives the upper bound $`2^{k-1}(d_1+\cdots+d_k-2k+2)`$ and explicit decompositions. Equality is known for $`k=2,d_1=d_2=3`$, where the rank is eight, so a nontrivial parameter case is resolved. The construction alone does not prove minimality for other tuples. No general exact formula was located.
