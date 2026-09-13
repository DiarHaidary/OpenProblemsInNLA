# IE-16 independent statement referee 2

**APPROVE the fifteen-contract statement boundary.** It retains the complete
canonical target and supplies the minimum-attainment and positivity bridges
needed to interpret the finite counterexample. No mathematical change is
requested before implementation.

Reviewer: `/root`, independent of the statement author, 13 September 2026.
This is an AI-agent source/statement review under the repository's adaptation
of Tau Ceti, not human peer review, proof verification or an official Tau Ceti
service. I performed no new Lean or Lake invocation for this review.

## Mathematical correspondence

I read the current Definitions, all fifteen Challenge declarations, numerical
targets, the canonical target and the source's finite-counterexample argument.
I checked the original complex Lagrange construction and exact nine-point
minimization, including the alternative positive-weight orthogonality route.
The stronger amplification theorem and an operator-level GMRES interpretation
are unnecessary to negate the actual displayed finite-polynomial inequality;
no formalization of those stronger claims is asserted.

`Poly` is Mathlib's `Polynomial ℂ`, with arbitrary complex coefficients and
actual polynomial evaluation. `natDegree ≤ k` agrees with degree at most k;
the constant-zero exception cannot satisfy `p.eval 0 = 1`. Constant one makes
the feasible set nonempty. Every finite norm maximum is nonnegative. Thus
`sInf (feasibleValues L k)` concerns a nonempty set bounded below. More
specifically, the two explicit `IsLeast` obligations require both membership
(a feasible attaining polynomial) and global minimality at the full witness
and every five-point subset. These identify every minimum used in the
counterexample, without relying on an unproved general attainment assertion.

`Finset.sup'` is the actual finite maximum, not a sampled or estimated norm.
`subsetFamily` is the full powerset filtered by cardinality k+1. Its maximum
therefore covers all relevant subsets; no enumeration table replaces the
quantifier. The positive `subsetMax` obligation rules out division by zero
and its empty-family totalization in the ratio argument. `admissible` preserves
cardinality and nonzero nodes; Finset membership preserves distinctness.
The universal assertion retains every n≥3 and 1≤k≤n−2, actual `Real.pi`,
and the original factor 4/π. The unconditional negation is explicit.

The witness is exactly the nine complex points ω^a+10^-3 ω^b with
ω=-1/2+(sqrt 3/2)i and a,b∈Fin 3. Its cardinality and nonzero conditions
are obligations, not hidden assumptions. The polynomial is exactly
1-((1+ε)/(1+ε+3ε²+ε³+ε⁴))X³, so degree three is allowed at k=4.
The norm and actual full minimum are required to equal
3003003000/1001003001001. The all-subset bound is strict and applies to each
actual five-point subset. These are substantive obligations still to prove.

I independently checked the exact rational substitution for the full value,
its strict lower bound 299/100000, the source's rational upper estimate below
23/10000, and (299/100000)/(23/10000)=13/10. A lower bound π>31/10 suffices
for 4/π<13/10. The finite witness n=9,k=4 satisfies every original range
condition. The existing Lagrange formula gives an appropriate proof of
minimum attainment and positivity on each subset. The three occupancy
profiles cover all subsets, while the weighted orthogonality argument can
avoid costly polynomial group averaging. These are proof strategies, not
additional premises of an approved theorem.

## Evidence actually checked

`check_boundary.py` passed with the metadata venv. It independently matched
all 36 recorded statement/evidence hashes and all six source snapshots to
their exact `git show` bytes at upstream commit
`b73cd1804e40e0d101294eedb156984f0d62b4a6`. Unlike a snapshot label alone,
this directly checks the available upstream Git object contents.

The aggregate All.lean exactly equals current Definitions followed by current
Challenge, with only the duplicate import and following blank line removed.
It also matches the actual executed input. The retained compiler result and
log match the original files: exit zero, Lean -M 2048, one thread, a 90-second
wrapper deadline, fifteen deliberate sorry warnings and no elaboration error.
This is existing bounded aggregate statement elaboration, not my own run or
a separate current-module proof build. Older twelve-contract logs remain
historical and are not substituted for this result.

All fifteen names match the Comparator configuration and YAML result entries.
The pinned v0.4 schema validates the metadata. Definitions contains no sorry;
Challenge's fifteen placeholders and sorryAx are disclosed. I inspected pinned
Mathlib definitions for IsLeast, polynomial degree and finite suprema, and
confirmed the local Mathlib source revision
`0df444a360eaa60ab8c11dca51a86af692955474` has no tracked modifications.
No dependency rebuild, current actual-types/axioms run, Linux verification or
Comparator execution is claimed. Successful proof and operational reviews
remain mandatory before catalog promotion or counting this problem.

Attribution distinguishes Sidney Holden's mathematical resolution from
George Stepaniants's formalization, with Computing and Mathematical Sciences,
California Institute of Technology affiliation and no George contact email.

Two documentation phrases should be corrected without changing the frozen
mathematics: only Challenge has placeholders; the source inventory contains
SHA-256 content hashes rather than Git blob object IDs. Preserve the reviewed
version and record those textual corrections explicitly.

## Approved immutable mathematical boundary

- Definitions: `e4681f2083d71d8980adcd70e7cf26367e0e84dbc1773f4d2f082bf2417c9507`
- Challenge: `85cbe24c7657d9ddc37728db5bb1740a80ddab60e3eb4676e329df40a7b1737c`
- Numerical targets: `e0fb3c0b10e29d2574efa62064f1bd45bcff1175b5538f580f5ebafb1025c950`
- Comparator: `963e1d217de9369cd5b4a3c282e983cb01986512d5221e18e1ea44d087fe7f09`
- Metadata: `3a7003dbd9010ee1ed0f8be032e7265815405ebf706a66effbe801a884c2a2f4`

CHECKS.json retains the actual independent checks and exact rational values.
The evidence manifest binds this report and its small source/check records.
