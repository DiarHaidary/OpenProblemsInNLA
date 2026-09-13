# IE-05 Lean statement draft

**Draft only: no proofs, independent approvals or Lean verification claim.**
The canonical problem remains Solved by its existing informal counterexample.
This separate directory prepares the complete original statement for review.

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
The mathematical counterexample and substantial AI assistance are attributed
as in the source; John Peca-Medlin retains the conjecture attribution.

Read [NUMERICAL_TARGETS.md](NUMERICAL_TARGETS.md),
[SourceCorrespondence.md](SourceCorrespondence.md),
[Definitions.lean](NLA/IE05/Definitions.lean) and
[Challenge.lean](Challenge.lean) together. The 17 intentional Challenge holes
specify complete generic pivot/QR/supremum bridges and the minimized exact
order-eight certificate. They prove nothing.

The source-only macOS check uses the campaign's ten pinned read-only package
sources, with existing objects for the imported dependencies, and a fresh own
prefix. `Cli` is a tooling dependency with no generated object directory in
this cache and is not imported by these statements. No Lake, download, cache
copy or shared-cache mutation is used. Run in the existing campaign environment:

```
python3 verification/statement-development/check_statements.py
python3 verification/statement-development/reconstruct.py
```

The first checks only elaboration and definition dependency trust; the second
is an exact Python arithmetic diagnostic. Neither proves the Challenge or
runs Linux Comparator. The checker retains each source snapshot, raw failure
and successful output, exact dependency identities and generated-object cleanup
hashes. No `Solution.lean` or mathematical implementation exists.

The draft is not frozen. A coordinator review followed by two independent
statement approvals and an explicit proof gate is required before implementation.
Canonical pages, original source files, permanent IDs and Git history are
untouched. No `formalization.yaml`, publication commit or PR is created here.
