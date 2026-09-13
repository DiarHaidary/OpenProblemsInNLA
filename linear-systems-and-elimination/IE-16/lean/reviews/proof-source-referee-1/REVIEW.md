# IE-16 independent full source referee report

**Reviewer:** `/root/lean_iv01_next` (AI agent)  
**Date:** 2026-09-13 (America/New_York)  
**Phase:** proof-draft source review; no final Lean/Comparator acceptance  
**Reviewed revision:** `28bdf9e85541764b6a5cb2debd647b9cebaea21f`  
**Verdict:** **mathematical fidelity PASS; mechanical verification BLOCKED**

## Scope and source identity

I read the IE-16 review protocol at
`/tmp/nla-ie16-development-worktree/docs/lean/REVIEW.md`, the canonical
problem and Holden manuscript retained at upstream source revision
`b73cd1804e40e0d101294eedb156984f0d62b4a6`, the approved statement boundary,
all proof modules, `Solution.lean`, `formalization.yaml`, and
`comparator.json`. The development worktree was clean at the reviewed
revision. No source file was edited and no local Lean, Lake, dependency, or
cache process was run.

The canonical retained-source hashes, verified against
`verification/source-snapshot/SOURCE_HASHES.json`, are:

| source | SHA-256 |
| --- | --- |
| `canonical-README.md` | `bc4ac8591a0dd4fc3533ad278741c335b43bb1677e4148340cb0b25f2938558f` |
| `canonical-problem.tex` | `f9bae980a686bbcce701b11a1e507acc53d86552a58fc946c998e4529051f81f` |
| `holden-solution.tex` | `e0b8de10f215fa216541985f5602787995a54d9f6908bd17095f8be942ce2390` |
| `holden-submission.md` | `e88e126c76616619abd2855fa666b219e2de77607b711dc94f062fa63a2fbe63` |
| `verify.py` | `7b8e0fdcbfcfe0a5c6f9442baf6352838f572099f23ec05a28fcfaac71c7cb7e` |
| `all_subset_certificate.json` | `29e452375dbedfa4bd31bb28d78e1beb0ce34df0072f8a41a0e58515914b6228` |

The exact Lean proof-source hashes at the reviewed commit are:

| file | SHA-256 |
| --- | --- |
| `NLA/IE16/Definitions.lean` | `e4681f2083d71d8980adcd70e7cf26367e0e84dbc1773f4d2f082bf2417c9507` |
| `Challenge.lean` | `85cbe24c7657d9ddc37728db5bb1740a80ddab60e3eb4676e329df40a7b1737c` |
| `NLA/IE16/Numeric.lean` | `c90b9378f26691bba31056c333fb92ea8406f21a64a82d4c72ef4f40c79887fa` |
| `NLA/IE16/Minimax.lean` | `4d2a8c38b3413e716a53ff81b9718089b4dbb48c4f0f1ab2e1ea0a92e87465c5` |
| `NLA/IE16/WeightedDraft.lean` | `1163f0f71fb5ce4f39374f09a1ea452a9580c853f8d1e17aad1b4a7482a21c36` |
| `NLA/IE16/WeightedBridgeDraft.lean` | `b082910816dd73ea012d77e2c3c63797b7c7cfee9eaec82fed619a458113c5c5` |
| `NLA/IE16/FullMinimumDraft.lean` | `ec971dbdf3cbe7de0c2707eea2facbc62f613d280e384c245478a98105f57ef0` |
| `NLA/IE16/SubsetBoundsDraft.lean` | `d88ff86286f881e342ae19f40ea742fd39e3b0b070f0c259f9709e368da95ce2` |
| `NLA/IE16/SubsetGeometryDraft.lean` | `a9324fbe3b761aa40a8a79ea8ff3245cc06877fda713ea7f400062ad79fd6bb2` |
| `NLA/IE16/FinalContractsDraft.lean` | `5b4bf1715e97677e1cf532990646aa3dea54c6dee58f50b3af7be55815ddbc7a` |
| `Solution.lean` | `dea94208561e823f1b76f831b4a8c5c5f419e9214c2b0a10ec5d4abc8612f69c` |

The boundary files are proof-independent `Definitions.lean` and the
intentional fifteen-placeholder `Challenge.lean`; their hashes match the
accepted boundary. The current approved `NUMERICAL_TARGETS.md` hash is
`e0fb3c0b10e29d2574efa62064f1bd45bcff1175b5538f580f5ebafb1025c950`.
The development snapshot has the recorded nonmathematical wording correction
`0bea606a903e7956cac9765048db9881f07f29819f405269545f1da12ec6d682`; its
correction record says that definitions, constants, quantifiers and sources
are unchanged.

## Fidelity review

The formal boundary retains the full target. `Poly` is `Polynomial ℂ`;
`feasible` requires actual complex polynomial degree at most `k` and value one
at zero; `maxModulus` is the finite supremum of actual complex norms;
`M` is the infimum over all feasible polynomials; and `subsetMax` is the
finite maximum over every powerset member of cardinality `k+1`. The universal
assertion quantifies over every `n ≥ 3`, every finite set of `n` distinct
nonzero complex points, and every `1 ≤ k ≤ n−2`. No floating-point or fixed
polynomial definition replaces these objects. Empty-set branches are merely
total definitions and are excluded by the hypotheses used in the proof.

The numerical module defines the exact nine-point image
`omega^a + (1/1000) omega^b`, proves injectivity and nonzero points, and
checks the exact witness polynomial and rational value
`3003003000/1001003001001`. The nine positive rational weights sum to one and
the four required weighted complex moments vanish. The weighted square
identity in `WeightedDraft`/`WeightedBridgeDraft` then gives a lower bound for
every feasible degree-four polynomial, so the witness objective plus this
lower bound establishes the actual full infimum and its `IsLeast` attainment.
This is a valid certificate route independent of the manuscript’s optional
amplification theorem.

The generic `Minimax` module proves the five-node complex Lagrange formula,
constructs an interpolating attainer with value one at zero, proves positivity
of the basis norm sum for nonzero nodes, and derives the lower bound for every
feasible polynomial. Thus the subset `M` values are actual infima with
attainment, rather than lookup values.

`SubsetBoundsDraft` and `SubsetGeometryDraft` preserve every five-point
subset. The label/image/cardinality lemmas are injective bridges between the
nine complex points and `Fin 3 × Fin 3`. The companion-count disjunction is
the exhaustive occupancy argument: either four points have one same-cluster
companion, or three points have two. The exact rational margins give the
strict coefficient bounds 109 and 146; hence the Lagrange sum exceeds 436 or
438, which implies the uniform `23/10000` upper bound. No subset is dropped.
`FinalContractsDraft` proves nonempty/positive subset maximum, the ratio
bound, `4/pi < 13/10`, and finally instantiates the original universal target
at `n=9`, `L=explicitL`, `k=4` to derive `¬ IE16Conjecture`.

The source attribution is truthful: the counterexample is attributed to
Sidney Holden, while the formalization metadata credits George Stepaniants,
Department of Computing and Mathematical Sciences, California Institute of
Technology, with no email address. `Solution.lean` contains no `axiom`,
`native_decide`, or `sorry`; its fifteen public exports have explicit
LeanCert kernel assertions and axiom prints. `Challenge.lean` is not imported
by `Solution.lean` and its placeholders are not proof evidence.

## Independent finite-certificate check

I ran the retained standard-library verifier, without Lean or Lake:

```text
python3 verification/source-snapshot/verify.py --digits 20 \
  --output /tmp/nla-ie16-independent-referee/certificate-run
```

The run passed. Its generated certificate has 126 records, nine positive
weights, exact full value `3003003000/1001003001001` as printed by the
program’s report, and profile counts 18, 27, 81. The generated
files are retained at `certificate-run/`: the JSON hash is
`7577f2e0b465b4f75e6a313f2b412d14426a2435918dff4447182a7f27566f2f` and the
human report hash is `e69a8bf5b2c8ed0ce48cdfbfd9d9bb785bdb0a502cdfb722b5bedd6f1821b3b0`.
The raw stdout is in `python-verify-stdout.txt`. This validates the finite
certificate and all 126 enumerated subsets; it does not validate Lean or the
analytic unbounded-family theorem.

## Concrete blockers and required next gates

The immutable development run `34771972369` at this revision did not compile
the proof graph. The raw logs at
`/tmp/nla-ie16-development-evidence/run-34771972369/extracted/` show:

* `Numeric.lean` timed out at `clusterPoint_injective`, then reported unresolved
  algebra goals in `witness_eval_sq_norm` and recursion-depth failures in the
  moment simplification. Later errors include the expected cascade from the
  failed declaration.
* `Minimax.lean` has pinned-parser errors for the `∑ z in S` notation and
  tactic failures in `lagrangeSum_pos` and `lagrangeValue_norm`.
* Because Numeric and Minimax failed, all later modules and `Solution` were
  skipped. No proof or Comparator conclusion can be inferred from this run.

The runtime repair must fix these exact errors, compile every module from a
clean pinned environment, inspect `#assert_trust kernel` and `#print axioms`
for all fifteen exports, and run the Linux Comparator against the same source
hashes. Before a publication PR, change the development `lakefile.toml`
default target from the statement `Challenge` to the completed `Solution` and
update the phase/status metadata only after those gates pass. The present
report therefore approves the mathematical source boundary conditionally but
does **not** authorize a Lean-verified count or solved-status promotion.
