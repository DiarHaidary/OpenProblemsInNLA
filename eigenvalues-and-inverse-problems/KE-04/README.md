# KE-04 — Strict interlacing across block Lanczos iterations

**Difficulty:** challenging  
**Importance:** interesting to the community  
**Status:** Lean verified  
**Last checked:** 2026-09-13  

**Rating rationale:** Challenging reflects a stronger strict interlacing law than general compression interlacing supplies; community impact is spectral information across block Krylov iterations.

## Lean proof and verification evidence — 2026-09-13

**Formalization: George Stepaniants**, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. Matthew J. Colbrook retains credit for the original mathematical proof; D. Šimonová and P. Tichý retain credit for the conjecture. The formalization used substantial AI assistance.

The [immutable Lean source](https://github.com/sgstepaniants/OpenProblemsInNLA/tree/40b0bf52e73e776e7769f0f12dbbda7cd9fff183/eigenvalues-and-inverse-problems/KE-04/lean) proves `NLA.KE04.blockLanczosConjecture`, the complete original largest-full-iteration statement. The proof derives it from the stronger full-prefix theorem. All 24 [registered theorem declarations](lean/comparator.json) are checked. The proof retains every dimension, real symmetric matrix, full-rank starting block, allowed iteration pair, strict interval index and independently chosen orthonormal Krylov basis. Eigenvalue multiplicities are retained, and no separated-endpoint or compatible-basis assumption is added. See the [definitions and source correspondence](lean/SourceCorrespondence.md) and [proof map](lean/PROOF-MAP.md).

Lean is pinned to **4.33.1**, Mathlib to `0df444a360eaa60ab8c11dca51a86af692955474`, and LeanCert to `621a43d7cf21f87872392a01e874f2f1dbddc926`. The argument uses exact finite-dimensional algebra; LeanCert checks the actual proof declarations in kernel mode. The [full dependency manifest](lean/lake-manifest.json) fixes all ten packages.

This campaign ran the real Ubuntu verifier: [workflow 34759746409, KE-04 job 103730400358](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34759746409/job/103730400358). Comparator accepted the 24 independently reviewed statements and proofs, Lean's default kernel accepted the exported proofs, and the transitive axiom reports permit only `propext`, `Classical.choice`, and `Quot.sound`. The actual sandbox and rejection controls passed. The [retained logs and independent operational audit](lean/verification/linux-2026-09-13/README.md) bind the run to the immutable source revision. The proof also passed two independent final mathematical reviews: [referee 1](lean/reviews/final-referee-1.md) and [referee 2](lean/reviews/final-referee-2.md). These are AI-agent reviews, not external human peer review.

From a clean checkout, reproduce on non-root Linux with the [documented prerequisites](../../tools/lean/HARNESS.md):

```
tools/lean/bootstrap.sh /tmp/nla-ke04-check
tools/lean/verify.sh \
  eigenvalues-and-inverse-problems/KE-04/lean /tmp/nla-ke04-check
```

## Resolution — 2026-09-11

**Affirmative resolution by Matthew J. Colbrook** (Department of Applied Mathematics and Theoretical Physics, University of Cambridge). See the [complete manuscript](solution.md), **Theorem KE-04, sections 1–3** ([PDF](solution.pdf) · [LaTeX](solution.tex)), prepared 11 September 2026.

Strict interval occupancy holds for every allowed pair of block Lanczos iterations and every indicated index, in exact arithmetic before the first loss of full block dimension. The quadratic-polynomial argument includes multiplicities and excludes coincident interval endpoints in the stated range.

The original proof draft was generated in a ChatGPT conversation. A separate Codex agent independently verified the full proof and its match to the exact target on 11 September 2026: [detailed PASS review](../../references/colbrook-2026-09-11/verification/reviews/KE-04-review.md). The review records a hash of the unchanged proof text. This is independent agent verification, not external human peer review or formal certification. [The submission history and diagnostic record](../../references/colbrook-2026-09-11/README.md) preserve the initial solution claim. The ratings above are historical, and the earlier literature checks below are retained.

## Original problem statement

Let $`A\in\mathbb R^{n\times n}`$ be symmetric and $`V\in\mathbb R^{n\times p}`$ have full column rank. Write

```math
\mathcal K_j=\mathop{\mathrm{range}}\nolimits[V,AV,\ldots,A^{j-1}V],
```

and let $`s`$ be the largest integer with $`\dim\mathcal K_s=sp`$. For $`1\le j\le s`$, choose an orthonormal basis $`Q_j`$ of $`\mathcal K_j`$ and order the eigenvalues of $`T_j=Q_j^TAQ_j`$ as
$`\theta_1^{(j)}\le\cdots\le\theta_{jp}^{(j)}`$, with multiplicity.

For every $`1\le k< j\le s`$ and $`1\le i\le(k-1)p`$, must the open interval

```math
(\theta_i^{(k)},\theta_{i+p}^{(k)})
```

contain an eigenvalue of $`T_j`$? The statement concerns exact arithmetic before the first loss of full block dimension. Although Lanczos supplies compatible block tridiagonal representations, the spectra do not depend on the chosen bases.

This would extend a scalar Lanczos property used to interpret later Ritz values and distinguish genuine eigenvalue approximation from clusters created by finite precision.

## References

 D. Šimonová and P. Tichý, *On finite precision block Lanczos computations*, arXiv:2507.16484v1 (22 July 2025), §2.1, unnumbered conjecture and final discussion ([primary manuscript](https://arxiv.org/html/2507.16484v1)). J. Liesen and Z. Strakoš, *Krylov Subspace Methods: Principles and Analysis*, Oxford 2013, the scalar Lanczos/orthogonal-polynomial background cited by the source ([publisher](https://doi.org/10.1093/acprof:oso/9780199655410.001.0001)).

## Status check — 2026-09-08

 The arXiv abstract/history and full §2.1 were inspected; v1 remains the only listed version. Searches “block Lanczos interlacing conjecture”, “Šimonová Tichý interlacing”, and 2026 proof/counterexample queries found no resolution. Standard weak Cauchy interlacing is not the asserted strict interval-occupancy result.

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

## Audit update — 2026-09-10

Rechecked the explicit conjecture and concluding discussion in the [2025 block-Lanczos manuscript](https://arxiv.org/html/2507.16484v1). Its block-width index ranges agree with this entry. Searches for later strict block-Lanczos interlacing proofs found no resolution; ordinary Cauchy interlacing is weaker than the displayed claim.
