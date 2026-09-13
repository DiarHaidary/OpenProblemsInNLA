# Minimax draft API review (source-only)

This is a read-only review against the pinned Mathlib source. No Lean/Lake
command was run, and this file is not proof evidence.

## Verified API choices

- `Lagrange.eq_interpolate` takes `Set.InjOn`, then a strict `WithBot ℕ`
  degree bound. `natDegree_le_iff_degree_le` and
  `natDegree_lt_iff_degree_lt` are the appropriate bridges.
- `Lagrange.eval_interpolate_at_node`, `degree_interpolate_lt`, and
  `interpolate_apply` are present in `Mathlib.LinearAlgebra.Lagrange`.
- `Finset.sup'_eq_of_forall`, `Finset.le_sup'`, `norm_sum_le`, and
  `Finset.sum_pos'` are present at the pinned revision.
- `Complex.norm_real` is the namespace-qualified theorem exposed by
  `Mathlib.Analysis.Complex.Norm`; `Complex.sq_norm` is the square-norm
  identity used by the finite witness calculations.

## Items for the remote compiler pass

1. The draft's `rw [Lagrange.basis, Polynomial.eval_prod]` and subsequent
   `simp only` may need the unqualified aliases `eval_prod`, `eval_mul`,
   `eval_C`, `eval_sub`, and `eval_X`, depending on elaborator resolution.
2. `lagrangeAttainer_eval_zero` currently relies on `exact_mod_cast` to turn a
   real sum-of-ratios identity into a complex cast identity. If that does not
   elaborate, rewrite with `map_sum` for `Complex.ofReal` and use `norm_cast`
   before the final `field_simp`.
3. `Polynomial.eq_interpolate` should be checked with an explicit
   `(f := p)` argument if inference does not recover the polynomial from the
   degree hypothesis.
4. `Finset.sum_pos'` may require the explicit function argument or a
   `Finset.sum_pos` proof after unfolding `lagrangeSum`; this is an API shape
   issue only.
5. The final inverse inequality uses `mul_le_mul_right hA` rather than an
   inverse-order lemma, avoiding any unproved sign assumption on the objective.

The draft's mathematical route is unchanged: interpolation proves the
five-point `IsLeast` bridge, while the full nine-point minimum must use the
positive-weight orthogonality certificate.
