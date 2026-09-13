# NR-03 independent statement review, referee 2

Date: 13 September 2026. Reviewer: `/root/nr03_statement_referee2`, an
independent Codex AI agent that did not author this package. Phase:
**statements before proof implementation**. Protocol: the repository's Tau
Ceti adaptation in `docs/lean/REVIEW.md`, SHA-256
`d967ddce620d4e754e2f9c25548f30cb537f76f4ddcf8ecf2574945bcd332553`.
This is not an official Tau Ceti service run or human peer review.

**Mathematical statement verdict: APPROVE. Package verdict: CHANGES
REQUESTED for one metadata schema error.** No change to a mathematical
definition or theorem signature is requested. Correct the single metadata
field below and validate the resulting YAML before accepting the package.
This review alone is not permission to bypass the second independent
statement review, and is not a proof-verification result.

## Exact reviewed boundary

The candidate was read from
`/tmp/nla-lean-nr03-project/nonnegative-and-positive-factorizations/NR-03/lean`.
The complete twelve-file snapshot and hashes are in `candidate/` and
`candidate-hashes.json`. The mathematical approval is bound to these bytes:

| File | SHA-256 |
|---|---|
| `NLA/NR03/Definitions.lean` | `5157fd499d2f63d218012f96bee43f30e5f57e5a2353fde13878af46d30fda04` |
| `Challenge.lean` | `4f1764cf9c604f33ed6f285e83ca32ebd1ae1fb1fd8f763a1c4a719ef068c335` |
| `NUMERICAL_TARGETS.md` | `817a0978869dcaf2bb918d846e4143df480665e5db3bc841cf4070bd3f683c42` |
| `SOURCE_MAP.md` | `68eb2be2121b176ad13d036b50e03146539a9c7fe1e9ece9b55fdae761d34ebf` |
| `comparator.json` | `ea1cea90b8e25535a31dca7fc620494ded851587609bb1473c651d07757f40bd` |
| `formalization.yaml` before the requested correction | `314067c75958a46c14c31f091f04f1a4e537f5bdeb3d6d3983363fc046bd54f7` |

The original target and complete Holden proof were read from Git commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`, not from a mutable web page or the
author's description. Their exact source bytes are retained under `source/`:

| Source | SHA-256 |
|---|---|
| Canonical NR-03 README | `a699bd54bda485d843739a5448f3e1ff4d77feb8761ea8944e767000d2b3955e` |
| Holden complete proof, `NR03_counterexample.tex` | `26cac3ed5aa30226530bbf8562a626b6582444abcc8ef8e8e69ebde6160565a3` |
| Exact certificate, `factors_n7.json` | `fa515775f9c77e5dfe85109125d3f730c4b36684894730096247cd67fcc60bb9` |

The original problem asks whether the fully prescribed real matrix
`C_n(a,b) = (1 - aᵀb)^2` has nonnegative rank `2^n` for every `n ≥ 3`.
The Holden construction gives a complete negative answer at `n = 7`.
Formalizing this one permitted dimension suffices to negate the universal
question; the stronger source bound at every `n ≥ 7`, exact ranks, and the
smallest counterexample dimension are properly excluded from the claims.

## Fidelity of definitions and all ten contracts

I inspected the source and the independently elaborated forms of all twelve
definitions in `types-axioms.log`. `BoolVec n` is the full function type
`Fin n → Bool`, not a mask subset. `boolToReal` maps false/true to real 0/1.
`boolDot` is the finite real dot product and `cMatrix` uses **real**
subtraction before squaring; entries with intersection size greater than one
are retained. The elaborated multiplication in `FactorizationData` is the
ordinary rectangular matrix product through all `Fin r` indices.

`HasNonnegativeFactorization` quantifies arbitrary **real** W and H with
entrywise nonnegativity and the exact equality W H = X. It does not restrict
the rank minimum to rational factors, a support pattern, or certificate
data. `nonnegativeRank` uses `Nat.find` on the set of all such widths when
that set is inhabited. The zero totalization outside that domain is explicit;
the n = 7 certificate and factorization obligations establish inhabitation
at the counterexample, so a rank bound cannot be obtained by using the
fallback branch. The attained-minimum contract exposes the proper semantic
bridge instead of treating the rank as an unexplained number.

`HasScaledIntegerCertificate` asks for all entries of two natural-valued
matrices and positive column denominators, then asserts the entire matrix
identity after real casts. The natural type on the certificate entries
ensures nonnegativity; it does not change the domain of the rank definition.
`scaledRightFactor V d` divides each V column by the corresponding positive
real denominator. The scaling contract explicitly requires that named factor
to be nonnegative and have the prescribed product.

I inspected the actual elaborated type of each export, including all implicit
indices and instances, rather than accepting the comments as the statement:

| Export in `NLA.NR03` | Assessment |
|---|---|
| `cMatrix_nonnegative` | Every entry of every C_n is a real nonnegative square. |
| `boolVec_seven_card` | All 128 Boolean vectors, without restriction. |
| `nonnegative_rank_attained_minimal` | Attained rank and minimality over every real factor width, under explicit inhabitation. |
| `rank_le_of_factorization` | One actual factorization bounds the genuine minimum. |
| `scaled_certificate_gives_factorization` | Positive denominators and full scaled identity give the explicit genuine real factors. |
| `witness_scaled_certificate` | Unconditional existence of the complete 128-by-127 and 127-by-128 integer certificate. |
| `witness_factorization` | Unconditional real width-127 factorization of the complete C_7. |
| `witness_rank_upper_bound` | The actual nonnegative rank is at most 127. |
| `witness_not_full_rank` | Strict inequality against the required `2^7`. |
| `not_targetStatement` | Negation of the entire original universal assertion. |

No final export assumes certificate correctness, a rank bound, or the desired
negative conclusion. A later implementation using mask-indexed data still
must prove its Boolean indexing bridge in Lean; the current target already
uses Boolean vectors directly and hides no such assumption.

## Independent checks actually performed

I ran the supplied statement-typecheck script independently, using only the
existing MI-22 dependency objects and fresh private output. Lean 4.33.1
elaborated Definitions and Challenge successfully. The script checked all ten
pinned dependency revisions and clean tracked sources. I then ran a separate
`Inspect.lean` to print all definitions, all ten theorem types, and transitive
axioms. `BoolVec` has no axioms, the other eleven definitions have only
`propext`, `Classical.choice`, and `Quot.sound`, and each of the ten Challenge
placeholders has those three plus `sorryAx`. This matches the declared
statement phase. Raw invocations, exit codes, and output are recorded in
`typecheck-EVIDENCE.json`, `typecheck-Definitions.log`,
`typecheck-Challenge.log`, `inspection-command.json`, and `types-axioms.log`.

I wrote and ran `independent_checks.py`; it imports neither the source
certificate generator nor its verifier. Its exact integer audit checked all
16,384 scaled matrix entries, including 5,103 zero targets and 11,281 positive
targets. It also checked the 128 Boolean/mask correspondence, all 16,384 dot
product/intersection correspondences, all 32,512 entries of W and V against
the source's four atom-family formulas, and all denominators. The dimensions,
2,648 W nonzeros, W maximum 2, V maximum 36, and denominator set
`{1,4,9,16,25,36}` agree with the numerical targets. These are independent
informal checks, **not** a Lean proof or a trusted proof oracle.

The source's polynomial identity and four-family contribution argument are
consistent with the full target. A future proof may avoid expensive dense
enumeration by proving this generic identity and the counting bridges, or use
the exact sparse certificate. No interval arithmetic is needed. Such
optimizations must retain every matrix entry and index correspondence.

The pinned Mathlib `Nat.find_spec`, `Nat.find_min'`, and `Matrix.mul_apply`
definitions support the claimed minimum and product meanings; the inspected
source excerpts and hashes are in `mathlib-api-inspection.json`. The package
uses small direct imports, with no new trusted abstraction. The
Schiffer/Forsythe metadata accurately labels them structural examples and does
not claim to import their theorems. LeanCert is pinned for the later kernel
workflow; no LeanCert calculation or assertion has yet proved these contracts.

## Required metadata correction

`formalization.yaml`, `sources[2].relationship`, is **`related`**. The pinned
v0.4 schema does not allow that value in a source relationship. My actual
PyYAML/jsonschema run rejects it with:

> 'related' is not one of ['', 'formalizes', 'adapts', 'independently-proves', 'background', 'other']

Use `background` for the retained Colbrook partial result (or the allowed
`other` value), then rerun schema validation and record the corrected file
hash. This is the sole requested package change. The full validation result
and exact command are in `independent_checks.json` and
`independent-checks-command.json`. The check deliberately records the failure
instead of silently normalizing the invalid field or claiming a schema PASS.

All ten Comparator export names match all ten YAML result entries and all ten
Challenge declarations. `sorry_count: 10`, zero definition holes, the stated
axiom lists, `whole_problem_verified: false`, and pending-review prose are
honest for the inspected phase. The source-map SHA-256 values and Git blob
IDs match the actual immutable sources. The license is present. George
Stepaniants receives formalization credit with Caltech and department, no
email; Sidney Holden retains authorship of the complete mathematical result
and Matthew J. Colbrook retains the earlier partial-result credit.

## Scope and remaining gates

I made no candidate edits and wrote no mathematical Lean proof. Raw logs
contain local absolute paths as execution evidence; the package's documented
reproduction command accepts an existing dependency root and generates a
fresh temporary output prefix. No dependency download, Lake invocation,
shared cache rebuild, or candidate object file was used. Pre-existing
dependency objects were reused, not independently rebuilt or authenticated by
a full kernel replay in this review.

This report approves only the mathematical statement boundary identified
above. It does not establish any of the ten theorems. Actual proof
implementation, LeanCert kernel checks, two independent final reviews,
transitive axiom checks without `sorryAx`, and a genuine Linux Comparator run
remain required. No problem should be counted as newly Lean verified from
this report. `EVIDENCE-MANIFEST.json` binds the compact retained source,
inspection, check, and report files; private generated `.olean` files are
deliberately not included in that evidence bundle.
