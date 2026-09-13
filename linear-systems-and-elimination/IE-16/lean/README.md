# IE-16 complete Lean formalization

The complete finite counterexample passed actual non-root Linux Comparator,
permitted-axiom closure and default-kernel replay at
`697a2a1d88337a6747aa5c82fb6e554d3ff1b356` in [run 34774629327, job 103770408910](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34774629327/job/103770408910).
The [Linux evidence](verification/linux-2026-09-13/README.md) retains the raw
records. Both independent final referees approved the complete canonical proof;
[coordinator acceptance](reviews/FINAL-ACCEPTANCE.json) binds their exact reports.

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
approvals. Historical source reviews and compiled-development addenda retain
their exact original scopes. [Final canonical acceptance](reviews/FINAL-ACCEPTANCE.json)
records both independent final mathematical and Linux-evidence approvals.
The separate [operational record](verification/linux-2026-09-13/README.md)
identifies its source-implementer collector and the independent review records.

Lean 4.33.1, Mathlib and LeanCert remain pinned in [lake-manifest.json](lake-manifest.json).
[The canonical Comparator log](verification/linux-2026-09-13/operational-record/extracted/verify-20260913T182805Z-4150/comparator.log) reports exactly
`propext`, `Classical.choice` and `Quot.sound` for all fifteen exports and
contains the successful default-kernel replay and statement-match markers.
The actual sandbox, kernel and comparator control suites also passed,
including rejection of `sorryAx` and a native-decide axiom.

Solution remains the Lake default. Its definitions, proof bodies, import
paths and all other mathematical files are byte-identical to the verified
revision. Only this guide and `formalization.yaml` require archived input
correspondence in the publication metadata map. Run
`python3 verification/verify_publication.py` from this directory for an
offline package-integrity check; authoritative rerun commands require Linux
and are documented with the retained evidence.

Original mathematical resolution and exact certificate: Sidney Holden,
Center for Computational Biology, Flatiron Institute, Simons Foundation.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA, with
AI assistance. Agent reviews are not external human peer review or official
Tau Ceti endorsement.
