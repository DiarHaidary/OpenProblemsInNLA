# IE-16 proof implementation handoff

This file records the source-only implementation plan while local Lean/Lake
execution is paused. It is not proof evidence and makes no solved or verified
claim.

## Frozen boundary

`NLA/IE16/Definitions.lean` and `Challenge.lean` remain byte-identical to the
approved files. Their SHA-256 values are respectively
`e4681f2083d71d8980adcd70e7cf26367e0e84dbc1773f4d2f082bf2417c9507` and
`85cbe24c7657d9ddc37728db5bb1740a80ddab60e3eb4676e329df40a7b1737c`.

The two permitted wording corrections in `NUMERICAL_TARGETS.md` are recorded
under `verification/num-targets-correction-20260913/`; no mathematical type,
constant, quantifier, or source snapshot was changed.

## Proof modules

`NLA/IE16/Numeric.lean` contains exact root-of-unity algebra, the injectivity
and nonzero checks for the nine points, witness feasibility/objective, and the
positive rational weighted moments. Its intended arithmetic is finite
`fin_cases` followed by `norm_num`/`ring`; it should be replayed in LeanCert
kernel mode after the resource pause is lifted.

The remaining module must establish the generic five-node complex Lagrange
lemma. For a nonempty `S : Finset ℂ` with `S.card = 5` and no zero node, put
`b z := (Lagrange.basis S id z).eval 0` and
`A := ∑ z in S, ‖b z‖`. `Lagrange.eq_interpolate` gives, for every feasible
degree-four polynomial,

```text
1 = ‖∑ z in S, p.eval z * b z‖ ≤ maxModulus S p * A.
```

The interpolant with node values
`(‖b z‖ / A : ℂ) * (b z)⁻¹` attains `1/A` at every node and has value one at
zero. This proves both membership and global lower bound in
`IsLeast (feasibleValues S 4) (1/A)`, hence the required `M` attainment after
`IsLeast.csInf_eq`. The full nine-point set instead uses the positive-weight
orthogonality certificate below; the five-node interpolation lemma is used
only for the subset minima.

For the full set, prove weighted orthogonality for powers 1 through 4 using
the exact weights in `Numeric.lean`. Expanding `p = p_* + q`, with `q.eval 0
= 0` and degree at most four, makes the weighted cross term vanish. The
weighted square identity gives the lower bound matching the witness objective.

For five-point subsets, classify cluster occupancies as `(2,2,1)`, `(3,1,1)`,
or `(3,2,0)`. The Lagrange basis norm is the product of four node moduli
divided by the four pairwise distances. In the first profile, four points
contribute one `sqrt 3 * epsilon` within-cluster factor and three cross-cluster
factors. In the other profiles, three points contribute two within factors and
two cross factors. The exact rational comparison at `epsilon = 1/1000` then
gives `M S 4 < 23/10000` for every subset. Finish the finite `sup'`, positivity,
ratio, certificate, and universal negation contracts from these lemmas.

## Required gates after implementation

1. Freeze the proof source after two independent proof reviews.
2. Replay every contract with the pinned LeanCert kernel configuration and
   no custom axioms beyond the Comparator allow-list.
3. Run the pinned Linux Comparator and inspect the public-source mapping.

Until those gates pass, this handoff must not be used to increment the Lean
verified count or mark IE-16 solved.
