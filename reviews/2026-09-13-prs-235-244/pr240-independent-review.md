# Independent audit of PR #240 (SP-06)

**PASS for mathematical fidelity, proof-source review and publication fidelity. No actionable blocker found in this scope.**

Reviewed head: `852c1683542180d25573bf0ea983fdcf3446c053`.
Published comparison base: `b73cd1804e40e0d101294eedb156984f0d62b4a6`.
Worktree: `/private/tmp/nla-audit-240`.
Audit date: 13 September 2026.

This review independently read the complete project-owned Solution import closure, every public contract and definition, the canonical statement and informal solution, the changed TeX and actual PDF, and live publication metadata. It did not run Lean/Lake or independently replay the default kernel; fresh CI and shared infrastructure checks belong to the coordinating reviewer. Supplied PASS reports were not used as substitutes for examining the mathematics.

## Original target and external correspondence

The original target is retained: every finite complex Laurent polynomial with positive lower/upper bandwidths and nonzero extremes, a continuous injective image of the unit circle avoiding zero on which the symbol is real, and real spectrum for every positive Toeplitz section. `Fin n` indexing preserves the original difference `i-j`. `ℤ →₀ ℂ` faithfully represents arbitrary finite complex coefficients; it does not narrow them to the rational witness.

The primary [Shapiro–Štampach v4 source](https://arxiv.org/pdf/1702.00741v4), equation (2), Theorem 1 and its appended erratum (printed pp. 27–28), confirms that the disputed implication is the Jordan-curve condition to all finite spectra being real. The correction explicitly distinguishes its weaker limiting-spectrum alternative. The counterexample therefore targets the intended question. No claim that the limiting-spectrum implication is refuted is introduced.

I retrieved and read the pinned Mathlib [Circle definition](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/Complex/Circle.lean) (definition at line 52, norm and inverse facts at lines 72–83) and [matrix spectrum/characteristic-root equivalence](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/LinearAlgebra/Matrix/Charpoly/Eigs.lean) (line 80). These are the actual complex unit sphere with its usual topology and algebra spectrum, not surrogate project definitions.

## Complete contract coverage and proof reasoning

All twenty Challenge contracts have identical source-level statement text after whitespace normalization in the Solution environment; the automated comparison supplements the manual definition and quantifier review. The public contracts are:

1. `witness_admissible`: the seven explicit coefficients have support in `[-2,4]`, with nonzero product of extreme coefficients.
2. `witness_composition`: for every nonzero complex z, finite Laurent evaluation equals `a(z)-a(z)^2`, with `a(z)=8/z+8z+z^2`.
3. `radial_lower_endpoint`: `F(1/2,c)=-3/4+c/32 ≤ -23/32 < 0` for every `c∈[-1,1]`.
4. `radial_upper_endpoint`: `F(2,c)=3+2c ≥ 1` over that entire interval.
5. `radial_uniform_slope`: the difference factors as `(r-s)[r+s+c(r²+rs+s²)/4]`. On `1/2≤s≤r≤2`, the bracket is at least 1/4: `r²≤2r`, `s²≤2s`, `rs≤r+s`, and `c≥-1` yield the stated bound. The proof uses nonnegative multiplication, not sampling.
6. `radial_root_exists_unique`: continuity and the intermediate value theorem give a root; strict endpoint signs place it in the open interval; the uniform separation proves uniqueness.
7. `radial_roots_lipschitz`: comparing equations at two parameters yields `|r-s|≤8|c-d|`, since the slope lower bound is 1/4 and `s³/4≤2`. Both possible root orderings are covered.
8. `continuous_radius_exists`: choice selects roots on every Circle point; the preceding Lipschitz estimate and the 1-Lipschitz real-coordinate map prove continuity of the selected radius. Continuity is proved, not assumed.
9. `radial_curve_continuous`: the product of the continuous radius embedding and circle inclusion is continuous.
10. `radial_curve_injective`: taking norms in `ρ(u)u=ρ(v)v` gives equality of positive radii, then cancellation gives equality of the circle points.
11. `radial_curve_nonzero`: the positive radius and nonzero circle point give a nonzero product.
12. `auxiliary_radial_im`: the unit-circle inverse/conjugate identity gives the exact imaginary-part formula `(8 Im(u)/r)F(r,Re(u))` for all positive r.
13. `radial_curve_symbol_real`: the profile root equation makes that imaginary part zero; real polynomial composition preserves reality.
14. `witness_real_jordan_curve`: explicitly assembles the continuous, injective, nonzero, everywhere-real witness map.
15. `witness_toeplitz_two`: checks every entry of `[[-128,8],[-8,-128]]` against the canonical indexing convention.
16. `witness_eigenvalue_mem`: computes the actual characteristic determinant and uses Mathlib's equivalence to put `-128+8i` in the actual complex spectrum.
17. `witness_eigenvalue_im`: its imaginary part is exactly 8.
18. `witness_nonreal_finite_spectrum`: instantiates the positive-size universal spectrum claim at n=2 and derives `8=0`.
19. `witness_counterexample`: assembles admissibility, genuine real Jordan curve and failure of universal finite-spectrum reality.
20. `not_targetImplication`: substitutes this witness into the complete original universal implication and contradicts item 18.

An independent Fraction-based Laurent-polynomial expansion confirms all seven coefficients; an independently implemented permutation determinant yields `λ²+256λ+16448=(λ+128)²+64`. The exact arithmetic does not substitute for the whole-curve proof.

The formalization does not separately claim both eigenvalues or topological enclosure of zero. These are stronger details of the informal manuscript, unnecessary for the canonical negative target, and their omission is explicitly disclosed in SOURCE_MAP.md and formalization.yaml.

## Proof boundary and source integrity

The complete project-owned closure is `Solution → NLA.SP06.Proof → NLA.SP06.Curve → NLA.SP06.Numeric → NLA.SP06.Definitions`, plus pinned Mathlib and LeanCert imports. I read all five files completely. No Challenge import, proof hole, custom axiom, native_decide, unsafe declaration, implementation replacement, custom elaborator or external evaluation is present in those files. The twenty intentional Challenge placeholders remain isolated in a separate module. Kernel trust assertions cover every public contract and the transparent target definitions. Runtime transitive axiom acceptance remains a separate CI obligation.

Independent hash checks reproduce all four historical source-map SHA-256/Git-blob pairs at source commit `50838e37dd793830e2cecd1055cfc7e0349490f1`; all five statement-freeze and thirteen final-freeze boundary hashes match the live package. The original mathematical target and informal manuscript have not been replaced.

## Current publication versus historical evidence

Canonical README, TeX and PDF consistently state Lean verified, give separate George Stepaniants/Caltech formalization and Matthew J. Colbrook/Cambridge mathematical credits, identify the immutable proof revision, and explain the distinction between the dated informal agent review and subsequent formal verification. AI involvement and the absence of claimed human peer review remain clear.

NUMERICAL_TARGETS.md is expressly a statement-stage draft, and FINAL-ACCEPTANCE.json is a dated local-review snapshot whose pending Linux language describes that earlier stage. These bytes are hash-bound historical evidence. Current README/YAML separately state the completed Linux stage and retain its provenance. I found no misleading current pending-status claim requiring those immutable records to be edited. Candidate metadata is explicitly archived through candidate-metadata-map.json.

I freshly rasterized the checked-in canonical PDF bytes and visually inspected all three pages of the actual changed `eigenvalues-and-inverse-problems/SP-06/problem.pdf`. The displayed theorem, references, attributions, historical headings and verification scope agree with the TeX/Markdown; there are no clipped formulas, unreadable glyphs or overlapping content. The title metadata and permanent SP-06 label are correct. The layout uses considerable whitespace on page two, which is cosmetic, not a blocker.

## Reproducible evidence and limit

`/private/tmp/nla-pr-240-241-independent-checks.py` and its JSON result record exact head identities, project proof-closure hashes, all twenty statement comparisons, frozen/source hashes, and independent exact arithmetic. The actual PDF images were generated in `/private/tmp/nla-audit-pdfs/` solely for read-only inspection. No PDF was rebuilt from TeX. No repository source or historical evidence was edited. Final operational acceptance depends on the coordinator's exact-head CI, input correspondence, registry/catalog and shared-harness audit.
