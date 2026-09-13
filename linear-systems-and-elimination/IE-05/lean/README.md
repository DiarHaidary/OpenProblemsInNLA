# IE-05 Lean verification: exact extremizers for partial pivoting

The complete negative resolution of IE-05 is implemented and has two accepted
independent final mathematical agent reviews. Independent candidate packaging
approval and the authoritative Ubuntu default-kernel/Comparator verification
are complete. The canonical problem is now **Lean verified**; its permanent ID,
canonical target and original attribution are unchanged.

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
The authoritative Linux run and independent operational audit are archived in
[`verification/linux-2026-09-13/`](verification/linux-2026-09-13/).

From this directory, the following checks the published package's integrity
and metadata; it does not run Lean or grant independent approval:

```sh
python3 verification/verify_publication.py
```

The check requires the PyYAML and jsonschema dependencies recorded
in `verification/candidate-package/schema/requirements.txt`.

The verifier checks every file in the current
[`publication inventory`](verification/publication-inputs.json), with that
inventory itself as the sole exclusion, and the complete sealed operational
evidence. It also checks all 29 historical inventories, the full 2,338-file
accepted draft, original source blob identities and the unchanged members of
the 2,404-file [historical candidate selection](verification/candidate-inputs.json).
Exactly two candidate metadata files, this README and `formalization.yaml`,
were refreshed for publication; their current bytes are bound by the new
inventory. The historical candidate inventory and its original verifier are
retained unchanged. Their default commands describe the earlier phase and
must not be used as a check of the later publication tree.

Within the earlier accepted-draft checks, three exact path-and-hash versions
redirect to preserved wrapper archives. Seven small pinned library source
archives make an old external-source inventory portable. No dependency cache
or Git object store is included.

The accepted mathematical gate is
[`verification/final-review-acceptance.json`](verification/final-review-acceptance.json),
following [`final referee 1`](reviews/final-referee-1.md) and
[`final referee 2`](reviews/final-referee-2.md). Referee 1 subsequently authored
this candidate package and therefore supplies no independent packaging approval.
That later role does not alter the earlier sealed mathematical review.
[`verification/candidate-package/HANDOFF.md`](verification/candidate-package/HANDOFF.md)
records the package boundary and the historical candidate selection.
