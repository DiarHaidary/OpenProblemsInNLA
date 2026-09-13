# RA-20 generic-data intersection helper

**Contract 9 is proved and available for Count integration** as
`NLA.RA20.generic_data_intersection_proved` in `NLA/RA20/Generic.lean`.
The source is frozen at SHA-256
`47676372aa8e028a2c12bf6c23951b0edf5b7404a18abd24487d36399b7fb007`.
No implementation change was needed during this inspection.

The result quantifies over the original arbitrary polynomial `q : Poly 3`.
If `q` has a nonzero value at some symmetric matrix, it also has a nonzero value
at symmetric data whose three off-diagonal entries are all nonzero. Diagonal
entries remain unrestricted. The proof parametrizes the full symmetric matrix
space with six independent complex coordinates and reconstructs every symmetric
matrix from them. Renaming `q` along this parameterization gives a nonzero
polynomial; multiplying by the three off-diagonal coordinate polynomials remains
nonzero. Mathlib's evaluation extensionality over the infinite integral domain
ℂ then supplies a point avoiding both zero sets. Genericity, density or a
nonvanishing conclusion is not introduced as an extra premise.

This is exact symbolic polynomial reasoning. LeanCert's real kernel trust
assertions inspect the proof dependencies; no artificial interval or numerical
certificate is needed. The helper imports frozen Definitions and primary
Mathlib polynomial results only, independently of Algebra, Smooth or Differential.

## Authorship, authorization and scope

Implementation: `/root`, under the pre-edit `gate-and-ownership.json` receipt,
SHA `568261f301cfe9868ee548316bc7fadbe465383c4272fa7dcc81475bd7c26d6d`.
The original statement gate is
`9fe55d622e50390cb3ed439989b9393455fa48eb50d42d84fb33c20fd8c883f3`.
Both accepted statement reviews preceded the helper implementation.

Packaging and fresh inspection: `/root/mf16_final_referee`, with a separate
pre-work `packaging-inspection-role.json` receipt,
SHA `bb1446bc02d222df4d56c018ece0dfff4766d3d329af9bc5f629fd2bb9465f6f`.
The inspector is already an RA-20 Differential proof contributor. This role
therefore adds **no independent final mathematical approval**. Two fresh
independent final referees are still required for the completed RA-20 project.

Formalization author: George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA, with AI assistance. No personal email is included. The original negative
resolution retains the repository's Codex automated maintainer audit attribution;
the original conjecture is due to Kubjas, Sodomaco and Tsigaridas.

## Actual commands and diagnostics

The successful author attempt is `attempt-wwp2k0kt`: **two separate Lean commands**
compiled Definitions and Generic. Its Generic build produced **four actual
LeanCert kernel assertions and standard-three axiom reports**, not one combined
command. The attempt's complete result hash is
`fd5346379e4779205a8c8fe7ea1acc250ce1baa77806c35fb3bd8a810876dffb`.

The earlier `attempt-dueo3o_u` is retained in full. Definitions compiled
successfully, then Generic failed on a matrix-index simplification type mismatch;
it also emitted a deprecated `push_neg` warning. LeanCert rejected the failed
main theorem's temporary sorry dependency. The final source uses `push Not` and
an explicit definitional `change`, and compiles without warnings. Partial
reports from the failed module are not counted as successful helper acceptance.
Thus the two author attempts comprise four Lean commands: three succeeded and
one failed; the complete successful attempt alone comprises two commands and
four reports.

The packager then used one new, initially empty private prefix to compile
Definitions, the unchanged Generic, a namespace-only diagnostic copy of the
frozen Challenge, and an inspector: **four successful direct-source commands**.
The actual theorem's elaborated type equals frozen contract 9. The inspector
traversed the actual types and bodies of **15 safe project declarations** and
required **13 material dependencies**, including reconstruction, renaming,
`MvPolynomial.funext`, coordinate nonvanishing and the actual GenericData
definition. No admitted reference, unsafe or partial project declaration,
nonstandard axiom or native-compiler axiom is admitted into the proof closure.

The fresh Generic build supplies four trust reports and the inspector supplies
one more: **five packager reports**, separately from the author's four. Every
successful report contains only `propext`, `Classical.choice`, and `Quot.sound`.
The diagnostic reference admissions are intentional and cannot occur in the
actual helper dependency traversal. All source snapshots, command identities,
raw logs, runner snapshots and failed author evidence remain intact.

The original author attempts recorded before/after checks of all ten exact
MI-22 dependencies. The packager's post-inspection check also found all ten
pinned revisions and source trees unchanged; a separate packager pre-inspection
pin sample is not claimed. Shared sources and artifacts were read-only, with no
Lake invocation, dependency copy, cache download or mutation. All checks here
were local macOS source builds, not Linux or Comparator verification.

## Freeze and handoff integrity

All 68 frozen statement-stage project inputs, 16 original source snapshots and
their Git blob identities remain exact. The complete three prior statement
inventories were rechecked. No frozen definitions, Challenge, canonical page,
Git state, metadata or whole-project proof freeze was edited. The original
author runner's object hashes/removal records are retained; the packager's eight
own completed objects were hash-recorded and removed separately, without
changing another owner's prefix or shared cache.

`validation.json` binds the actual counts and checks. `EVIDENCE-MANIFEST.json`
binds all files in this helper evidence directory, the unchanged helper source,
and its full frozen statement/prior-review input closure. Only that exact outer
manifest is excluded from its own inventory; all nested manifests are retained.
`verify_seal.py` rechecks the complete seal without compiling anything.

Full RA-20 integration and its remaining contracts, two independent final
mathematical reviews, actual Linux default-kernel replay, Lean4 Comparator and
controls, operational acceptance and publication remain pending. This is a
scoped helper handoff only.
