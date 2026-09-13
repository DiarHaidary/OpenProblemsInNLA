# SP-06 independent final proof referee 2

**Phase:** final local proof review (after statement approval)

**Reviewer:** OpenAI Codex subagent `/root/lean_ie17_next` (AI reviewer,
independent of the proof author and of the first final referee)

**Verdict:** **APPROVE for the local final-proof gate.** I found no material
fidelity, proof-correctness, API, documentation, or attribution defect in the
reviewed source. This is not Linux Comparator acceptance and does not itself
change the catalog status.

## Identity and hashes

The reviewed candidate is
`/tmp/nla-lean-sp06-project/eigenvalues-and-inverse-problems/SP-06/lean`.
The canonical source boundary is commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`.

Proof/configuration hashes at review time:

| file | SHA-256 |
|---|---|
| `NLA/SP06/Definitions.lean` | `5f3e071b9aabbbda27a794f9396022e54585f5d2d254827e50ea90baf80e72b1` |
| `NLA/SP06/Numeric.lean` | `16052a754e8680c587163e1a57d150094ae96a36464a56cc499ec09e9aa5b111` |
| `NLA/SP06/Curve.lean` | `151ff3586667091b16eab3acf03aed32fa5c7db8422a4077095bf914c4392677` |
| `NLA/SP06/Proof.lean` | `d22146a65804efd8ff5c7f7b81ddcd55af8dc1bab7a2518f4961d7699abc9b48` |
| `Solution.lean` | `4aa92168bf3dccc0a03180795c60b404a7e6b531b188eb4ab1d93cf109c3eb42` |
| `Challenge.lean` | `cd75a8f37a174d7dfb68927f7e6aeb23cf0982eb3161d7d9e5a63a7583d73bef` |
| `NUMERICAL_TARGETS.md` | `bfd2a0bcc5c5328ac9f3fd85d56ac7d3b8a5d551236cee68e227cb9acbea1959` |
| `SOURCE_MAP.md` | `b81a8cc5f9e5c1dda318c65c80ed840825a3216d95d53bcfc43cd8bbf7c594f2` |
| `README.md` | `484c547056d30799c805092abd2b23c7094011037f8573ee040047a3b4088dfe` |
| `formalization.yaml` | `ab4ff6aaf2bb1beee1f7379359f67dd40dd88be8747e36f59374fcbbe24357c6` |
| `comparator.json` | `5d19e5fe9d3ac4a69d07a1b14d40e31784a295e7fe8c6925964bfffe97203bb9` |
| `lakefile.toml` | `bd9766f1845b61c296dfda0f5d90ebea58162823e6b4255b8248386485cb383c` |
| `lake-manifest.json` | `fc670db46b75e916e357afa39caba663fade917249f6b4c14b10260b8f9e4c4d` |
| `lean-toolchain` | `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71` |
| `LICENSE` | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

The immutable canonical hashes recorded in `SOURCE_MAP.md` were independently
matched against `git show` at the pinned commit: README
`e2eb891930c96d6a3bdd25c75bfe6bd2798cc8c540ce00ec851f7bf1f0ceb25c`, solution
Markdown `c7adb8f97238049b20e82044d8527b70301779ba041169f74fe603a88ea1ae7a`,
problem TeX `183127180596a36c108ed8575420e3845ca890f3048a32ec1252d61cf60d5311`,
and solution TeX `b7340bf85e0b776ed49a4303af64820b72708eb249fbdc885b9179945e60ffc9`.

## Independent mechanical checks

I ran the package's direct fresh-prefix check with the existing pinned MI-22
objects:

```text
SP06_DEP_ROOT=/private/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages \
  python3 verification/compile_development.py Solution
```

It passed for `Definitions`, `Numeric`, `Curve`, `Proof`, and `Solution`,
checking all ten manifest revisions and clean tracked dependency sources. The
result was recorded in a new temporary prefix; no Lake invocation, dependency
download, shared-cache build, or candidate mutation occurred. Raw copied
evidence is under `raw/`; its `EVIDENCE.json` hash is
`3c279fa0de56d4e77acf45cdc4e2a8df23c08e0f5835134090f1c04b368a1977`.
The five empty module-log hashes are
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
After that direct run, the maintainer made a configuration-only `lakefile.toml`
correction (`defaultTargets = ["Solution"]` and a separate `Solution` library);
the proof, definitions, Challenge, dependency pins, and metadata hashes above
were unchanged. I inspected the corrected file and its separate-library layout
against the adjacent KE-04 package below.

I also directly elaborated an independent `Inspect.lean` against that fresh
prefix and printed the types and axioms of every one of the 14 transparent
definitions and 20 exported theorems. The check passed. The retained
`types-axioms.log` has SHA-256
`4a36ee4841e6f15a9b82de21acc2434f141a0f9e448980a685196023e4f8879c`.
Every exported theorem depends only on `propext`, `Classical.choice`, and
`Quot.sound`; no `sorryAx`, custom axiom, unsafe declaration, or native proof
shortcut was found. The source contains 51 kernel trust assertions, including
all definitions and all 20 exports.

## Fidelity and mathematical proof audit

`LaurentCoefficients` is the full finite-support type `ℤ →₀ ℂ`, so the target
retains arbitrary complex coefficients. `hasAdmissibleBand` expresses positive
lower and upper bandwidths, zero coefficients outside the band, and nonzero
extreme coefficients. `toeplitz` uses the source exponent `i-j` after the
`Fin n` index shift. `allFiniteSpectraReal` quantifies every `n ≥ 1` and uses
Mathlib's actual complex matrix spectrum. `hasRealJordanCurve` is a continuous
injective map from Mathlib's actual `Circle` into `ℂ`, requires nonzero image,
and requires the actual Laurent evaluation to have zero imaginary part on the
whole image. No sampled, limiting, circular-only, or assumed curve replaces
the target.

The exact witness composition is checked coefficient-by-coefficient in
`witness_composition`. The endpoint inequalities and `radial_uniform_slope`
give a root in `(1/2,2)` for every real circle coordinate and prove uniqueness.
The `radial_roots_lipschitz` estimate gives continuity of the selected radius
on the entire Circle. `radial_curve_continuous`,
`radial_curve_injective`, and `radial_curve_nonzero` establish the Jordan and
punctured-plane conditions. `auxiliary_radial_im` and
`radial_curve_symbol_real` prove exact reality on every point of that curve.
The order-two Toeplitz identity and characteristic-polynomial calculation give
the genuine spectral point `-128 + 8*I`; its imaginary part is proved to be
exactly `8`. The final `witness_counterexample` and `not_targetImplication`
combine these obligations without adding assumptions or weakening a
quantifier. One nonreal spectral point at `n=2` is sufficient to negate the
universal finite-section conclusion. The weaker limiting-spectrum question is
explicitly outside scope, matching the canonical source.

## API, packaging, and attribution audit

The definitions use actual Mathlib `Circle`, `spectrum`, matrix notation, and
finite Laurent evaluation. The proof uses exact algebra and a global scalar
root-separation estimate; no custom axiom or hidden numerical certificate is
introduced. Names and module placement follow the statement/proof separation
used by the pinned Schiffer/Forsythe references. The current `lakefile.toml`
has `defaultTargets = ["Solution"]` and separate `NLA`, `Challenge`, and
`Solution` libraries, matching the adjacent KE-04 Comparator-ready layout:
Comparator can build the solution independently of the placeholder Challenge.

`formalization.yaml`, `SOURCE_MAP.md`, README, Apache-2.0 LICENSE, and
`comparator.json` preserve Matthew J. Colbrook's mathematical attribution and
George Stepaniants's formalization affiliation (CMS, Caltech), disclose AI
assistance, and publish no George email. Comparator configuration and the
metadata `main_results` list match all 20 theorem exports.

## Remaining limitations

This report is an independent local final-proof review and macOS direct
elaboration only. It is not the authoritative Linux default-kernel run or a
Comparator acceptance run; `formalization.yaml` correctly keeps
`whole_problem_verified: false` and Linux/Comparator pending. It is not
external human peer review, a literature-priority certification, or a catalog
status change.
