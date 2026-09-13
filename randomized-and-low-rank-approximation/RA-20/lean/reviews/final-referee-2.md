# RA-20 independent final mathematical referee 2

**Verdict: APPROVE the complete frozen mathematical formalization.** I found no
mathematical or statement-fidelity defect requiring a proof change. This is one
independent AI-agent final review, not an authoritative Linux verification run
or approval to promote the catalog status by itself.

Reviewer: `/root/ra20_final_referee2`, 13 September 2026. I am a fresh referee and
contributed neither RA-20's statements nor its proof. I did not consult the other
final referee's report. My only writes are this report and its adjacent evidence
directory. Earlier statement reviews and author validation were inspected as
historical evidence; their verdicts did not replace my source and proof review.

## Frozen scope and original target

The reviewed proof freeze is
`verification/proof-freeze.json`, SHA-256
`f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f`.
I independently rehashed all **521 frozen project files**, including all nested
manifests, and all **16 original source/policy files**. Original Git blob
identities agree with base `5830ed4fb06da0659414a3deb2a40ad327aca052`.
I also independently validated every entry of the **13 nested statement,
development and coordinator manifests**, including retained earlier attempts.
None of those historical bytes changed during this review.

Important reviewed identities:

| File | SHA-256 |
| --- | --- |
| `NLA/RA20/Definitions.lean` | `a649164ee7f11e88d8bfae4167ee0d9b9252a8683f253ab5a69981cde0e7cf94` |
| `Challenge.lean` | `eb62545ea3e527c186b832a186fbaefa560409bf23be74486b9b00f04e00a2e9` |
| `NLA/RA20/Smooth.lean` | `99ab24934f75382e9bad4a8e84945d0f1e14123804d5172a66b0da17a9eceb88` |
| `NLA/RA20/Count.lean` | `99e44e2ec0d376cb346822c8f5a7edcc72c78448083361e5b4f2ea3aceb92c96` |
| `NLA/RA20/Proof.lean` | `d3cb0dab572eb54795e6568c717e9e6f8200eb20f299e319fc3be36bbe8aaea1` |
| `Solution.lean` | `755a58cc081172804c644ea83518581235763a6ecefcbff6c92f131ca44c32b5` |

I read the complete canonical problem, complete Markdown and TeX resolution,
retained independent informal reconstruction and exact results, all mathematical
source files, all twelve Challenge and Solution declarations, numerical targets,
source correspondence, proof map, and repository contribution/review policy.
I directly opened the primary [author manuscript](https://arxiv.org/pdf/2010.15636v2):
Sections 2.2–2.3 specify the complex bilinear distance convention; Conjecture 5.6
and Table 7 on printed page 21 contain the four formulas and the value four for
the three-by-three hollow symmetric case. This was a targeted source check,
not a literature or priority search.

The canonical target is the joint assertion for every `n ≥ 3` and
`1 ≤ s ≤ min(4,n)`. `criticalCountConjecture` preserves that entire range and all
four formulas. Natural-number subtraction has the intended values throughout
this range. The allowed instance `n=s=3` predicts four. Refuting that instance
negates the original conjunction; it does not prove or refute the remaining
individual parameter formulas or provide corrected sequences.

## Independent mathematical audit

1. **Actual matrix variety and reduced coordinate ring.** `variety` uses complex
   `Matrix.IsSymm`, actual matrix rank at most two, and exactly the first `s`
   diagonal constraints. No Hermitian or real-only substitution occurs.
   `definingIdeal` is the vanishing ideal of this point set in all matrix
   coordinates, and the quotient is the reduced coordinate ring. In
   `Algebra.lean`, the determinant is computed as `2abc`; the zero-product
   cases have explicit width-two factorizations. The reverse direction uses
   actual full rank from nonzero determinant. Every member of the original
   variety has the stated hollow form. Distinct polynomial variables are prime
   and relatively prime, so `abc` is squarefree and its ideal radical. The
   actual Nullstellensatz, the proved matrix-point correspondence, and a
   surjective hollow substitution identify the full original ideal as the
   pullback of `(abc)`. The resulting algebra equivalence preserves every
   original matrix coordinate. The representation is proved, not assumed.

2. **Genuine smooth locus, including singular rank-two axis points.** The
   `SmoothPoint` definition requires the point prime in the actual quotient to
   pull back to the evaluation prime and belong to `Algebra.smoothLocus ℂ`.
   I read the pinned library definition: this is formal smoothness of the
   localized coordinate ring. For the finitely presented affine complex
   algebra at hand it gives the usual algebraic smooth locus. There is no
   built-in `ExactlyOneZero`, rank-stratum, dimension or Jacobian premise.
   `SmoothTransport.lean` transports the actual prime localizations along the
   proved algebra equivalence. `Smooth.lean` proves both smooth and nonsmooth
   directions for the actual localized quotient, then proves that its point
   corresponds to the original matrix evaluation prime.

3. **The square-zero obstruction is substantive and correct.**
   `triple_product_not_formallySmooth` uses the library's actual criterion that
   a surjection from a formally smooth presentation admits a section modulo
   the square of its kernel. Representatives of the lifted coordinates are
   `a+abc*u`, `b+abc*v`, and `c+abc*w`. Their product lies in `(abc)^2`.
   Cancellation of the nonzero `abc` in the presentation domain gives an
   equation whose evaluation at a point with `ab=ac=bc=0` says `1=0` in a
   nontrivial ring. The localized polynomial presentation remains a domain,
   the product is proved nonzero there, evaluation really extends to that
   localization, and the presentation map is proved surjective with the
   required kernel. No unavailable smoothness fact is inserted as a premise.
   Conversely, where the other two coordinates are nonzero, they become units
   in the localized quotient; the remaining coordinate is zero. Coordinate
   erasure supplies an actual algebra retraction from the smooth localized
   polynomial presentation. The lifting property proves formal smoothness of
   the retract. Thus exactly one zero coordinate characterizes smoothness;
   axes and the origin are excluded, regardless of matrix rank.

4. **The tangent condition covers the entire vanishing ideal.**
   `TangentVector` quantifies over every polynomial in `definingIdeal`, in all
   nine ambient coordinates. `Tangent.lean` proves the directional sum's
   polynomial rules and its hollow-substitution rule by polynomial induction.
   Testing actual ideal elements gives symmetry, zero diagonal and
   `bc*Z01 + ac*Z02 + ab*Z12=0`. For the converse, every substituted ideal
   element is a multiple of `abc`, so the product/substitution rules annihilate
   it under precisely these conditions. The only point premise is `abc=0`.
   At component intersections the equation degenerates and the larger tangent
   space is retained; tangent directions receive no additional rank bound.

5. **Actual derivatives and correct metric coefficients.** The objective is
   the sum of all entry squares over `ℂ`, without conjugation. The general
   affine-square calculation in `Differential.lean` constructs actual
   `HasFDerivAt` proofs. It then differentiates the continuous-linear-map-valued
   gradient to obtain the actual second Fréchet derivative. Consequently the
   proof cannot exploit `fderiv`'s zero fallback for nondifferentiable functions.
   Specialization gives `2 sum_ij (Xij-Uij) Zij` in every matrix order, and the
   full symmetric hollow objective retains all three diagonal constants and
   coefficient two on off-diagonal squares. All three plane Hessians are the
   actual bilinear form `4 sum h_j v_j`; testing coordinate directions proves
   its zero kernel. This is valid even for nonsymmetric data in that supporting
   theorem. No scheme-theoretic multiplicity theorem is exported or needed
   for the canonical distinct-critical-point count.

6. **All actual generic critical points are exhausted.** `Critical.lean` first
   proves equivalence between actual smooth criticality and orthogonality to
   every complex tangent direction. On each smooth plane, coordinate tests
   force precisely the two unconstrained data coordinates. The converse checks
   all tangent directions. For nonzero off-diagonal data, all three proposed
   matrices are smooth and critical, are pairwise distinct, and exhaust every
   actual smooth critical point. The equality with `Set.range (candidate U)`
   is a theorem about the original critical-set definition, not a replacement
   definition or a three-point list with presumed completeness. Data diagonals
   remain arbitrary.

7. **Genericity is nonvacuous and the unknown exceptional set stays arbitrary.**
   `HasGenericCriticalCount` requires a polynomial nonzero at some symmetric
   datum and asserts the count at every symmetric datum where it is nonzero.
   This is the usual principal-open formulation of a generic algebraic
   assertion. `Generic.lean` restricts an arbitrary such polynomial to all six
   independent symmetric coordinates; its given nonzero evaluation proves the
   restricted polynomial nonzero. Its product with the three off-diagonal
   coordinate variables is nonzero in the polynomial domain. Actual
   polynomial-function extensionality over the infinite field `ℂ` provides a
   datum avoiding both exceptional sets. This proves the required intersection
   with every possible generic-count witness, not just one convenient datum
   or the author's chosen open set.

8. **Actual cardinal counting closes the full target.** `HasCriticalCount` is
   `Cardinal.mk` of the actual critical-point subtype, equal to a finite
   cardinal. Infinite sets cannot silently acquire a finite default count.
   `Count.lean` applies the actual cardinality theorem for an injective range
   of `Fin 3`, hence obtains three. The explicit generic polynomial has a
   nonvanishing symmetric witness; that witness is data and need not belong
   to the approximation variety. Any proposed generic count four intersects
   the established open set, assigning both cardinals three and four to the
   same subtype, a contradiction. Instantiating the complete original
   conjecture at `n=s=3` supplies the unconditional final negation.

Every advertised export was checked along that proof path:

| Exports, with prefix `NLA.RA20` | Actual implementation reviewed |
| --- | --- |
| `hollow_variety_semantics`, `reduced_coordinate_ring` | `Algebra.lean` |
| `algebraic_smooth_locus` | `Smooth.lean`, `SmoothTransport.lean` |
| `algebraic_tangent_space` | `Tangent.lean` |
| `full_frobenius_differential`, `hollow_distance_semantics`, `component_hessians` | `Differential.lean` |
| `generic_critical_locus` | `Critical.lean` |
| `generic_data_intersection` | `Generic.lean` |
| `generic_count_three`, `generic_count_not_four`, `not_criticalCountConjecture` | `Count.lean` |

## Fresh checks, trust and reproducibility

I ran **13 successful direct-source Lean commands** into a genuinely new private
prefix: all 11 real source modules, a separately namespaced copy of the frozen
Challenge, and my own inspector. No prior RA-20 object or dependency object was
copied into that prefix. The ten exact pinned dependency packages were reused
read-only and their revisions and tracked cleanliness checked before and after.
Lean reports version 4.33.1; Mathlib is
`0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert is
`621a43d7cf21f87872392a01e874f2f1dbddc926`. This is not a claim to rebuild those
dependencies from source.

The renamed reference differs only in its namespace. All **12 elaborated
export types match** by Lean definitional equality, with no definition
exceptions. The deliberate reference admissions are present in their own
namespace and absent from the actual proof dependency closure. This diagnostic
is not Comparator. I independently traversed the actual types and values of
**214 project declarations**, rejected unsafe/partial declarations and all
nonfoundational transitive axioms, and checked **28 material dependencies**
including the actual reduced ideal, smooth locus, full-ideal derivative,
generic-open intersection and cardinality APIs. The full trace is retained in
`command-050/raw.log` and independently parsed in `parsed-closure.json`.

The fresh real-source compilations execute **61 LeanCert
`#assert_trust kernel` assertions**; my inspector adds 12. All **69 printed
axiom reports** contain only `propext`, `Classical.choice` and `Quot.sound`.
LeanCert's pinned auditor implementation was read: it recursively collects
axioms and rejects native compiler trust, admissions and unknown axioms in
kernel mode. No numerical interval certificate is needed for this exact
algebra/calculus/cardinality proof. The entire successful direct-source work
took approximately 75 seconds of recorded command wall time; no performance
guarantee is inferred from that measurement.

No Lean build or inspection attempt failed. The only warnings were two existing
`letI` style suggestions in `Differential.lean` and the twelve intentional
reference-hole warnings. Navigation-only failures are disclosed separately in
`navigation-diagnostics.json`; none was a proof failure. All 70 subprocess
records, all raw output and all source snapshots remain. The 26 files generated
in my own prefix, totaling 5,951,839 bytes, were hashed before that prefix alone
was removed. Shared dependency trees and frozen project files were untouched.

The outer evidence inventory binds this report, all my evidence, the entire
521-file proof boundary, the proof-freeze file, and all 16 original sources,
including every nested manifest. It excludes only its own exact path. The other
final referee's separately owned work is outside this review's inventory scope.

## Quality, attribution and remaining publication gates

The proof meets the applicable NLA adaptation of Tau Ceti's correctness, scope,
proof-quality, reuse, generality, API, naming, placement, documentation and
attribution criteria. It uses actual pinned Mathlib APIs rather than custom
assumptions with familiar names. Its reusable formal-smoothness transport,
retraction, product obstruction and finite quadratic-derivative lemmas are
appropriately stated; fixed-order component calculations are small. Exact
algebra eliminates interval subdivision entirely while keeping the original
domain. The statement/implementation separation and checker workflow follow
the campaign's credited Schiffer/Forsythe examples; no theorem from either
example project is a mathematical dependency.

Two nonblocking documentation observations are relevant to candidate packaging.
The frozen statement-stage README still describes proof work as pending, and
the Lake default target remains `Challenge`; current reproduction instructions
must explicitly build/check `Solution` and distinguish historical statement
files from the completed proof. Also, the `abcLocalChart` comment calls its
target the “complete local ring”; the actual type is ordinary
`Localization.AtPrime`, with no adic completion. I interpret that comment as
referring to the entire local ring. The types and proof are unambiguous, and
this review claims no completion theorem. I did not edit frozen bytes for either
editorial observation.

Formalization credit remains **George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA**, with AI assistance and no contact email. The negative-resolution
mathematics remains attributed to the repository's Codex automated maintainer
audit, and the conjecture to Kubjas, Sodomaco and Tsigaridas. No human peer review,
official Tau Ceti endorsement, or historical priority is claimed.

The separate second independent final approval, actual fresh non-root Linux
Comparator/default-kernel/control run, independent operational audit, truthful
`formalization.yaml`, and reviewed canonical publication remain coordinator
gates. I have not run or accepted those future operations. Subject to those
separate gates, the frozen proof is a complete negative resolution of the
original RA-20 target; no mathematical correction is requested.
