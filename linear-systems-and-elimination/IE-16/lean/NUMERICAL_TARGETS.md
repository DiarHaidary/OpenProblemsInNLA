# IE-16 statement boundary and numerical obligations

Status: **statement stage**. `Definitions.lean` is proof-independent;
`Challenge.lean` contains the deliberate placeholders. No proof module or
solution is present. Implementation must wait for two independent statement
reviews.

The original negative resolution and analytic manuscript are by **Sidney
Holden**. This Lean formalization is by **George Stepaniants**, Department of
Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA. No email address is included.

## Frozen sources

The canonical problem is
`linear-systems-and-elimination/IE-16/README.md` at upstream revision
`b73cd1804e40e0d101294eedb156984f0d62b4a6`. The complete source is
`references/holden-ie16-2026-09-12/submitted/source/solution.tex` at the same
revision. The exact certificate source and JSON are retained in
`verification/source-snapshot/`; `SOURCE_HASHES.json` binds every copied input
to its upstream SHA-256 content hash.

The formalization uses only the finite nine-point counterexample in Theorem
`finite` of the manuscript. The stronger three-cluster amplification theorem
and all asymptotic claims are outside scope because the finite witness alone
refutes the complete universal assertion.

## Exact mathematical definitions

* `Poly` is `Polynomial ℂ`, so coefficients and evaluations are genuinely
  complex. `feasible L k p` means `p.natDegree ≤ k` and `p.eval 0 = 1`.
* `maxModulus L p` is the maximum of the actual complex norms
  `‖p.eval z‖` over the finite set `L`; its empty-set branch is only a total
  definition and is never used by the admissible target.
* `M L k` is the infimum over all feasible complex polynomials of that actual
  finite maximum. No candidate polynomial is substituted for the infimum.
* `subsetFamily L k` is exactly the powerset members of cardinality `k+1`.
  `subsetMax L k` is the corresponding finite maximum of `M S k`.
* `admissible L n` records `L.card = n` and exclusion of zero. Finset
  distinctness supplies the original distinct-point condition.
* `IE16Conjecture` retains every original quantifier: all `n ≥ 3`, all finite
  sets of `n` distinct nonzero complex points, and every `1 ≤ k ≤ n−2`, with
  the candidate factor `4 / π`.

## Exact finite witness

Set

```text
omega = -1/2 + (sqrt 3 / 2) * I
epsilon = 1/1000
L = { omega^a + epsilon * omega^b : a,b in {0,1,2} }
k = 4
```

The definitions use the actual `Real.sqrt 3`, complex coercions, and an
image of `Finset.univ : Finset (Fin 3 × Fin 3)`. The following are the
statement obligations, not assumptions hidden in a proof:

1. `explicitL.card = 9` and `admissible explicitL 9` (distinct and nonzero).
2. The exact polynomial
   `1 - ((1+epsilon)/D) * z^3`, where
   `D = 1 + epsilon + 3 epsilon^2 + epsilon^3 + epsilon^4`, is feasible and
   has maximum modulus `3003003000 / 1001003001001`.
3. The actual minimax value satisfies
   `M explicitL 4 = 3003003000 / 1001003001001 > 299/100000`, and its
   infimum is attained:
   `IsLeast (feasibleValues explicitL 4) (M explicitL 4)`.
4. Every `S ∈ subsetFamily explicitL 4` satisfies
   `M S 4 < 23/10000` and
   `IsLeast (feasibleValues S 4) (M S 4)`. Consequently
   `subsetMax explicitL 4 < 23/10000` and
   `0 < subsetMax explicitL 4`.
5. The resulting ratio is greater than `13/10`, and `4/π < 13/10`.
6. These facts imply `¬ IE16Conjecture` by instantiating the original
   universal assertion at `n=9`, `L=explicitL`, and `k=4`.

The intended proof of item 4 uses the three genuine occupancy profiles
`(2,2,1)`, `(3,1,1)`, and `(3,2,0)` and the Lagrange interpolation bound; it
does not silently replace the maximum over subsets by the supplied Python
enumeration. The intended proof of item 3 uses the threefold symmetry
reduction and the explicit quadratic minimization in the source. The exact
certificate is supplementary evidence and is not imported as an axiom.

## Public Challenge exports

`Challenge.lean` declares fifteen intentional placeholders:

* `explicitL_card`, `explicitL_admissible`, and `witness_feasible`;
* `witness_objective`, `full_minimum_exact`, `full_minimum_isLeast`, and
  `full_lower_bound`;
* `every_five_point_subset_upper`,
  `every_five_point_subset_minimum_isLeast`, `subset_max_upper`, and
  `subset_max_positive`;
* `ratio_lower_bound` and `ratio_exceeds_candidate`;
* `counterexample`, bundling the complete finite certificate;
* `not_IE16Conjecture`, the unconditional negation of the full original
  universal target.

The later `Solution.lean` must reproduce these declarations from completed
proof modules without importing `Challenge.lean`. No statement may be
weakened to a fixed polynomial, a single subset, a floating-point claim, or
the nine-point certificate without the final universal negation.

## Verification plan

The statement build is direct Lean elaboration using the pinned toolchain and
the existing pinned Mathlib/LeanCert artifacts. It must not download or build
dependencies. The final proof will use exact algebra over `ℂ`, finite sums and
finite maxima, with any numerical scalar comparison certified in LeanCert
kernel mode. It must contain no unproved custom axioms, `native_decide`, or
native execution trust. Two independent statement referees must approve the
actual definitions, all fifteen Challenge types, and this numerical boundary
before proof implementation begins.
