# Independent audit of PRs #195–#228

This record covers the 25 submitted pull requests listed below. The published integration base is `2db1e5857a4813ca627b60b4e30fa9bf6258c1cc`; every submitted source branch starts at `5830ed4fb06da0659414a3deb2a40ad327aca052`. Exact reviewed heads appear in the individual reports and source-preservation inventory. The integration retains the source commits as ancestors.

Independent Codex agents read the mathematical arguments and proof-assistant statements, checked relevant primary sources, and reproduced the stated available computations. Supplied PASS reports were not accepted as proof. Informal mathematical review is distinguished from Lean verification. Original authors retain credit; this record does not claim external human peer review or historical priority.

| PR | Problem | Reviewed contribution | Catalog status |
| --- | --- | --- | --- |
| [195](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/195) | MI-27 | Full coefficient-one inequality and sharpness | Solved |
| [197](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/197) | RA-17 | Exact real four-by-four rank-one measurement count and further bounds | Partially resolved |
| [199](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/199) | RA-05 | All-exponent lower bound and negative subsidiary answer | Partially resolved |
| [201](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/201) | RA-04 | Earlier narrow-band and exact-tail partial results | Solved by #207 |
| [202](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/202) | MI-16 | Exact finite algebraic determination for every spectrum | Solved |
| [203](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/203) | IS-03 | Lean proof of the original negative target | Lean verified |
| [204](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/204) | RE-06 | Full nonadaptive finite-family approximation | Solved |
| [205](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/205) | TR-08 | Full sparse threshold | Solved |
| [207](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/207) | RA-04 | Full clustered-gap block Krylov bound | Solved |
| [209](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/209) | PF-04 | Maximum order-six completely positive rank is nine | Solved |
| [211](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/211) | PF-03 | Counterexample to rational factorization at every width | Solved |
| [213](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/213) | PF-01 | Structural necessary conditions | Partially resolved |
| [214](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/214) | NR-03 | Exact counterexample to the universal rank equality | Solved |
| [216](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/216) | NM-01 | Conditional recovery and certificate obstructions | Open |
| [217](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/217) | NR-01 | Exact ranks for orders 17–20 | Partially resolved |
| [218](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/218) | TR-09 | Local ALS and supporting algebraic results | Open |
| [219](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/219) | MD-02 | Fixed-point criterion and first two iterate bounds | Open |
| [220](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/220) | RA-14 | Universal finite-accuracy lower bound and matched regimes | Partially resolved |
| [222](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/222) | RA-05 | Unrestricted quartic classification | Partially resolved |
| [223](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/223) | RA-17 | Further topological bounds; optional checker corrected in integration | Partially resolved |
| [224](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/224) | MF-16 | Lean proof of order-two word-equation nonuniqueness | Lean verified |
| [225](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/225) | RA-08 | Lean proof of the spectral-transfer counterexample | Lean verified |
| [226](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/226) | RE-03 | Improved HODLR lower and upper bounds | Partially resolved |
| [227](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/227) | RA-09 | Lean proof of concave Frobenius-error transfer | Lean verified |
| [228](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/228) | RA-20 | Lean proof of the full symmetric rank-two critical count | Lean verified |

Individual reports are named `pr-N-independent-review.md`. MI-27 received a [second analytic review](pr-195-cross-review.md). MI-16 also received a [second independent review](pr-202-cross-review.md): its finite algebraic prescription meets the retained exact-value target, without claiming an efficient algorithm or a compact structural formula for arbitrary spectra.

The [upstream Lean CI authentication](upstream-lean-ci.json) binds 6,318 complete tracked input hashes and 59 theorem exports to the five reviewed submissions. It checks GitHub artifact digests, checked commit parents and trees, actual default-kernel acceptance, standard-axiom reports, Comparator regressions, admitted/native-proof rejection and Linux sandbox controls. The [source-boundary audit](lean-source-boundaries.json) separately addresses correspondence to the original mathematical targets. Final combined-branch checks are recorded separately; upstream success alone is not the integration merge gate.

Integration retains the earlier MI-16, MI-27, RA-04, RA-05, RA-14 and RA-17 contributions and credits on their canonical pages. Historical RESOLVED.md records now distinguish their former scopes from later full results. The six combined problem PDFs were regenerated and every page visually inspected. The shared renderer changes concern only page layout. All 217 IDs, canonical paths and original targets are retained.

The RE-03 archive lacks some historical continuation test programs. Only its available five smoke cases and twelve fresh implementation regressions were reproduced; the complete mathematical proof and its included appendices were reviewed directly. NM-01, TR-09 and MD-02 supporting results do not establish the original requested target, and those entries remain Open.

The optional RA-17 saved-certificate checker had two reproduced false-acceptance paths. The [maintainer correction](../../references/holden-ra17-continuation-2026-09-13/MAINTAINER_CHECKER_CORRECTION.md) records the tested fix while preserving the original submission manifest and archives.

Final local validation passed all 77 repository tests without skips, the 17 permanent-ID tests, and the 10 checker regressions on the integrated files. Catalog regeneration reports 24 Lean verified, 77 Solved, 46 Open and 70 Partially resolved entries: 217 permanent IDs, with 116 targets still counted as open.

The final [independent preservation review](preservation-review.md) passed on commit `b7495d4cf9442c2e1a12956dbd99edc0b8ad5477`. This final publication commit adds only audit records and this link. The [checker repair cross-review](pr-223-checker-repair-cross-review.md) independently verifies the exact repair and optimized-Python controls.

The preservation script uses the bundled source-PR metadata and Git history; rerun it with `python3 verify_preservation.py --repo /path/to/full/clone --ref COMMIT --output-prefix /tmp/preservation-check`. The [authored-file manifest](authored-file-manifest.json) records every reviewed source file.
