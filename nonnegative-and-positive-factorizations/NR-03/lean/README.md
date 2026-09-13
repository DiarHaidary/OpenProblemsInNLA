# NR-03 Lean proof candidate

This package contains the statement boundary and a **source-only modular
proof candidate** for NR-03, “Full nonnegative rank of the quadratic
correlation matrix.” The certificate bridge has passed a bounded Linux
conditional diagnostic; the complete 58-module graph remains pending its
canonical verification gates. It is authored by **George Stepaniants**, Department of
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

## Statement contracts and candidate proof

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

The active implementation is the 58-module graph at reviewed development
commit `3b3eb8f3fa384e4b3bf640d48bca87cf40db9565`. It includes the exact
seven-path certificate-bridge overlay on `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`, recorded in
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
`native_decide`, or custom axiom token. This is a source-only candidate: it has
not yet passed the authoritative Linux LeanCert/default-kernel/Comparator
harness or independent final proof reviews. A separate bridge-only Linux
diagnostic passed for the six lightweight modules; its receipt is retained in
`reviews/bridge-diagnostic/`. That conditional result does not establish the
complete graph, the ten public exports, or a Comparator/default-kernel pass.
It does not add to the Lean-verified count or change the existing Solved status.

## Checks and reproduction boundary

The bridge-only diagnostic receipt is retained in
`reviews/bridge-diagnostic/RECEIPT.json`; its raw artifact and full logs remain
separately hash-bound in the recorded Linux run. It is not a substitute for the
canonical verifier described in the [shared guide](../../../docs/lean/README.md).

The existing statement-only check may be run with pre-existing pinned objects:

```bash
NR03_DEP_ROOT=/path/to/existing/.lake/packages \
  python3 verification/statement-typecheck.py
```

That script checks the statement boundary and writes fresh logs outside this
package. It is not a proof or a Linux Comparator run. No local Lean/Lake build
was run to prepare this draft, and no build artifacts or dependency caches are
included.

The unchanged foundations, all 48 row modules, `FamilyIdentities.lean`,
`Rank.lean`, `Solution.lean`, the frozen boundary, and all pinned project files
remain byte-identical to the recorded source commit. The overlay replaces only
`NLA/NR03/Certificate.lean` and adds `NLA/NR03/CertificateBridge.lean` in the
active graph; the exact seven development paths and their hashes are retained
in `ACTIVE-MODULE-MANIFEST.json` and the `certificate-bridge/` provenance
records. The development generator and compilation driver are provenance
inputs only; they are deliberately not advertised as runnable from this
canonical draft because their relative paths and remote-only controls are
development-specific. The [GitHub workflow](../../../.github/workflows/lean-verification.yml)
configures Linux isolation and runs the shared verifier from the repository root:

```bash
tools/lean/verify.sh nonnegative-and-positive-factorizations/NR-03/lean \
  "$RUNNER_TEMP/nla-lean-tools"
```

That verifier must compile the full active graph and check the pinned LeanCert
dependencies, default kernel, Comparator declarations, permitted axioms, and
sandbox controls before this candidate can be accepted.

## Source identity and status

The canonical mathematical source base is commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`. Exact source correspondence and
authorship are recorded in `SOURCE_MAP.md`, `NUMERICAL_TARGETS.md`, and the
retained two statement-referee records.

The active-module manifest records every source hash, the exact bridge
overlay, the excluded historical development material, the conditional bridge
diagnostic, and the fact that full canonical verification is still pending.
The candidate remains `whole_problem_verified: false` in `formalization.yaml`.

Current package hashes are recorded in `reviews/proof-candidate-hashes.json`.
The bridge diagnostic receipt retains its historical package metadata binding;
the inventory records the later documentation transition. Its checked Lean
sources are unchanged.
