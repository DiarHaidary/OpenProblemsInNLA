"""K1 (exact over Q). Checks, for 1 <= p, q <= 7:
 (a) Lemma 2: for i in {0,1}, 0 <= k <= q: Ann(T)_(i,k) = beta1^2 * S_(i,k-2)  (dimension equality + containment),
     and symmetrically for k in {0,1}, 0 <= i <= p: Ann(T)_(i,k) = alpha1^2 * S_(i-2,k).
     Also the general fact used in the discussion: Ann(T)_(i,k) = (alpha1^2, beta1^2)_(i,k) for all i <= p, k <= q.
 (b) rank Cat_(1,q)(T) = 4 and rank Cat_(p,1)(T) = 4.
 (c) Lemma 4 identity: Gram matrix of (g,h) -> (gh)∘T equals A!B! V1^T W V2 for random integer decompositions
     (F = sum w_j nu(P_j) expanded exactly), and the Sylvester inequality n >= h(i,k)+h(A-i,B-k)-rank Cat
     for all (i,k), on random integer point sets (sizes 2..2(p+q)+2).
"""
import random, itertools, sys
from math import comb, factorial
from common import *

random.seed(20260913)
ok_all = True
PQ = [(p, q) for p in range(1, 8) for q in range(1, 8)]
for p, q in PQ:
    A, B = p + 1, q + 1
    T = T_dict(p, q)
    for i in range(0, A + 1):
        for k in range(0, B + 1):
            M, cols, rows = cat_matrix(T, A, B, i, k)
            r = rank_Q(M)
            dimS = (i + 1) * (k + 1)
            dimAnn = dimS - r
            # dimension of (alpha1^2, beta1^2) in bidegree (i,k): complement spanned by monomials with
            # alpha1-degree <= 1 and beta1-degree <= 1
            h = min(i + 1, 2) * min(k + 1, 2)
            if i <= p and k <= q:
                if r != h:
                    print("FAIL Ann=(a1^2,b1^2) dim", p, q, i, k, r, h); ok_all = False
                # containment: monomials with alpha1-deg>=2 or beta1-deg>=2 annihilate
                for c, (s, t) in enumerate(cols):
                    if (i - s) >= 2 or (k - t) >= 2:
                        if any(M[row][c] for row in range(len(rows))):
                            print("FAIL containment", p, q, i, k, s, t); ok_all = False
            if i <= 1 and k <= q:
                if dimAnn != (i + 1) * max(k - 1, 0):
                    print("FAIL Lemma2 (i<=1)", p, q, i, k, dimAnn); ok_all = False
            if k <= 1 and i <= p:
                if dimAnn != (k + 1) * max(i - 1, 0):
                    print("FAIL Lemma2 (k<=1)", p, q, i, k, dimAnn); ok_all = False
    rc1 = rank_Q(cat_matrix(T, A, B, 1, q)[0]); rc2 = rank_Q(cat_matrix(T, A, B, p, 1)[0])
    if rc1 != 4 or rc2 != 4:
        print("FAIL rank Cat", p, q, rc1, rc2); ok_all = False
print("(a),(b) Lemma 2 and rank Cat_(1,q) = rank Cat_(p,1) = 4 for 1<=p,q<=7:", ok_all)

def expand(points, weights, A, B):
    F = {}
    for (a, b, c, e), w in zip(points, weights):
        for m in range(A + 1):
            for n in range(B + 1):
                F[(m, n)] = F.get((m, n), 0) + w * comb(A, m) * a**m * b**(A - m) * comb(B, n) * c**n * e**(B - n)
    return F

def evalmono(s, t, i, k, P):
    a, b, c, e = P
    return a**s * b**(i - s) * c**t * e**(k - t)

ok_c = True; nsyl = 0
for p, q in [(1, 1), (2, 1), (1, 3), (2, 2), (3, 2), (3, 3), (4, 4), (5, 3)]:
    A, B = p + 1, q + 1
    for trial in range(3):
        n = random.randint(2, 2 * (p + q) + 2)
        pts = [tuple(random.randint(-3, 3) for _ in range(4)) for _ in range(n)]
        pts = [P for P in pts if (P[0], P[1]) != (0, 0) and (P[2], P[3]) != (0, 0)]
        n = len(pts)
        w = [random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(n)]
        F = expand(pts, w, A, B)
        for i in range(A + 1):
            for k in range(B + 1):
                # Gram matrix of b(g,h) = (gh)∘F
                colsg = [(s, t) for s in range(i + 1) for t in range(k + 1)]
                colsh = [(s, t) for s in range(A - i + 1) for t in range(B - k + 1)]
                G = []
                for (s1, t1) in colsg:
                    row = []
                    for (s2, t2) in colsh:
                        # (gh)∘F with gh = alpha0^(s1+s2) alpha1^(A-s1-s2) beta0^(t1+t2) beta1^(B-t1-t2)
                        S0, T0 = s1 + s2, t1 + t2
                        val = 0
                        for (m, nn), f in F.items():
                            c2, _ = contract_mono(A, S0, B, T0, A, B, m, nn)
                            val += c2 * f
                        row.append(val)
                    G.append(row)
                V1 = [[evalmono(s, t, i, k, P) for (s, t) in colsg] for P in pts]
                V2 = [[evalmono(s, t, A - i, B - k, P) for (s, t) in colsh] for P in pts]
                G2 = [[factorial(A) * factorial(B) * sum(V1[j][r] * w[j] * V2[j][c] for j in range(n))
                       for c in range(len(colsh))] for r in range(len(colsg))]
                if G != G2:
                    print("FAIL Gram identity", p, q, i, k); ok_c = False
                # Sylvester inequality with distinct points (dedupe projectively is not needed for the inequality
                # as stated with rows = terms; we test it on the multiset rows, which is the same statement)
                rC = rank_Q(cat_matrix(F, A, B, i, k)[0])
                if rC != rank_Q(G):
                    print("FAIL rank b = rank Cat", p, q, i, k); ok_c = False
                h1, h2 = rank_Q(V1), rank_Q(V2)
                if not (n >= h1 + h2 - rank_Q(G)):
                    print("FAIL Sylvester", p, q, i, k); ok_c = False
                nsyl += 1
print("(c) Gram identity, rank b = rank Cat, Sylvester inequality on", nsyl, "random (decomposition, bidegree) pairs:", ok_c)
print("ALL OK" if ok_all and ok_c else "SOME FAILURE")
