# Referee report: TR-29 k = 2 (R(W_{d1} ⊗ W_{d2}) = 2(d1+d2−2)) and Theorem B / monomial ranks

Date 2026-09-13. Adversarial referee pass over `tr29k2/REPORT.md` (with `PROOF_DRAFT.md`, `scripts/`, `logs/`,
`referee/`), against the source texts `tr29/galazka.txt` (arXiv:1601.06211v3), `tr29/bbcg.txt` (arXiv:1803.01623),
`tr29/ccs.txt` (arXiv:2512.05828). Own code: `tr29k2review/tests/`; logs: `tr29k2review/logs/`; literature notes:
`tr29k2review/lit/`. Nothing under the read-only folders was modified.

## Verdicts

| Claim | Verdict |
|---|---|
| (1) R(x^p y ⊗ u^q v) = 2(p+q) for all p, q ≥ 1 over C, i.e. R(W_{d1}⊗W_{d2}) = 2(d1+d2−2) | **Correct.** No error, no gap. |
| (2) Theorem B, Proposition C and the monomial formula R(x^a y^b ⊗ u^c v^d) = (a+1)(c+1) − (a−b)(c−d) | **Correct.** No error, no gap. |

The only issues are attribution and presentation (§3). None affects correctness.

## 1. Claim (1): line-by-line check

Notation as in REPORT §1: A = p+1, B = q+1, T = x^p y u^q v, S acts by differentiation.

### (C) and the Hilbert function: correct
- For g ∈ S_(i,k) with i ≤ A and k ≤ B, g∘[(ax+by)^A(cu+ev)^B] = (A!/(A−i)!)(B!/(B−k)!) g(a,b,c,e)(ax+by)^{A−i}(cu+ev)^{B−k}.
  Both sides are bihomogeneous of the same degree in (a,b) and in (c,e), so rescaling a representative rescales ν(P)
  and g(P) consistently. The weights absorb this.
- h_Z(i,k) = rank [g_r(P_j)] does not depend on representatives: rescaling a point rescales a row. Repeated
  points give repeated rows, so the rank is unchanged.

### Lemma 1: correct
Only (i,k) ≤ (A,B) is needed, so that (C) applies. Zero weights are allowed. Each use satisfies the range condition:
(1,k) with k ≤ q < B, (i,1) with i ≤ p < A, and in §4 (r−1,k) with r−1 ≤ A/2 and k ≤ s′−1 ≤ B.

### Lemma 2: correct in every bidegree used
- **Factor Ann(u^q v) in degree k ≤ q.**
  - β0^k∘u^q v = q!/(q−k)! u^{q−k}v ≠ 0, and β0^{k−1}β1∘u^q v = q!/(q−k+1)! u^{q−k+1} ≠ 0. These are different
    monomials.
  - Every β1^{≥2} term is killed.
  - Hence G∘u^q v = 0 ⟺ β1² | G.
  - k = 0 and k = 1 are covered.
  - k ≤ q is essential: at k = q+1, β0^{q+1} ∈ Ann. My test E1 confirms that the statement fails exactly there.
- **i = 0.** Immediate.
- **i = 1.** α0∘x^p y = p x^{p−1}y and α1∘x^p y = x^p are independent for p ≥ 1, so both G0 and G1 must be divisible
  by β1².
- **dim.** dim β1²S_(1,k−2) = 2(k−1), so rank Cat_(1,q)(T) = 2(q+1) − 2(q−1) = 4, including q = 1.
- **Symmetric statement.** Same computation with the factors exchanged. The image of Cat_(1,q) is
  ⟨x^{p−1}y, x^p⟩⊗⟨u,v⟩ (E2).

### Lemma 3 (peeling): correct, including all edge cases
- **Setup.** k is minimal in [0,q] with (I_Z)_(1,k) ≠ 0. Lemma 1 applies because (1,k) ≤ (A,B).
- **Each step stays in range.**
  - Lemma 2 is applied only in bidegree (1,k) with k ≤ q, exactly its range.
  - It gives k ≥ 2 and g = β1²g1.
  - g2 = β1g1 has bidegree (1,k−1) with 1 ≤ k−1 ≤ q−1, so it is again in the range, and it vanishes on Z.
  - The descent never leaves the range where Ann(T) = β1²S.
- **Termination.** Minimality of k is contradicted after one step, with no iteration. Equivalently, by descent, every
  vanishing form would have to be divisible by arbitrarily high powers of β1. The k ≤ 1 cases are excluded directly
  by Lemma 2 (Ann = 0 there).
- **Points over u (e = 0).** β1(P) = 0 there, so g2(P) = 0 without using g1. For points with e ≠ 0,
  0 = g(P) = e²g1(P).
- **Points over x (b = 0).** These play the same role in the (i,1) statement with α1, and the same argument works.
- **Points over y or over v.** No special role.
- **Minimality and distinctness are not used.** Z is any finite set with T ∈ span ν(Z), zero weights allowed. Only
  the set-theoretic vanishing of g on Z is used, which is what "Z reduced" means in BBCG Prop 4.4.
- **The draft's squarefree-radical version is also correct.** A squarefree g′ vanishing on Z lies in Ann(T) by
  Lemma 1, yet Ann(T) in these bidegrees contains only multiples of β1². The final version is cleaner.

### Lemma 4: correct; its hypotheses are exactly right
- **Pairing.** b(g,h) = (gh)∘F = h∘(g∘F), because differential operators commute. The left kernel is ker Cat_(i,k)(F)
  since S_(A−i,B−k) × R_(A−i,B−k) → C is perfect, so rank b = rank Cat_(i,k)(F).
- **Factorisation.** By (C) at (A,B), b(g,h) = A!B! Σ_j w_j g(P_j)h(P_j), i.e. Gram = A!B!·V1ᵀWV2.
- **Sizes and ranks.**
  - V1 has size n × dim S_(i,k) and rank h_Z(i,k).
  - X = V1ᵀW has size dim S_(i,k) × n, and Y = V2 has size n × dim S_(A−i,B−k).
  - Sylvester's inequality rank(XY) ≥ rank X + rank Y − n uses n = the number of columns of X, which is the number
    of terms.
  - rank X = rank V1 needs W invertible.
- **Direction of the inequality.** Correct: rank Cat = rank(XY) ≥ h_Z(i,k) + h_Z(A−i,B−k) − n.
- **The evaluation vectors are consistent.** The same representatives (a,b,c,e) are used in ν(P_j), in V1 and in V2.
- **Nonzero weights are necessary, not cosmetic.**
  - Counterexample with zero weights (E3): F = x³u³ with Z = {(x,u)} ∪ {m generic points}, split (1,1)/(2,2).
  - This gives n = 1+m but h(1,1) + h(2,2) − rank Cat = 1+2m for m ≤ 3.
  - The Theorem applies Lemma 4 only to a minimal decomposition, where every weight is nonzero, so the use is legitimate.
  - Lemma 3 is applied to the same Z, and it needs no minimality.
- **Distinct points are not needed.** Repeated points duplicate rows of V1 and V2. The claim "The points need not be
  distinct" is right.
- **Bidegree bookkeeping.** In the Theorem, (i,k) = (1,q) and (A−i,B−k) = (p,1). h_Z(1,q) = dim S_(1,q) = 2q+2 and
  h_Z(p,1) = 2p+2 by Lemma 3. rank Cat = 4 by Lemma 2. So n ≥ 2(p+q).

### Upper bound §3: correct
- **Coefficient of x^i y^{A−i} u^k v^{B−k}.** It is C(A,i)C(B,k) Σ_ε ε^{k+1} Σ_a a^{i+k}. Only t = i+k ∈ {0, N, 2N}
  can survive.
  - t = 0 cancels.
  - t = N forces k ≡ q (mod 2), and with i ≤ p+1 this forces (i,k) = (p,q). The coefficient is 2N(p+1)(q+1).
  - t = 2N occurs only for N = 2, and it cancels.
- **Distinct points.** The 2N points are pairwise distinct, in both parities of q.
- **Other decompositions.** I also checked Gałązka's own construction independently over F_P for all W cases with
  d1, d2 ≤ 4 (G1 below).

### Remarks and side statements
- **Remark (i).** "char 0 or char > max(p,q)+1" is right. Lemma 4 needs A!B! ≠ 0 and a perfect contraction pairing,
  so char > max(A,B). Lemma 2 needs q!/(q−k)! ≠ 0.
- **The finite-field checks.** They are therefore honest tests of the same argument over F_P, and not only sanity
  checks. They used P = 5 only with A, B ≤ 4, P = 7 and P = 11 (mine and theirs).
- **Identification.** W_d ~ x^{d−1}y (BBCG convention) and R_{d1,d2} = Gałązka's r on P¹×P¹ were already verified in
  `tr29review/REVIEW.md` §1(ix).

## 2. Claim (2): line-by-line check

### Definitions and hypotheses: correct
- **Annihilator of a binary form.** For F ∈ C[x,y]_A with A ≥ 1, Ann(F) = (φ,ψ) is a complete intersection with
  deg φ = r ≤ s = deg ψ and r + s = A+2 (Macaulay / Sylvester).
- **Border rank.** br(F) = r.
- **Rank (Comas–Seiguer, Found. Comput. Math. 11 (2011) 65–78).**
  - If r < s, then R(F) = r when φ is squarefree, and R(F) = s otherwise.
  - If r = s, then R(F) = r: a generic member of the base-point-free pencil Ann(F)_r is squarefree (Bertini).
- **So (H_F) ⟺ R(F) = s = deg F + 2 − br(F),** exactly as in §0.
- **Pure powers.** For F = ℓ^A (r = 1), φ is linear, so (H_F) fails and R = br = 1. This is consistent.
- **Missing citation.** The report states the rank theorem as "Classically (Sylvester; Comas–Seiguer)" without an
  exact reference. Add the citation above (issue 5).

### (a) Annihilator of F⊗G: correct
- Cat_(i,k)(F⊗G) = Cat_i(F) ⊗ Cat_k(G) as maps S_i⊗S_k → R_{A−i}⊗R_{B−k}.
- Hence ker = ker⊗S_k + S_i⊗ker.
- rank Cat_(i,k)(F⊗G) = h_F(i)h_G(k).

### (b) Low annihilator: correct
- **Range.** For i ≤ r−1, Ann(F)_i = 0. For k ≤ s′−1, Ann(G)_k = φ′·C[β]_{k−r′}; this is 0 if r′ = s′ or k < r′.
- **Result.** Ann(F⊗G)_(i,k) = φ′·S_(i,k−r′).
- **Checked exactly (E5)** on non-monomial pairs:
  - (x⁴y+y⁵) ⊗ u²v;
  - (x⁴+x²y²+y⁴) ⊗ u²v;
  - (x³y+2xy³+3y⁴) ⊗ (u⁴v+v⁵), a non-monomial G with φ′ = β0β1²;
  - x³y² ⊗ u²v.

### (c) Peeling for general binary forms: correct
- **Range.** (r−1,k) ≤ (A,B).
- **Descent.** A nonzero g ∈ (I_Z)_(r−1,k) with k minimal lies in φ′·S_(r−1,k−r′). This forces r′ < s′ and k ≥ r′.
- **Use of (H_G).** φ′ = λ²μ with λ linear (over C every factor is linear).
- **Why the step works.**
  - g = λ²(μg0) and λμg0 ∈ (I_Z)_(r−1,k−1), with k−1 ≥ r′−1 ≥ 1.
  - It vanishes on Z by the same case split: either λ(P) = 0, or λ(P)² ≠ 0 forces (μg0)(P) = 0.
  - The descent stays in the range k ≤ s′−1, where (b) holds.
- **Analogue of Lemma 3.** This is the exact analogue of Lemma 3: points on the line λ = 0 play the role of the
  points over u.
- **Both (H) are needed for (c).** They matter only when r < s, and they are necessary. Computationally, where (H)
  fails the formula is violated. My negative control: (x⁴+y⁴) ⊗ u²v has a 6-point support over F_5, while the naive
  formula would give 10.

### Theorem B: correct
- **Splits.**
  - First multidegree: (r−1, s′−1).
  - Complementary multidegree: (A−r+1, B−s′+1) = (s−1, r′−1), because r+s = A+2 and r′+s′ = B+2.
- **Hilbert function values.**
  - By (c) with (H_G): h_Z(r−1,s′−1) = r s′.
  - By (c) with (H_F), swapped: h_Z(s−1,r′−1) = s r′.
- **Catalecticant rank.**
  - By (a), rank Cat_(r−1,s′−1) = h_F(r−1)·h_G(s′−1) = r·r′.
  - Here h_F(r−1) = r.
  - h_G(s′−1) = s′ − dim φ′C[β]_{s′−1−r′} = r′. For r′ = s′ it is s′ = r′ directly.
- **Lemma 4 gives** n ≥ rs′ + sr′ − rr′.
- **Algebra.** R(F)R(G) − (R(F)−br(F))(R(G)−br(G)) = ss′ − (s−r)(s′−r′) = rs′ + sr′ − rr′. Correct.

### Proposition C: correct (proof is roundabout)
- **The detour.** Under (H_F) alone, (c) gives h_Z(s−1,r′−1) = sr′, and n ≥ |Z| ≥ h_Z(s−1,r′−1) already gives
  R ≥ sr′. The detour through Lemma 4 adds rr′ − rr′ = 0.
- **The consequence is correct.** "R(F⊗G) = R(F)R(G) unless both factors have R > br" holds: every binary form
  satisfies R = br or (H), and the four cases are covered by Prop C, its swap, or the flattening bound rr′.

### §4.1 monomials: correct
- **Annihilator.** For x^a y^b with a ≥ b ≥ 1, Ann = (α1^{b+1}, α0^{a+1}), so r = b+1 and s = a+1.
- **(H_F).** If a > b, φ = α1^{b+1} has a repeated factor (b+1 ≥ 2). If a = b, then r = s.
- **Bound.** Theorem B gives (b+1)(c+1) + (a+1)(d+1) − (b+1)(d+1).
- **Algebra.** Expanding both sides gives a + c + 1 + ad + bc − bd, so this equals (a+1)(c+1) − (a−b)(c−d).
- **Matching Gałązka's upper bound.**
  - His Thm 1.5(i) (galazka.txt l.175–178) with (k0,k1,l0,l1) = (a,b,c,d) is (k0+1)(l1+1) + (k1+1)(l0+1) − (k1+1)(l1+1),
    which is identical.
  - His hypotheses are k0 ≥ k1 ≥ 1 and l0 ≥ l1 ≥ 1, exactly the corollary's range.
  - His proof (l.1177ff) treats k0 = k1 or l0 = l1 via eq. (2), and otherwise uses the M-point binomial scheme.
  - I re-verified that construction computationally (G1): |Z| = M, F ∈ span ν(Z), and equality holds in Lemma 4 at
    the Theorem B split, for 10 exponent tuples including the non-W cases x³y²u²v, x⁴yu³v², x⁵y²u³v, x⁴y³u⁴v² and
    x⁴y²u³v.
- **Consistency with Gałązka's lower bounds.**
  - (ii) is Prop C for monomials.
  - (iii) (k1+2)(l1+2) − 1 coincides with the formula when a = b+1 and c = d+1.
  - The formula is ≥ both in general: formula − (a+1)(d+1) = (b+1)(c−d) ≥ 0.

## 3. Issues found

| # | Location | Severity | Issue | Fix |
|---|---|---|---|---|
| 1 | §0 "The earlier values are re-proved…", §7 "Known lower bounds and cases", "What is new here" | **moderate (attribution/novelty)** | The (4,4) case R(W_4⊗W_4) = R(x³yu³v) = 12 was claimed before, in M. Gałązka's unrefereed note *On the bihomogeneous rank of x^3yu^3v* (homepage mimuw.edu.pl/~mgalazka/example.pdf, PDF dated 2021-05-24). It is proved by radical-ideal peeling plus Thm 1.5(iii). Separately, Gałązka Thm 1.5(ii) with l0 = l1 already gives the whole d2 = 2 row, and (i)+(iii) give the (3,3) value. | Cite the note and say that (4,4) was claimed there. Say that (d1,2) follows from Gałązka (ii) as well as from BBCG Prop 4.4. |
| 2 | Lemma 4, §7 "What is new here" | moderate (attribution) | Lemma 4 is, up to notation, the key step of K. Wang–A. Seigal, *Lower bounds on the rank and symmetric rank of real tensors*, arXiv:2202.11740 (J. Symbolic Comput. 2023), Thm 1.8 / Thm 3.13 (srk T ≥ sdrk_j T + sdrk_{d−j} T − rk T^(j)). Their proof writes T^(j) = UΛS with evaluation matrices U, S and applies Sylvester's rank inequality; the report's Lemma 4 is the same argument with rk U = h_Z. What is new is the application: the unbalanced split (1,q)/(p,1), where the Hilbert functions are maximal and the catalecticant rank is only 4. | Credit Wang–Seigal for the Sylvester-rank device and present the split as the new ingredient. |
| 3 | Lemma 3 and §4(c) "adapts BBCG Prop 4.4" | minor (attribution) | The peeling step (a radical ideal lets you divide out a squared linear factor) is also in Gałązka's proofs of Thm 1.5(ii) (descending induction, galazka.txt l.1233–1262) and (iii) ("t1 is divisible by β1², so t1/β1 ∈ I", l.1272). In particular, (c) for monomials in bidegree (k0,l1) *is* Gałązka's proof of (ii), and Prop C for monomials *is* Gałązka (ii) / BBGV Prop 4.3. | Cite Gałązka's proofs of (ii) and (iii) next to BBCG 4.4. |
| 4 | Proposition C proof | cosmetic | The detour through Lemma 4 is unnecessary: n ≥ |Z| ≥ h_Z(s−1,r′−1) = sr′ directly by (c). The Lemma 4 terms rr′ − rr′ cancel. | Shorten to one line. |
| 5 | §4 Setting "Classically (Sylvester; Comas–Seiguer)" | minor | The rank dichotomy R(F) ∈ {r, s} (with (H_F) ⟺ R = s, and R = r when r = s by Bertini) is used essentially but has no exact reference. | Cite G. Comas, M. Seiguer, *On the rank of a binary form*, Found. Comput. Math. 11 (2011) 65–78, and Sylvester / Kung–Rota for br = r. Add the one-line Bertini remark for r = s. |
| 6 | Lemma 4 statement | cosmetic (already right) | "With all w_j ≠ 0" is necessary, not cosmetic: my E3 test shows the inequality fails with zero-weight points. A reader could miss this, because Lemma 1 and Lemma 3 allow zero weights. | Add "(the inequality fails with zero weights)". |
| 7 | §4.2 | cosmetic | The name "naive formula" is used loosely. Where (H) fails, rs′+sr′−rr′ can exceed R(F)R(G), so the *statement* would be false. That is correct, but the example list mixes F-side and G-side failures. | Optional. |
| 8 | §0 / §4.1 novelty wording "Gałązka proved only bounds" | minor | True for the general monomial. Before this report, the rank was already determined exactly when a = b, c = d, or (a,c) = (b+1,d+1) (Gałązka), and for (3,1,3,1) (the 2021 note). §4.1 lists the first cases, but §0 does not. | Harmonise. |

No issue affects correctness. Issues 1–3 must be fixed before any novelty claim.

## 4. Tests run by the referee

All code is independent of the agent's scripts. The exact tests use sympy over Q (the tr29 venv, run with
PYTHONDONTWRITEBYTECODE). The exhaustive tests use a C program (`tests/spansearch.c`, generator `tests/gen.py`). At most
2 CPUs were used.

**What the finite-field tests mean.** By Remark (i) the whole argument works over any field of characteristic
> max(A,B): Lemma 4, the Lemma 2 constants and the peeling. So an F_P-support of size below the bound, with P > A, B,
would refute the argument itself, not just a sanity check. P = 5 was used only with A, B ≤ 4.

**How the search works.** It is a DFS over increasing index subsets of P¹×P¹(F_P) with incremental elimination mod P.
Linearly dependent extensions are pruned. This is lossless: if T lies in the span of an n-subset, it lies in the span
of an independent sub-subset, and every prefix of that sub-subset is independent. The search reports every
independent subset of size ≤ n whose span first contains T at its last element.

| Id | What | Result |
|---|---|---|
| E1/E2 `exact_checks.py` | Over Q, all 1 ≤ p,q ≤ 5: Ann(T)_(i,k) in **every** bidegree i ≤ 1, k ≤ q+1 and k ≤ 1, i ≤ p+1. Dimension and divisibility by β1² (α1²), plus sharpness at k = q+1 (i = p+1). rank Cat_(1,q) = rank Cat_(p,1) = 4, and the image monomials | OK: Lemma 2 holds exactly in its range and fails exactly at k = q+1 |
| E3 `exact_checks_e35.py` | Lemma 4 with zero weights: F = x³u³ plus m generic zero-weight points, split (1,1)/(2,2) | Violated for m = 1…5 (n = 1+m < RHS), so the hypothesis w_j ≠ 0 is necessary. The report's use (minimal decomposition) is fine |
| E4 `exact_checks.py` | Lemma 4 on 758 (random integer decomposition of a random F, bidegree) pairs, A, B ≤ 4, n ≤ 9 | 0 violations |
| E5 `exact_checks_e35.py` | Theorem B ingredients (b) and rank Cat = rr′ over Q for (x⁴y+y⁵)⊗u²v, (x⁴+x²y²+y⁴)⊗u²v, x³y²⊗u²v, (x³y+2xy³+3y⁴)⊗(u⁴v+v⁵), x²y²⊗(u⁴v+3v⁵) | All OK. Bounds 11 (vs R(F)R(G) = 12), 9, 11 (= formula, vs 12), 12, 12 |
| G1 `galazka_upper_fp.py` | Gałązka Thm 1.5(i) construction Z = V(u^{k1+1}−v^{l1+1}, u^{k0+1}v^{l0−l1}−1) over F_P (P ≡ 1 mod M) for (k0,k1,l0,l1) = (2,1,2,1), (3,1,2,1), (3,2,2,1), (2,1,3,1), (4,1,3,2), (3,2,4,1), (5,2,3,1), (4,3,4,2), (3,1,3,1), (4,2,3,1): \|Z\| = M, F ∈ span ν(Z), h_Z at the Theorem B split | ALL OK. \|Z\| = M = formula, F in span, both h_Z maximal, so Lemma 4 is attained with equality |
| S1 `span_quick.log` | W2⊗W2 over F_7, F_11, F_13, n = 3. Control over F_7, n = 4 | 0 / 0 / 0. Control: 45 supports |
| S2 | W2⊗W3 = xy⊗u²v over F_7 (n = 5) and F_11 (n = 5; 4.98e8 nodes); W3⊗W2 over F_7 (n = 5) | 0 supports in each (R ≥ 6) |
| S3 | W3⊗W3 = x²y⊗u²v over F_7, n = 7 (7.03e8 nodes) | 0 supports (R ≥ 8) |
| S4 | **W3⊗W4 = x²y⊗u³v** over F_5, n = 9 (1.34e8 nodes) | 0 supports (R ≥ 10) |
| S5 | **W4⊗W4 = x³y⊗u³v** over F_5, n = 11 (9.88e8 nodes) | 0 supports (R ≥ 12) |
| S6 | x²y⊗u²v² over F_5, n = 8 (formula 9) | 0 supports |
| S7 | x²y²⊗uv over F_7, n = 5 (formula 6) | 0 supports |
| S8 | Non-monomial Prop C / Theorem B: (x⁴+xy³+y⁴)⊗u²v over F_5 (r = s = 3 mod 5, bound 9), n = 8 and n = 9 | n = 8: 0 supports. n = 9: **8 supports**, so the bound is attained and doubles as a positive control |
| S9 | Non-monomial: (x³y+2x²y²+3y⁴)⊗u³v over F_5 (r = s = 3, bound 12), n = 11 (9.88e8 nodes) | 0 supports |
| C1 | Negative control, hypotheses fail: (x⁴+y⁴)⊗u²v over F_5, n = 6 (the formula would say 10) | 4 supports of size 6, so the formula is false without (H) |
| C2 | Planted controls: a random 5-point combination (dim 15, F_7) and a random 8-point combination (dim 25, F_5) | Found in both, the planted support included |

**Not done.**
- An exhaustive test of a non-W monomial with b ≥ 2 and a > b, c > d (for example x³y²⊗u²v, formula 11). It needs
  P ≥ 7 (A = 5), and C(64,10) ≈ 1.5·10¹¹ subsets is too many.
- The x³y⊗u²v² run (a known case) was stopped for budget reasons.
- These cases are covered only by the hand proof and by E5/G1.
- No numerical search over C: border-rank artefacts make it uninformative, see `tr29review/REVIEW.md` T7.

## 5. Literature (search by a sub-agent on 2026-09-13; key texts re-read by me)

Full notes are in `lit/LIT_NOTES.txt`. Downloaded texts are in `lit/`.

1. **M. Gałązka, *Multigraded apolarity*, arXiv:1601.06211 (v2 2018, v3 2020); Math. Nachr. 296 (2023) 286–313.**
   - Thm 1.5 (= Thm 1.8 in the published version) gives three bounds:
     - (i) the upper bound, which equals the F2 formula;
     - (ii) r ≥ (k0+1)(l1+1);
     - (iii) r ≥ (k1+2)(l1+2)−1.
   - He says the rank is determined only when l0 = l1 (or k0 = k1), or when (k0,l0) = (k1+1,l1+1).
   - v1 has no P¹×P¹ theorem. The published text is paywalled and was not compared.
   - **No general formula.**
2. **M. Gałązka, *On the bihomogeneous rank of x^3yu^3v*, unrefereed 2-page note**
   (https://www.mimuw.edu.pl/~mgalazka/example.pdf, linked from his homepage; PDF CreationDate 2021-05-24).
   - It proves "multihomogeneous rank of F = x³yu³v is 12" over C, with apolarity, radical-ideal peeling and Thm 1.5(iii).
   - This is **F1 at (4,4) and F2 at (3,1,3,1)**. I read the note: the statement is exactly this.
   - The note is not on arXiv and nothing found cites it.
3. **M. Gałązka, PhD thesis, Univ. Warsaw, 2023.**
   - Remark 1.8: the monomial case "remains open".
   - Remark 1.10: "The author expects to be able to prove that the bihomogeneous rank of x^k y z^m w over the reals is
     2(k+m)." That is F1 over R, as an expectation.
4. **E. Ballico, A. Bernardi, M. Christandl, F. Gesmundo, arXiv:1803.01623, Rend. Lincei 30 (2019).**
   - Prop 4.2: R(W3⊗W3) = 8. Prop 4.4: R(W2⊗Wd) = 2d, by the reducedness/peeling argument.
   - §7.2: flattenings.
   - Semantic Scholar lists 32 citing works (OpenAlex 19). None has a new exact value.
5. **E. Ballico, A. Bernardi, F. Gesmundo, E. Ventura, arXiv:1909.03811.** Prop 4.3 has the same lower bound as
   Gałązka (ii). Four citing works; none relevant.
6. **S. Canino, A. Casarotti, P. Santarsiero, arXiv:2512.05828; Proc. AMS, doi:10.1090/proc/17856 (online 2026-07-30,
   per OpenAlex).**
   - Only the upper bound (Thm 1.1). For k = 2 it "coincides with [Gal23, Thm 1.8(i)]".
   - Called "sharp" only because (3,3) gives 8.
   - Zero citing works so far.
7. **A. Oneto, E. Ventura, *Ranks of tensors: geometry and applications*, Boll. UMI 18 (2025).** Question 12 lists the
   W-product rank as open.
8. **K. Wang, A. Seigal, *Lower bounds on the rank and symmetric rank of real tensors*, arXiv:2202.11740v2,
   J. Symbolic Comput. (2023).**
   - Thm 1.8 / 3.13: srk T ≥ sdrk_j T + sdrk_{d−j} T − rk T^(j).
   - The proof writes T^(j) = UΛS with evaluation matrices and applies Sylvester's rank inequality.
   - I re-read l.565–612: this is the report's Lemma 4 (with h_Z = rk U), in the symmetric setting.
   - The Segre–Veronese version is a straightforward transcription.
9. **Checked, no F1/F2 content.**
   - Monomials, cactus rank and apolarity: Landsberg–Teitler 0901.0487 (Thm 1.3, a different shape);
     Carlini–Catalisano–Geramita 1110.0745 (Waring rank of monomials; Thm 3.1, a different shape); 1907.03487 (border
     rank of monomials); 1707.06389 (cactus rank); Mourrain–Oneto 1805.11940.
   - Citing works of Gałązka, BBCG or BBGV: 2607.04712 (Lotter–Preiss 2026); 2410.20390 (Colarte-Gómez–Galuppi 2024,
     a different "psrk"); 2606.24349 (Li–Liu 2026); 2411.05721; 2310.19625; 2307.02560; 2302.03715; 2601.19558;
     2512.05195; 2512.05215; 2012.00574; 2002.05367; 2002.09720; 1507.06083; 1701.06845; 1601.00694.
   - Re-checked from the earlier pass: 2305.08162, 2407.18138, 2501.16849, 1810.07679, Shitov PJM 334 (2025).
   - The arXiv API was rate-limited, so keyword searches went through web search. The Math. Nachr. and Proc. AMS full
     texts were not accessible.

**Novelty conclusion.**
- **F1 (all d1, d2): new as a theorem.** Previously known:
  - d2 = 2 or d1 = 2 (BBCG 4.4; Gałązka (ii)+(2));
  - (3,3) (BBCG 4.2; Gałązka (i)+(iii));
  - (3,d) for all d in `tr29/` (this project, earlier today);
  - (4,4), claimed in Gałązka's unrefereed 2021 note.
- **F2 (all a ≥ b ≥ 1, c ≥ d ≥ 1): new.** No source determines it. Previously exact: a = b, c = d,
  (a,c) = (b+1,d+1), and (3,1,3,1).
- **Method.** Lemma 4 is Wang–Seigal's Sylvester device transcribed to P¹×P¹. Lemma 3 / (c) is the BBCG / Gałązka
  peeling. The new ingredient is combining them at the unbalanced split, where both Hilbert functions are maximal.
- **Search limits.** Not exhaustive: paywalled published versions were not seen, and the arXiv full-text search was
  rate-limited. No preprint proving F1 or F2 turned up in searches of citations of all four anchor papers or in
  keyword searches.
