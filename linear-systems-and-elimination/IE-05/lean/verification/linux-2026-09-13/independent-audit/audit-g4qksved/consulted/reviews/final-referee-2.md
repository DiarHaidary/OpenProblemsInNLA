# IE-05 independent final mathematical review 2

**Verdict: APPROVE the complete frozen mathematical formalization.** No
mathematical correction is requested. This approval does not attest to the later
Linux, Comparator, packaging or publication gates.

Reviewer: `/root/mf16_final_referee`, an independent AI agent. I made no IE-05
statement, certificate, implementation or proof contribution. My KE-04 proof
work is unrelated. I formed this judgment from the original sources and actual
Lean implementation without reading the other final referee's verdict. The
pre-work role receipt is `final-referee-2-evidence/ROLE.json`.

## Exact reviewed boundary

- Complete proof freeze: `reviews/proof-freeze.json`, SHA-256
  `72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251`.
  Every one of its **1800** named files and sizes was independently rehashed,
  before and after the review. No concurrent final-referee-1 additions are
  included in this review's seal.
- `NLA/IE05/Proof.lean`:
  `f8ef9d1901845439e7c09f4e9d004eb49d87ed28d8a6d567d48ac4d16199a950`.
- `Solution.lean`:
  `3e12274c074f9d221230bd3939a76d433532b067c7123a12effe2b9e6f6a5c9a`.
- The **27** original snapshots were independently matched, byte for byte and
  Git blob for Git blob, to commit
  `5830ed4fb06da0659414a3deb2a40ad327aca052` using the RA-20 checkout's object
  store. The retained IE-05 canonical page is Solved at that base, with its
  permanent ID and path unchanged. This is not a fresh remote-status claim.
- Fourteen nested statement/helper inventory manifests were checked against
  their exact historical membership and roots, including nested manifests and
  the full 733-file statement freeze. No basename-based exception or demand that
  a historical inventory contain later files was used.

I read the complete canonical target, canonical `solution.md` and `solution.tex`,
all definitions and seventeen Challenge signatures, `NUMERICAL_TARGETS.md`,
`SourceCorrespondence.md`, `PROOF-MAP.md`, all twelve final `NLA/IE05` modules and
`Solution.lean`. The raw identities and source searches are retained in
`final-referee-2-evidence/source-audit-2/`.

## Mathematical findings

**The final theorem is the full original negation.**
`OrthogonalExtremizerConjecture` quantifies every natural dimension at least two
and compares the real supremum over all orthogonal matrices and all admissible
partial-pivoting paths with the stipulated first-available path of the specified
positive-diagonal QR candidate. The proof gives a strict supremum gap at dimension
eight and contradicts that universal equality. It does not replace the target by
an integer inequality, a selected subset supremum or an assumed extremizer.

**QR and the norm convention are genuine.** `euclideanColumns` uses
`EuclideanSpace ℝ (Fin n)` and normalized Mathlib Gram-Schmidt. The proof relates
its actual inner product to matrix multiplication, obtains independent columns
from the nonsingular unit-lower matrix, proves orthogonality, upper triangularity
and strictly positive diagonal, and proves uniqueness of both factors. The
candidate at order eight is then identified with its literal normalized integer
columns through the Gram identity and the positive triangular inverse. This
identification is a theorem, not a definition of the desired candidate.

**The elimination path is actual elimination, including ties.** `rowSwap`,
`schurStep` and `trajectory` implement the active Schur recurrence; discarded
coordinates are zero-padded. `firstPivotIndex` is the specified finite row scan
with strict-improvement updates, so equal maxima retain the first eligible row.
The proof establishes the scan's maximum and tie properties and the uniqueness
of a first-available path. Its nonsingularity argument maintains injectivity on
the active block and reconstructs the eliminated coordinate when proving Schur
injectivity. It does not falsely assume that the padded full matrix remains
invertible. Thus division by a zero pivot is excluded where required. The generic
scaled-LU theorem proves the whole no-swap trajectory, including the terminal
zero stage, and proves that it is the stipulated admissible path.

**The witness is the original one.** `integerLower true` changes zero-based
`(7,1)`, hence one-based `(8,2)`, from `-1` to `0`. The witness `H`, `T` and
candidate `H₀` literals match the complete source manuscript. Both Gram and LU
identities, positive scales, positive upper diagonal, unit-lower structure and
multiplier bounds are proved over the integers and transferred explicitly to
the reals. The witness is therefore an actual real orthogonal matrix with the
actual required pivot path. This is not the distinct recovered variant.

**The computation reduction preserves what the theorem needs.** The finite
entry obligations are 64 witness input inequalities and 204 active candidate
inequalities, together with one candidate input entry, the witness final pivot
and the exact positive rational gap. They imply the one-sided bounds
`5272/63 ≤ firstGrowth witnessQ` and
`firstGrowth (candidateQ 8)^2 ≤ 17948132/2601`. Square-root positivity and all
denominator signs are proved symbolically. The strictly positive difference
`117335164/1147041` gives strict growth without proving the manuscript's stronger
complete tables of maxima. Those tables and exact growth equalities are not
advertised as exports. No interval partition or artificial interval is needed.

**The real supremum is justified.** The NNReal finite maxima are proved to be
the actual real entry maxima, including attainment when the dimension is
nonempty. The factor-two Schur bound yields the universal growth bound for every
admissible path. Nonemptiness of the orthogonal growth set comes from the
identity matrix and an established admissible first path; boundedness is proved
for the entire defined set. The witness belongs to that set, and `le_csSup` is
used with its actual boundedness hypothesis. The supremum comparison therefore
does not exploit totalized `sSup` on an empty or unbounded set.

**Degenerate cases are handled at their natural scope.** The original target
starts at dimension two. Maximum/growth lemmas requiring a nonempty index set
explicitly assume `1 ≤ n`; the first-path and generic algebra lemmas also allow
empty dimensions where their quantified path assertions are vacuous. Scales
and pivots used in division have proved positivity or nonzeroness. Initial
stage zero is included in growth, and the zero terminal stage is correctly
excluded from its `Fin n` stage maximum. Equal pivot magnitudes are allowed
throughout rather than removed by a generic-position assumption.

## Fresh independent mechanical evidence

I explicitly compiled all twelve final modules in dependency order, followed by
`Solution.lean` and my own `Inspect.lean`: **14 successful Lean commands** from
immutable source copies and an initially empty private output prefix. No default
Lake target was used. The nine existing compiled dependency directories were
read-only; all ten package source pins were checked clean before and after.
Lean was the pinned macOS `v4.33.1`; Mathlib was
`0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert was
`621a43d7cf21f87872392a01e874f2f1dbddc926`. No dependency was copied, downloaded or
rebuilt.

My inspector constructs proof-free expected `Prop` expressions from the exact
frozen signatures and compares all **17 elaborated types** by definitional
equality. It imports `Solution`, never `Challenge`; no reference proof hole is
loaded or used. Its independent traversal inspects actual declaration types
and proof bodies, checks reached project declarations are safe and nonpartial,
and checks their transitive axioms:

- The final negation reaches **152** project declarations and all **27** selected
  material dependencies, including the actual integer certificates, cast/QR/LU
  bridges, actual trajectories and growth, `Real.sq_sqrt`, `le_csSup`, normalized
  Gram-Schmidt and `of_decide_eq_true`.
- The complete seventeen-export traversal reaches **181** project declarations
  and also explicitly retains the all-path GEPP, first-path and positive-QR
  contracts.
- **106 actual axiom reports** and **106 successful explicit LeanCert
  `#assert_trust kernel` checks** admit only `propext`, `Classical.choice` and
  `Quot.sound`. The actual certificate commands use `decide +kernel`; no native
  computation, custom axiom, proof admission or reference-hole dependency is
  present. LeanCert is used as the actual trust audit, not an artificial
  numerical side theorem.

The fourteen disposable objects were hashed before deletion. Source copies,
commands, outputs, input/pin identities and all diagnostic records remain.
The authoritative local validation receipt is
`final-referee-2-evidence/successful-build-validation/result.json`, SHA-256
`76421db3a622500e7be24c64e968b5c5eae096775ac1cc87dbeb61300113d177`.
The independent original-source, nested-seal and supplementary exact arithmetic
audit receipt is `final-referee-2-evidence/source-audit-2/result.json`, SHA-256
`3501618c620df041537e0140cf1529c2628e21c82ba81d6a9da15e2c987a1828`.
The Python rational reconstruction is supplementary evidence, not the universal
proof or a kernel certificate.

Two reviewer-tool diagnostics are fully retained: an incorrect existing-Forsythe
checkout path, and an overstrict Python warning policy for unused hypothesis
names in my generated expected propositions. All actual Lean commands succeeded;
the implementation emitted no warnings. The exact fourteen reviewer warnings
were classified from the raw output without altering or rebuilding the proof.
Neither failed receipt was overwritten. See `final-referee-2-evidence/DIAGNOSTICS.md`.

## Tau Ceti review angles within the NLA adapter

I applied the actual pinned `docs/lean/REVIEW.md` and Tau Ceti common protocol
plus all ten rubrics at `afb424eda89e8ac96d9eb69f6a88972055a4cd1b`. The latter's
complete pinned Git tree and selected rubric blobs were independently checked.

| Angle | Assessment |
|---|---|
| Correctness | Full target, genuine objects, signs, dimensions, tie quantifiers and supremum prerequisites checked as above; no hidden conclusion in a premise. |
| Scope | One complete permanent IE-05 target, with genuine prerequisites used by the final theorem. No claim about the true extremal value or asymptotic growth. |
| Proof quality | Finite exact certificates are separated from reusable real algebra; the actual recurrence and QR uniqueness have explicit bridges. The square-root manipulations are local transparent coercions, not assumed analytic enclosures. |
| Reuse | Actual pinned Gram-Schmidt, matrix inverse/triangular, finite-sup and conditional-sup APIs are reused. The retained searches found no existing Mathlib GEPP/first-pivot API replacing this active-block development. |
| Generality | Real scaled-Gram/LU and finite GEPP lemmas are proved once before both numerical specializations; the original dimension restriction remains on the exported target. |
| API design | The seventeen frozen boundary exports expose the needed semantics, existence, bounds and complete negation. Implementation helpers have real consumers; public boundary wrappers serve the separate reference/proof contract, not an obsolete compatibility layer. |
| Naming | Names distinguish upper/lower bounds, exact identities, paths and the negated conjecture. The weaker computational auxiliaries are not named exact growth equalities. |
| Placement | Definitions, certificates, QR, pivot/GEPP, LU, witness and growth are separated by dependency. The solution imports only the completed proof module. |
| Documentation | The proof map accurately distinguishes the completed proof from historical statement-stage files and explains the reduced finite obligations. Historical live wrapper refresh remains a packaging gate. |
| Attribution | George Stepaniants, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA, is credited without publishing his email. John Peca-Medlin retains the original conjecture/analysis attribution, and the mathematical counterexample and AI formalization roles are disclosed. |

The pinned Schiffer Challenge and Forsythe Challenge/checked-bound module were
inspected as structural references, with their recorded licenses. No claim is
made that their numerical methods or earlier validations establish IE-05, or
that this is an official Tau Ceti service review.

## Remaining gates and limits

The frozen historical `lakefile.toml` still selects `Challenge` as its default
target, and the old README/source-correspondence stage text remains historical.
Candidate packaging must explicitly select `Solution` and refresh those live
wrappers before publication while retaining the frozen originals. That known
packaging task does not change this mathematical approval.

This is independent AI review and fresh local macOS compilation. It is not
external human peer review, actual Linux Comparator execution, independent
default-kernel replay, sandbox/negative-control validation, or publication
approval. Those remain separate campaign gates. No mathematical, frozen,
canonical, metadata, Git, dependency or status file was edited by this reviewer.
