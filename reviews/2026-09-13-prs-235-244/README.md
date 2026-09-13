# Independent audit of PRs #235, #237 and #239–244

All eight submissions passed independent mathematical review for the scopes below. The six partial-result entries retain their unrestricted original targets. SP-06 and IS-02 move from Solved to Lean verified after review of the actual definitions and proofs plus authentication of fresh Linux verification. These are AI-agent audits, not external human peer review or novelty certificates.

Published comparison base: `b73cd1804e40e0d101294eedb156984f0d62b4a6`.

| PR | Problem | Accepted scope | Catalog status |
| --- | --- | --- | --- |
| [235](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/235) | RA-11 | General bounds, matching special regimes and product subclasses; source projection-conjecture obstruction | Partially resolved |
| [237](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/237) | RA-01 | RPCholesky tail-envelope guarantees; full arbitrary-spectrum target remains open | Partially resolved |
| [239](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/239) | RA-18 | Complex extension refuted; real frames with at most r+2 row directions | Partially resolved |
| [240](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/240) | SP-06 | Complete Jordan-curve counterexample, all 20 public contracts | Lean verified |
| [241](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/241) | IS-02 | Complete spectral-uniqueness counterexample, all 9 public contracts | Lean verified |
| [242](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/242) | MI-05 | Fourteen-term identity, affirmative classes and sharp orthogonal common-weight obstruction | Partially resolved |
| [243](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/243) | RA-14 | Restricted query classification, conditional posterior and ensemble-specific bound | Partially resolved |
| [244](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/244) | TR-29 | Exact complex rank for every two-factor W product, plus binary monomial products; k>=3 remains open | Partially resolved |

## Review and reproduction

The eight `pr*-independent-review.md` reports record exact heads, proof coverage, primary-source correspondence, actual reruns, PDF inspection and limits. Additional independent cross-reviews cover MI-05's global-maximization/support arguments and TR-29's apolar edge cases. Newly authored independent computational checks and their results are retained alongside the reports. The original submissions' reference packages and all 460 added source files are preserved byte-for-byte.

The complete mathematical targets and complete project-owned Solution import closures were read for both Lean submissions. The current CI evidence is bound to the exact source commit, synthetic merge parents/tree, complete Git-tracked input set and pinned checker. The authenticated source runs are [SP-06 run 34768457824](https://github.com/ajt60gaibb/OpenProblemsInNLA/actions/runs/34768457824) and [IS-02 run 34768938972](https://github.com/ajt60gaibb/OpenProblemsInNLA/actions/runs/34768938972). Their machine-readable receipts are `pr240-source-ci-authentication.json` and `pr241-source-ci-authentication.json`; the read-only authentication program is `prs235-244-ci-authenticate.py`.

Both runs accepted all public exports through the pinned Comparator and Lean default kernel, with standard-axiom restrictions, three actual kernel controls, five actual Comparator regressions, rejection of admitted/native-decision fixtures and both unprivileged Linux sandbox modes. All 276 source inputs matched their Git blobs. SP-06 uses 34 silent `#assert_trust kernel` commands covering every export and transparent target, so its current log has **zero printed axiom reports**. IS-02 prints nine. The absence of SP-06 diagnostic prints is not represented as printed evidence; its axiom acceptance is enforced by the actual Comparator, whose negative controls were authenticated. No repository checker or workflow was weakened or changed.

## Integration and publication fixes

All eight audited source heads are retained as merge ancestors. Only overlapping RESOLVED insertions needed manual conflict resolution; every contribution block was retained. Catalog counts were regenerated under the permanent-ID validator. TR-29's source PR updated its README and TeX but omitted its canonical PDF; that PDF was rebuilt and both pages visually inspected. The TeX reproduced the audited source byte-for-byte. Other source/reference/proof files were not edited.

All 217 permanent registry entries, original targets and canonical paths remain intact. All 23,571 base paths are retained, including 2,959 byte-identical previously published reference files. The only shared-code change is PR #237's reviewed RA-01 page-break addition in the renderer. Validation covers all 77 repository tests with no skips, both formalization manifests and GitHub mathematics formatting. The preservation script and its receipt record the exact blob and history checks.

The resulting catalog has **44 Open, 72 Partially resolved, 73 Solved and 28 Lean verified** entries: 116 open targets and 217 permanent entries. Partial progress does not reduce the open-target count.

Final publication remains gated on successful checks of the combined integration head, authentication of its new Linux proof artifacts, an unchanged base/head immediately before merge, and verification of the published merge tree. The integration PR records those final CI receipts and outcome, avoiding changes to already verified proof inputs merely to attach later logs.
