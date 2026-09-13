# Recovery provenance and limitations

Recovery date: 12 September 2026.

The user requested recovery of an interrupted investigation of IE-27 and delivery
of a ZIP archive. At the start of recovery, the current `/mnt/data` directory
contained no files from the previous run. Consequently this is a reconstruction,
not a byte-for-byte retrieval of an existing archive.

Recoverable execution excerpts contained the stage-construction routine, an
integer-interval certificate checker, the numerical candidate generator, and
explicit three-stage matrices and determinant calculations. They also showed
that the arbitrary-stage proof had not been completed. No completed manuscript
or successful all-stage argument was recovered.

This archive reimplements those mathematical components, regenerates the
included finite certificates, checks all of them anew, and supplies a new
write-up. The standard-library Q(sqrt(6)) checker and regression suite provide
additional checks during recovery. The verifier was reviewed for outward
rounding, root isolation, factorization normalization, and the exact meaning of
its accepted inequalities.

The fresh verification set is exactly

    {2, 3, ..., 64} union {80}.

All 64 cases pass. For each listed q, the conclusion quantifies over every
positive shift. Earlier execution excerpts also mention larger numerical
experiments; their original data files are absent. They are not counted as
verified results and their numerical outputs are not presented as recovered
certificates.

The archive does not claim a complete solution, a counterexample, independent
peer review, proof-assistant formalization, or mathematical novelty of the
low-order spectral results. It does not claim that a requested duration of work
was completed. It does not assert that no proof could exist elsewhere.

The bibliography identifies the exact target and related primary literature.
The live problem README was read directly through its raw website URL; no
GitHub plugin was used. No commit-pinned copy of the repository is included.

All theorem claims in this archive are limited to the scope stated in the
manuscript. In particular, the existence of a useful common metric at finitely
many stages does not establish its existence at arbitrary stages.
