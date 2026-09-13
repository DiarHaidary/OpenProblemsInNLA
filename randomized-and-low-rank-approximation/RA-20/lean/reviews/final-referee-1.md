# RA-20 independent final mathematical referee 1

**APPROVE the complete frozen mathematical proof.** No required mathematical
correction. This is one independent final mathematical approval, dated
13 September 2026; it is not an actual Linux Comparator result, permission to
skip the remaining gates, or a claim of external human peer review.

Reviewer: `/root/ra20_final_referee1`, a fresh AI agent. I did not design the
statements, implement a proof module, prepare the author validation, or edit the
reviewed mathematics. I wrote only this report and my separate diagnostic
evidence. The four disclosed implementers are different agents. I reviewed the
source independently rather than treating their reports or successful builds
as mathematical evidence.

## Exact scope and preservation

The complete proof freeze is
`f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f`:
521 project inputs, together with 16 original source/policy files at immutable
repository base `5830ed4fb06da0659414a3deb2a40ad327aca052`. I independently
rehashed every input, checked the original files against their actual Git blobs,
and verified all 68 statement-stage inputs before and after the fresh replay.
All twelve nested manifests/package inventories were separately traversed and
their entries rehashed. No frozen file changed.

| Mathematical boundary | SHA-256 |
| --- | --- |
| Frozen Definitions | `a649164ee7f11e88d8bfae4167ee0d9b9252a8683f253ab5a69981cde0e7cf94` |
| Frozen Challenge | `eb62545ea3e527c186b832a186fbaefa560409bf23be74486b9b00f04e00a2e9` |
| Proof assembly | `d3cb0dab572eb54795e6568c717e9e6f8200eb20f299e319fc3be36bbe8aaea1` |
| Solution exports | `755a58cc081172804c644ea83518581235763a6ecefcbff6c92f131ca44c32b5` |
| Prior statement freeze | `6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8` |

I read the complete canonical target, complete Markdown and TeX solution,
historical independent informal reconstruction and exact-check source/output,
the mathematical contracts, correspondence, proof map, author completion,
all eleven mathematical source modules, and the repository contribution and
independent-review protocols. The two earlier statement approvals remain
historical approvals; their authors' subsequent implementation work does not
make them independent final referees.

I also opened the primary [author manuscript](https://arxiv.org/pdf/2010.15636v2)
directly. Section 2.2 uses generic complex smooth critical points and a bilinear
extension; Section 2.3 gives the full-entry Frobenius distance. Conjecture 5.6
and Table 7 on printed page 21 give four at the relevant case. This was a
targeted convention/formula check, not a later-literature search or a review
of the whole paper.

## Independent semantic assessment

**The full original conjecture is negated.** `criticalCountConjecture` retains
all four formulas and every `n ≥ 3`, `1 ≤ s ≤ 4`, `s ≤ n`. Natural-number
subtraction agrees with ordinary subtraction throughout this range. The final
proof specializes that universal assertion at the admissible `n=s=3`, where
`predictedCount` is four, and contradicts a genuine generic count theorem.
It does not replace the original target by a fixed witness assertion. It also
does not separately settle any of the other parameter formulas.

**The matrix geometry is genuine.** Matrices have complex entries and actual
transpose symmetry, not Hermitian symmetry. The rank condition is Mathlib's
dimension of the range of the matrix linear map. `definingIdeal` is the ideal
of every polynomial vanishing on the actual constrained matrix set.
`CoordinateRing` is its quotient; the proposed three-variable equation is not
inserted into those definitions.

In [Algebra](../NLA/RA20/Algebra.lean), explicit width-two factorizations prove
the zero-determinant implication without assuming a rank criterion as a new
axiom. The reverse direction uses actual full rank for a nonzero determinant.
The exact determinant is `2abc`. Primality and relative primality of the three
different variables prove squarefreeness of `abc`, hence radicality of its
principal ideal. The actual Nullstellensatz then identifies its whole vanishing
ideal. The hollow substitution has an explicit section, its quotient map is
surjective, and its kernel is the original nine-variable defining ideal.
The quotient equivalence follows from the actual first-isomorphism theorem,
with every original coordinate's image proved.

**Smoothness has not been assumed or defined to mean the desired case split.**
`SmoothPoint` requires the actual quotient point prime over the evaluation
prime and actual `Algebra.smoothLocus` membership. I inspected the pinned
library definition: this is formal smoothness of the localization at that
prime, the ordinary algebraic smooth-at-a-point notion for this finitely
presented complex affine variety. It is not a claim that the localized algebra
itself is finitely presented.

The substantial argument in [Smooth](../NLA/RA20/Smooth.lean) proves both
directions using actual localization and infinitesimal lifting. Where exactly
one coordinate vanishes, the other coordinates become units, the relation
forces the remaining coordinate to zero, and elimination supplies an actual
algebra retraction from a formally smooth localized polynomial algebra.
At a component intersection, formal smoothness would split the square-zero
thickening of the localized presentation. Representatives of the lifted
coordinates differ from their original values by multiples of `abc`.
Their product, divided by the nonzero `abc` in the polynomial localization,
and then evaluated at the point, gives `1=0`, because all pairwise products
vanish. The localization is a domain and that cancellation premise is proved.
The coordinate equivalence and evaluation-prime equality transport this
characterization to the original matrix ring. Thus the origin and all
coordinate axes are excluded, including axis matrices of rank two.

**The whole tangent ideal is handled.** [Tangent](../NLA/RA20/Tangent.lean)
proves the directional derivative's elementary rules and its hollow-substitution
rule by polynomial induction. Actual vanishing polynomials force the symmetry
and diagonal conditions and the determinant-gradient equation. Conversely,
every polynomial in the original vanishing ideal pulls back to a multiple of
`abc`; the product/substitution rules and `abc=0` make its differential zero.
This proves the stated equivalence for singular points as well as smooth
points. No rank condition is imposed on tangent directions, and no unproved
Jacobian-criterion hypothesis replaces the ideal calculation.

**Differentiation uses the original objective.**
[Differential](../NLA/RA20/Differential.lean) proves actual `HasFDerivAt`
statements for finite sums of squared affine complex linear functionals.
It then differentiates the continuous-linear-map-valued gradient. This rules
out using `fderiv`'s zero value at nondifferentiable functions as a shortcut.
The full-entry first derivative is proved for every order, including zero;
on symmetric data the two off-diagonal entries give coefficient four in the
three hollow coordinates. The restricted distance preserves the arbitrary
diagonal contribution. The actual second derivatives in all three plane
charts equal `4∑hᵢvᵢ`, and testing basis directions proves zero radical.
The chart Hessian theorem even permits nonsymmetric data, correctly: those
data affect only the affine and constant terms of the restriction.

**All generic complex critical points are exhausted.**
[Critical](../NLA/RA20/Critical.lean) derives its coordinate criticality
equivalence from genuine smoothness, the entire-ideal tangent theorem and the
actual derivative. On each component, all complex tangent directions force the
two free coordinates to equal the data coordinates. Conversely those choices
annihilate every allowed tangent direction. Every smooth point belongs to
one of these three components. Nonzero off-diagonal data make all three
candidates smooth and pairwise distinct. Therefore the full actual critical
set equals the injective range, rather than being defined as that range.

**Genericity and counting are nonvacuous.** `HasCriticalCount` uses
`Cardinal.mk` of the actual critical-point subtype; an infinite set is not
silently assigned a finite count. `HasGenericCriticalCount` permits an
arbitrary exceptional polynomial but requires a symmetric datum at which it
is nonzero. This is equivalent to a generic assertion outside a proper
algebraic exceptional set: a nonempty complement contains a nonempty principal
open set, and a nonempty principal open has a proper closed complement.

In [Generic](../NLA/RA20/Generic.lean), an arbitrary such polynomial is
restricted to six independent symmetric coordinates. Its known nonzero value
proves that restriction is nonzero. Multiplying it by the three off-diagonal
variables stays nonzero in the polynomial domain. Actual polynomial-function
extensionality over the infinite field `ℂ` supplies a datum where the product
does not vanish. This proves intersection with every competing generic open,
not merely with a chosen witness or a real-data subset; diagonal coordinates
remain unrestricted. [Count](../NLA/RA20/Count.lean) uses the actual injective
range cardinality theorem to obtain three. Any proposed generic count four
would give the same critical subtype cardinality both three and four at an
intersection datum. The last theorem then negates the original conjunction.

## Fresh checks and exact trust boundary

My own initially empty prefix compiled Definitions, Algebra, SmoothTransport,
Smooth, Tangent, Differential, Generic, Critical, Count, Proof and Solution
directly from source, followed by an isolated reference and inspector.
All **13 commands passed**, taking approximately **90.7 seconds** of aggregate
local command time. No existing RA-20 objects were used. All ten exact pinned
dependency packages were checked at their Git revisions with clean tracked
source before and after, and reused read-only. I invoked no Lake build,
dependency download, package copy, or shared-cache mutation.

My inspector uses a namespace-only transform of frozen Challenge to avoid any
name collision with Solution. Each of the twelve actual exports is a theorem;
its elaborated type is both structurally identical as a Lean expression and
definitionally equal to the corresponding reference type. No definition
exceptions are allowed. The intentional twelve reference admissions are
required to remain isolated: traversal from actual proof bodies cannot reach
any reference declaration. This is an in-process local type check, distinct
from the required independently replayed Linux Comparator.

I adapted the inspected assembly traversal as diagnostic structure and reran
every check, adding an independent all-environment scan: **236 project
declarations** have no unsafe/partial declaration or nonstandard transitive
axiom. The actual export proof/type closure contains **214 safe declarations**,
and all **39 required mathematical dependencies** are genuinely present,
including the smooth-locus, Nullstellensatz, actual derivative, whole-ideal
and cardinality APIs. Bodyless nonstructural declarations and reference
dependencies are rejected. The complete closure output is retained.

All **61 source and 12 diagnostic LeanCert `#assert_trust kernel` assertions**
passed. The raw successful logs contain **69 printed axiom reports**: each
contains exactly `propext`, `Classical.choice`, and `Quot.sound`. Four additional
source assertions do not print an axiom report, explaining the different
counts. I inspected LeanCert's actual classifier: it rejects admissions,
custom axioms and native-compiler trust. This project uses LeanCert's kernel
trust auditor; it does not claim to need or perform an interval computation.

There were no failed elaborations in my replay. The only successful-source
warnings are two previously disclosed Differential style suggestions; the
other twelve warnings belong to the deliberately admitted reference. An
initial read-only lookup of a nonexistent author `run.py`, and two unsuccessful
web fetches of example Forsythe files, are recorded as diagnostics rather than
claimed successes. Every source/command/output from my actual replay is
retained; only my own hashed generated object prefix is removed afterward.

## Review standards, quality and publication limits

I applied the repository's adaptation of all ten Tau Ceti review angles and
read the retained original rubrics. Exact target, nonvacuity, real dependencies
and completeness were the principal adversarial checks above. I searched the
pinned Mathlib smoothness, derivative and polynomial APIs and inspected the
actual definitions/theorems used. The broad algebra-retraction, local
smoothness-transport and quadratic-derivative lemmas have actual consumers;
the fixed-order coordinate work is appropriately specialized to this
counterexample. I found no located API that directly replaces a substantive
bridge. The proof is split by its mathematical dependencies, with exact ring
algebra and a fixed three-coordinate reduction avoiding numerical search.
The explicit contract forwarding in Solution serves the frozen-checker
interface, not a compatibility-only API.

The local Schiffer Challenge provided an inspected example of separating
definitions, exact mathematical contracts and admitted reference statements.
The pinned Forsythe checker structure is credited in the campaign source lock;
my two direct attempts to retrieve its example proof files failed and add no
new review claim. No theorem from either project is a mathematical dependency.
This is an NLA review, not an official Tau Ceti service run or an assertion that
Tau Ceti's own roadmap/compatibility policies govern these permanent IDs.

Two documentation precisions do not change my mathematical approval. The word
“complete” in the `abcLocalChart` comment refers here to extending to the whole
ordinary local ring; no adic completion is constructed or proved complete.
Publication prose should say “localization” or “entire local ring.” Also the
exported Hessian theorem proves nondegeneracy, not a separately formalized
scheme-theoretic intersection-multiplicity theorem. The original canonical
target counts distinct generic smooth critical points, which is fully proved.
Do not advertise a stronger multiplicity formalization.

The frozen README and statement-stage comments deliberately retain their
earlier phase descriptions. They are superseded by the dated completion and
must receive truthful candidate/publication wrappers later, with archived
original bytes. In particular, default Lake targets still name Challenge;
reproduction must explicitly build/check Solution, as my direct replay did.
The missing `formalization.yaml`, authoritative non-root Ubuntu default-kernel
replay, sandbox/negative controls, actual Comparator and independent operational
audit are still separate required gates. I performed none of those Linux
operations and do not authorize marking the canonical page Lean verified yet.

Formalization credit correctly names **George Stepaniants, Department of
Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA**, with AI assistance and without an email. The
Codex automated maintainer audit retains the negative-resolution mathematics;
Kubjas, Sodomaco and Tsigaridas retain the conjecture attribution. No
historical-priority or external human-review claim is added.

The adjacent [validated result](final-referee-1-evidence/validated-results.json)
and [complete evidence manifest](final-referee-1-evidence/EVIDENCE-MANIFEST.json)
bind the actual logs, inspected source, this report, every frozen proof input,
all nested manifests and original source identities. Only the exact outer
manifest excludes itself. Approval is specific to these bytes.
