# RA-20 author statement check

**Verdict: ready for two independent statement reviews, not approved for proof
implementation.** This report is by the statement authoring agent
`/root/formal_review_standards`; it is not an independent referee report.

The complete original canonical problem, both published resolution formats and
complete independent historical review were read. All four generic formulas,
the allowed endpoint `n=s=3`, the complex field and bilinear full-Frobenius metric
are retained. The mathematical resolution remains attributed to the original
Codex maintainer audit; formalization authorship is George Stepaniants with his
approved Caltech department and university attribution, without contact email.

The definitions do not assume a coordinate description of the smooth locus.
They use the reduced coordinate ring obtained from the entire vanishing ideal
of the actual rank-constrained matrix set, and Mathlib's algebraic smooth locus
at the point prime. Tangent equations use that entire ideal. Criticality uses
the actual complex Fréchet derivative. A cardinal equality provides the count;
genericity quantifies over arbitrary nonempty principal opens of all symmetric
data, and a separate required theorem proves intersection with the chosen
generic set. No generic-count uniqueness theorem is assumed.

The twelve reference signatures passed fresh direct source elaboration. The
final recorded run is `verification/statement-checks/attempt-0kvxnk1o/`: all
three commands exited zero, with exactly twelve intentional `Challenge.lean`
placeholder warnings and no warnings in Definitions or the definition inspector.
Nine actual definition/library trust checks printed only `propext`,
`Classical.choice`, and `Quot.sound`. All ten read-only dependency heads were
checked clean at their pinned revisions both before and after the run. Input
source identities remained unchanged throughout. These checks establish typing
and definition trust only, not any of the twelve mathematical conclusions.

The two failed development attempts are retained: one identified the missing
matrix topology import; one found only an invalid inspector request for an
unscoped matrix norm instance and the omitted `kernel` keyword in trust commands.
A preceding successful three-command run is also retained. No failed output or
error-recovery term is being presented as a proof.

The independent sparse-coefficient reconstruction checks the generic determinant
and full-distance identities, their coordinate gradients, all three restricted
Hessians, the optional rational-data distances, and the elementary leading terms
that motivate a possible nonsmoothness obstruction. It expressly does not prove
the algebraic smooth locus, genericity, the critical count, or the Lean target.

The main implementation risk remains explicit: the coordinate-ring isomorphism
and genuine smoothness/non-smoothness theorem must be proved using actual
localization/formal-smoothness machinery or an equally faithful route. Replacing
this obligation with a definition based on exactly-one-zero coordinates, or
counting the matrix rank-two stratum instead, is unacceptable. The exact
second-derivative obligation also supports the source's nondegeneracy claim;
it is not a hypothesis hiding an algebraic multiplicity assertion.

No `Proof.lean`, `Solution.lean`, custom axiom, native certificate, dependency
override, canonical edit, Git mutation or publication was produced. LeanCert's
planned role is kernel/dependency trust auditing for this pure exact argument;
no artificial interval certificate is needed. The statement package must still
pass two fresh independent semantic/referee checks and the root's gate before
mathematical implementation.
