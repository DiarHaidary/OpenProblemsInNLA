# IE-05 exact certificate synthesis fix

**Tested fix:** add the two computable, module-level local instances in
`DECIDABILITY-FIX.patch`, and use `unfold UnitLower UpperTriangular` before the
existing `decide +kernel`. The complete copied module then proves all three
original certificate theorems, without any changed hypothesis, numerical data,
statement, native execution, or new axiom. The live mathematical source was not
edited by this diagnostic task.

The two instances specialize integer equality at the actual two-index matrix
entries. Their values are the core `Int.instDecidableEq`, which is defined as
`Int.decEq` in the pinned Lean source. They are locally registered for typeclass
search, so importing the resulting module does not globally install these
specialized instances.

The coordinator's retained synthesis trace shows failure when typeclass search
tries to lift the general integer equality instance through both `Fin 8`
binders. Direct closed full-matrix Gram and LU equalities already worked. The
specialized entry instances remove that failed higher-order matching step;
there is no need to expand the matrix products or enumerate all indices with
`fin_cases`.

A focused first attempt supplied the same instances using tactic-local `letI`.
This made synthesis and elaborator reduction succeed, but `decide +kernel`
rejected its auxiliary lemma because the instance proof still contained local
free variables. The pinned `Lean/Elab/Tactic/Decide.lean` explains this behavior:
`preprocessPropToDecide` zeta-reduces the proposition, while `doKernel` passes the
synthesized proof to `mkAuxLemma`. Module-level declarations yield a closed
instance expression and avoid that failure. All code still runs through the
ordinary kernel decision path.

A second attempt using three module-level instances passed. A final focused
check removed the redundant inequality instance and passed again. Only the two
equality instances remain in the returned patch. All three diagnostic attempts,
including the local-instance/free-variable error, are retained intact.

The final run is `attempt-jjksz6of`: fresh Definitions and the complete copied
certificate module both returned zero in **8.454 seconds**. The mathematical
copy emitted no warnings, and all three `#assert_trust kernel` commands and
three printed axiom reports passed with exactly `propext`, `Classical.choice`,
and `Quot.sound`. The complete factor certificate, the 64+204 entry certificate,
and the rational gap are all present; this is not a test of an isolated
surrogate proposition. The frozen contract headers remain unchanged.

The check used Lean 4.33.1 on macOS with the ten exact clean dependency pins and
nine existing dependency object directories read-only. No Lake invocation,
download, cache copy, or shared-cache write occurred. Private generated objects
were hashed and removed. All 733 frozen inputs and the complete existing
GEPP/LU/QR seals were preserved. The result is proof-contribution diagnostics,
not an independent final mathematical review or actual Linux Comparator result.

The copied complete source is `PatchedCertificates.lean`; the machine-readable
handoff binds its exact hash, the unified patch, the successful run, and the
primary implementation-source hashes. George Stepaniants retains the existing
full Caltech department affiliation and mathematical credit in the source;
no contact email was added.
