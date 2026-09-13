# IS-02 — Where a symmetric stochastic matrix can be spectrally unique

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

**Difficulty:** challenging  
**Importance:** interesting to specialist  
**Status:** Lean verified
**Last checked:** 2026-09-13

**Rating rationale:** Challenging reflects the geometry of isospectral stochastic families in arbitrary dimension; specialist impact concerns the narrow property of spectral uniqueness within that class.

## Resolution — 2026-09-11

**Negative resolution by Matthew J. Colbrook** (Department of Applied Mathematics and Theoretical Physics, University of Cambridge). See the [complete manuscript](solution.md), **Theorem IS-02, sections 1–2** ([PDF](solution.pdf) · [LaTeX](solution.tex)), prepared 11 September 2026.

The order-four counterexample is real symmetric, nonnegative and stochastic, has spectrum $`\{1,1,0,-1\}`$ and positive trace, and is spectrally unique up to permutation. It lies outside every segment in the proposed locus, disproving the universal necessary condition at an allowed dimension.

The original proof draft was generated in a ChatGPT conversation. A separate Codex agent independently verified the full proof and its match to the exact target on 11 September 2026: [detailed PASS review](../../references/colbrook-2026-09-11/verification/reviews/IS-02-review.md). The review records a hash of the unchanged proof text. That dated informal review is independent agent verification and did not establish a formal certificate. The separate Lean verification is recorded below; no external human peer review is claimed. [The submission history and diagnostic record](../../references/colbrook-2026-09-11/README.md) preserve the initial solution claim. The ratings above are historical, and the earlier literature checks below are retained.

## Lean proof and verification evidence — 2026-09-13

**Formalization: George Stepaniants**, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. Original mathematical proof credit remains Matthew J. Colbrook, Department of Applied Mathematics and Theoretical Physics, University of Cambridge.

The [immutable complete proof](https://github.com/sgstepaniants/OpenProblemsInNLA/tree/522f091b9f0d39d4846f5939bcafc1549ba16a55/eigenvalues-and-inverse-problems/IS-02/lean) uses Lean 4.33.1, LeanCert `621a43d7cf21f87872392a01e874f2f1dbddc926`, and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The [project guide](lean/README.md), [exact targets](lean/NUMERICAL_TARGETS.md), and [source correspondence](lean/SOURCE_MAP.md) identify all nine exports and dependency pins.

`NLA.IS02.counterexample_claim` proves the exact order-four witness has positive trace and the required spectrum, is spectrally unique among all real symmetric stochastic competitors up to permutation, and lies outside every segment in the proposed locus. The characteristic-polynomial bridge preserves eigenvalue multiplicities, and the vertex predicate denotes genuine extreme points. `NLA.IS02.not_targetNecessaryCondition` negates the complete original universal target. No restriction to rational competitors or selected vertices is imposed.

The [successful Ubuntu job](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34766178560/job/103747466088) checked the pinned proof revision. All nine Comparator statements and Lean's default kernel passed, together with sandbox and rejection controls. Every export's actual Linux axiom report contains only `propext`, `Classical.choice`, and `Quot.sound`. The [raw Linux evidence, independent operational audit and reproduction commands](lean/verification/linux-2026-09-13/README.md) are retained. Two statement reviews preceded implementation; two independent mathematical reviews and independent cleanup checks passed. AI assistance and agent review are disclosed; no human peer review or Tau Ceti endorsement is claimed.

## Problem statement

For $`n\geq4`$, put
$`\mathcal S_n=\{A\in\mathbb R^{n\times n}:A=A^T,\ A\geq0,\ A\mathbf1=\mathbf1\}`$
and $`C_n=(\mathbf1\mathbf1^T-I)/(n-1)`$. A matrix $`A\in\mathcal S_n`$
is *spectrally unique* if every $`B\in\mathcal S_n`$ with the same eigenvalues,
including multiplicities, satisfies $`B=R^TAR`$ for a permutation matrix $`R`$.
Let $`[X,Y]=\{(1-t)X+tY:0\leq t\leq1\}`$.

Prove or disprove the following necessary condition: every spectrally unique
$`A\in\mathcal S_n`$ with $`\mathop{\mathrm{tr}}\nolimits A>0`$ belongs to

```math
[I,C_n]\ \cup\!
\bigcup_{V\in\mathop{\mathrm{vert}}\nolimits(\mathcal S_n)}
\bigl([I,V]\cup[C_n,V]\bigr).
```

Here a vertex is an extreme point of the indicated convex polytope; it need
not be a permutation matrix. Only the stated implication is asserted.
This asks where recovering a nonnegative symmetric stochastic matrix from its
spectrum can be unique up to relabeling, a different issue from mere spectral
feasibility.

## References

Mourad and Abbas, [2013 preprint](https://arxiv.org/pdf/1310.1273),
definitions in §1 and Conjecture 5.1, p. 10;
[published article](https://doi.org/10.1080/03081087.2014.903590),
*Linear and Multilinear Algebra* 63 (2015), 869–881.

## Earlier status check — 2026-09-08

Searches for the exact title, `symmetric doubly stochastic
Conjecture 5.1`, and author/title combinations with `counterexample` and
`2026` found no resolution. The source solves order three, which is excluded
from the remaining statement above.

## Audit update — 2026-09-10

Rechecked [Mourad–Abbas](https://arxiv.org/pdf/1310.1273), §5, Conjecture 5.1, against the trace and locus restrictions here. Searches for spectrally unique symmetric stochastic matrices and later work on that conjecture found no general answer. The order-three classification is outside the displayed unresolved dimensions, so it does not change this entry's status. Evidence remains historical rather than a recent explicit reaffirmation.
