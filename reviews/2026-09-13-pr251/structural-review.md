# PR 251: independent NR-03 structural Lean review

Verdict: **PASS; no blocking mathematical or structural source finding.** The live source proves an actual real nonnegative factorization of the complete prescribed matrix C₇ through 127 atoms, hence rank₊(C₇) ≤ 127 < 128 and the negation of the original universal assertion. This verdict is based on source inspection and independent exact calculations, not submitted PASS reports.

Reviewed read-only checkout: `/private/tmp/nla-audit-251`, exact head `589ec79798ee42adc7a7160a376c67252280a121`. Original published base: `752218e5417998b7f4d2aee9c447ca5d256fe530`. Project: `nonnegative-and-positive-factorizations/NR-03/lean`.

## Scope and evidence

I read Definitions, Challenge, comparator.json, Solution and all ten non-batch modules in the actual Solution import closure: Definitions, Encoding, FamilyDefs, Core, Index, FamilyIdentities, CertificateBridge, Certificate, Rank and Solution. I independently traversed the imports, finding exactly 58 project modules: these ten and all 48 row-certificate modules. The row modules' full literal proofs and numerical certificate were independently audited by colleague `/root/review_249_ie27_ie28`; that colleague reports exact whole-file template agreement for every block and an independently derived rational product check of every C₇ entry. I independently checked their integration into the structural proof.

My repeatable scratch check is `/private/tmp/nla-251-structural-check.py`, with results `/private/tmp/nla-251-structural-check.json`. It completed successfully under `/private/tmp/nla-batch-python/bin/python` and verifies:

- Actual import closure, all 48 expected blocks and all 384 row references in their respective family aggregations.
- Exact whitespace-normalized statement equality between each of the ten Challenge contracts and its proved Rank declaration; each export is declared once in the active source and receives both `#assert_trust kernel` and `#print axioms` in Solution.
- No uncommented `sorry`, `admit`, custom `axiom`, `native_decide`, `unsafe`, `implemented_by`, `sorryAx`, `run_tac` or `run_cmd` in the live project closure. All modules disable automatic implicit parameters. Challenge's ten statement holes and supplementary CertificateData are not imported by Solution.
- Exact agreement between the actual closure and all manifest paths, byte counts and SHA-256 hashes.
- Byte identity of every active source and the Challenge/comparator/build boundary with the claimed verified source commit `f664d07e82aaa60bc9c78dd1946e763168c5c530`.
- Unchanged original canonical README Context and Problem text and unchanged 217-entry problem-ID registry relative to the published base.
- Symbolic verification of both equalities in the informal polynomial identity, and all 36 finite cardinality cases `0 ≤ t ≤ s ≤ 7`, with positive denominators and nonnegative four-family contributions.

## Original target and definitions

Definitions.lean:24–65 uses every Boolean function `Fin n → Bool` as a row and column index. `boolDot` is the ordinary real sum of Boolean 0/1 products. `cMatrix n a b = (1 - boolDot a b)^2` is a square over ℝ, including the fixed values at intersections larger than one. There is no free matrix completion, omitted row, selected column, or change to the entries beyond intersections 0/1.

`FactorizationData` requires entrywise nonnegative real W and H and exact matrix equality W*H=X. `HasNonnegativeFactorization` quantifies arbitrary real coordinates, so the rational witness is a valid witness for the original real rank. The minimum definition uses `Nat.find` on existence of an actual finite factorization. Rank.lean:82 proves both attainment and minimality under that existence premise; the concrete witness supplies it before using the minimum. Its default-zero totalization for a matrix without any nonnegative factorization has no role in this counterexample. Every Cₙ is a finite nonnegative matrix and admits the usual identity factorization, so the mathematical target still has its usual meaning for all n.

The target is exactly `∀ n : ℕ, 3 ≤ n → nonnegativeRank (cMatrix n) = 2^n`. Rank.lean:113 instantiates that quantifier at n=7 and contradicts the strict rank bound. It does not require the stronger informal all-n construction to be formalized, nor does it claim rank₊(C₇)=127 or that seven is the smallest counterexample.

The primary original source independently checked was [Vandaele, Gillis, Glineur and Tuyttens, §6.4, Conjecture 4](https://arxiv.org/html/1411.7245#S6.SS4). It specifies the complete 2ⁿ×2ⁿ Boolean-indexed matrix `(1-|aᵀb|)^2` and full nonnegative rank. Since Boolean dot products are nonnegative, its absolute value makes no difference. The canonical target and formal definition agree with this source.

## Structural proof audit

Encoding.lean:29–116 proves a structural binary encoding for all Boolean vectors, not an assumed Python correspondence. `maskVector_maskOfVector a = a` suffices to pull back every mask identity to every Boolean row and column. The absence of a second inverse theorem is harmless: no arbitrary Boolean vector is excluded, and the real target is connected directly by `natTarget_cast`.

Encoding.lean:65 and 122 handle natural subtraction correctly. The helper is `(1-t)^2` when t≤1 and `(t-1)^2` otherwise, and its real cast is proved equal to the required real square for every natural t. Thus entries with overlap 2 through 7 remain 1,4,9,16,25,36.

FamilyDefs implements the same four atom families as the original informal construction: 64 complementary row pairs, seven singleton columns, all 21 pairs, and all 35 four-element sets. Their index intervals are [0,64), [64,71), [71,92), [92,127). Index.lean splits a sum over Fin127 exactly into these four intervals and proves both factor evaluations on each embedded index. There is no missing atom, duplicated contribution in the decomposition, or incompatible factor ordering.

Core.lean proves that each row belongs to exactly one selected complementary pair by the representative `a` if a<64 and `127-a` otherwise. The complement bits, involution and overlap complement identity establish that the core contributes `(1-t)^2(1-(s-t))^2`. The finite complement-bit theorem uses `decide +kernel`; the sum reduction and representative argument are structural.

FamilyIdentities.lean assembles the singleton, pair and four-set identities using `fin_cases a` and the exact row0 through row127 theorem of the correct family, once each and in order. Each row theorem retains the universal column variable, so this covers all 16,384 ordered pairs per family. The code proves `maskCard b ≤ 7` and `maskDot a b ≤ maskCard b`, then applies the closed arithmetic theorem over Fin8. I independently checked all 36 relevant (s,t) cases, including s=0 and s=1, which require the singleton correction and denominator convention.

CertificateBridge.lean:90 and 108 intentionally state conditional algebraic helper theorems. Certificate.lean:21 supplies all five component/closed-identity premises from the proved core, singleton, pair, four and closed-family identities; Certificate.lean:30 then supplies this unconditional full identity to the casting bridge. No certificate correctness premise survives in a public witness theorem.

`genericW`, `genericV` and `genericD` are defined from these families at every encoded Boolean vector. The denominator is one for column cardinality zero or one and `(s-1)^2` otherwise; its strict positivity is proved independently. The scaling bridge turns the finite natural sum into the exact real matrix identity by cast preservation, not by a numeric approximation.

Rank.lean:23 proves that a positive column-scaled integer certificate gives real nonnegative factors `castNatMatrix W` and `scaledRightFactor V d`. It explicitly pulls the column's common divisor outside the finite sum, proves the real denominator nonzero from strict positivity, uses the scaled identity, and cancels the divisor. Rank.lean:63 constructs the unconditional width127 certificate; the remaining public results obtain an actual factorization, an attained/minimal rank, the upper bound, the strict inequality against 2⁷, and the universal negation.

All ten comparator exports match their declared original obligations:

| Export | Established content |
| --- | --- |
| `cMatrix_nonnegative` | Every entry of Cₙ is nonnegative, for every n. |
| `boolVec_seven_card` | The complete Boolean row/column type has 128 elements. |
| `nonnegative_rank_attained_minimal` | The actual minimum is attained and no larger than every admissible width. |
| `rank_le_of_factorization` | An actual width-r factorization bounds the minimum. |
| `scaled_certificate_gives_factorization` | Positive integer scaling yields the named nonnegative real factors and exact equality. |
| `witness_scaled_certificate` | Unconditional complete C₇ certificate with 127 atoms. |
| `witness_factorization` | Unconditional real nonnegative width127 factorization of C₇. |
| `witness_rank_upper_bound` | rank₊(C₇)≤127. |
| `witness_not_full_rank` | rank₊(C₇)<2⁷. |
| `not_targetStatement` | Negation of the entire original universal assertion. |

## Informal proof correspondence and limits

I read the original factor construction and entrywise proof in `references/holden-nr03-2026-09-13/NR03_counterexample.tex`, including its all-n upper bound and strictness argument. The same core, singleton, pair and four-set contributions and denominator appear in the Lean construction. The finite Lean closed arithmetic is a valid n=7 specialization of the informal polynomial identity; independent symbolic expansion confirms the full identity. The general informal construction gives `2^(n-1)+n+choose(n,2)+choose(n,4)` atoms and strictness for all n≥7, but those stronger general-n results are outside the ten formal exports and unnecessary for this complete negative resolution.

The colleague's independent finite audit additionally reports all 16,384 entries of the rational W*H product equal to the fixed C₇, and all four family identities (65,536 entry identities total), with pair/four literals equal to the full respective subset families. Their checker did not use submitted factors to derive the target or construction; it compared Lean supplementary arrays and submitted JSON/CSVs afterward. Evidence: `/private/tmp/nla-pr-251-finite-check.py` and corresponding JSON/log.

I did not compile Lean locally or authenticate GitHub actions/artifact downloads; the root reviewer owns that separate check. Byte identity with the claimed verified source is established here, but kernel acceptance and exact dependency/axiom authentication must come from that root-owned evidence. Metadata/provenance wording and PDF raster inspection are owned by the other reviewer and are not claimed as completed within this structural audit. No source, GitHub state or shared checkout was modified; only the scratch checker, its output and this report were written.
