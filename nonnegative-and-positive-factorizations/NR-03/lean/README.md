# NR-03 Lean verification

This package contains the statement boundary and the complete 58-module
Lean proof for NR-03, “Full nonnegative rank of the quadratic correlation
matrix.” The canonical Linux LeanCert, Comparator, default-kernel and sandbox
gates passed at the immutable revision f664d07e82aaa60bc9c78dd1946e763168c5c530. It is authored by **George Stepaniants**, Department of
Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA. ChatGPT assistance is disclosed.
The complete mathematical negative result is by **Sidney Holden**, Center for
Computational Biology, Flatiron Institute, Simons Foundation. The earlier
partial result by Matthew J. Colbrook is retained in the canonical problem
page and is not replaced by this formalization.

## Exact statement

`NLA.NR03.cMatrix n` is indexed by the full type `Fin n → Bool` on both sides
and has entry

```text
(1 - sum i, (a i as Real) * (b i as Real)) ^ 2
```

The subtraction is in `ℝ`; dot products larger than one remain part of the
prescribed matrix. `targetStatement` is exactly
`∀ n, 3 ≤ n → nonnegativeRank (cMatrix n) = 2 ^ n`.

`nonnegativeRank` is the minimum natural width of a factorization through
real entrywise-nonnegative matrices. Its definition is totalized with value
zero only when no finite factorization exists; the Challenge contracts expose
the attained-minimum and minimality semantics under the explicit existence
hypothesis. This is the original rank definition, with no restricted support,
rational-only, or ordinary-rank replacement.

## Statement contracts and complete proof

The package retains the ten deliberate contracts in `Challenge.lean`:

1. entrywise nonnegativity of every `cMatrix n`;
2. cardinality `Fintype.card (BoolVec 7) = 128`;
3. attained-minimum and minimality of `nonnegativeRank`;
4. the upper-bound bridge from a real factorization to the minimum;
5. the denominator/scaling bridge from an integer certificate to real factors;
6. a complete scaled integer certificate for `cMatrix 7` at width 127;
7. the resulting real width-127 factorization;
8. `nonnegativeRank (cMatrix 7) ≤ 127`;
9. strict failure of the claimed value `2^7 = 128`;
10. negation of the complete universal target at `n = 7`.

The accepted implementation is the 58-module graph at immutable proof
commit `f664d07e82aaa60bc9c78dd1946e763168c5c530`. It includes the exact seven-path certificate-bridge
overlay on `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`, recorded in
[`certificate-bridge/INTEGRATION-PATHS.json`](certificate-bridge/INTEGRATION-PATHS.json).
It has five foundational modules, one certificate-bridge support module, 48
sequential literal-row blocks, and four assembly/export modules. The row coverage is complete; see
[`FULL-ROW-COVERAGE.md`](FULL-ROW-COVERAGE.md) and
[`ACTIVE-MODULE-MANIFEST.json`](ACTIVE-MODULE-MANIFEST.json). The graph keeps
all Boolean vectors in the public matrix and proves the mask correspondence
before consuming the finite family identities. It does not narrow the target
to selected rows or columns.

The real target uses real subtraction exactly. Some finite integer helper
lemmas use guarded natural subtraction; the proof includes the explicit cast
identity `natSquareOneMinus_cast` showing that this helper agrees with the
corresponding real square before it is used in the certificate bridge. The
retained `CertificateData.lean` table is supplementary comparison data; the
active proof does not import it or treat it as a correctness premise.

`Challenge.lean` intentionally retains the ten statement contracts as the
Comparator boundary, so its bodies contain `sorry`. The active `Solution.lean`
root supplies all ten corresponding theorem exports and contains no `sorry`,
`native_decide`, or custom axiom token. The canonical Linux run
[canonical Ubuntu job 103799711659](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34785341662/job/103799711659) passed the complete graph, all ten
Comparator identities, LeanCert kernel assertions, the default kernel and the
sandbox/negative controls. Every public export reports only `propext`,
`Classical.choice` and `Quot.sound`. Raw receipts and the two final reviews are
retained in [canonical raw evidence](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/codex/lean-nr03-verification/nonnegative-and-positive-factorizations/NR-03/lean/verification/linux-2026-09-13/OPERATIONAL-REVIEW.md),
[final referee 1](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/codex/lean-nr03-verification/nonnegative-and-positive-factorizations/NR-03/lean/reviews/final-referee-1/REVIEW.md) and
[final referee 2](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/codex/lean-nr03-verification/nonnegative-and-positive-factorizations/NR-03/lean/reviews/final-referee-2/REVIEW.md).

## Checks and reproduction boundary

The complete canonical evidence is retained in
[canonical raw evidence](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/codex/lean-nr03-verification/nonnegative-and-positive-factorizations/NR-03/lean/verification/linux-2026-09-13/OPERATIONAL-REVIEW.md), including the raw run, artifact digest,
Comparator/default-kernel output and sandbox controls. The bridge-only
conditional diagnostic remains historical provenance and is not used as the
acceptance result. Reproduction instructions and pinned prerequisites are in
the [shared guide](../../../docs/lean/README.md) and the project files below.

The existing statement-only check may be run with pre-existing pinned objects:

```bash
NR03_DEP_ROOT=/path/to/existing/.lake/packages \
  python3 verification/statement-typecheck.py
```

That script checks the statement boundary and writes fresh logs outside this
package. It is not a proof or a Linux Comparator run. No local Lean/Lake build
was run to prepare this draft, and no build artifacts or dependency caches are
included.

The active-module manifest records current hashes for every source file and
the exact bridge overlay. The frozen Definitions/Challenge/config/toolchain
boundary and all 48 row-certificate modules are preserved; any later proof
repair is listed as an exact source delta rather than silently treated as part
of the historical bridge receipt. The exact seven development paths and their
hashes are retained in `ACTIVE-MODULE-MANIFEST.json` and the
`certificate-bridge/` provenance records. The development generator and
compilation driver are provenance inputs only; they are deliberately not
advertised as runnable from this canonical draft because their relative paths
and remote-only controls are development-specific. The [GitHub workflow](../../../.github/workflows/lean-verification.yml)
configures Linux isolation and runs the shared verifier from the repository root:

```bash
tools/lean/verify.sh nonnegative-and-positive-factorizations/NR-03/lean \
  "$RUNNER_TEMP/nla-lean-tools"
```

The canonical run compiled the full active graph and checked the pinned
LeanCert dependencies, default kernel, Comparator declarations, permitted
axioms and sandbox controls. The exact run and artifact identifiers are recorded
in `formalization.yaml` and the linked evidence.

## Source identity and status

The canonical mathematical source base is commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`. Exact source correspondence and
authorship are recorded in `SOURCE_MAP.md`, `NUMERICAL_TARGETS.md`, and the
retained two statement-referee records.

The active-module manifest records every source hash, the exact bridge
overlay and the excluded historical development material. The accepted
verification record binds the complete graph to the canonical run
`34785341662`, job `103799711659` and artifact
`10326896988`; `whole_problem_verified: true` is recorded in
`formalization.yaml`.

Current package hashes are recorded in `reviews/proof-candidate-hashes.json`.
The bridge diagnostic receipt retains its historical package metadata binding;
the inventory records the later documentation transition. Its checked Lean
sources are unchanged.
