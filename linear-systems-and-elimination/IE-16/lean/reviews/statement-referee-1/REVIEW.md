# IE-16 independent amended statement approval

**APPROVE the amended fifteen-contract mathematical statement boundary at the
hashes below.** All three substantive requests in my original review are
satisfied. The full original inequality, arbitrary complex polynomial domain,
complete five-point subset family, exact witness and numerical values remain
unchanged. No further mathematical statement revision is requested.

Reviewer: `/root/is02_cleanup_referee`, independent Codex AI agent, 13 September
2026. This is a separate bounded recheck after the original requested-changes
report, not a rewrite of that historical report. I did not author or edit the
candidate and ran no Lean, Lake, Git, network or heavy computation. I inspected
the existing bounded elaboration evidence and performed small source/hash/schema
checks only. This is statement approval, not proof verification, human peer
review, an official Tau Ceti service, Linux verification or Comparator execution.

## Closure of the original requests

The original report is preserved at
`/tmp/nla-ie16-statement-referee1/REVIEW.md`, SHA-256
`fff7c5dabea2b484d592c7200ae7088433f2cd0942f047b6819a3c4a2112fc48`.
I verified that its bytes remain unchanged. It reviewed the complete canonical
README, complete Holden manuscript and certificate, original definitions and
twelve numerical statements, with the source scrutiny and small rational
checks detailed there. The present report incorporates that mathematical
review and closes its explicit bridge requests.

1. `full_minimum_isLeast` now states
   `IsLeast (feasibleValues explicitL 4) (M explicitL 4)`. This requires an
   actual feasible complex polynomial attaining the full value, as well as
   a lower bound against every feasible polynomial. Thus the encoded infimum
   has the original minimum interpretation at the nine-point witness.
2. `every_five_point_subset_minimum_isLeast` quantifies every actual finite
   S in `subsetFamily explicitL 4`, with no extra assumption. It supplies the
   same attainment and lower-bound interpretation on every five-point subset.
   The manuscript's Lagrange interpolation argument provides an appropriate
   proof route; no generic all-input compactness theorem is needed here.
3. `subset_max_positive` requires strict positivity of the actual encoded
   subset maximum. This explicitly excludes the empty-family/default-zero
   branch and zero-division case in the ratio and final inequality conversion.

All three properties are also required by `ExplicitCertificate`, listed in
NUMERICAL_TARGETS, exported by Challenge, covered by Comparator and represented
in the fifteen YAML result entries. They are obligations to prove, not new
hypotheses allowing the desired conclusion to be assumed.

I checked the exact old/new source diff. Removing exactly these three new
Challenge declarations recovers the old Challenge byte-for-byte. Removing
exactly the three new certificate conjuncts recovers the old Definitions
byte-for-byte. All definitions preceding ExplicitCertificate, all twelve old
Challenge signatures, all constants and the universal target are unchanged.
The author's preserved old-source files match my independently hash-checked
old-source reconstruction exactly.

The bounded negative resolution needs minimum attainment only on the explicit
nine-point set and its five-point subsets to identify every canonical quantity
used by the counterexample. The amended contracts do this. There is no claim
to an affirmative inequality on a modified domain, and no stronger amplification
or dimension-growth theorem is being substituted for the original problem.

## All fifteen contracts and scope

The following complete boundary is approved:

| Contracts | Original-target obligation |
|---|---|
| explicitL_card, explicitL_admissible | Nine distinct nonzero actual complex points. |
| witness_feasible, witness_objective | Normalized degree-at-most-four polynomial, actual finite norm exactly the stated rational. |
| full_minimum_exact, full_minimum_isLeast, full_lower_bound | Exact full optimum, actual attainment/global minimality, strict rational lower bound. |
| every_five_point_subset_upper, every_five_point_subset_minimum_isLeast | Upper bound and attained-minimum interpretation for every five-point subset. |
| subset_max_upper, subset_max_positive | True complete subset maximum bounded above and strictly positive. |
| ratio_lower_bound, ratio_exceeds_candidate | Ratio above 13/10 and actual 4/Real.pi below 13/10. |
| counterexample, not_IE16Conjecture | Complete certificate and unconditional negation of the original universal target. |

`Poly` remains Polynomial ℂ, feasibility remains `natDegree ≤ k` with actual
`p.eval 0 = 1`, and the finite objective remains the maximum of complex norms.
The degree convention, nonempty feasible-value set and lower bound zero are
unchanged and are explained in the original review. The full powerset filter,
n >= 3, cardinality n, nonzero points and 1 <= k <= n-2 remain exact.
The actual square root defining omega and actual Real.pi remain present;
no rational approximation has replaced either mathematical constant.
No comparator/certificate list restricts the quantifiers to sampled polynomials
or selected subsets. The fixed n=9, k=4 witness suffices to refute the entire
universal assertion.

## Existing bounded elaboration evidence

I independently checked all 36 entries in the final STATEMENT_HASHES inventory.
All match their inspected files. The current aggregate `All.lean` is exactly
the current Definitions text, one intervening newline, and the current
Challenge text with its import line and following blank line removed. This
merely combines the definitions and contracts in one environment; no theorem,
assumption, type, namespace or arithmetic expression was altered. Its source
hash is
`f7e02a750cb5d076642220384de3b77970fef912a0159981f37d9594be1ae940`.
The retained aggregate is byte-identical to the original executed input at
`/tmp/nla-lean-ie16-project/recheck/All.lean`.

The retained result JSON and raw Lean log are byte-identical to the original
files under `nla-bounded-lean-8ydab99_`. The command invokes the pinned Lean
4.33.1 binary with `-M 2048 -j 1`; the wrapper records a 90-second wall-time
limit. Exit status is zero, elapsed time is about 13.1 seconds, and the log
contains exactly fifteen deliberate sorry warnings plus the known unused-L
binder warning. There are no elaboration errors. I inspected the wrapper's
source: it inserts the memory/thread limits, rejects caller overrides, uses
an exclusive local-compiler lock, and terminates the process on timeout.
This record is a bounded statement elaboration, not a full proof run.

The old twelve-contract logs are retained and explicitly labeled pre-change;
they are not presented as the amended result. I did not rerun Lean to duplicate
this check or print actual types/axioms independently. Imported dependency
objects were reused by the recorded run. I made no claim to independently
check all live Git dependency heads or rebuild those objects.

The fifteen Challenge names match Comparator and YAML in order and coverage.
The v0.4 JSON schema validates the YAML. Definitions has zero sorry and Challenge
has fifteen intentional placeholders; metadata reports those counts and sorryAx
truthfully. There is no Solution/proof module and no Linux or Comparator result.
The attribution continues to distinguish Holden's mathematical resolution from
George Stepaniants's formalization, department and Caltech affiliation, with
no George email added.

## Minor documentation notes and limits

Two nonblocking wording suggestions from the original review remain: the
numerical-target introduction says both Definitions and Challenge contain
placeholders, although only Challenge does; and it calls the SHA-256 content
hashes “upstream blob hashes.” Describe those as content hashes unless actual
Git object IDs are provided. These phrases do not alter the mathematical
boundary, metadata's correct zero/fifteen counts, or this approval.

Source copies remain bound to the supplied upstream-commit label, with their
contents independently hash-checked. This task did not independently retrieve
the upstream Git tree. The coordinator must obtain the second amended
statement approval before implementation, and complete actual proof reviews,
LeanCert trust checks and authoritative Linux Comparator later. This report
alone neither authorizes catalog promotion nor increments a verified count.

## Approved hashes

| File | SHA-256 |
|---|---|
| NLA/IE16/Definitions.lean | e4681f2083d71d8980adcd70e7cf26367e0e84dbc1773f4d2f082bf2417c9507 |
| Challenge.lean | 85cbe24c7657d9ddc37728db5bb1740a80ddab60e3eb4676e329df40a7b1737c |
| NUMERICAL_TARGETS.md | e0fb3c0b10e29d2574efa62064f1bd45bcff1175b5538f580f5ebafb1025c950 |
| comparator.json | 963e1d217de9369cd5b4a3c282e983cb01986512d5221e18e1ea44d087fe7f09 |
| formalization.yaml | 3a7003dbd9010ee1ed0f8be032e7265815405ebf706a66effbe801a884c2a2f4 |

CHECKS.json retains the actual hash, coverage, schema and raw-record checks.
Definitions.diff and Challenge.diff show the complete mathematical change.
EVIDENCE-MANIFEST.json supplies portable relative-path hashes for this report,
reviewed source and compact evidence. Historical raw logs retain their actual
execution paths. Rebuildable objects and caches are excluded.
