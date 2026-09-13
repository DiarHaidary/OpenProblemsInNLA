# SP-06 independent statement referee 1

**Phase:** pre-proof statement review, 13 September 2026  
**Reviewer:** OpenAI Codex independent AI referee `/root/lean_ie17_next`; I did not author the SP-06 candidate code.  
**Standard:** `docs/lean/REVIEW.md` at the pinned repository revision, applying its Tau Ceti-inspired fidelity, scope, API, attribution, and mechanical-evidence requirements.

## Verdict

**APPROVE — statement boundary only.** I found no material statement, quantifier,
dimension, source-fidelity, or hidden-bridge defect requiring a change before
proof implementation. This approval does not approve any proof: all twenty
Challenge bodies remain deliberate `sorry` placeholders, and SP-06 must remain
uncounted until proof, Linux kernel, axiom, and Comparator gates pass.

## Reviewed identities

Canonical source commit:

`50838e37dd793830e2cecd1055cfc7e0349490f1`

The complete README, problem source, solution manuscript, and solution TeX were
read from that commit with `git show` and independently hashed:

| source | SHA-256 |
|---|---|
| `eigenvalues-and-inverse-problems/SP-06/README.md` | `e2eb891930c96d6a3bdd25c75bfe6bd2798cc8c540ce00ec851f7bf1f0ceb25c` |
| `eigenvalues-and-inverse-problems/SP-06/problem.tex` | `183127180596a36c108ed8575420e3845ca890f3048a32ec1252d61cf60d5311` |
| `eigenvalues-and-inverse-problems/SP-06/solution.md` | `c7adb8f97238049b20e82044d8527b70301779ba041169f74fe603a88ea1ae7a` |
| `eigenvalues-and-inverse-problems/SP-06/solution.tex` | `b7340bf85e0b776ed49a4303af64820b72708eb249fbdc885b9179945e60ffc9` |

The candidate files reviewed were:

| candidate file | SHA-256 |
|---|---|
| `NLA/SP06/Definitions.lean` | `5f3e071b9aabbbda27a794f9396022e54585f5d2d254827e50ea90baf80e72b1` |
| `Challenge.lean` | `cd75a8f37a174d7dfb68927f7e6aeb23cf0982eb3161d7d9e5a63a7583d73bef` |
| `NUMERICAL_TARGETS.md` | `bfd2a0bcc5c5328ac9f3fd85d56ac7d3b8a5d551236cee68e227cb9acbea1959` |
| `SOURCE_MAP.md` | `b81a8cc5f9e5c1dda318c65c80ed840825a3216d95d53bcfc43cd8bbf7c594f2` |
| `formalization.yaml` | `6ff843982c3cdef97424ef86e48f2dd82f02876212730b0580f1c72f00c41b39` |
| `comparator.json` | `5d19e5fe9d3ac4a69d07a1b14d40e31784a295e7fe8c6925964bfffe97203bb9` |
| `README.md` | `834a2176794e9eaddec99b63dabc399019ef89e71a4fc9f89721cbcf6ad911a8` |

## Source and target fidelity

The original target quantifies over arbitrary finite complex Laurent polynomials
with positive integer bandwidths, nonzero extreme coefficients, an actual
Jordan curve in the punctured complex plane on which the symbol is real, and
every finite section size `n >= 1`. The candidate preserves all of these
quantifiers. Its `LaurentCoefficients := ℤ →₀ ℂ` gives finite support; the
admissible-band predicate enforces zero coefficients outside the signed band
and nonzero coefficients at both extremes. The `Fin n` index shift preserves
`i-j`, and `spectrum ℂ (toeplitz b n)` is the actual complex algebra spectrum.
The condition `z.im = 0` is exactly membership in the real axis for complex `z`.

The unit-circle domain is Mathlib's actual `Circle`, not a finite sample or an
angle interval. `hasRealJordanCurve` requires a continuous injective map from
that circle, nonzero image at every point, and reality of the actual Laurent
evaluation. The candidate's root construction does not assume a curve or its
continuity: `continuous_radius_exists` is an explicit Challenge obligation.
The source's stronger enclosure-of-zero assertion is omitted because it is not
part of the original problem target; the candidate explicitly documents this
scope choice. A single nonreal eigenvalue at one admissible finite size is
logically sufficient to negate the universal all-finite-spectra conclusion.

## Definition audit

I inspected every definition in `NLA/SP06/Definitions.lean`:
`LaurentCoefficients`, `laurentEval`, `hasAdmissibleBand`, `toeplitz`,
`hasRealJordanCurve`, `allFiniteSpectraReal`, `targetImplication`, `witness`,
`auxiliary`, `radialEquation`, `radiusProfile`, `radialCurve`,
`nonrealEigenvalue`, and `counterexampleClaim`. None hides the desired
conclusion or assumes existence/continuity of the curve. Negative integer powers
are used only through the actual Laurent evaluation, while the target curve is
required to avoid zero.

The 20 Challenge contracts were all checked by their elaborated types:

1. `witness_admissible` — exact band and signed-index support.
2. `witness_composition` — all seven Laurent coefficients agree with `a-a²` for nonzero `z`.
3. `radial_lower_endpoint` — exact lower endpoint bound.
4. `radial_upper_endpoint` — exact upper endpoint bound.
5. `radial_uniform_slope` — quantitative monotonic separation on the full box.
6. `radial_root_exists_unique` — one root in the open interval for every `c ∈ [-1,1]`.
7. `radial_roots_lipschitz` — root dependence bound with constant 8.
8. `continuous_radius_exists` — actual continuous radius on `Circle`.
9. `radial_curve_continuous` — continuity bridge.
10. `radial_curve_injective` — injectivity from positive radius and unit-circle directions.
11. `radial_curve_nonzero` — punctured-plane bridge.
12. `auxiliary_radial_im` — exact imaginary-part identity.
13. `radial_curve_symbol_real` — reality of the witness on the entire curve.
14. `witness_real_jordan_curve` — complete Jordan-curve premise.
15. `witness_toeplitz_two` — exact order-two section.
16. `witness_eigenvalue_mem` — genuine algebra-spectrum membership.
17. `witness_eigenvalue_im` — exact imaginary part 8.
18. `witness_nonreal_finite_spectrum` — negation of the all-finite conclusion.
19. `witness_counterexample` — complete witness conjunction.
20. `not_targetImplication` — explicit negation of the original universal implication.

The contracts expose every bridge from numerical data to the target. In
particular, they do not replace the entire-circle assertion by sampled points,
replace complex coefficients by real ones, use a circular curve as an assumed
premise, or assert a nonreal matrix entry instead of a nonreal eigenvalue.

## Independent exact checks

Without importing candidate code, I ran a standard-library Fraction check and
integer coefficient-dictionary multiplication. It independently reproduced:

- `a-a² = -64 z⁻² + 8 z⁻¹ - 128 - 8 z - 63 z² - 16 z³ - z⁴`;
- `F(1/2,1) = -23/32` and `F(2,-1) = 1`;
- the worst-case slope-bracket vertex values `9/16`, `15/16`, and `3/4`, all above `1/4`; and
- `T₂ = [[-128,8],[-8,-128]]`, trace `-256`, determinant `16448`, discriminant `-256`, and eigenvalues `-128 ± 8i`.

The positive slope follows by checking the concave worst-case bracket on the
triangle's vertices. It gives existence and uniqueness by the intermediate
value theorem and strict monotonicity. The same separation estimate and
`s³/4 <= 2` give the stated Lipschitz constant 8. Lipschitz dependence on the
real part of the actual Circle point supplies the continuous radius. Positive
radius plus the unit-circle coercion supplies injectivity and nonvanishing.
These are the required analytic bridges, not numerical sampling claims.

## Direct Lean evidence

I independently ran `verification/statement-typecheck.py` with the existing
pinned MI-22 dependency objects. It used direct Lean elaboration into a fresh
private temporary output directory, without Lake, downloads, or shared-cache
builds. Result: `PASS`, with exactly the expected twenty `sorry` warnings.

Evidence retained under this referee directory:

- `typecheck-EVIDENCE.json`, SHA-256 `d847787e57e02de6f9c25fefc7cbc9312cac2c0c022587696d4e763af8ac8515`;
- `types-axioms.log`, SHA-256 `c7279d1a8e108143b034d524b8b12958a04b39f5bd6acf9cf86920679219b8f8`;
- `defs-axioms.log`, SHA-256 `0992d0c9e91413b405b3a8e60e5b16561ba94c63ca6e1f3ae5895dd6d8c665fa`;
- `independent_checks.json`, SHA-256 `d2dd5ea42267130ac35168d129fe58a7833f601f50abaa4f8f85b9847bf34c90`.

The elaborated definition declarations depend only on `propext`,
`Classical.choice`, and `Quot.sound`. Each Challenge theorem additionally
shows `sorryAx`, as expected for this phase. The existing manifest pins
LeanCert at `621a43d7cf21f87872392a01e874f2f1dbddc926`, Mathlib at
`0df444a360eaa60ab8c11dca51a86af692955474`, and Lean 4.33.1; the typecheck
log records all ten clean dependency revisions.

## Limits

This is an independent pre-proof statement review, not external human peer
review, a proof correctness review, a LeanCert proof result, a Linux run, or a
Comparator acceptance. The twenty Challenge placeholders establish no
mathematics. The verdict is bound to the hashes above; any change to the
numerical boundary, definitions, contracts, or source pins requires renewed
review.
