# Independent informal review — SP-07 continuation

Reviewer: separate Codex AI agent `/root/review_sp07_sp08`, 14 September 2026 (UTC). This review is independent of the integration agent and submission authorship; it is informal AI review, not external human peer review or formal verification. No Lean verification was attempted.

**Verdict: PASS for the identified partial results; FAIL to satisfy the completion criterion for Solved.** Retain `Open` for the canonical sharp-constant target, describing the certified bound as supporting partial progress. This follows the existing SP-07 treatment and the repository definition of Partially resolved in terms of proved substantive cases of the displayed target: the new examples do not determine any exact fixed-dimensional or universal sharp constant.

## Scope and mathematical audit

The canonical target asks for the exact dimension-independent sharp normal spectral-matching constant, not a counterexample to constant one or to any other proposed lower-bound value. The new report's Sections 2–4 prove a strict global lower bound `C_normal > 103077/100000`. Section 4 also proves the weaker five-dimensional lower bound `>1.02671`. These are substantive additions to the earlier repository's two-eigenvalue subclass lemma and are not duplicates of a full solution.

I checked the rational reflection construction in Lemma 2.1, normality by orthogonal similarity, multiplicities in the spectral lists, the deficient Hall block, and positivity of the full norm certificate. With `t=10000001/10000000`, the seven-dimensional squared matching distance is exactly `1062488691325671649394413/10^24`, greater than `(103077*t/100000)^2`. Positivity of `t²I-M* M` implies the strict full operator-norm bound. Thus the ratio conclusion follows without a numerical eigensolver or rectangular-block norm substitution.

I also read the written proofs in Sections 6–8: the rank-one reflection compression to dimension three, the two-values-per-Hall-side compression and the resulting at-most-three-distinct-values reduction to `c_3`, and the distinct-value refinement of the truncated singular-value estimate. The subspaces used in the normal-compression argument retain two reducing eigenvectors with at most a one-dimensional remaining complement. The rank-one argument preserves normal diagonal compression and its Hall gap. No gap was found in these supporting arguments. None evaluates `c_3` or proves a finite-dimensional reduction for unrestricted normal pairs.

## Reproduction and independent checks

The supplied standard-library `check_certificate.py` was inspected and rerun, with assertions enabled and site packages disabled, on the seven- and stronger five-dimensional inputs. Both passed; records are `seven.json`, `five.json`, and `five.log`.

I wrote a separate checker, `independent_check.py`, which reconstructs the rational reflection with Fraction arithmetic, realifies the full complex difference as a 14-by-14 real matrix, and verifies 14 positive Schur-elimination pivots of its norm Gram bound. It additionally enumerates all 5040 permutations independently of the supplied matching algorithm. This passed (`independent.json`, `independent.log`). Reproduce with:

```sh
python3 -S independent_check.py PATH_TO_PACKAGE/results/certificate_seven.json independent.json
```

The input SHA-256 is `c9c438f33153286f970739dd8833cc7c854a9afd7f6c7c68ce9b9ddfce053d4c`. Source snapshot hashes (not a claim that every file was individually audited) appear in `reviewed-sha256.json`. The proof does not rely on the saved optimization campaigns, which were not rerun in this review.

## Resolution-policy decision and remaining obligations

Under CONTRIBUTING.md and RESOLVED.md, an independently audited partial theorem cannot be promoted to Solved. A dimension-uniform matching sharp upper bound, exact extremal value, and global sharpness argument are missing. The package expressly disclaims them. The historical literature's numerical upper endpoint was not independently literature-verified here and is not needed for the accepted lower-bound claim; do not present it as a new result. No novelty priority is certified by this audit. Preserve the permanent ID and mathematical target.
