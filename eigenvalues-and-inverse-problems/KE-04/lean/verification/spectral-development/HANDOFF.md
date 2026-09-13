# KE-04 Spectral helper handoff

Completed source: `NLA/KE04/Spectral.lean`, SHA-256
`64e8255697387e32e65cf591a0cb7dbf7986f471c82b4f1715c9a88a7650e20e`.
Imports only Definitions from the project; no Frames or Krylov dependency.

Exact frozen exports in `NLA.KE04._proved`:

- `orderedSpectrum_semantics`: monotone ordered eigenvalues, matching basis action,
  actual characteristic-root multiset equality and valid natural-index lookup.
- `quadratic_semantics`: monic degree two, actual polynomial matrix evaluation and
  `M^2 - (a+b) • M + (a*b) • 1` expansion.
- `spectral_gap_quadratic_psd`: actual PSD from the exact all-eigenvalue gap premise,
  for `a ≤ b`, including `a=b` and repeated eigenvalues.
- `psd_zero_form_iff_kernel`: `form M x = 0 ↔ act M x = 0` for actual PSD `M`.

Additional reusable interface:

```lean
quadratic_apply_eigenvector {m : ℕ} (M : Mat m) (a b mu : ℝ) (v : Vec m)
    (hv : act M v = mu • v) :
    act (quadraticMatrix M a b) v = ((mu - a) * (mu - b)) • v
```

Final fresh run `attempt-k2z1xc0b` passed Definitions/Spectral/Inspect with zero
warnings. Four exact types, a 22-declaration actual project closure, 25 required
dependencies and ten material kernel trust checks passed. All 1598 frozen inputs,
the historical 110-file checkpoint and all four attempts remain preserved.

Read the [author completion report](../../reviews/spectral-development.md),
`HANDOFF.json`, `audit-result.json`, and the actual final attempt logs.
From the project root, verify the bounded evidence without executing Lean:

```
python3 verification/spectral-development/verify_seal.py
```

This is scoped author completion, not independent final mathematical approval or
Linux/Comparator execution. The contributor is ineligible as an independent final
KE-04 mathematical referee.
