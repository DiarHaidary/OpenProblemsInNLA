# NR-03 first canonical Linux run: retained failure

Run **34783909558**, verify job **103795825608**, failed at commit
`523c5aeaddd8bf7c2dc01afb053bb0dea8811335`. Only NR-03 was selected.
The job started at **21:28:23 UTC** and ended at **21:47:23 UTC** on
13 September 2026: **19 minutes**. This report is an implementer operational
audit, not independent mathematical acceptance.

The actual failure is a Lean elaboration error in **NLA/NR03/Rank.lean:40:4**:

```text
mod_cast has type
  (0 : ℕ) ≤ W i k
but is expected to have type
  (0 : ℝ) ≤ castNatMatrix W i k
```

The source branch establishes entrywise nonnegativity of the cast left factor.
The observed error identifies a cast expression that has not been exposed to
the cast tactic. A minimal proposed direction is to expose
`(0 : ℝ) ≤ (W i k : ℝ)` before applying that tactic. This monitor made no
source change or new run. Other declarations after this error are not inferred
successful merely because no further error appeared.

The raw log establishes these completed build boundaries:

- all 48 row modules, with all 384 literal-row axiom diagnostics;
- all three original full-family identities;
- CertificateBridge's four theorem diagnostics;
- the unconditional Certificate module in 2.2 seconds, including both
  full_identity and generic_scaled_identity with standard-three axiom reports.

There are exactly **393 observed theorem axiom diagnostics** before the failure,
and all use only `propext`, `Classical.choice`, and `Quot.sound`. Rank failed
in 2.3 seconds. Solution did not build, the ten public export diagnostics did
not occur, and the full default-kernel and Comparator acceptance stages were
not reached. NR-03 therefore remains unverified.

All ten actual dependency checkout revisions in `dependencies.log` match the
candidate manifest. The user-service/sandbox checks, three kernel-control cases,
five Comparator regressions, and both expected sorry/native rejections passed
before the solution build. Passing these controls does not establish the
candidate theorem proofs.

The artifact is **15,415 bytes**, ID **10325664210**, ZIP SHA-256
`c4ada14feed7c89326c3df7219c958abeea241bb7729ed85f43ab0ab75d2d650`.
The raw archive, extracted logs, and run/job/artifact API responses are retained.
The main raw log is
`extracted/verify-20260913T212930Z-4157/comparator.log`.

`CANDIDATE-GIT-INPUTS.json` retains all 102 expected source hashes recomputed
from the exact canonical Git commit. Because the verifier failed before its
success receipt, no raw accepted-result input inventory was emitted. This
report does not misrepresent the candidate Git inventory as such a receipt.
`FAILURE-DETAILS.json` contains the complete actual diagnostic/axiom/control
observations; `FAILURE-CHECKS.json` retains the initial log-stage classification.

No local compiler/cache, source edit, restart, duplicate workflow, cap change,
public status update, or full verification claim was made by this monitor.
