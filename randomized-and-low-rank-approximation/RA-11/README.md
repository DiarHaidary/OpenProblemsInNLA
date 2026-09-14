# RA-11 — Optimal trace-estimation complexity using Kronecker matrix-vector queries

**Difficulty:** extreme  
**Importance:** interesting to the community  
**Rating rationale:** Extreme because optimal adaptive information bounds remain unknown even across exponential tensor-order scales; community impact is reliable computation with tensor-structured matrix access.  
**Topic:** Structured randomized trace estimation.  
**Last checked:** 2026-09-14  
**Status:** Partially resolved  


## Further partial results — probability-sensitive probes, 14 September 2026

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation. [Verified affiliation and submission record](../../references/holden-further-2026-09-14/README.md).

[Theorems 2.1–2.2 and Corollary 2.3](../../references/holden-further-2026-09-14/RA-11/manuscript.pdf) give new upper bounds for every real PSD input in the original full-vector real product-query model. In particular, with $`N=n^q`$,

```math
Q(n,q,\varepsilon)\le\min\{N,2\lceil\sqrt{6N}/\varepsilon\rceil\}.
```

The constant $`6`$ improves to $`3`$ when $`N`$ is a power of two. The diagonal-control construction uses bounded-fair-bit, nonadaptive real product queries. The fractional-moment branch has fixed-accuracy exponential rate $`D_n=\log n+1-H_n`$ in tensor order, where $`H_n=\sum_{j=1}^n1/j`$. Its sharpness is only for the specified empirical-average estimator; it is not an unrestricted oracle lower bound. A finite-bit version exists, with no efficient discretization implementation claimed.

The new partial results passed a separate [independent Codex AI-agent audit](../../reviews/2026-09-14-further-submissions/RA-11-review.md). Exact diagonal and complex-response interpolation checks and a floating moment grid passed; the numerical simulation suite was not rerun. **The unrestricted joint minimax characterization remains open**, so status remains Partially resolved. Inherited bounds in the manuscript are outside this fresh audit; the prior independently reviewed contribution below is retained. [Proof text](../../references/holden-further-2026-09-14/RA-11/manuscript.md). AI assistance is disclosed; no Lean verification, external human peer review, formal verification or novelty claim is asserted.


## Partial results — Sidney Holden, 13 September 2026

**The general RA-11 target remains open.** Sidney Holden (Center for Computational Biology, Flatiron Institute, Simons Foundation) supplies [partial results](../../references/holden-ra11-2026-09-13/manuscript/ra11_partial_results.pdf), with [proof source](../../references/holden-ra11-2026-09-13/manuscript/ra11_partial_results.tex), [verified affiliation and submission record](../../references/holden-ra11-2026-09-13/README.md), and a separate [independent informal Codex AI-agent audit](../../references/holden-ra11-2026-09-13/independent-review.md).

Theorem 1.1 gives general upper and lower bounds that do not match throughout the parameter range. It yields $`Q(n,q,\varepsilon)=\Theta(n^q)`$ when $`\varepsilon\le n^{-q}`$. Under the additional promise that the unknown matrix is a tensor product of PSD factors, the manuscript establishes $`\Theta(\min\{n,\sqrt q/\varepsilon\})`$ queries. It also gives a $`q+1`$-call real simulation of a complex product query, promised low-rank recovery, and a counterexample to the source's Conjecture 23. That counterexample does not settle RA-11.

The audit passed these partial scopes; exact and numerical checks were rerun. The surviving question is the unrestricted adaptive complexity for arbitrary PSD matrices, uniformly in all three parameters. No full resolution, external human peer review, novelty certification or formal verification is claimed. No Lean verification was performed. The original target follows unchanged.

Let $`n,q\ge2`$ be integers and $`0<\varepsilon<1/2`$. An unknown real symmetric PSD matrix $`M\in\mathbb R^{n^q\times n^q}`$ is accessible only through an exact oracle which, on input $`v_1,\ldots,v_q\in\mathbb R^n`$, returns

```math
M(v_1\otimes\cdots\otimes v_q)\in\mathbb R^{n^q}.
```

Let $`Q(n,q,\varepsilon)`$ be the smallest integer $`t`$ for which a randomized algorithm can, for every such $`M`$, make at most $`t`$ oracle calls and output $`\widehat t\in\mathbb R`$ satisfying

```math
\Pr\bigl\{|\widehat t-\mathop{\mathrm{tr}}\nolimits(M)|\le\varepsilon\mathop{\mathrm{tr}}\nolimits(M)\bigr\}\ge\frac23.
```

Queries may depend on previous responses and internal randomness. The algorithm may perform arbitrary finite exact arithmetic between calls; only oracle calls are counted. The inputs $`n,q,\varepsilon`$ are known. Neither the query vectors nor their concatenation are required to have bounded condition number, and there is no restriction to Hutchinson estimators.

Determine $`Q(n,q,\varepsilon)`$ up to universal constant factors, simultaneously in all three parameters.

This is a precise query-complexity formulation of the source's request for tight trace-estimation bounds. It would quantify the cost of exploiting rank-one tensor queries when ordinary matrix access is unavailable.

## References

1. R. A. Meyer, W. Swartworth, and D. P. Woodruff, [Understanding the Kronecker Matrix-Vector Complexity of Linear Algebra](https://arxiv.org/html/2502.08029v2), ICML 2025, PMLR 267, 43909–43933. Definition 1 specifies the oracle; §6, final sentence, asks for tight trace-estimation bounds. Theorem 7 bounds a conditioned scalar quadratic-form oracle; its following discussion distinguishes full-vector responses. [Published record](https://proceedings.mlr.press/v267/meyer25a.html).
2. R. A. Meyer and H. Avron, [Hutchinson's Estimator is Bad at Kronecker-Trace-Estimation](https://arxiv.org/abs/2309.04952), *SIAM Journal on Matrix Analysis and Applications* 47 (2026), 353–387, abstract and trace-estimator bounds. These tight rates concern the specified estimator and query distributions.

## Status check — 2026-09-08

Checked the first paper's latest listed arXiv v2 (2025-02-13), §6, and its ICML publication record; checked the second paper's latest listed v2 (2025-01-31) and 2026 journal record. Searches for “Kronecker trace estimation tight 2026” and the exact first title found no solution for unrestricted adaptive algorithms. The available trace lower bound assumes both scalar quadratic-form queries and bounded query conditioning; it does not establish a lower bound for the unrestricted full-vector oracle defined here. The 2026 Hutchinson article establishes estimator-specific rates and therefore does not determine $`Q`$. The minimax definition and explicit parameter range are editorial formalization of a source-stated complexity question, not a quoted formula from the paper.

## Audit — 2026-09-10

Rechecked [Meyer–Swartworth–Woodruff, §6](https://arxiv.org/html/2502.08029v2) and the [2026 Hutchinson publication](https://doi.org/10.1137/24M1720895). Kronecker-trace-complexity searches found no unrestricted adaptive characterization. Conditioned scalar-query lower bounds and estimator-specific rates still do not settle the full-vector oracle.

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->
