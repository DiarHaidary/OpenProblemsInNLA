# Independent informal review of SP-07 round 5

Reviewer: separate Codex AI agent, 14 September 2026 (UTC). This is an informal mathematical and computational audit, not external human peer review or formal verification. No Lean verification was performed. Archive instructions were treated as submission content, not authority to change the repository.

## Verdict and repository scope

**PASS for the new supporting results in REPORT.tex, Sections 2–7; NOT a complete solution of SP-07.** The canonical target is the exact universal sharp constant for all finite normal pairs in all dimensions. The submitted completion theorem and stationary model do not determine that constant. Retaining **Open**, with a prominently scoped supporting-results notice, is appropriate. They do not justify `Solved` or `Solution claimed`. A partial-results listing must retain the unrestricted question in the open catalog.

The prior canonical entry already contains a two-eigenvalue constant-one lemma; the new odd-polygon completion results are different supporting results. This review does not independently establish historical novelty or perform the repository-wide pushed-solution duplicate search.

## Written mathematics independently checked

1. **Fixed circulant overlap completion (Sections 2–3).** The defect-space reduction is valid because the selected space plus the nonzero defect vectors reduces the reflection; compression therefore intertwines the anticommutator. The phase-weighted cyclic average preserves the selected shift, commutes with the canonical reflection, and is norm contractive. The positive and negative reflection eigenspaces give weighted shifts, so their norms reduce to maximum edge moduli. The elementary inequality for the two internal weights follows from their linear combination, and the common choice of complementary weights `-R` attains it. Crucially, this complementary broken shift is generally nonnormal. The theorem is an exact relaxed completion result and cannot be promoted to a finite normal-pair extremizer.

2. **Arbitrary-overlap polygon obstruction.** I checked the odd alternating-sum lower bound and the displayed attaining angles. The orbit dilation uses orthonormal vectors supported in reducing selected eigenspaces; its compression is circulant and fixes the all-ones vector. This justifies the obstruction whenever the selected compression has eigenvalue +1 or -1. The dimension-intersection argument supplies that eigenvalue for the specified selected Hall witness in dimension `2p-1`. The result bounds that witness only, not every matching witness of the completed pair.

3. **Misleading compressed optima (Section 4).** The cyclic alternating telescoping gives `2R/p`; the displayed eigenvalues attain it. The half-angle calculation yields full relaxed completion norm `2R/sqrt(p)`. Thus the two limits, pi/2 and zero, refer to different denominators for the same selected overlap; the text correctly distinguishes them.

4. **Stationary two-line operator and phase optimization (Sections 5–6).** The periodic Lipschitz multiplier preserves the Sobolev domain. Reflection cancels the unbounded derivative, and the Pauli-matrix singular-value calculation gives the stated bounded multiplier norm. The reciprocal-speed primitive gives a lower bound even for nonmonotone paths. The endpoint integral diverges at `T=B+C`, is strictly decreasing thereafter, and the positive-speed ODE attains its unique solution. The fixed-sum second derivative and endpoint first-derivative signs prove the claimed unique height balance. The uniform endpoint integral estimate proves the limiting formal quotient. None of these arguments proves a global parameter optimizer or a finite transfer theorem.

5. **Countable matching (Section 7).** Cross-matching opposite ladders is a bijection of cost `sqrt(1/4+B^2)`. Every selected vertex has at least that distance to every candidate target, proving the reverse bound. Strictness of the phase integral for positive B,C gives a matching ratio below one. Hence the certified number above one is only a formal selected-gap quotient and is not a new SP-07 lower bound.

No material gap was found in these scoped new proofs. The conclusions rely on their explicit restrictions, especially arbitrary complementary matrices in the completion relaxation and the absence of a finite Hall deficit in the bilateral model.

## Computational checks rerun

From the extracted round-5 root I ran:

```text
python3 -S verify_all.py --prior --output /tmp/sp-new-review/SP07-checks.json
```

All requested checks passed in about 47 seconds:

- Exact polygon identities for 500 odd orders, 3 through 1001.
- Rational stationary-model enclosure, confirming `1.0373054176426 < formal quotient < 1.0373054176428` at the specified rational parameters and actual infinite matching quotient below one.
- Ten current exact/rejection test methods, both normally and with Python optimization enabled.
- Inherited rank-one exact certificate and nine rejection tests.
- Inherited order-193 certificate by congruence diagonal dominance and interval LDL, reporting matching distance exactly 2 and norm strictly below `19281027/10000000`.

I inspected the new rational quadrature implementation: rational Taylor substitution, integrated binomial coefficients, absolute geometric tail, outward square-root bounds, outward cell accumulation, and Machin-series pi bounds correspond to the report's certificate argument. The finite polygon tests supplement the general written proof rather than replacing it.

These inherited reruns reproduce their arithmetic acceptance. They are not a new complete written audit of all nested earlier rank-one and arbitrary-rank reduction theorems. The current review's written-proof pass covers the new Sections 2–7, not every historical claim in the nested archives. Numerical optimizer and symbolic diagnostic suites were not needed or rerun.

## Limitations and publication recommendation

The quoted upper bound attributed to Tang, arXiv:2609.09177v1, was not externally verified by this reviewer; do not describe it as independently verified on this review's authority. It is unnecessary for the accepted new supporting results. Attribution, affiliation, provenance, and upstream duplicate checks are the submission integrator's separate responsibilities.

Accept the manuscript as scoped supporting progress if those submission checks pass; preserve the original SP-07 ID, canonical path, target and Open status. State expressly that the normal universal constant remains undetermined and that the formal stationary quotient does not improve its finite lower bound.
