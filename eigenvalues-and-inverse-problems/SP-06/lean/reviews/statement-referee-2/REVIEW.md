# SP-06 independent statement review 2

Reviewer: OpenAI Codex agent `/root/lean_iv01_next` (AI), 13 September 2026.
Phase: statement boundary only; no proof implementation. I did not author the
SP-06 package and did not rely on the other statement referee's report.

## Verdict

**Mathematical statement boundary: APPROVE. Overall package: REQUESTED
CHANGES**, for one minor documentation portability issue described below.

The reviewed canonical source boundary is upstream commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`. The four source hashes recorded
in `raw-results.json` match `SOURCE_MAP.md` exactly for the canonical README,
solution Markdown, problem TeX and solution TeX. The formal package has 20
deliberate Challenge contracts, and its Comparator names and metadata results
match the declarations in order. There is no `Solution.lean`; no proof or
Lean-verified status is claimed.

## Fidelity and scope

The target retains arbitrary finite complex Laurent coefficients, positive
lower and upper bandwidths, nonzero extreme coefficients, every positive
finite section size, the `i-j` Toeplitz convention, the actual Mathlib unit
circle, a continuous injective map avoiding zero, and the actual complex
matrix algebra spectrum. `Fin n` uses zero-based representatives but preserves
the original exponent difference. The formal target's `hasAdmissibleBand`,
`hasRealJordanCurve`, `allFiniteSpectraReal`, and `targetImplication` cover
the complete original universal implication. The stronger source claim that
the curve encloses zero is intentionally omitted because the catalog target
requires only avoidance of zero.

The 20 contracts expose the complete negative-resolution bridge: admissible
witness, exact Laurent composition, both root endpoints, uniform slope,
existence and uniqueness, root Lipschitz control, continuous radius, curve
continuity/injectivity/nonzero, the exact imaginary-part identity, symbol
reality on the entire curve, the order-two Toeplitz matrix, actual spectral
membership, nonzero imaginary part, nonreal finite spectrum, the concrete
counterexample, and negation of the universal target. No contract assumes the
existence or continuity of the radius inside the final Jordan-curve theorem.

The exact coefficient calculation gives
`a-a^2 = -64 z^(-2) + 8 z^(-1) - 128 - 8 z - 63 z^2 - 16 z^3 - z^4`.
The endpoint values are `F(1/2,-1)=-25/32`, `F(1/2,1)=-23/32`,
`F(2,-1)=1`, and `F(2,1)=5`. Factoring the difference of `F` on
`1/2 <= s <= r <= 2`, `-1 <= c <= 1` gives the declared uniform slope;
the endpoint signs and strict slope give the unique root. Comparing two
roots gives `|r-s| <= 8 |c-d|` from the slope and `s^3/4 <= 2` (or the
symmetric bound). This is the required continuity bridge, without samples,
finite subdivision, or an implicit-function assumption. Positive radial
scaling on the actual unit circle gives continuity, injectivity and a
nonzero image. The exact order-two section is
`[[-128,8],[-8,-128]]`, with characteristic polynomial
`(lambda+128)^2+64` and eigenvalue `-128+8i`; hence the actual spectrum is
not wholly real and the universal target is negated.

## Mechanical statement checks

Direct Lean 4.33.1 elaboration of `Definitions.lean` and `Challenge.lean`
passed using the pre-existing clean MI-22 dependency objects at the pinned
revisions. The output contains exactly 20 intentional `sorry` warnings. A
separate direct Lean inspection checked all 20 declaration types and reports
exactly `[propext, sorryAx, Classical.choice, Quot.sound]` for each; the
`sorryAx` is expected at this statement-only phase and is not proof evidence.
No Lake command, dependency download, or shared-cache build was used.

## Requested change

`formalization.yaml` field
`reproduction.statement_boundary.evidence_prefix` contains an absolute
author-machine `/var/folders/...` temporary path. Replace it with a portable
repository-relative evidence location or a sentence saying that the command
creates a fresh temporary prefix. This does not change any mathematical
statement or contract, but it should be corrected before final publication.

The exact package/source hashes, raw direct-Lean receipts, declaration-type
inspection and compact check results are in `raw-results.json`,
`typecheck-EVIDENCE.json`, `actual-types-axioms.log`, and the self-hashed
`EVIDENCE-MANIFEST.json`. This report is an independent statement review; it
is not approval to label SP-06 Lean verified.
