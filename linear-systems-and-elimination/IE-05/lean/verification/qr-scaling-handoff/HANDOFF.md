# IE-05 QR and scaling helper handoff

Root authored these helpers after the accepted statement gate. The exact
approved `scaledColumns_orthogonal` and `candidate_positiveQR` contracts compile
under `NLA.IE05._proved`. All sixteen material helper declarations passed
explicit LeanCert kernel assertions and print exactly the three standard axioms.
This is author development evidence, not an independent review or a complete
IE-05 solution; Linux and Comparator verification remain later gates.

Scaling distributes the positive column denominators through the actual Gram
matrix. QR uses Mathlib's actual Euclidean-space normalized Gram--Schmidt,
proves orthogonality, positive diagonal and triangularity from nonsingularity,
and proves uniqueness by increasing-index projection induction. The prescribed
unit lower triangular matrix has determinant one. No numerical square-root
evaluation or interval subdivision is used.

All earlier immutable attempts remain, including the initial unused simp
warning, failed QR elaborations, and the later unreachable-tactic warning.
These are not accepted proofs. The final fresh Definitions/Scaling/QR run
has no warnings or errors. `HANDOFF.json` names its exact result and sources.
The complete 733-input statement freeze is unchanged. Sixteen selected primary
API source snapshots and ten clean dependency pins are bound. Existing matching
dependency objects were read; no cache was copied or rebuilt. Every root-owned
helper object was hashed and removed after completion, retaining all logs.

Other proof modules and referee evidence are outside this author's edit scope.
The evidence manifest includes every file in both helper development directories,
the frozen statement inputs and freeze, the proof gate, both current helper
sources and this complete handoff directory. Only its exact own outer manifest
path is excluded; nested manifests are included as ordinary evidence.
