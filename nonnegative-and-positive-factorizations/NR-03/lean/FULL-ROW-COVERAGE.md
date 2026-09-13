# NR-03 full-row coverage

This source-only draft retains the complete finite family obligations needed by
the n = 7 certificate. It does not narrow the matrix to selected rows or
columns.

The active graph has three explicit finite source families:

- `Singleton`: 128 literal row lemmas, each universally quantified over all
  128 `Mask7` columns;
- `Pair`: 128 literal row lemmas, each universally quantified over all 128
  `Mask7` columns;
- `Four`: 128 literal row lemmas, each universally quantified over all 128
  `Mask7` columns.

Thus the graph contains **128 × 128 × 3 = 49,152 ordered row/column-family
obligations**, represented by **384 literal row lemmas**. Each family is split
into 16 modules of eight rows, for **48 sequential block modules** total. Each
block imports its predecessor; `FamilyIdentities` imports the final `Four`
block and assembles the three complete family identities. The complementary
core family is proved structurally in `Core.lean` and is included in the full
127-atom decomposition.

The development driver at source commit
`fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f` selected the original 57-module
graph. The private package adds one reviewed certificate-bridge support module
and replaces the Certificate wrapper through the exact seven-path overlay
recorded in `certificate-bridge/INTEGRATION-PATHS.json`; it therefore has 58
active modules. The row modules copied here are byte-identical to the base
commit. Probe
files, optional structural drafts, generators, and development CI records are
excluded from the active package. Their exclusion changes compilation
organization only; it does not remove any target row, column, family, or
matrix entry.

This file records source scope, not a compilation result. The authoritative
Linux run must still elaborate every block and the final exports under the
pinned LeanCert/default-kernel/Comparator and sandbox controls.
