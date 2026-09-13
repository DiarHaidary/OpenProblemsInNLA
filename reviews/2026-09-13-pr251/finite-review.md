# PR #251 independent finite-certificate audit

**Verdict: no actionable correctness finding in the finite row certificates or arithmetic bridge.** The independent exact check establishes a genuine nonnegative rational factorization of the original complete `C_7` through 127 terms, hence an upper bound `rank_+(C_7) <= 127 < 128`. It does not establish exact rank 127 or a minimal counterexample dimension.

Head reviewed: `589ec79798ee42adc7a7160a376c67252280a121`, read-only worktree `/private/tmp/nla-audit-251`. All reviewer artifacts are in `/private/tmp`; the worktree remains clean. Remote build authenticity, canonical control receipts and final public theorem contracts are separately assigned to the coordinator and structural reviewer. This report does not claim a fresh local Lean compilation.

## Complete literal-row source audit

I inspected the actual Block00 and Block15 files for all three families and checked **every byte of all 48 block files** against the complete reviewed source template, including header, exact predecessor import, options, namespace, all eight theorem signatures and proof bodies, axiom-print commands and namespace terminator. Any additional source command, altered type, import, tactic, row literal, duplicate or omitted row would fail this check. All 48 files matched exactly; their SHA-256 hashes are recorded in the checks JSON.

There are exactly 16 blocks per family and eight theorems per block. Each of Singleton, Pair and Four contains rows 0 through 127 once, and each theorem quantifies over **every** `b : Mask7` (`Fin 128`). Thus the batch layer contains 384 distinct literal-row theorems covering 49,152 ordered family/row/column obligations. Each proof is `decide +kernel`; none uses `native_decide`, a supplied table, an assumption, or a changed decidability instance. The chain starts at FamilyDefs, proceeds through all Singleton blocks, all Pair blocks and all Four blocks. `FamilyIdentities` imports `Four.Block15`, retaining the complete chain. The complementary core is separate structural work, not an omitted fourth finite family.

The two literal mask arrays in FamilyDefs were parsed as inert data and matched against independently enumerated coordinate subsets: exactly all 21 pairs and all 35 four-element subsets, in the defined atom order. None is omitted or duplicated.

## Arithmetic boundary audit

I read Encoding, FamilyDefs, CertificateBridge, Certificate and Rank in full to trace the original matrix into and out of the finite identity. The structural reviewer independently owns those modules' complete proof review.

- `BoolVec 7` is the full type of seven-coordinate Boolean functions. Encoding proves the vector/mask correspondence structurally. There is no restriction to a selected row or column subset.
- The target subtraction is over the reals. `natSquareOneMinus` explicitly branches at one, using `(1-t)^2` when `t<=1` and `(t-1)^2` otherwise. Its cast proof uses guarded natural subtraction and a ring identity, preserving entries with dot product greater than one.
- The four atom blocks have sizes 64,7,21,35, totaling 127. Core atoms represent complementary row pairs; singleton atoms repair columns of weight one; pair atoms are supported only on containing columns; four-set atoms use the nonnegative truncated cardinality excess.
- `sourceD` is 1 for column weights zero or one and `(p-1)^2` otherwise. Its strict positivity theorem correctly distinguishes these cases. There is no zero denominator.
- `CertificateBridge` splits the full sum into the four families using existing index identities, combines the explicit component premises, and casts the resulting natural matrix product to the real original `cMatrix`. `Certificate` supplies each component premise with the completed family/core/closed theorem; the final certificate has no added hypotheses.
- `scaled_certificate_gives_factorization` takes W and V as natural matrices, so their casts are entrywise nonnegative. The right factor is the actual real matrix `V[k,b]/d[b]`. The proof distributes the column's common denominator through the finite sum and cancels it only after proving it nonzero. No square-root or floating-point bridge is used. The resulting factorization is suitable for the actual minimum-width rank definition.

## Independent exact arithmetic

The reviewer script `/private/tmp/nla-pr-251-finite-check.py` uses only the Python standard library. It imports no submitted generator, checker or PASS log. It completed successfully using `/private/tmp/nla-batch-python/bin/python`.

1. Enumerated all 128 Boolean 7-tuples and independently reconstructed the **original** matrix using ordinary coordinate dot products and signed integer subtraction: `C[a,b]=(1-sum(a_i*b_i))^2`. This retains all 16,384 prescribed entries. Checks include empty-row values 1, dot-one values 0 and the all-ones diagonal value 36.
2. Constructed the four atom families directly from mathematical sets and their complements; obtained 128x127 W, 127x128 V, and 128 positive column denominators. Formed the actual rational H using `Fraction(V[k,b],d[b])`.
3. Verified entrywise nonnegativity of W, V and H; all denominators positive with values `{1,4,9,16,25,36}`; and every exact rational product entry `sum_k W[a,k]*H[k,b] = C[a,b]`.
4. Independently checked each of the four family sums against its cardinality formula for all 128x128 row/column pairs: **65,536 exact component identities**, including the structural core, and the scaled full identity for all 16,384 entries.
5. Only after establishing the independent construction, compared it with the inactive retained Lean W/V/d arrays, submitted factor JSON and four numeric CSV files. Every entry agrees. The inactive CertificateData table is not imported by Solution and is not used as a theorem oracle.
6. Negative controls correctly rejected an omitted singleton correction, a changed atom entry and replacing signed subtraction in the original target by truncated natural subtraction.

Evidence: `/private/tmp/nla-pr-251-finite-checks.json` contains complete source hashes and check counts; `/private/tmp/nla-pr-251-finite-check.log` records the successful run. These computations independently substantiate the finite mathematical claim and coverage, while compilation/authentication remains the separate canonical verification audit.
