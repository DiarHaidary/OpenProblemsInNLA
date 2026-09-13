# NR-03 implementation checkpoint

**Status:** private source-only canonical packaging draft; the bridge-only
conditional Linux diagnostic passed, while the complete graph remains
uncompiled, unverified, and not countable.

**Author/formalizer:** George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena,
California, USA. No email is published. The complete mathematical result is
attributed to Sidney Holden; Matthew J. Colbrook's earlier partial result is
retained as historical context.

The active implementation is a 58-module graph based on the reviewed
development driver at `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`: five
foundational modules, one certificate-bridge support module, 48 sequential
literal-row modules, `FamilyIdentities`, the bridge-backed `Certificate`,
`Rank`, and the public `Solution` export assembly. The exact seven-path overlay
is recorded in `certificate-bridge/INTEGRATION-PATHS.json`; all other base
implementation bytes remain unchanged. Historical probes, optional structural
drafts, generators, and CI logs are not active inputs.

The three finite source-family identities cover all 128 rows against all 128
columns. They are represented by 384 literal row lemmas in 48 blocks (16
blocks per family, eight rows per block), with the block import chain enforcing
sequential compilation. The complementary core family is handled by its
structural identity. This is complete 128-by-128-by-3 coverage, not a selected
submatrix; see `FULL-ROW-COVERAGE.md`.

The public target remains over every `Fin n → Bool` and real subtraction. The
integer helper `natSquareOneMinus` uses guarded natural subtraction only in the
finite certificate arithmetic, with `natSquareOneMinus_cast` proving its exact
agreement with the real square. The corrected `CertificateData.lean` header
records that the retained table is supplementary data and is not imported as a
formal bridge or correctness oracle.

No local Lean/Lake/cache process was run for this package. The six-module
bridge-only Linux diagnostic passed under unchanged resource limits; its actual
receipts are in `reviews/bridge-diagnostic/`. The authoritative complete-graph
Linux LeanCert/default-kernel/Comparator run, raw logs, sandbox controls, and
two independent final proof reviews remain pending. No solved-status claim is
made.
