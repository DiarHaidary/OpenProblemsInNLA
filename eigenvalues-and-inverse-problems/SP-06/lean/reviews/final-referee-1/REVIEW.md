# SP-06 independent final proof referee 1

**Phase:** final proof review, 13 September 2026  
**Reviewer:** OpenAI Codex agent `/root/lean_ie15_next`; I did not author the SP-06 candidate.  
**Candidate:** `/tmp/nla-lean-sp06-project/eigenvalues-and-inverse-problems/SP-06/lean`  
**Standard:** statement-first review, source fidelity, complete-target coverage, LeanCert kernel trust, reproducibility, and explicit separation of local evidence from Linux/Comparator acceptance.

## Verdict

**PASS — complete local proof candidate.** I found no substantive mathematical, statement-fidelity, proof-path, or trust defect. The result is ready for the remaining independent final referee and authoritative Linux/Comparator gates. This report does not itself label SP-06 Lean verified or change the canonical repository status.

## Inputs and source fidelity

I read the frozen `Definitions.lean`, `Challenge.lean`, `NUMERICAL_TARGETS.md`, and `SOURCE_MAP.md`, the complete `Numeric.lean`, `Curve.lean`, `Proof.lean`, `Solution.lean`, `formalization.yaml`, and `comparator.json`. The approved statement boundary is unchanged: `Definitions.lean` has SHA-256 `5f3e071b9aabbbda27a794f9396022e54585f5d2d254827e50ea90baf80e72b1` and `Challenge.lean` has SHA-256 `cd75a8f37a174d7dfb68927f7e6aeb23cf0982eb3161d7d9e5a63a7583d73bef`.

The canonical source bytes at `nla-upstream/main` reproduce the four `SOURCE_MAP.md` hashes:

- README: `e2eb891930c96d6a3bdd25c75bfe6bd2798cc8c540ce00ec851f7bf1f0ceb25c`;
- `solution.md`: `c7adb8f97238049b20e82044d8527b70301779ba041169f74fe603a88ea1ae7a`;
- `problem.tex`: `183127180596a36c108ed8575420e3845ca890f3048a32ec1252d61cf60d5311`;
- `solution.tex`: `b7340bf85e0b776ed49a4303af64820b72708eb249fbdc885b9179945e60ffc9`.

The target remains the original universal implication over arbitrary finite complex Laurent coefficients, positive lower and upper bands with nonzero extremes, a continuous injective map from the actual Mathlib `Circle` avoiding zero on which the actual Laurent evaluation is real, and all positive finite Toeplitz sections with the actual algebra spectrum. `hasAdmissibleBand`, `hasRealJordanCurve`, `allFiniteSpectraReal`, and `targetImplication` in `Definitions.lean` encode these quantifiers directly. The `Fin n` index shift in `toeplitz` preserves `i-j`. No definition assumes the curve, its continuity, or spectral failure.

The source proof is faithfully reduced to one counterexample. The witness is
`-64 z^(-2) + 8 z^(-1) - 128 - 8 z - 63 z^2 - 16 z^3 - z^4`; the formal `witness_composition` establishes it as `a-a^2` for `a=8/z+8z+z^2` away from zero. The unit-circle radial construction is retained as an actual global curve: the exact endpoint bounds, uniform root separation, root uniqueness, Lipschitz radius, continuity, injectivity, nonvanishing, and the imaginary-part identity are all explicit contracts and implemented proofs. The order-two section and an actual nonreal algebra-spectrum element then negate the universal finite-spectrum conclusion. The source's stronger enclosure-of-zero and second eigenvalue are outside the catalog target and are not silently used.

## Proof-path review

The numerical layer (`Numeric.lean`, lines 25–141) proves the finite Laurent support and exact composition by Finsupp algebra, the endpoint signs, the full-box slope inequality, the root Lipschitz estimate, the exact order-two matrix, spectrum membership through `Matrix.mem_spectrum_iff_isRoot_charpoly`, and imaginary part 8. The slope proof factors the difference and proves the bracket lower bound algebraically over the complete interval; it does not use a finite mesh or floating-point approximation.

The curve layer (`Curve.lean`, lines 21–134) obtains a root by the intermediate value theorem, excludes both endpoints using strict signs, proves uniqueness from the uniform slope, chooses a root at every actual `Circle` point, and proves a uniform Lipschitz estimate through the real-part distance bound. Thus `continuous_radius_exists` proves continuity rather than assuming it. `radial_curve_continuous`, `radial_curve_injective`, and `radial_curve_nonzero` supply the exact Jordan-curve bridges. `auxiliary_radial_im` and `radial_curve_symbol_real` show reality on the entire curve, not at samples.

The final layer (`Proof.lean`, lines 13–25) applies the actual spectrum predicate at `n=2`, derives a contradiction from the exact imaginary part, and packages the admissibility, Jordan curve, and nonreal finite spectrum into `counterexampleClaim` and `not_targetImplication`. `Solution.lean` imports only `NLA.SP06.Proof`; it never imports `Challenge.lean`, so the twenty deliberate Challenge `sorry` bodies are not in the proof dependency closure.

The Comparator configuration lists exactly the twenty exported contracts in the modules that implement them, and the names match the declarations inspected in the proof sources. No definition names are required. A Linux Comparator run remains a separate gate and was not claimed here.

## Independent exact checks

I independently checked the Laurent coefficient dictionary, endpoint values, slope bracket vertices, and order-two characteristic equation with Python `fractions`, without importing candidate code. The checks reproduce `a-a^2` coefficients `{-2:-64,-1:8,0:-128,1:-8,2:-63,3:-16,4:-1}`, `F(1/2,1)=-23/32`, `F(2,-1)=1`, slope-bracket values `13/16`, `19/16`, and `1` at the triangle vertices, and the root `-128+8i` for the displayed order-two matrix. These checks are supplementary; the universal curve and spectrum arguments are established by Lean proofs.

## Fresh local Lean evidence

I ran the prescribed command with the existing pinned MI-22 dependency objects:

```text
SP06_DEP_ROOT=/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages python3 verification/compile_development.py Solution
```

It exited 0 and reported:

```text
PASS: requested development modules elaborated; not an independent review or Linux result
```

The script compiled `Definitions`, `Numeric`, `Curve`, `Proof`, and `Solution` into a fresh private output prefix, verified the ten dependency revisions were clean and pinned, and did not run Lake, download dependencies, or write shared dependency objects. The retained raw record is `local-compile-EVIDENCE.json` in this referee directory; its fresh object prefix was `/var/folders/pw/wkdn0vxs0b54swhpwjg6s0x00000gn/T/nla-sp06-development-r61rcxiw`.

I then inspected all twenty exported theorem declarations with direct Lean `#print axioms`. Every one depends only on `propext`, `Classical.choice`, and `Quot.sound`; none has `sorryAx`, a custom axiom, or compiler-trust residue. The output is retained in `axioms.log`. The source's `#assert_trust kernel` checks cover all twenty exports and every transparent target definition, with `set_option leancert.trust "kernel"` enabled in the proof modules.

The pinned dependency revisions observed by the compile were LeanCert `621a43d7cf21f87872392a01e874f2f1dbddc926`, Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`, and the remaining manifest revisions recorded in `local-compile-EVIDENCE.json`. Candidate and source hashes are in `INPUT-HASHES.sha256`; all referee artifacts are bound by `MANIFEST.sha256`.

After the proof review, I also reread the current candidate `README.md` and
`formalization.yaml` metadata snapshot. The README now describes the twenty
local exports and keeps both final reviews and Linux Comparator verification
pending; the YAML likewise records `sorry_count: 0`, the three permitted
axioms, `whole_problem_verified: false`, and the same pending gates. Their
current hashes are recorded in `INPUT-HASHES.sha256` so the review is bound to
the metadata state seen by the coordinator.

## Remaining gates

This is a final local proof review, not the authoritative Linux Comparator result. A second independent final referee should review the same frozen bytes. The package's `formalization.yaml` correctly records these gates as pending and reports zero proof `sorry_count`; that metadata should be updated only after the Linux/Comparator acceptance is actually obtained. No canonical file, Git branch, status, or solved marker was changed during this review.
