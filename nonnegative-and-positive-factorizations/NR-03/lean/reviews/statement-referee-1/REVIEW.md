# NR-03 independent statement review 1

Reviewer: OpenAI Codex primary agent `/root` (AI), 13 September 2026. I did
not author the NR-03 package. This review applies `docs/lean/REVIEW.md`, the
repository's Tau Ceti adaptation, against canonical commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`.

**Mathematical statements: APPROVE. Package: one metadata correction required.**
The verdict concerns statements only and establishes no mathematical proof.

I read the entire canonical problem and the complete Holden TeX proof and
Markdown proof, then inspected all twelve candidate definitions and all ten
Challenge types, including their actual elaborated types and transitive
axioms. The exact file identities are recorded in `checks.json`.

The index type is every function `Fin n → Bool`. The dot product is the real
sum of the original zero-one products and subtraction in the square is real,
so none of the entries with intersection above one are lost. Factorizations
quantify arbitrary real nonnegative matrices and the minimum is a genuine
`Nat.find` over all feasible widths. The totalization outside the feasible
case is expressly separated; the n=7 result must first construct a genuine
factorization, so it cannot exploit that branch. The generic attained/minimal
and rank-upper-bound contracts expose the full minimum semantics for every
feasible matrix, including empty dimensions. All original matrices are
nonnegative squares and admit finite identity factorizations mathematically.

The scaled-integer certificate contract requires actual natural W and V,
all 128 Boolean rows and columns, 127 atoms, positive integer denominators,
and every real-cast scaled product identity. The separate scaling theorem
retains those same witnesses and names the actual divided right factor.
No certificate, Python checker, positivity, or correctness claim is an axiom.
The final theorem explicitly negates the original universal assertion, using
the admissible dimension seven. Neither exact rank 127 nor the stronger
all-n bound or smallest counterexample dimension is claimed.

The source's complementary-pair, singleton, pair and four-set construction
has a complete exact polynomial-identity proof. Its singleton-column and
zero-column cases account for the positive denominator convention. I also
independently multiplied the supplied integer factors using sparse left rows
and verified all 16,384 required entries against integer mask intersection
counts, without importing the source generator or verifier. This confirms
source data only; eventual Lean code still has to prove any mask/Boolean
bridge and every product identity or an equivalent generic family theorem.

I independently ran the direct statement checker with all ten clean pinned
dependencies and a fresh private output prefix, then ran a separate Lean file
printing all twelve definition and ten contract types/axioms. Both succeeded.
There are exactly ten intentional Challenge placeholders. Definitions have
only the standard foundational axioms (the BoolVec abbreviation has none);
Challenge declarations additionally contain `sorryAx`, as disclosed. No Lake,
shared-cache build, download, Linux run or Comparator run was performed.

Holden's complete mathematical authorship, Colbrook's historical partial
credit, and George Stepaniants's separate formalization credit and Caltech
CMS affiliation are correctly distinguished. No George email is included.
The statement-only status, pending review, toolchain and source/example pins
are honestly documented. No Solution module or completed formalization is
present.

## Required metadata correction

The pinned v0.4 JSON schema rejects `sources[2].relationship: related`.
Replace that value with `background` (or `other`). I ran the pinned schema
validator with PyYAML/jsonschema and found this one error; raw output is in
`metadata-schema.json`. This changes no mathematical boundary and can be
closed by a coordinator schema rerun while retaining the present report.

## Reviewed mathematical boundary

- `NLA/NR03/Definitions.lean`: `5157fd499d2f63d218012f96bee43f30e5f57e5a2353fde13878af46d30fda04`
- `Challenge.lean`: `4f1764cf9c604f33ed6f285e83ca32ebd1ae1fb1fd8f763a1c4a719ef068c335`
- `NUMERICAL_TARGETS.md`: `817a0978869dcaf2bb918d846e4143df480665e5db3bc841cf4070bd3f683c42`
- `SOURCE_MAP.md`: `68eb2be2121b176ad13d036b50e03146539a9c7fe1e9ece9b55fdae761d34ebf`
- `comparator.json`: `ea1cea90b8e25535a31dca7fc620494ded851587609bb1473c651d07757f40bd`

The initial YAML hash and all source identities are in `checks.json`.
`raw-commands.json`, `typecheck-EVIDENCE.json`, `actual-types-axioms.log`,
and `statement-typecheck.log` retain the commands and outputs I actually
examined. This is not external human peer review or proof acceptance.
