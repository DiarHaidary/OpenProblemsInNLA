# IE-16 Lean proof candidate

All ten project modules and all fifteen public exports pass bounded Linux
development compilation and LeanCert kernel-trust assertions at revision
`281fc3790412b7ab2b05c202c0351b4d259a6382`, in
[run 34773404263](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34773404263).
Canonical Comparator, separate default-kernel replay and final compiled-source
acceptance remain pending. This candidate does not change the canonical
problem’s verified status or permanent ID.

The target is the original inequality
`M_k(L) ≤ (4/π) max_{S ⊆ L, |S|=k+1} M_k(S)` for every `n ≥ 3`,
every set of `n` distinct nonzero complex points, and every `1 ≤ k ≤ n−2`.
`M` ranges over arbitrary complex polynomials of degree at most `k` normalized
by `p(0)=1`, using the actual maximum of complex norms. Explicit `IsLeast`
contracts require attained minima on the full witness and every relevant subset.

Read [NUMERICAL_TARGETS.md](NUMERICAL_TARGETS.md),
[Definitions.lean](NLA/IE16/Definitions.lean) and [Challenge.lean](Challenge.lean)
for the approved fifteen-contract boundary. [Solution.lean](Solution.lean)
exports those fifteen names through the proof modules. Challenge’s deliberate
placeholders remain isolated from Solution. The successful development run
elaborated the complete proof source without proof placeholders.

The exact witness is `L={ω^a+εω^b : a,b∈Fin 3}`, with `ε=1/1000` and
`ω=−1/2+(√3/2)i`, at `k=4`. Holden’s Section 6 positive weights and four
vanishing complex moments give a weighted norm-square identity against every
feasible polynomial. The witness attains the resulting full minimum
`3003003000/1001003001001 > 299/100000`. The
[numeric optimization](NUMERIC_OPTIMIZATION.md) uses exact rational root
coordinates and symbolic powers of `√3` through degree seven.

For arbitrary five nonzero complex nodes, the generic Lagrange argument
constructs an attainer and proves that the minimum is the reciprocal of the
sum of the absolute Lagrange coefficients at zero. Injective labels preserve
every five-point subset. The [occupancy/product bounds](SUBSET_BOUND_OPTIMIZATION.md)
give either four coefficients above 109 or three above 146, covering all 126
subsets. Their minima are below `23/10000`. A positive actual subset maximum
then yields `M_4(L)/subsetMax(L,4)>13/10>4/π` and the full universal negation.
The stronger amplification theorem and operator-level GMRES construction are
outside scope.

[Statement acceptance](reviews/STATEMENT-ACCEPTANCE.json) binds both pre-proof
approvals. The [first](reviews/proof-source-referee-1/REVIEW.md) and
[second](reviews/proof-source-referee-2/REVIEW.md) independent AI mathematical
source reviews cover `28bdf9e85541764b6a5cb2debd647b9cebaea21f`, which failed
Numeric/Minimax elaboration. Both require addenda on the exact final compiled
source. [PACKAGING-PROVENANCE.json](PACKAGING-PROVENANCE.json) records source,
boundary and report hashes. The earlier reviewed numerical targets are
preserved with their two documented wording corrections.

Lean 4.33.1, Mathlib and LeanCert are pinned in
[lake-manifest.json](lake-manifest.json). The
[actual development log](verification/development-run-34773404263/extracted/compile-Solution.stdout)
reports exactly `propext`, `Classical.choice` and `Quot.sound` for each export.
[DEVELOPMENT-EVIDENCE-CHECKS.json](DEVELOPMENT-EVIDENCE-CHECKS.json) records
independent checks of all 60 input copies, ten dependency pins and raw module
results. The development run compiled Solution explicitly. The canonical package now
selects Solution as the Lake default. The
[presentation transition](verification/candidate-presentation-transition/TRANSITION.json)
records its path, leading-comment and default-target changes; all mathematical
body bytes and the approved Definitions/Challenge remain unchanged. Final
canonical verification must still complete the separate default-kernel replay
and Comparator and retain both final review addenda.

Original mathematical resolution and exact certificate: Sidney Holden.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA, with
AI assistance. Documentation preparation by the second independent AI source
referee does not constitute mathematical proof authorship.
