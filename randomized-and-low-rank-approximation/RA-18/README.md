# RA-18 — The Goreinov–Tyrtyshnikov–Zamarashkin conjecture on square-submatrix inverse norms

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

**Difficulty:** challenging
**Importance:** interesting to the community
**Status:** Partially resolved
**Last checked:** 2026-09-13

**Rating rationale:** Improving the classical bound is challenging and would sharpen stability guarantees for skeleton/CUR approximation.

## Problem statement

For integers $`1\le r< n`$, let $`U\in\mathbb R^{n\times r}`$ satisfy $`U^TU=I_r`$.
Write $`U_I=U(I,:)`$ for $`I\subseteq\{1,\ldots,n\}`$ with $`|I|=r`$, and let $`\|\cdot\|_2`$ denote the spectral norm.

**Conjecture** (Goreinov–Tyrtyshnikov–Zamarashkin [1, Eq. (2.6)]).
Every such $`U`$ admits a nonsingular square submatrix $`U_I`$ satisfying

```math
\|U_I^{-1}\|_2\le\sqrt n.
```

In the notation of [1], this is $`t(r,n)\le\sqrt n`$, where

```math
t(r,n)=
\max_{\substack{U\in\mathbb R^{n\times r}\\U^TU=I_r}}
\qquad
\min_{\substack{I\subseteq\{1,\ldots,n\}\\|I|=r,\ \det(U_I)\ne0}}
\|U_I^{-1}\|_2.
```

The minimum is over nonsingular submatrices; at least one exists because $`\mathop{\mathrm{rank}}\nolimits(U)=r`$.

## Known bounds and cases

The bound

```math
t(r,n)\le\sqrt{r(n-r)+1}
```

is well known and follows from various arguments: maximal volume [1], Bischof–Stewart QR (BSQR) [2, 3], or volume sampling [4, 5] just to name a few.
Also, $`t(r,n)\ge\sqrt n`$ whenever $`r+1`$ divides $`n`$ [1, Lem. 2.2], so the conjectured constant is sharp.

The real case $`r=1`$ is elementary.
Nesterenko [6] proved the real case $`n=4`$, $`r=2`$; Sengupta–Pautov [7] subsequently proved $`r=2`$ for all $`n`$.
Orthogonal completion gives $`t(r,n)=t(n-r,n)`$, leaving $`3\le r\le n-3`$ as the general open range.
These inverse norms control pseudoskeleton approximation errors [1, Thms. 3.1–3.2].

## Proposed complex extension (retained statement; refuted below)

Define $`t_{\mathbb C}(r,n)`$ analogously using $`U\in\mathbb C^{n\times r}`$ with $`U^*U=I_r`$, where $`*`$ denotes conjugate transpose.
The minimization again runs only over nonsingular $`U_I`$.
The classical bound $`\sqrt{r(n-r)+1}`$ also holds over $`\mathbb C`$ [3].

**Conjecture (proposed by the contributor).** There is an absolute constant $`\alpha`$, independent of $`r`$ and $`n`$, such that

```math
t_{\mathbb C}(r,n)\le\alpha\sqrt n,
\qquad 1\le r< n.
```

The proposed dimension-independent bound is refuted by the submission below. The optimal dimension-dependent growth remains undetermined.
The constant $`\alpha=1`$ fails: $`t_{\mathbb C}(2,4)=\sqrt{3+\sqrt3}>2`$ [8, 9].
For two columns, Nesterenko [9, Prop. 1] proves

```math
t_{\mathbb C}(2,n)\le c_2\sqrt n,
\qquad c_2=\left(2-\frac2{\sqrt3}\right)^{-1/2}\approx1.08766,
```

with equality whenever $`4\mid n`$, which already ruled out $`\alpha< c_2`$; the new result rules out every finite universal $`\alpha`$.

## Partial resolution — 13 September 2026

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation ([verified affiliation and provenance](../../references/holden-ra18-2026-09-13/SUBMISSION.md)).

**The separate complex extension is resolved negatively; the original real conjecture remains open.** [Theorem 2.1 and Section 3 of the manuscript](../../references/holden-ra18-2026-09-13/manuscript/ra18.pdf) give an explicit recursive family. Set

```math
\omega=e^{2\pi i/3},\qquad
 a=\frac{(1,1,1)^T}{\sqrt3},\qquad
 c=\frac{(1,\omega,\omega^2)^T}{\sqrt3},\qquad
 U_0=\frac{(1,1)^T}{\sqrt2},
```

and define

```math
U_{k+1}=[\,U_k\otimes a\quad I_{2\cdot3^k}\otimes c\,].
```

Then $`U_k\in\mathbb C^{(2\cdot3^k)\times3^k}`$ has orthonormal columns and every row has squared norm $`1/2`$. Every nonsingular square row submatrix obeys

```math
\|U_{k,I}^{-1}\|_2^2\ge\frac{3\cdot4^k+1}{2},
\qquad
\frac{t_{\mathbb C}(3^k,2\cdot3^k)}{\sqrt{2\cdot3^k}}
\ge\sqrt{\frac{3\cdot4^k+1}{4\cdot3^k}}\longrightarrow\infty.
```

The proof classifies every nonsingular lifted selection and proves the squared-inverse-norm recurrence $`b(U_{k+1})\ge4b(U_k)-3/2`$; it does not infer a universal claim from sampled matrices. Sections 5–6 additionally give exact spectra and basis counts and the all-dimensions lower bound

```math
t_{\mathbb C}(r,n)\ge\sqrt{\frac3{32}}\,\sqrt n\,
\min(r,n-r)^{\log_3 2-1/2}.
```

For real matrices, Theorem 7.2 proves the original $`\sqrt n`$ bound when the nonzero rows occupy at most $`r+2`$ one-dimensional subspaces, with arbitrary lengths and multiplicities. Its weighted-complement argument uses the real two-column theorem [7]. Section 8 supplies sharp real examples for every $`1\le r< n`$; this is a lower bound, not a proof of the conjectured upper bound for arbitrary real frames.

The [independent Codex AI-agent audit](../../references/holden-ra18-2026-09-13/independent-review.md) passed these stated scopes and records the reproducibility checks and their limits. This is informal automated review, not external human peer review or formal verification. No Lean verification was performed, and no priority claim is asserted. [Manuscript source](../../references/holden-ra18-2026-09-13/manuscript/ra18.tex) · [Code, results and submission record](../../references/holden-ra18-2026-09-13/README.md).

**Remaining target:** the unrestricted real conjecture, in particular general frames with $`3\le r\le n-3`$ outside the proved structured class. Realifying the complex construction does not settle it. RA-18 retains **Partially resolved**, its original ID and statement, and its place in the open count. The optimal complex growth rate also remains undetermined.

## References

1. S. A. Goreinov, E. E. Tyrtyshnikov, and N. L. Zamarashkin, *A theory of pseudoskeleton approximations*, Linear Algebra and its Applications **261** (1997), 1–21.
   [Published paper](https://doi.org/10.1016/S0024-3795(96)00301-1).
2. A. Damle, *Computing Strong Rank-Revealing Factorizations for Matrices with Orthonormal Rows*, arXiv: 2607.13532v1 (2026).
   [Preprint](https://arxiv.org/pdf/2607.13532v1).
3. A. I. Osinsky, *Close to optimal column approximation using a single SVD*, Linear Algebra and its Applications **725** (2025), 359–377.
   [Published paper](https://doi.org/10.1016/j.laa.2025.07.016).
4. H. Avron and C. Boutsidis, *Faster subset selection for matrices and applications*, SIAM Journal on Matrix Analysis and Applications **34** (2013), 1464–1499.
   [Published paper](https://doi.org/10.1137/120867287).
5. A. Cortinovis and D. Kressner, *Adaptive Randomized Pivoting for Column Subset Selection, DEIM, and Low-Rank Approximation*, SIAM Journal on Matrix Analysis and Applications **47** (2026), 25–47.
   [Published paper](https://doi.org/10.1137/24M1719189).
6. Y. Nesterenko, *Submatrices with the best-bounded inverses: revisiting the hypothesis*, arXiv: 2303.07492 (2023; revised 2024).
   [Preprint](https://arxiv.org/abs/2303.07492).
7. R. Sengupta and M. Pautov, *On the submatrices with the best-bounded inverses*, arXiv: 2604.05944v5 (2026).
   [Preprint](https://arxiv.org/html/2604.05944v5).
8. Y. Nesterenko, *Submatrices with the best-bounded inverses: Studying $`\mathbb R^{n\times2}`$ and* $`\mathbb C^{n\times2}`$, arXiv: 2408.16631v1 (2024).
   [Preprint](https://arxiv.org/html/2408.16631v1).
9. Y. Nesterenko, *Submatrices with the best-bounded inverses: an asymptotically tight upper bound for* $`\mathbb C^{n\times2}`$, arXiv: 2604.24087v1 (2026).
   [Preprint](https://arxiv.org/html/2604.24087v1).

## Earlier literature status check — 2026-09-11

The earlier check of [1]–[9] and later-resolution searches found no general real-case resolution or resolution of the proposed complex extension. The latter finding is superseded by the independently audited submission above.
The real two-column result is a preprint and supports the partially resolved status.
