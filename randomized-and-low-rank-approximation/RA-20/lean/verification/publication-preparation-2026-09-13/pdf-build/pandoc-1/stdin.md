**Topic:** Symmetric structured low-rank approximation  




**Rating rationale:** Historical rating of the proposed all-order formulas. The negative resolution below is elementary; it does not establish corrected formulas in the remaining cases.

## Negative resolution - 2026-09-11

The displayed universal conjecture is false: **$`e_{3,3}=3`$, whereas its formula gives** $`4`$. For $`n=s=3`$, write the off-diagonal entries as $`(a,b,c)`$. The determinant is $`2abc`$, so the variety is the union of three coordinate planes. Each smooth component has exactly one simple critical point for generic full-Frobenius data. Their intersections are singular and are excluded by the definition below.

[Complete proof](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/solution.md) · [Proof PDF](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/solution.pdf) · [Standalone TeX](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/solution.tex) · [Independent audit and exact verification](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/references/research-expansion-2026-09-11/ra20-resolution/README.md).

This counterexample was identified and independently checked during the Codex maintainer audit. That dated audit was automated-agent review. The separate Lean verification below certifies the complete original negative target; external human peer review is not claimed. The source's Table 7 repeats the value $`4`$; this is not a transcription error in the entry. The complete original target, including its dimension range and all four formulas, is retained below. No conclusion about corrected formulas or the other parameter cases is claimed, and no priority claim is made.

## Lean proof and verification evidence - 2026-09-13

**Formalization:** George Stepaniants, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA, with AI-agent assistance. The **Codex automated maintainer audit** retains credit for the original negative resolution; Kubjas, Sodomaco and Tsigaridas retain credit for the conjecture.

The [proof at immutable revision 43603b17](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/43603b173beb294c2588d83f936a8a96246fd5f0/randomized-and-low-rank-approximation/RA-20/lean/Solution.lean) proves `NLA.RA20.not_criticalCountConjecture`: the full original four-formula conjecture is false, since the genuine generic count at $`n=s=3`$ is three, not its predicted four. The original complex field, symmetry, rank bound, zero-diagonal constraints, bilinear full-Frobenius metric and all quantifiers remain. The other formulas are not separately settled.

All twelve checked exports have namespace `NLA.RA20`:

- `hollow_variety_semantics`; `reduced_coordinate_ring`.
- `algebraic_smooth_locus`; `algebraic_tangent_space`.
- `full_frobenius_differential`; `hollow_distance_semantics`.
- `generic_critical_locus`; `component_hessians`.
- `generic_data_intersection`; `generic_count_three`.
- `generic_count_not_four`; `not_criticalCountConjecture`.

The definitions use the actual reduced coordinate ring modulo the **entire vanishing ideal**, its genuine algebraic smooth locus and whole-ideal tangent space, actual complex derivatives, and the cardinality of the full smooth critical-point subtype. Arbitrary nonempty generic opens are compared on the complete symmetric data space. Every bridge and every premise needed to refute the target is proved, with no new unproved literature assumption. The [proof map](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/PROOF_MAP.md), [exact contracts and metadata](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/formalization.yaml), and [detailed proof scope](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/README.md) identify the correspondence. Exact algebra eliminates interval computations; LeanCert audits kernel trust. The source comment describing a complete local ring denotes ordinary `Localization.AtPrime`, not an adic completion. Hessian nondegeneracy is proved; no separate scheme-theoretic multiplicity theorem is claimed.

Two independent statement reviews preceded implementation; two independent final mathematical reviews and independent packaging review passed. This catalog ran [Ubuntu workflow 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047) on 13 September 2026 and reviewed its original artifacts. The real Comparator matched all twelve exports without definition holes, and Lean's default kernel replayed the solution. All **61 LeanCert kernel assertions** passed; **57 source axiom reports, covering 45 distinct names**, contain only `propext`, `Classical.choice` and `Quot.sound`. Both real control suites passed as a non-root user, including invalid-proof, statement-mismatch, quotient and forbidden-axiom rejection. All 17 workflow jobs succeeded. The [independent operational report](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/reviews/linux-operational-referee-2026-09-13.md), [original successful log and artifacts](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/verification/linux-run-2026-09-13/runtime-verification.json), and [coordinator acceptance](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json) bind all 1,092 candidate inputs. Local macOS development checks are separate.

The checked toolchain is **Lean 4.33.1**. Dependency revisions are:

- Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`.
- LeanCert: `621a43d7cf21f87872392a01e874f2f1dbddc926`.

The [Lake manifest](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-20/lean/lake-manifest.json) pins all ten dependencies. The fresh proof build used 8,690 official matching Mathlib cache files, rather than rebuilding all dependencies from source. To reproduce from a clean checkout of revision `43603b173beb294c2588d83f936a8a96246fd5f0`, use a non-root Linux host with the [documented prerequisites](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/tools/lean/HARNESS.md) and run from the repository root:

```
tools/lean/bootstrap.sh /tmp/nla-ra20-check
tools/lean/selftest.sh /tmp/nla-ra20-check
tools/lean/verify.sh \
  randomized-and-low-rank-approximation/RA-20/lean \
  /tmp/nla-ra20-check
```

These commands run the actual controls, Comparator, permitted-axiom checks and default-kernel replay. A local `lake build Solution` is a separate development check; the historical default build target is Challenge. All original statement and source material below remains unchanged.

## Statement

For $`s\in\{1,2,3,4\}`$ and $`n\ge\max\{3,s\}`$, define

```math
W_{n,s}=\{X\in\mathbb C^{n\times n}:X^{\mathsf T}=X,
\ \mathop{\mathrm{rank}}\nolimits X\le2,\ x_{11}=\cdots=x_{ss}=0\}.
```

For generic symmetric $`U\in\mathbb C^{n\times n}`$, let $`e_{n,s}`$ be the number of complex critical points on the smooth locus of $`W_{n,s}`$ of

```math
d_U(X)=\sum_i(x_{ii}-u_{ii})^2+
2\sum_{i< j}(x_{ij}-u_{ij})^2.
```

Generic means outside a proper algebraic exceptional set. A point is critical if the differential vanishes on its tangent space. Thus $`e_{n,s}`$ is the Euclidean distance degree for the bilinear extension of the **full Frobenius metric**; the off-diagonal terms have weight two, and complex conjugation is absent.

**Conjecture (Kubjas–Sodomaco–Tsigaridas, Conjecture 5.6, $`n\ge3`$).**

```math
e_{n,s}=\begin{cases}
3(n-1)-2,&s=1,\\
9(n-2)-2,&s=2,\\
27(n-3)+4,&s=3,\\
81(n-4)+28,&s=4.
\end{cases}
```

All four zero counts form one target. The explicit $`n\ge3`$ restriction avoids a degenerate endpoint in the printed statement: when $`n=2`$, the rank bound is vacuous and both possible varieties are linear with ED degree one, whereas the displayed $`s=2`$ formula does not apply.

## Evidence and numerical significance

The source's Table 7 reports values matching its formulas through order ten, but the $`n=s=3`$ value conflicts with the exact calculation above. The table therefore cannot establish the conjecture's validity. The problem counts stationary candidates for symmetric Frobenius approximation with prescribed diagonal zeros. It concerns fixed rank two, unlike [corank-one approximation in general square matrices](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-19/README.md).

## References and status check

- K. Kubjas, L. Sodomaco and E. Tsigaridas, *Exact solutions in low-rank approximation with zeros*, Linear Algebra and its Applications 641 (2022), 67–97. [DOI](https://doi.org/10.1016/j.laa.2022.01.021); [current author manuscript](https://arxiv.org/abs/2010.15636v2), 29 January 2022. Conjecture 5.6 and Table 7, manuscript p.21; §2 and §5 supply the distance convention.

The initial literature search on 2026-09-11 found no later resolution and compared the formulas with Table 7. The subsequent independent maintainer audit supplied the counterexample above, superseding the initial Open classification. Excluding $`n=2`$ does not remove the admissible counterexample $`n=s=3`$. The separate nonsymmetric formulas in Conjecture 5.2 have a table/label discrepancy and are not imported here. The permanent ID, original target and canonical path are retained.