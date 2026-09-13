# IE-16 — A sharp subset bound for worst-case normal GMRES

**Difficulty:** challenging  
**Importance:** interesting to the community  
**Status:** Lean verified
**Last checked:** 2026-09-13

**Historical rating rationale:** Challenging reflects extending a discrete real approximation principle to complex spectra with a sharp constant; community impact concerns usable worst-case GMRES bounds for normal matrices.

## Resolution: negative, 12 September 2026

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation. [Verified affiliation and submission record](../../references/holden-ie16-2026-09-12/README.md).

[Theorem 1.1, proved in Sections 2-3 of the manuscript](solution.pdf) disproves the displayed universal inequality. With $`\omega=e^{2\pi i/3}`$, take the nine distinct nonzero points $`L=\{\omega^a+10^{-3}\omega^b:0\le a,b\le2\}`$ and $`k=4`$. Then

```math
M_4(L)=\frac{3003003000}{1001003001001}>\frac{299}{100000},
\qquad \max_{S\subseteq L,\ |S|=5}M_4(S)<\frac{23}{10000}.
```

The ratio is therefore greater than $`13/10>4/\pi`$. Here $`n=9`$ and $`1\le4\le n-2`$, so all original assumptions and quantifiers are addressed by this counterexample. Theorem 1.2 (Sections 4-5) additionally proves that no finite dimension-independent replacement constant exists. The finite counterexample alone settles IE-16 negatively; no case of the original universal truth question remains open.

The complete proof passed a separate [independent Codex AI-agent informal audit](../../references/holden-ie16-2026-09-12/INDEPENDENT-REVIEW.md). The supplied exact-arithmetic verifier passed all 126 subset checks, and reviewer-written rational checks passed independently. That dated informal audit was not external human peer review or formal verification. The separate Lean verification is recorded below. [Proof source](solution.tex) · [Exact verifier and certificates](../../references/holden-ie16-2026-09-12/submitted/README.md).

## Lean proof and verification evidence — 2026-09-13

**Formalization: George Stepaniants**, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. Original mathematical proof and exact certificate: **Sidney Holden**, Center for Computational Biology, Flatiron Institute, Simons Foundation.

The [immutable complete Lean proof](https://github.com/sgstepaniants/OpenProblemsInNLA/tree/697a2a1d88337a6747aa5c82fb6e554d3ff1b356/linear-systems-and-elimination/IE-16/lean) uses Lean 4.33.1, [LeanCert 621a43d7cf21](https://github.com/alerad/leancert/tree/621a43d7cf21f87872392a01e874f2f1dbddc926) and [Mathlib 0df444a360ea](https://github.com/leanprover-community/mathlib4/tree/0df444a360eaa60ab8c11dca51a86af692955474), with full pins in the [dependency manifest](lean/lake-manifest.json). The [project guide](lean/README.md), [exact targets](lean/NUMERICAL_TARGETS.md), [definitions](lean/NLA/IE16/Definitions.lean) and [fifteen-contract boundary](lean/Challenge.lean) record the precise source correspondence.

`NLA.IE16.not_IE16Conjecture` negates the complete displayed universal inequality. The nine-point witness at degree four uses arbitrary normalized complex polynomials, actual complex norms and `Real.pi`. The full minimum is attained and equals `3003003000/1001003001001`; every five-point subset has an attained minimum below `23/10000`, and their actual maximum is positive. The ratio exceeds `13/10>4/π`. Exact root coordinates, positive weights and four vanishing moments certify the full optimum. Generic Lagrange interpolation and a finite occupancy argument cover every five-point subset. The stronger unbounded-ratio theorem remains an informal source result outside this formalization; the finite counterexample already settles the original universal target.

The repository ran [successful non-root Ubuntu verification](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34774629327/job/103770408910) on the pinned canonical proof. All fifteen Comparator statements, permitted axiom closures and Lean’s default kernel passed, together with actual sandbox and rejection controls. Every exported theorem reports only `propext`, `Classical.choice` and `Quot.sound`. [Raw evidence and reproduction commands](lean/verification/linux-2026-09-13/README.md), [statement acceptance](lean/reviews/STATEMENT-ACCEPTANCE.json) and [final canonical referee acceptance](lean/reviews/FINAL-ACCEPTANCE.json) preserve the verification scope. AI assistance and independent agent reviews are disclosed; no external human peer review or official Tau Ceti endorsement is claimed.

## Original problem (retained)

Let $`L\subset\mathbb C\setminus\{0\}`$ consist of $`n\ge3`$ distinct points. For a nonempty $`S\subseteq L`$, define

```math
M_k(S)=\min_{p\in\mathbb C[z],\ \deg p\le k,\ p(0)=1}\max_{z\in S}|p(z)|.
```

Is it true, simultaneously for every such $`L`$ and $`1\le k\le n-2`$, that

```math
M_k(L)\le\frac4\pi\max_{S\subseteq L,\ |S|=k+1}M_k(S)?
```

The constant is required to be independent of dimension, degree, and the locations of the points.

For a normal matrix with spectrum $`L`$, $`M_k(L)`$ is the largest relative residual norm attainable at GMRES step $`k`$, over unit initial residuals. The smaller-set quantities have explicit formulas through Lagrange interpolation. The question therefore asks for a sharp, dimension-independent certificate of worst-case convergence using small subsets of the spectrum. It is distinct from equality of ideal and worst-case GMRES for a nonnormal Jordan block (IE-02).

## References

 J. Liesen and P. Tichý, *The worst-case GMRES for normal matrices*, BIT 44 (2004), 79–98, conjecture (3.16), pp. 91–92, and Appendix ([author copy](https://page.math.tu-berlin.de/~liesen/Publicat/LieTic04.pdf)). Their *A min-max problem on roots of unity*, TU Berlin Preprint 28-2003, conclusion (9.1), proves selected roots-of-unity cases and sharpness of $`4/\pi`$ ([university record](https://doi.org/10.14279/depositonce-14263)). Their survey *Convergence analysis of Krylov subspace methods*, GAMM-Mitteilungen 27 (2004), discussion after (11), restates the conjecture ([author copy](https://page.math.tu-berlin.de/~liesen/Publicat/LiTiGAMM.pdf)).

## Status check — 2026-09-08

 Searched the original title with “conjecture”, “4/pi”, “4/π”, “proof”, “counterexample”, and 2025–2026; checked the authors' current publication lists. The later Jordan-block papers concern a different conjecture. No resolution or recent explicit reaffirmation of this particular bound was located; its open-status evidence is historical and bounded.

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

## Audit update — 2026-09-10

The [primary paper](https://page.math.tu-berlin.de/~liesen/Publicat/LieTic04.pdf), §3.2.1, proves the stronger subset equality for every real spectrum, a substantive subclass of the displayed target. Its complex-spectrum conjecture remains in §3.2.2. Searches for the Liesen–Tichý conjecture and later sharp normal-GMRES subset bounds found no general resolution; the current status records the real-spectrum partial result without asserting exhaustive literature coverage.
