# IS-02 independent final mathematical review 2

Reviewer: OpenAI Codex primary agent `/root` (AI), 13 September 2026. I did
not implement this proof. I independently reviewed the complete canonical
README and solution manuscript, all definitions and nine Challenge contracts,
all 1,354 implementation lines and the Solution wrappers, under the
repository's Tau Ceti adaptation in `docs/lean/REVIEW.md`.

**APPROVE the complete mathematical proof at the hashes below.** I found no
missing original-target assumption, hidden certificate, circular bridge, or
incorrect proof step. Naming and documentation cleanup has been requested and
must receive a narrow final recheck; actual Linux Comparator remains pending.
This report does not promote the canonical problem or increase the count.

## Whole-target correspondence

The target preserves arbitrary n >= 4 and arbitrary real symmetric entrywise
nonnegative matrices with row sums one. Positive trace is explicit. Spectral
uniqueness quantifies every real competitor and equality of eigenvalues with
multiplicity, encoded by characteristic polynomials. The generic bridge
proves the characteristic polynomials split for real symmetric matrices and
reconstructs their equality from equal real root multisets using monicity.
It does not discard zero or repeated eigenvalues. Simultaneous permutation
of indices is exactly the original permutation similarity relation.

The locus contains all three original segment families with every genuine
extreme point of the symmetric stochastic polytope. The vertex definition
is the ordinary nontrivial-convex-combination condition, not a replacement
by permutation matrices. The canonical real 4-by-4 witness, trace one, and
spectrum {1,1,0,-1} are implemented entrywise. The complete counterexample
and explicit universal negation are both exported, without hypotheses
assuming uniqueness, nonmembership, or the desired conclusion.

## Actual proof path

The exact characteristic-polynomial calculation uses the displayed block
matrix and diagonal comparison. The imported finite-dimensional eigenvalue
API gives a nonzero real -1 eigenvector for every isospectral competitor;
the characteristic-polynomial next coefficient transfers trace one.

Symmetry and stochasticity give column sums one as well. The expanded double
sum of B_ij (z_i+z_j)^2 is zero by the eigenvector equation. Each summand is
nonnegative, so every individual summand vanishes. This is a formal exact
identity and order argument, not a sampled certificate. On the eigenvector
support, diagonal entries vanish; entries crossing its support vanish too.

The implementation exhausts all sixteen support patterns on four indices.
Empty support contradicts the nonzero eigenvector; full support contradicts
trace one. Single support forces a zero row. Triple support forces the
remaining three-by-three block to have all off-diagonal entries one half,
whose eigenvector equations force the purported support to vanish. For each
of the six two-point supports, row sums and trace force the swap block and
the complementary all-one-half block; explicit permutations identify the
witness. The proof therefore covers every arbitrary-real competitor, without
assuming graph irreducibility, rational coordinates, or a support pattern.
This finite support argument validly replaces the manuscript's general
component/bipartite classification and avoids unnecessary infrastructure.

The witness is the midpoint of two distinct symmetric stochastic matrices,
so it is not a vertex. A zero diagonal entry forces any representation on
an identity-to-vertex segment to its vertex endpoint. A zero off-diagonal
entry similarly forces a flat-matrix-to-vertex representation to its vertex
endpoint; nonnegativity and 0 <= t <= 1 are retained. Both contradict the
explicit nonvertex proof. Unequal diagonal entries exclude the identity/flat
segment. The final union elimination covers all three families.

## Independent mechanical checks

I freshly ran `verification/proof-typecheck.sh` with pinned Lean 4.33.1,
IS02_DEP_ROOT set to the existing MI22 dependency objects, and a fresh
private output prefix. It exited zero. Raw output, including the harmless
unused-tactic/simp warnings, is retained in `local-compile.log`; it is not
silently presented as a warning-free build. All nine exported LeanCert
`#assert_trust kernel` checks and printed transitive axiom reports passed.

I separately verified all ten dependency source heads and clean tracked
checkouts, then inspected actual elaborated types and transitive axioms of
the target definitions and all nine public exports against the fresh output.
`commands.json`, `CHECKS.json`, and `actual-types-axioms.log` retain the actual
commands, source hashes, counts and results. Public exports have only
propext, Classical.choice and Quot.sound. No Challenge module is imported by
Solution. No Lake, dependency download, shared-cache write, default-kernel
export replay or Linux Comparator run was performed by this local audit.
Pre-existing dependency objects were reused, not freshly rebuilt here.

## Presentation requests and publication limits

Production implementation helpers still have exploratory `test_*` names,
`open Polynomial` is repeated, and the wrapper has a stray initial indent.
Use descriptive helper names, brief support-case comments and ordinary
formatting without changing the approved statements or mathematical proof.
Clarify automation metadata: exact arithmetic is discharged by norm_num,
ring and linear/nonlinear arithmetic tactics; LeanCert audits kernel trust.
The local reproduction helper should actively verify the ten clean manifest
pins and retain its raw invocation records. These are presentation and
reproducibility requests, not substantive mathematical gaps. Preserve the
old files/evidence and provide an identifier mapping and narrow change review.

The original Colbrook mathematical authorship and George Stepaniants's
separate formalization credit, Caltech and Computing and Mathematical Sciences
department are retained. No George contact email is needed. This is an
independent AI-agent review, not human peer review or Tau Ceti endorsement.
The original target remains Solved until the remaining reviewed publication
and genuine Linux verification gates pass.

## Reviewed immutable proof inputs

- proof_sha256: `f108eb9d89a524514bd24b6cc379bc500b03d00143b49b14938aa75cbe72bde8`
- solution_sha256: `8cf1db571f72a181107bd5cbea8910bc2fd4ff6266bbea2218783ea88cdba545`
- definitions_sha256: `4d2d2914838a91a30f12b1e20490c957d2b4e943eb2a51f7415cc2fedd0bf321`
- challenge_sha256: `d72b58465096cb7049d453206727837eb53b87845a5d8faa97d88f5fb9244cff`
