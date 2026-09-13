# RA-20 proof correspondence

The completed author proof establishes all twelve frozen contracts. It gives a
negative answer to the complete original generic critical-count conjecture:
at `n=s=3` the actual generic count is three, whereas the asserted formula is
four. It does not separately settle the formulas for the other values of `s`.
Independent final mathematical reviews and authoritative Linux verification
remain pending; current local evidence is in
[the assembly handoff](verification/conclusion-development/HANDOFF.md).

The immutable [Definitions](NLA/RA20/Definitions.lean),
[Challenge](Challenge.lean) and [mathematical targets](NUMERICAL_TARGETS.md)
were accepted before implementation. Their statement-stage wording is retained
as historical evidence. The completed implementation imports no Challenge and
uses none of its reference admissions.

## Original target and retained semantics

The original variety consists of **complex symmetric** matrices of rank at most
two with the specified diagonal entries zero. Symmetric means transpose
symmetry, not Hermitian symmetry. Its coordinate ring is the quotient by all
polynomials vanishing on the actual matrix point set. Smooth points use
Mathlib's algebraic smooth locus at the actual point prime of that reduced ring.
The tangent condition annihilates the differential of every member of the full
vanishing ideal. It is not defined to be a determinant-gradient condition or the
rank-two stratum.

The distance is the complex bilinear polynomial `∑ i, ∑ j, (X i j-U i j)^2`.
Its actual complex Fréchet derivatives are used; complex conjugates are absent.
Generic data range over the entire space of complex symmetric matrices, with
unrestricted diagonal entries. `HasGenericCriticalCount` permits an arbitrary
exceptional polynomial that is nonzero somewhere on that symmetric space.
The count is `Cardinal.mk` of the actual smooth critical-point subtype, so an
infinite set is never assigned a finite count by convention.

## Exact export and module correspondence

All names below have prefix `NLA.RA20`. [Solution](Solution.lean) supplies the
exact frozen public types by applying their corresponding `_proved` theorems.
[Proof](NLA/RA20/Proof.lean) assembles and audits the genuine implementations.

| Public export | Implementation | Main correspondence |
| --- | --- | --- |
| `hollow_variety_semantics` | [Algebra](NLA/RA20/Algebra.lean) | Actual determinant `2abc`, explicit width-two rank factorizations and the full matrix-point correspondence. |
| `reduced_coordinate_ring` | [Algebra](NLA/RA20/Algebra.lean) | Coordinate-preserving equivalence from the actual reduced matrix coordinate ring to `ℂ[a,b,c]/(abc)`. |
| `algebraic_smooth_locus` | [Smooth](NLA/RA20/Smooth.lean), [SmoothTransport](NLA/RA20/SmoothTransport.lean) | Genuine localized algebraic smoothness holds precisely when exactly one hollow coordinate is zero. |
| `algebraic_tangent_space` | [Tangent](NLA/RA20/Tangent.lean) | Every polynomial in the reduced ideal is handled, at smooth and singular points alike. |
| `full_frobenius_differential` | [Differential](NLA/RA20/Differential.lean) | Actual complex Fréchet derivative for every natural matrix order, including zero. |
| `hollow_distance_semantics` | [Differential](NLA/RA20/Differential.lean) | The three diagonal squares remain constant, and each off-diagonal square occurs twice. |
| `generic_critical_locus` | [Critical](NLA/RA20/Critical.lean) | Equality of the entire actual smooth critical set with an injective three-matrix enumeration. |
| `component_hessians` | [Differential](NLA/RA20/Differential.lean) | Actual second derivatives in all three charts give the nondegenerate bilinear Hessian `4I`. |
| `generic_data_intersection` | [Generic](NLA/RA20/Generic.lean) | Every nonempty principal open set in symmetric data meets the displayed generic set. |
| `generic_count_three` | [Count](NLA/RA20/Count.lean) | Actual critical-subtype cardinality and a nonempty principal-open witness establish generic count three. |
| `generic_count_not_four` | [Count](NLA/RA20/Count.lean) | Any proposed generic count four contradicts the same subtype's cardinality at an intersection datum. |
| `not_criticalCountConjecture` | [Count](NLA/RA20/Count.lean) | Substitution of the allowed parameters `n=s=3` refutes the complete original four-formula assertion. |

## Substantive bridges

**Reduced coordinate ring.** Distinct polynomial variables are prime and
pairwise relatively prime, so `abc` is squarefree and its principal ideal is
radical. Mathlib's actual Nullstellensatz identifies the vanishing ideal of its
complex zero set with `(abc)`. The proved hollow matrix-point correspondence
then identifies the original nine-variable vanishing ideal as its pullback.
An explicit section of the hollow substitution proves surjectivity, and the
quotient first-isomorphism theorem gives the actual algebra equivalence. Every
matrix coordinate's image is proved; no coordinate-ring claim is assumed.

**Smooth locus.** The smooth helper works with actual point-prime localizations.
On a component away from its intersections, the invertible coordinates give a
local algebra retraction from a smooth chart. At an intersection, a square-zero
lifting obstruction proves the relevant localized algebra is not formally
smooth. These two directions establish the real Mathlib smooth-locus predicate,
including the axes and origin. The proved coordinate-ring equivalence and
point-prime transport transfer that result to the original matrix variety.
An axis point can have matrix rank two and still be singular in this variety;
the proof does not confuse these predicates.

**Entire-ideal tangent space.** The finite partial-derivative sum obeys proved
constant, variable, sum, difference and product rules. Polynomial induction
proves its substitution rule through the hollow map. Testing actual vanishing
polynomials gives symmetry, zero diagonal and `bc Z01+ac Z02+ab Z12=0`.
Conversely, every substituted vanishing polynomial is a multiple of `abc`, and
the product and substitution rules show its differential vanishes. Tangent
directions receive no rank restriction; component intersections retain their
larger tangent spaces.

**Derivatives and exhaustion.** A reusable finite sum-of-squares calculation
proves the actual first and second Fréchet derivatives. Specializing it to the
full matrix entries and the three component charts retains doubled
off-diagonals and unrestricted data diagonals. On each genuinely smooth chart,
orthogonality to all actual tangent directions forces exactly its coordinate
projection of the datum. Every smooth point lies on one of these three charts.
For nonzero off-diagonal data, the three projections are smooth, critical and
pairwise distinct. The Hessian calculation is a separate exact export, not a
replacement definition of a derivative or a presumed nonsingularity premise.

**Genericity and count.** An arbitrary exceptional polynomial is restricted to
six free symmetric coordinates. Its nonvanishing assumption proves that this
restriction is a nonzero polynomial. Multiplication by the three off-diagonal
coordinates stays nonzero; polynomial-function extensionality over the infinite
field `ℂ` supplies a datum avoiding both exceptional sets. The actual injective
range cardinality theorem then counts the full critical subtype. The argument
excludes every competing generic-open count four, not only the displayed open
set or one chosen datum.

## Reuse, computation and trust

The proof uses the actual pinned Mathlib matrix rank/determinant, multivariate
polynomial, Nullstellensatz, localization/formal-smoothness, Fréchet calculus
and cardinal APIs. Exact algebra replaces numerical eigenvalue or interval
work. Matrix calculations have fixed order three; the polynomial and generic
open-set arguments are universal. No artificial singleton or interval
certificate is added. LeanCert's actual kernel trust auditor is used throughout.

The campaign's direct-source and proof-dependency inspection structure is
reused with new source hashes and fresh results. [The assembly validation](verification/conclusion-development/validation.json)
records thirteen successful commands in an initially empty private prefix,
twelve exact frozen-type matches, 214 safe project declarations, 39 required
material dependencies and 69 printed standard-three axiom reports. This is
author validation on macOS, not the authoritative Linux Comparator gate.

Formalization author: George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. Original negative-resolution mathematics remains attributed to the
repository's Codex automated maintainer audit; the original conjecture is due
to Kubjas, Sodomaco and Tsigaridas. Agent implementation roles are disclosed in
[the assembly handoff](verification/conclusion-development/HANDOFF.md); none of
its proof contributors is counted as an independent final referee.
