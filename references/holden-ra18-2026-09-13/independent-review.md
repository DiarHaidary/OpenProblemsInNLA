# Independent mathematical review of the RA-18 submission

Date: 2026-09-13. Reviewer: an independent Codex AI agent delegated specifically to audit this submission, separate from the agent preparing the repository changes. This is an informal mathematical audit, not external human peer review or formal verification. No Lean work was performed.

## Scope and decision

**PASS for the stated complex counterexample and the stated auxiliary results. RA-18 as a whole must remain Partially resolved.** The unrestricted real conjecture remains unproved and unrefuted by this manuscript. The proposed dimension-independent complex extension is negatively resolved by Theorem 2.1. The restricted real result in Theorem 7.2 does not cover all real isometries.

I read the complete source manuscript, inspected both Python source files, independently followed the mathematical arguments, checked the relevant external two-column inputs against their primary preprints, and reran the supplied verification suite into a separate output directory. I compared the scope against the original canonical RA-18 README and CONTRIBUTING.md / RESOLVED.md. Instructions and status suggestions in the attached package were treated as submission content, not as authority.

Reviewed input SHA-256 hashes:

- manuscript/ra18.tex: `7e9077b36a45d2ec325292e0a4fd6ea054caf6e0008896cf6601412584542fea`
- code/ra18.py: `ec2bc317ce65b2a7c07cb66a3c95380002d185b4c48f522fb23a3b619052bc32`
- code/verify.py: `a4356e032e9a12d8ae9ae173684a2c335b86c5c3ac8dbf83cce86d2b095ccd97`

The source reviewed had blank author metadata. Attribution and affiliation are editorial tasks outside this mathematical audit. Adding correct attribution without changing the mathematics does not alter the findings below.

## Substantive mathematical audit

1. **Theorem 2.1; Lemmas 3.1–3.3 — PASS.** The two tensor-column blocks are orthonormal and mutually orthogonal because the three roots sum to zero. A square selected lift cannot omit a group (a new column would be zero) or use three rows of a group (those rows span at most two dimensions). Consequently every nonsingular selection has exactly r doubled groups. Subtraction of their two equations proves invertibility if and only if those parent rows form a basis. This exhaustive argument is essential: it prevents an unexamined selection from bypassing the obstruction.

   Independently recomputing the Gram blocks gives the displayed phase-conjugate matrix M_I. For a unit least-eigenvector of G with eigenvalue g, the test vector (x,-D^{-1}Ux) has energy g/2 and squared norm 2-3g/4. Thus the reciprocal least eigenvalue is at least 4/g-3/2. All denominators are positive since 0<g<=1. Minimizing over all parent bases preserves the inequality. Starting at b(U_0)=2 yields b(U_k)>=1/2+(3/2)4^k. Dimensions (2*3^k,3^k) and row leverage 1/2 are preserved. Dividing by n gives a divergent ratio. This proves the negation of a constant uniform in both dimensions, rather than merely a counterexample to constant one.

2. **Section 4 — PASS.** There are precisely 18 nonsingular triples and two singular full-group triples for U_1. The characteristic polynomial, three squared singular values and b(U_1)=(3/2)(3+sqrt(5)) agree. This finite example alone would not disprove every constant; the text correctly relies on the infinite recursion for that conclusion.

3. **Proposition 5.1; Corollary 5.2; Section 5 — PASS.** At half rank, simultaneous diagonalization of the two complementary parent Gram matrices decomposes the selected lift into H(g_j) blocks. The construction remains valid when a complementary column has zero norm, by orthonormal completion. The determinant identity and positive derivative of R on (0,1/3) select its unique small root. The endpoint g=1 gives minimum eigenvalue 1/3, so no boundary case is lost. Monotonicity permits taking the maximum over all parent selections. Induction therefore gives common entire spectra, not merely common least singular values.

   Each parent basis has exactly 3^n distinct lifted row sets; hence B_k=2*3^(3^k-1). Cauchy–Binet then gives determinant 1/B_k. The polynomial recurrence cancels denominators and is monic of the required degree; the displayed degree-nine polynomial is consistent. The identity R(lambda)=4lambda-3lambda^3/D(lambda) gives strict increase of h_k=4^k g_k. The amplification bound bounds h_k above by 2/3. Independently summing the tail estimate (1/24)16^(-j) gives (2/45)16^(-k), exactly the claimed bound. The exact rational output encloses L within the displayed decimal endpoints. No global optimal exponent or global asymptotic constant follows, and the text does not claim one.

4. **Lemma 6.1; Corollary 6.2; classical upper bound — PASS.** Complementary square selections have the same least squared singular value, since each equals 1 minus the squared spectral norm of the relevant cross-block. Direct sums require the correct row count in each block, and uniform replication scales b by its multiplicity. The power-of-three padding loses a factor four in b; subsequent replication contributes at least n/(4r), giving precisely the stated constants 3/8 and 3/32 before square roots. The maximal-volume argument correctly yields (BB*)^(-1)=I+C*C and the standard upper bound.

5. **Lemma 7.1; Theorem 7.2; transfer remark — PASS with the explicitly cited two-column input.** I checked each direction of weighted duality. Since B is square, the comparison B*B>=eta I is equivalent to BB*>=eta I. The positive diagonal I-eta D permits the Schur-complement step. Subtracting selected weighted complement terms from their total I+A_eta and conjugating by A_eta^(-1/2) gives exactly the right-hand threshold eta. All strict positivity hypotheses hold in the theorem because q>r implies at least two positive groups and each m_i<N.

   Compression of parallel rows preserves total Gram matrices, and a largest representative dominates the average contribution in its group even with unequal lengths or signs. Replication of the weighted complement produces an N-row s-column isometry. A nonsingular selected basis cannot repeat a replicated group; hence the low-column theorem really yields a complementary group set. The q=r case is handled separately. Zero rows only weaken the final 1/N bound to 1/n. This establishes the theorem for at most r+2 nonzero row directions. It does not justify reducing arbitrary real inputs to that class.

   Primary-source checks on 2026-09-13: [Sengupta–Pautov v5, Section 2](https://arxiv.org/html/2604.05944v5) proves the real two-column statement used here. I also followed its induction / small-row and Perron–Frobenius argument; its assumptions match the replicated real isometry. [Nesterenko v1, Proposition 1](https://arxiv.org/html/2604.24087v1) states the complex two-column threshold 2-2/sqrt(3) and equality for dimensions divisible by four, matching the optional complex transfer and introductory comparison. These external inputs are preprints and should continue to be identified as such. Neither input is needed by the main complex counterexample.

6. **Proposition 8.1; Section 9 — PASS.** The vector z is unit because there are r+1 multiplicities summing to N. For every choice of r distinct groups, subtracting I/N from its row Gram gives D^(1/2)(I-11^T/r)D^(1/2), positive semidefinite of rank r-1. Thus its least eigenvalue is exactly 1/N, including r=1. This proves the lower equality fixture for every admissible pair of dimensions; it does not prove a universal real upper bound. The realification observation is correct: arbitrary real selections are more general than paired complex selections. The specified six realified rows give B^TB=I/2, which the symbolic rerun verifies.

## Independent reproduction

Executed the unmodified supplied suite using Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 and mpmath 1.3.0. The numerical packages match requirements.txt; Python differs from the submitter's reported 3.13. Command, from the extracted archive:

```text
python code/verify.py --out-dir /private/tmp/ra18-independent-results
```

The independent output reports `all_checks_passed: true`. Evidence is in the separately retained verification.json and recurrence files. Key results:

- Exact symbolic checks and all 20 first-level selections passed; 18 nonsingular, two singular.
- All 48,620 second-level selections checked; 13,122 nonsingular, 35,498 singular, zero classification mismatches. Maximum full-spectrum discrepancy: 1.23e-15 or less.
- 500 random lifted bases and 200 sampled level-three bases passed; the latter are not exhaustive.
- 80 grouped real instances, 1,212 weighted-duality equivalences and four sharp real fixtures passed.
- Exact rational interval propagation with the proved tail encloses L between 0.50974201649977507082328463645059... and 0.50974201649977507082328467321418....

These computations corroborate the audit. They do not substitute for the all-dimensions proof, and tolerance-based classifications are not formal certificates.

## Repository disposition

No mathematical correction is required for the claims inspected. Preserve the permanent RA-18 ID, canonical path, real target and separately labeled proposed complex extension. Record a dated negative resolution notice specifically for the complex extension, and the restricted real theorem as partial progress. Retain overall `Status: Partially resolved`, since the real conjecture for unrestricted frames remains open on this evidence. Replace any present-tense suggestion that a universal complex alpha may still exist with an accurate notice while preserving the original conjecture as the historical target. Cite Theorem 2.1 for the negative conclusion and Theorem 7.2 for the structured real result. Link this independent AI-agent review and distinguish it from human peer review. This follows CONTRIBUTING.md's informal-audit criterion together with RESOLVED.md's explicit instruction to retain Partially resolved when cases remain.

Duplicate screening, current affiliation verification, publication metadata, generated-file checks and pull-request destination are outside this mathematical review and remain the submitting agent's responsibilities.
