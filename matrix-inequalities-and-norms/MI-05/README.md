# MI-05 — The Marcus–de Oliveira determinantal conjecture

**Difficulty:** extreme  
**Importance:** broadly interesting  
**Status:** Partially resolved  
**Last checked:** 2026-09-13

**Rating rationale:** This decades-old spectral enclosure conjecture for arbitrary normal pairs is a major matrix-theory barrier with consequences for determinant and spectral analysis.

## Problem statement

For every integer $`n\ge1`$, let $`A,B\in\mathbb C^{n\times n}`$ be normal matrices, meaning $`AA^*=A^*A`$ and $`BB^*=B^*B`$. List their eigenvalues with algebraic multiplicity as $`a_1,\ldots,a_n`$ and $`b_1,\ldots,b_n`$. Is

```math
\det(A+B)\in\mathop{\mathrm{conv}}\nolimits\left\{\prod_{i=1}^n(a_i+b_{\sigma(i)}):\sigma\in S_n\right\}?
```

Here $`S_n`$ is the permutation group and the convex hull is taken in $`\mathbb C\cong\mathbb R^2`$.

## Partial result — 13 September 2026

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation. [Submission and verified affiliation](../../references/holden-mi05-2026-09-13/README.md).

[Theorem 2.1](../../references/holden-mi05-2026-09-13/report.pdf) gives a fourteen-term signed determinant identity for every order-four complex unitary and every pair of complex spectra. Theorems 3.1–3.2 establish optimal common negative mass on the positive-obstruction regions and show that at most one such obstruction is positive. Corollary 4.1 and Theorem 4.2 prove the original inclusion for a specified class of relative unitaries, including an operator-norm ball of radius $`1/100`$ around the displayed Hadamard matrix; Corollary 4.3 extends these classes by block sums. Theorem 5.1 reduces the remaining support directions, and Theorem 7.2 gives a sharp real-orthogonal obstruction bound. [Proof source](../../references/holden-mi05-2026-09-13/report.tex).

**The unrestricted target remains open.** The manuscript does not establish the determinant inclusion for arbitrary order-four unitaries, much less all dimensions. Negative spectrum-independent weights are not counterexamples to the spectrum-dependent convex-hull assertion. The zero-obstruction classification is also left open. These are partial results under the retained original assumptions and quantifiers, not a full resolution.

The stated partial results passed a separate [independent informal Codex AI-agent audit](../../references/holden-mi05-2026-09-13/independent-review.md), with fresh [exact and regression checks](../../references/holden-mi05-2026-09-13/verification/audit.json). No Lean verification, external human peer review or novelty claim is asserted. The original ID, path, statement and source credit are retained.

## Why it matters

The conjecture would bound a determinant using only two spectra, even when the matrices are not simultaneously diagonalizable. It is a fundamental spectral enclosure problem for structured matrix computations.

## References

1. A. Kovacec, *A conjecture more precise and stronger than the one by Marcus and de Oliveira*, DMUC Preprint 26-11 (7 April 2026), §1, Conjectures 1 and 1′. [Primary paper](https://www.mat.uc.pt/preprints/ps/p2611.pdf).
2. N. Bebiano and J. P. da Providência, *Revisiting the Marcus–de Oliveira conjecture*, Mathematics 13(5) (2025), 711, §1. [DOI](https://doi.org/10.3390/math13050711).
3. J. I. Mulero-Martínez, *A variational framework for determinantal inequalities of normal matrices: Successes and obstructions*, Linear Algebra and its Applications 740 (2026), 19–38; abstract and structured-class results. [DOI](https://doi.org/10.1016/j.laa.2026.03.019).

## Status check — 2026-09-10

The April 2026 preprint proposes a stronger conjecture rather than proving this one. The July 2026 journal paper explicitly describes the unrestricted conjecture as open and proves structured cases. Searches included `Marcus de Oliveira conjecture 2026 proof`, `Marcus Oliveira determinant counterexample`, and the exact 2026 titles. No complete proof or counterexample was located. Primary full text was checked for reference 1; reference 3's status evidence was its publisher abstract, not an independently audited proof.

**Audit update (2026-09-10):** Rechecked Kovacec’s Conjecture 1 and the July 2026 publisher abstract of Mulero-Martínez, then searched for a full resolution. The latter explicitly retains the general conjecture while proving structured spectral classes. This is a bounded literature check, not a proof that no solution exists.

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->
