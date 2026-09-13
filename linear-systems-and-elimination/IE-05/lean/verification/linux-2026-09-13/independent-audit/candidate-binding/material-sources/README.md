# IE-05 Lean candidate: exact extremizers for partial pivoting

The complete negative resolution of IE-05 is implemented and has two accepted
independent final mathematical agent reviews. **Independent candidate packaging
approval and actual Ubuntu default-kernel/Comparator verification are pending.**
The canonical problem remains **Solved** by its existing informal counterexample;
this candidate does not change its permanent ID, canonical pages, or verification
status.

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA, is the author of
the original counterexample and this substantially AI-assisted formalization.
John Peca-Medlin retains credit for the conjecture and cited element-growth
analysis. No external human peer review or official Tau Ceti endorsement is
claimed.

[`Solution.lean`](Solution.lean) imports the complete proof in
[`NLA/IE05/Proof.lean`](NLA/IE05/Proof.lean). Its 17 exports match the original
[`Challenge.lean`](Challenge.lean) contracts in the two independent macOS source
checks. The final theorem, `NLA.IE05.orthogonalExtremizerConjecture`, proves
`¬ OrthogonalExtremizerConjecture`: the full universal equality between the real
orthogonal GEPP growth supremum and the prescribed positive-diagonal QR
candidate is false, by dimension eight.

The proof uses actual normalized Euclidean Gram–Schmidt, proves positive QR
existence and uniqueness, and handles all admissible partial-pivoting tie paths.
It proves the first-available scan and nonzero pivots from nonsingularity, exact
zero-padded active Schur trajectories, finite entry maxima, and the nonempty
bounded growth set underlying the real supremum. The witness changes the
one-based entry `(8,2)`, or zero-based `(7,1)`, from `-1` to `0`. Exact integer
Gram/LU certificates and only 64 witness-input plus 204 candidate-active
inequalities, together with the witness final pivot, suffice for the strict gap.
The exported numerical estimates are one-sided; the stronger exact growth
equalities in the informal manuscript and the true supremum are not claimed as
additional Lean results.

Read [`SourceCorrespondence.md`](SourceCorrespondence.md),
[`NUMERICAL_TARGETS.md`](NUMERICAL_TARGETS.md),
[`PROOF-MAP.md`](PROOF-MAP.md), and
[`formalization.yaml`](formalization.yaml) for scope, dependencies, and credits.
The proof map, Challenge comments, development logs, freezes, and review reports
retain their exact historical phase language. The live README and correspondence
supersede their statements about work that was then pending.

Lean is pinned to `leanprover/lean4:v4.33.1`; all ten dependencies are fixed in
[`lake-manifest.json`](lake-manifest.json), including Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`. With these dependencies available,
the local proof build is:

```sh
lake build Solution
```

The candidate's default target is also `Solution`. `Challenge` is a separate
intentional reference environment with 17 holes and is never imported by the
solution. The live proof development has no admissions. Actual transitive axiom
inspection in both independent source checks found only `propext`,
`Classical.choice`, and `Quot.sound`, with explicit LeanCert kernel assertions.
These macOS checks do not substitute for the pending authoritative Linux run.

From this directory, the following checks only package integrity and metadata;
it does not run Lean or grant independent approval:

```sh
python3 verification/candidate-package/verify_inventory.py
python3 verification/candidate-package/audit_metadata.py
```

The metadata check also requires the PyYAML and jsonschema dependencies recorded
in `verification/candidate-package/schema/requirements.txt`.

The archive-aware verifier checks every member of all 29 historical inventories,
the full 2,338-file accepted draft, original source blob identities, and the
complete [`verification/candidate-inputs.json`](verification/candidate-inputs.json)
selection. Only three exact path-and-hash versions redirect to preserved wrapper
archives; no inventory name or basename is excluded. Seven small pinned library
source archives make an old external-source inventory portable. No dependency
cache or Git object store is included.

The accepted mathematical gate is
[`verification/final-review-acceptance.json`](verification/final-review-acceptance.json),
following [`final referee 1`](reviews/final-referee-1.md) and
[`final referee 2`](reviews/final-referee-2.md). Referee 1 subsequently authored
this candidate package and therefore supplies no independent packaging approval.
That later role does not alter the earlier sealed mathematical review.
[`verification/candidate-package/HANDOFF.md`](verification/candidate-package/HANDOFF.md)
records the package boundary and pending gates.
