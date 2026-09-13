# KE-04 Krylov author completion

The five frozen range, shift, independence, full-prefix and largest-iteration
contracts compile with their exact approved types. This is a bounded helper
completion, not independent mathematical review or complete KE-04 verification.

The proof uses the genuine span of indexed matrix-power columns. Its coefficient
map is the finite linear-combination map; independence follows from finite span
dimension and restricts along the injective prefix embedding. At positive block
width, full rank bounds the iteration by the ambient dimension, and the first
full iteration makes the finite set nonempty. `Nat.findGreatest` therefore yields
the actual greatest full iteration. Zero block width is not silently admitted to
that existence contract. No numerical search, interval calculation or native
decision certificate is required.

The mf16_final_referee agent drafted this helper. After its recorded checkpoint,
the coordinator completed five elaboration fixes and removed one unnecessary
`simpa` warning. The first coordinator build passed, then a separate fresh final
Definitions/Krylov/Inspect build passed. Both attempts and the original failed
agent attempt remain byte-for-byte recorded. The historical checkpoint's old
source hash refers to its exact retained attempt source, not today's live module.

The final inspection compared all five actual theorem types to proof-free
propositions extracted from frozen Challenge headers. It traversed the actual
type/body closure of 30 project declarations and retained 14 required material
dependencies. Fourteen source and five inspection LeanCert kernel assertions
passed; their 19 axiom reports contain only propext, Classical.choice, Quot.sound.
Definitions has no warnings. The mathematical proof retains one harmless unused
`hr` simp-argument warning, without changing its successful elaboration. The inspection has three
retained, harmless unused hypothesis-name warnings in expected propositions;
their hypotheses remain universally quantified and no linter was disabled.

All 1598 frozen statement inputs matched. The final run checked all ten pinned
source repositories before and after compilation and used nine existing read-only
dependency object directories. It compiled three project modules into an empty
private prefix, hashed all generated objects and removed only that owned prefix.
This macOS author check is not an actual Ubuntu/default-kernel/Comparator run.

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA, with
substantial AI assistance. Original mathematical proof: Matthew J. Colbrook.
The coordinator and original helper contributor are proof authors, not independent
final referees of KE-04. Canonical status, IDs, metadata, Git and publication are
unchanged by this helper handoff.
