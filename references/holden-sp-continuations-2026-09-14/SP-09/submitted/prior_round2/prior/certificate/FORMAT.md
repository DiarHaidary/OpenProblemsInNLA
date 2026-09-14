# Exact certificate format

All coefficients belong to Q(s), with s^2 = -3 and conjugate(s) = -s. The intended embedding is s = i sqrt(3). Integer pairs `(a,b)` represent a + b s.

The free projection letters, in order, are P1, P2, Q1, Q2. Each pair P1,P2 and Q1,Q2 consists of orthogonal self-adjoint projections. Reduced words alternate between the P and Q families. Words are ordered first by length and then lexicographically, including the empty word first.

The degree-four word list B has 61 members. The degree-three list L has 29. Let tau be a normalized trace with tau(Pi)=tau(Qi)=1/3. Put

    D = [-2 + 4s + (14-2s)(P1+Q1) + (5+3s)(P2+Q2)]/13,
    h1 = 27/13 - D*D,
    h2 = 27/13 - DD*.

The three local moment matrices are M0[u,v]=tau(u* v), M1[u,v]=tau(u* h1 v), and M2[u,v]=tau(u* h2 v), on B,L,L respectively.

The file contains a positive integer N in `coordinate_denominator`. Each block stores an integer matrix K and an integer Hermitian matrix Z, both represented by `real` and `s` parts. Their sizes are K0:61x52, K1:29x26, K2:29x26, and Z0:52x52, Z1,Z2:26x26.

The coefficient vector q_num has 29 entries. Only its first five are nonzero:

    (-114-18s, 372+120s, 381-93s, 372+120s, 381-93s).

Set c=q_num/388 and q=sum c_w w. Its normalized trace is exactly one. The Gram coefficient matrices are

    Y0 = K0 Z0 K0* / (388^2 N),
    Y1 = [K1 Z1 K1* + N q_num q_num*] / (388^2 N),
    Y2 = K2 Z2 K2* / (388^2 N).

The exact identity is

    Tr(Y0 M0) + Tr(Y1 M1) + Tr(Y2 M2) = 0.

The first verifier checks every cyclic-word coefficient of this identity, after imposing only the projection relations, trace cyclicity, tau(1)=1, and the four trace constraints. It does not impose finite-dimensional polynomial identities or rank-one conditions.

Each block also stores an integer matrix S as a positivity witness. Exact congruence computes G=S* Z S. Every row satisfies

    G_ii > sum_{j != i} (|Re_s G_ij| + 2 |Im_s G_ij|).

Here Re_s and Im_s are the two integer coefficients in Q(s). Since |a+b s| <= |a|+2|b|, this proves G positive definite. Therefore S is invertible and Z is positive definite. The optional `preconditioner_scale` and recorded margins describe construction/check output; the verifier recomputes positivity and does not trust those margins.

If ||D||^2 < 27/13, both localizers h1,h2 dominate a positive scalar epsilon. All three trace terms are nonnegative, while the distinguished rank-one term is at least epsilon*tau(q*q) >= epsilon*|tau(q)|^2 = epsilon. This contradicts the exact zero identity.

For equality rigidity, the second verifier establishes that the 52 columns of K0 span exactly the degree-four relation kernel of the displayed three-dimensional model. Positive definiteness of Z0 then forces these relations in any equality case. The first nine words have degree at most two and form a basis of M3; all their products have degree at most four. Consequently the equality representation is a unital *-representation of M3.
