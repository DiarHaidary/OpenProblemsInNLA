# IE-11 — The exact fifth complete-pivoting growth factor

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

**Difficulty:** challenging  
**Importance:** interesting to specialist  
**Status:** Open  
**Last checked:** 2026-09-13  

**Rating rationale:** Challenging reflects a nonconvex global optimization problem with a high-degree algebraic candidate; specialist impact is an exact low-order pivoting constant.

## Context and notation

All elimination in this problem is in exact arithmetic. Write $`\|A\|_{\max}=\max_{ij}|a_{ij}|`$. A pivoting path creates successive active Schur complements $`S_1=A,S_2,\ldots,S_n`$, with row/column permutations as appropriate. Its element-growth factor is

```math
\rho(A)=\frac{\max_{1\leq j\leq n}\|S_j\|_{\max}}{\|A\|_{\max}}.
```

Partial pivoting chooses a largest-magnitude entry in the active first column; complete pivoting chooses one anywhere in the active matrix. If ties occur, a universal statement includes every admissible tie choice; a supremum includes all admissible paths. These conventions remove implementation-dependent ambiguity. Matrices are nonsingular unless otherwise stated.

## Problem statement

Let

```math
g_5=\sup\{\rho_{\mathrm{CP}}(A):A\in\mathbb R^{5\times5}\text{ nonsingular}\}.
```

Let $`\alpha`$ be the unique real root in $`(4,5)`$ of the integer polynomial $`P_5`$ displayed in Equation (2.15) of the primary reference below. This definition specifies an exact algebraic number; numerically $`\alpha\approx4.1325170786324728542`$. Prove or disprove

```math
g_5=\alpha.
```

All complete-pivoting paths are included in the supremum. The lower bound $`g_5\geq\alpha`$ is already established in the cited paper. The unresolved part is global optimality over all allowable patterns of active constraints, not exact evaluation of a particular numerical example. Order five is independently singled out by the literature as the first unresolved dimension; this catalog does not split the same question into entries for every subsequent order.

## Reference

Chen, Edelman, and Urschel, [*The largest 5th pivot may be the root of a 61st degree polynomial*](https://arxiv.org/html/2602.20390v1), February 2026, Equation (2.15), Conjecture 2.1, Theorem 2.2, and Theorem 3.5. The current rigorous interval is $`\alpha\leq g_5\leq4.84`$.

## Earlier status check — 2026-09-08

Searches for the paper title and `complete pivoting maximum five 2026` found no global proof. Shah–Urschel's August asymptotic result leaves this exact finite-dimensional optimum undetermined.

## Audit update — 2026-09-10

The [February 2026 primary preprint](https://arxiv.org/abs/2602.20390) still presents the degree-61 candidate as conjecturally optimal, rather than proving the matching upper bound. Title-based and fifth-pivot resolution searches found no later exact determination. The broader complete-pivoting bounds do not certify this finite-order optimum.

## Reviewed supporting results — 13 September 2026

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation.

The [submitted report](../../references/holden-ie-extensions-2026-09-13/manuscripts/IE-11/report.pdf), Section 5 (Theorem 5.1), certifies strict local maximality of the algebraic candidate in all 24 free entries with the normalization and diagonal complete-pivoting path fixed. Sections 3–4 reconstruct the candidate and degree-61 polynomial; Section 6 provides a strictly feasible rational witness. The candidate and established lower bound remain attributed to Chen, Edelman and Urschel. Section 7 certifies an auxiliary relaxation optimum of 81/16, which is not a feasible complete-pivoting growth example.

The [independent informal AI-agent review](../../references/holden-ie-extensions-2026-09-13/verification/review-ie11-ie20.md) supports the explicitly limited claims. **Status remains Open:** the work supplies supporting local and certificate results, but no matching global upper bound and no counterexample. All original matrices and admissible pivot paths remain part of the target.

[Submission record and verified affiliation](../../references/holden-ie-extensions-2026-09-13/README.md). Substantial AI assistance is disclosed. The review is informal automated review, not external human peer review or formal verification. No Lean verification was performed.
