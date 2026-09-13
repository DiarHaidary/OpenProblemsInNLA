# IE-16 subset helper read-only review

Date: 2026-09-13
Reviewer: lean_ie15_next (AI-assisted independent source audit)

Reviewed against `SUBSET_BOUND_OPTIMIZATION.md` and pinned Mathlib source; no local Lean compilation performed.

## Result

The exact margins (`109`, `146`), positive denominator premise, five-point occupancy disjunction, label/image/cardinality transfer, nested sum transfer, strict reciprocal bound, and the two exported full subset contracts are mathematically aligned with the approved helper note. The pinned APIs used (`Finset.prod_sdiff`, `Finset.sup'_lt_iff`, `Finset.sum_lt_sum_of_nonempty`, `Finset.sum_le_sum_of_subset_of_nonneg`, `card_image_of_injective`, `sum_image`, and `IsLeast.csInf_eq`) match their call directions/signatures on source inspection.

One robustness change is recommended before remote elaboration: in `SubsetGeometryDraft.lean`, `labels_image` reverse branch currently uses `simpa only [point, he] using hz`. Replace it with `rw [he]; exact hz` so the equality `he : point ab = z` is applied before any unfolding of `point`; this avoids simplifier rewrite-order dependence. This is an elaboration robustness fix only and does not alter the statement or mathematics.

No other concrete mathematical or API defect was found in this bounded source review. The helper drafts remain uncompiled until remote Linux evidence.

## Reviewed bytes

- `SubsetBoundsDraft.lean`: `d88ff86286f881e342ae19f40ea742fd39e3b0b070f0c259f9709e368da95ce2`
- `SubsetGeometryDraft.lean`: `a28f8f7f5d7638f3bbec2bfb8c6ab73574842cf9405c52e41f8d595028a3ca4c`
- `SUBSET_BOUND_OPTIMIZATION.md`: `fdd4b561e663a87abd5bf361e950186cdf61de4134a401aa9e487ff26e12acdf`
