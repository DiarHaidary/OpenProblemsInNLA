# MI-32 — Spectral norms of independent entries with regular moment growth

<!-- navigation -->
[All categories](../../README.md) · [Category index](../README.md) · [Read PDF](problem.pdf) · [LaTeX source](problem.tex)
<!-- /navigation -->

**Topic:** Expected spectral norms of inhomogeneous random matrices  
**Difficulty:** challenging  
**Importance:** interesting to the community  
**Status:** Lean verified  
**Last checked:** 2026-09-14

**Lean verified — 2026-09-14. Formalization: Diar Heidary, unaffiliated.** The upper
comparison displayed below, which is the whole of the conjecture stated in this
entry, is proved in Lean 4 and machine-checked. The proof source, its mechanical
verification and its transitive axiom report are recorded in
[Lean proof and verification evidence](#lean-proof-and-verification-evidence--2026-09-14)
below. The conjecture remains credited to Latała and Świątkowski, and the
reverse inequality quoted in this entry remains their Theorem 4.1 and is not
formalized. AI assistance is disclosed; no external human peer review is claimed.

**Rating rationale:** The missing upper estimate must account for localized random fluctuations across all variance profiles. Even weighted random signs retain an iterated-logarithm gap. A sharp estimate would improve quantitative understanding of the largest singular value in random matrix models.

## Statement

For a real random variable $`Z`$ and $`r>0`$, write
$`\|Z\|_{L_r}=(\mathbb E|Z|^r)^{1/r}`$. Fix $`\alpha\ge1`$. Let
$`X=(X_{ij})\in\mathbb R^{n\times n}`$ have independent mean-zero entries
with finite absolute moments of every order, satisfying

```math
\|X_{ij}\|_{L_{2r}}\le\alpha\|X_{ij}\|_{L_r}
\qquad(1\le i,j\le n,\ r\ge1).
```

Set $`[n]=\{1,\ldots,n\}`$ and

```math
M(X)=\max_i\left(\sum_j\mathbb E X_{ij}^2\right)^{1/2}
+\max_j\left(\sum_i\mathbb E X_{ij}^2\right)^{1/2},
```

```math
D(X)=\max_{1\le k\le n}\;
\min_{\substack{I\subseteq[n]\\|I|\le k}}
\sup_{\substack{s,t\in\mathbb R^n\\\|s\|_2,\|t\|_2\le1}}
\left\|\sum_{\substack{i\notin I\\j\notin I}}X_{ij}s_it_j
\right\|_{L_{\ln(k+1)}}.
```

**Conjecture (Latała–Świątkowski).** For every $`\alpha\ge1`$ there is a
constant $`C_\alpha>0`$ such that, for every $`n\ge1`$ and every such matrix,

```math
\mathbb E\|X\|_2\le C_\alpha\bigl(M(X)+D(X)\bigr),
```

where $`\|X\|_2`$ is the spectral norm. The constant is independent of the
dimension and entry laws. The same deterministic index set $`I`$ deletes both
rows and columns; the supremum is outside the random-variable moment.
The definition includes $`L_{\ln2}`$ when $`k=1`$, using the displayed moment
functional even though its exponent is below one.

The reverse inequality up to a constant depending only on $`\alpha`$ is
proved, so the target is equivalent to the source's two-sided comparison.
No identical-distribution or symmetry assumption is imposed on the entries.

## Lean proof and verification evidence — 2026-09-14

### Proof source, toolchain and pinned dependencies

The formalization is the Lean 4 project
[DiarHaidary/Spectral-norms-of-independent-entries-with-regular-moment-growth](https://github.com/DiarHaidary/Spectral-norms-of-independent-entries-with-regular-moment-growth)
at the immutable revision
[`762bd5ec5050a96f5e6ba3926b6cda4816fcd4b0`](https://github.com/DiarHaidary/Spectral-norms-of-independent-entries-with-regular-moment-growth/tree/762bd5ec5050a96f5e6ba3926b6cda4816fcd4b0). That exact commit is registered with
the Palomar registry as
[PALOMAR-2026-09-14-000006, version 1](https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-14-000006&version=1),
which also preserves an archival fork of it.

- Lean toolchain: `leanprover/lean4:v4.33.0`.
- `mathlib` pinned at `db584cd6d46c92f209a44c0f1c829460d327499d`; the remaining
  eight Lake dependencies are pinned to exact commits in the committed
  `lake-manifest.json`.
- `Challenge.lean` imports Mathlib only.

### Compared declaration and its correspondence to this entry

Comparator selects the single declaration `MI32.main_upper`, with
`definition_names` empty, so no part of the statement is a replaceable hole.
Its literal Lean text is in
[`Challenge.lean`](https://github.com/DiarHaidary/Spectral-norms-of-independent-entries-with-regular-moment-growth/blob/762bd5ec5050a96f5e6ba3926b6cda4816fcd4b0/Challenge.lean), the file a reader is
expected to audit. In the notation of this entry it asserts

```math
\forall\,\alpha\ge1\quad\exists\,C>0\quad\text{such that}\quad
\mathbb E\|X\|_2\le C\bigl(M(X)+D(X)\bigr)
```

for every $`n\ge1`$ and every admissible $`X`$. The correspondence between the
displayed quantities and the definitions in that file is:

- $`\|Z\|_{L_r}`$ is `moment`, defined as $`(\int|Z|^r)^{1/r}`$ with a *real*
  exponent. It is therefore the displayed functional also when $`r<1`$, so the
  order $`\ln2`$ at $`k=1`$ is kept literally and is not replaced by one.
- The hypotheses on $`X`$ are `RegularEntries`: entry measurability; joint
  independence of the family indexed by ordered pairs, as `iIndepFun`; each
  entry has Bochner integral zero; $`|X_{ij}|^p`$ is integrable for every real
  $`p>0`$; and $`\|X_{ij}\|_{L_{2r}}\le\alpha\|X_{ij}\|_{L_r}`$ for every real
  $`r\ge1`$. Neither identical distribution nor symmetry is assumed.
- $`\|X\|_2`$ is `spectralNorm`, the operator norm of the Euclidean linear map
  of the matrix.
- $`M(X)`$ is `varianceScale`, the supremum of the row standard deviations plus
  the supremum of the column standard deviations.
- The inner supremum over $`\|s\|_2,\|t\|_2\le1`$ after deleting $`I`$ is
  `weakMoment`: a real supremum, over deterministic test vectors, of the scalar
  moment of `deletedBilinear`. That bilinear form sums over `Finset.univ \ I` on
  both axes, so one and the same deterministic set deletes rows and columns, and
  the supremum sits outside the random-variable moment.
- $`D(X)`$ is `deletionScale`, the supremum over $`1\le k\le n`$ of the infimum,
  over index sets of cardinality at most $`k`$, of `weakMoment` at the order
  $`\ln(k+1)`$.
- The conjectured inequality is `UpperBoundAt`, quantified over every
  $`n\ge1`$, every type, every measurable space on it, every probability measure
  and every such $`X`$. The constant is bound before all of those, so it depends
  only on $`\alpha`$ and not on the dimension or the entry laws.

The probability space is an arbitrary type rather than a finite one, and no
estimate enters as a hypothesis or as a custom axiom. The constant is explicit:
`SymmetricDeletion.deletionConstant` evaluated at $`2\alpha`$, times $`e`$. It
is conservative and is not claimed to be sharp.

The hypothesis class is not vacuous. `MI32.RegularWitness.exists_regularEntries`
exhibits an independent fair-sign matrix satisfying the hypotheses at
$`\alpha=1`$ with $`M(X)=\sqrt n>0`$, so the displayed bound is a genuine
constraint rather than a statement about an empty class.

### Verification record

This catalog **reviewed a public verification record**; it did not rerun the
checks itself. Palomar's mechanical verification of the registered commit ran on
Palomar's own Linux infrastructure on 2026-09-14T14:07:31Z:

- [workflow run 34852526384](https://github.com/PalomarRegistry/PalomarSubmission/actions/runs/34852526384)
  in `PalomarRegistry/PalomarSubmission`;
- Comparator at `575674928e239f5bc452aab72d1dd7b0f1326494`, checking that the
  Solution declaration proves the Challenge statement in a separate environment;
- an independent NanoDa kernel replay at
  `68d5ca9db226849b41a6fff59d796ff19d0a8840`;
- `lean4export` at `15f6055e299ad5b89345e533cc2192f4cc00f659` and the `landrun`
  sandbox at `811cfff51ceaf3d9843708aa6d22e9b84ccac8b4`.

The registry entry records trust level `high`, and its AI editorial review
returned outcome `neutral`, meaning that no blocking problem was identified.

The author's own local checks are reproducible from the repository root with:

```
lake exe cache get
lake build
lake env lean Audit.lean
lake build Challenge Solution
lake env lean FullTargetAudit.lean
python3 scripts/verify.py
```

The last of these exits zero only when the whole gate passes, and writes a dated
record to `verification/status.json`. A successful build is not on its own
evidence of the result; the Comparator and kernel-replay run above is.

### Transitive axiom report

```
'MI32.main_upper' depends on axioms: [propext, Classical.choice, Quot.sound]
```

produced by `lake env lean FullTargetAudit.lean` and retained at
`verification/full-target-axioms.log`. The Comparator configuration permits only
those three axioms and the mechanical run enforced that. There is no `sorryAx`,
no custom axiom and no reliance on native execution. `Challenge.lean` retains a
deliberate `sorry`, which is the Challenge hole by construction and is never
imported by the proof.

### Scope, attribution and limits

- **Scope.** Only the upper comparison displayed in this entry is formalized.
  The reverse inequality, Theorem 4.1 of Latała–Świątkowski, is quoted in this
  entry for context and is not formalized or selected. No quantile or two-sided
  statement is claimed, and no claim is made about the sharpness of the
  constant's dependence on $`\alpha`$.
- **Mathematical attribution.** The conjecture is Conjecture 4.3 of
  Latała–Świątkowski. The proof argument and its formalization are by Diar
  Heidary. The manuscript is
  [MI32.pdf](https://github.com/DiarHaidary/Spectral-norms-of-independent-entries-with-regular-moment-growth/blob/bd00df8dca9c6128cf528591d3485f8ca9eecd88/docs/manuscript/MI32.pdf), with its
  [LaTeX source](https://github.com/DiarHaidary/Spectral-norms-of-independent-entries-with-regular-moment-growth/blob/bd00df8dca9c6128cf528591d3485f8ca9eecd88/docs/manuscript/MI32.tex); its
  formal-verification section tabulates, statement by statement, which Lean
  declaration carries each numbered result.
- **Deliberate divergences from the manuscript**, recorded in the project's
  `docs/SOURCE_FIDELITY.md`: the formal far-remainder estimate avoids the
  variance-envelope input of Latała–van Handel–Youssef by raising the screening
  threshold and using an elementary centered-Gram second moment, and the formal
  decomposition runs on the original rectangular matrix rather than on the
  matrix-symmetric dilation.
- **AI assistance is disclosed.** The proof, the Lean development and the
  exposition were produced with substantial AI-agent assistance under the
  author's direction. The statement-fidelity review and the registry's editorial
  review are AI reviews. Neither is human peer review and none is claimed.
  Registration with Palomar is not acceptance, endorsement or a novelty claim.

## Known cases and numerical significance

The source proves the Gaussian-mixture case under the same moment condition.
Weighted signs $`X_{ij}=a_{ij}\varepsilon_{ij}`$, with independent fair
$`\varepsilon_{ij}\in\{-1,1\}`$, satisfy the condition with $`\alpha=1`$ and
form the source's earlier Conjecture 1.2. Latała proves this case when
$`a_{ij}\in\{0,1\}`$ and proves the general weighted-sign estimate with an
additional factor of order $`\log\log\log n`$. Meller's 2026 result gives
an iterated-logarithm loss for a wider class of symmetric entries; it does
not remove that loss. These cases remain grouped in this entry.

The spectral norm is the largest singular value and measures the largest
Euclidean amplification by a random matrix. The formula combines row and
column variance scales with moments of bilinear forms after deleting a
limited number of coordinates, accounting for concentration on small parts
of a matrix that simpler variance-only bounds can miss.

## References and status check

- R. Latała and W. Świątkowski, *Norms of randomized circulant matrices*, Electronic Journal of Probability 27 (2022), paper 80, 1–23. [DOI](https://doi.org/10.1214/22-EJP799); [current arXiv v2](https://arxiv.org/pdf/2106.03139v2), dated 2022-05-27. Conjecture 4.3 on preprint p.25, with condition (25) on p.24, states the target. Theorem 4.1 supplies the lower bound; Proposition 4.4 and the paragraph before it cover Gaussian mixtures. Conjecture 1.2 on p.2 is the weighted-sign special case.
- R. Latała, *On the spectral norm of Rademacher matrices*. [DOI](https://doi.org/10.1090/tran/9637); [current arXiv v2](https://arxiv.org/html/2405.13656v2), dated 2025-08-18. Equations (1.2)–(1.3), Theorem 1.1, and Theorem 1.9 give the weighted-sign conjecture and the stated partial results. This paper uses the comparable truncated logarithm $`\max\{1,\ln k\}`$ in place of $`\ln(k+1)`$.
- R. Meller, *Spectral norm of matrices with independent entries up to polyloglog*, [arXiv:2512.23673v2](https://arxiv.org/html/2512.23673v2), dated 2026-01-29, introduction, equation (3), and Theorem 1.1. It explicitly identifies the remaining logarithmic gap and Conjecture 4.3.

On 2026-09-11, checked the original paper's current version, both later
papers, and exact-title, author/conjecture, Rademacher spectral-norm,
proof/counterexample and 2026 searches. No full resolution was found.
Gaussian operator-norm results and the general Bernoulli-process theorem
do not prove this displayed formula. This is a bounded literature check.
