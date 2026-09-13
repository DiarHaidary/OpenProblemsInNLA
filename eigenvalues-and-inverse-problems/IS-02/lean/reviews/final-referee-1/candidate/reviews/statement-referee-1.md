# IS-02 independent statement review 1

**Verdict: approve the exact mathematical statement boundary for implementation.**

Reviewer: `/root`, OpenAI Codex AI agent and campaign coordinator. Date:
13 September 2026. I did not author or edit these IS-02 definitions or
contracts, and have not implemented their proofs. This is independent AI
statement review under the repository's adaptation of Tau Ceti standards;
it is neither human peer review nor a completed formal verification.

I read the canonical problem and entire retained mathematical solution at
upstream commit `50838e37dd793830e2cecd1055cfc7e0349490f1`, then read all
definitions, all nine Challenge signatures, the numerical targets, source
map and metadata. After forming my initial mathematical assessment, I read
the second referee's report as a cross-check. I then independently elaborated
the boundary and inspected its actual declarations and transitive axiom
lists. The direct audit here is my own separate execution, not a quotation
of that referee's PASS.

## Exact source identity

The candidate is
`/tmp/nla-lean-is02-project/eigenvalues-and-inverse-problems/IS-02/lean`.

| Approved file | SHA-256 |
|---|---|
| `NLA/IS02/Definitions.lean` | `4d2d2914838a91a30f12b1e20490c957d2b4e943eb2a51f7415cc2fedd0bf321` |
| `Challenge.lean` | `d72b58465096cb7049d453206727837eb53b87845a5d8faa97d88f5fb9244cff` |
| `NUMERICAL_TARGETS.md` | `85680cac4c689f1b0f373a60f2c4f0e3e96263fad8fb3326185afa13927e25d3` |
| `SOURCE_MAP.md` | `584f77bc097fab678a7bf969d4b060b856bb919d3bde7a843330f11d31534947` |
| `comparator.json` | `0c0af16af051b15d0b3892318738d82199f4116e5708a025653587b451bec7ed` |

`EVIDENCE.json` independently records all thirteen candidate files before
and after the audit, the original Git blob IDs, exact source hashes and
all executed commands. Candidate bytes remained unchanged.

The original README hash is
`92f7c04c5ac0be67a7f6a4efd0d2439caaf000295fa27d259e01a22368f7ae24`;
the complete mathematical solution Markdown hash is
`ae29570308b2a78678875c5e56076ce09e65cea732ce6b51142399a4b234577f`.
Both agree with the source map. The corresponding TeX sources were also
read and hashed; exact retained bytes are included in this audit.

## Fidelity and logical scope

The ambient object is Mathlib's actual real square matrix on `Fin n`.
Symmetry, entrywise nonnegativity and row sums equal to one are expressed
entrywise with no rationality, support, block, positivity-of-every-entry or
finite-enumeration restriction. The trace is the full diagonal sum.

`sameSpectrum` is equality of the actual characteristic polynomials.
This retains multiplicities. For real symmetric matrices their real root
multisets exhaust the eigenvalues and determine the monic polynomial.
The boundary explicitly requires the general theorem
`sameSpectrum_iff_realEigenvalueMultiset_eq`; both symmetry hypotheses are
present and no needed splitting theorem is assumed as an axiom. The
zero-dimensional case in this helper is harmless: both characteristic
polynomials are one. It does not enlarge the original target, whose
dimension is explicitly at least four.

`spectrallyUnique` quantifies over every competing real matrix in the same
polytope. Simultaneous relabeling is the existential permutation action
on both indices, equivalent to permutation similarity; either inverse
convention for the permutation represents the same set of matrices.
The definition does not assume the component classification, the required
uniqueness, or the desired conclusion.

The vertex definition is intrinsic extremality in that exact polytope.
For an interior segment parameter it forces its two endpoints to agree;
the convex identity then forces both to equal the purported vertex.
This is the usual definition of an extreme point. There is no replacement
by permutation matrices. Segment endpoints are included, and the locus
contains all three required families: identity to the flat matrix,
identity to any vertex, and the flat matrix to any vertex. The use of
natural subtraction in `flatMatrix` has the correct real denominator at
all relevant dimensions `n >= 4`.

The explicit four-by-four witness is exactly the submitted matrix. The
comparison diagonal is `diag(1,1,0,-1)`, and trace one and strict positive
trace are separate obligations. The final proposition is the negation of
the entire original universal implication, with no hypotheses. Its proof
must instantiate the complete counterexample at the allowed dimension
four. Thus the project has not substituted a helper identity for the
canonical target.

## Consistency with the complete source proof

I checked the logical route for the arbitrary-real competitor theorem.
The symmetric nonnegative stochastic Dirichlet identity describes the
one-eigenspace as vectors constant on support components. Multiplicity
two therefore gives two components. A component with eigenvalue minus
one has alternating nonzero equal-magnitude eigenvector coordinates,
no loops, and two sign classes of equal size by symmetry and stochastic
crossing weights. With four vertices and two components this component
has size two, as does the other. Their spectra force the swap block and
the all-halves block. This universal step is an outstanding proof
obligation, not established by the finite witness arithmetic.

For the locus exclusion the submitted midpoint of `diag(S,I_2)` and
`diag(S,S)` is a genuine nontrivial convex decomposition. A zero diagonal
entry forces the endpoint on every identity-to-vertex segment; the zero
entry at `(0,2)` does the same on flat-matrix-to-vertex segments.
On the direct identity-to-flat segment the latter entry instead forces
the identity endpoint, which is unequal to the witness. These arguments
cover all endpoints and do not classify the polytope's vertices.

All numerical data are exact rational values, so neither floating-point
experiments nor interval subdivision is needed for them. A proof may use
another verified argument for the arbitrary competitors, but it must
retain the reviewed full statement and all necessary bridges.

## Independent mechanical observations

`python3 /tmp/nla-is02-statement-referee1/audit.py` succeeded. It invoked
the actual Lean 4.33.1 binary directly, read existing dependency objects,
and wrote new objects only inside this review directory. It did not run
Lake, download dependencies or rebuild a shared cache. All ten dependency
checkout revisions equal `lake-manifest.json`, and their tracked source
trees are clean. This checks the dependency source identities but is not
a claim that their existing objects were rebuilt from source in this audit.

Definitions, Challenge and the separate inspection script each elaborated
with exit code zero. Challenge has exactly nine deliberate `sorry`
warnings. All eighteen definitions use only the standard three axioms;
all nine placeholder theorems additionally use `sorryAx`. The raw logs and
the actual printed declarations are retained. This is statement checking
on macOS, not a Linux Comparator run or a proof certificate.

## Packaging corrections and remaining gates

Before publication correct the stale `NLAKE04` root name in the manifest,
the phrase “eight bodies” in the typecheck note, and the README's promise
of source-recheck commands absent from its source-map file. These are
nonmathematical corrections and do not block implementation of the
unchanged approved boundary. Metadata must continue to disclose the
nine placeholders; its current `axioms: []` is not the observed audit.

Only implement after the second independent statement approval is recorded
and the boundary is frozen. Any mathematical change needs renewed review.
The complete proofs still need independent final reviews, actual LeanCert
kernel trust checks, default-kernel/standard-axiom checks and real Linux
Comparator verification. Preserve Matthew J. Colbrook's mathematical
authorship and George Stepaniants's formalization credit with his
department and Caltech affiliation, without adding his email. The
canonical problem remains Solved, not Lean verified, at this stage.
