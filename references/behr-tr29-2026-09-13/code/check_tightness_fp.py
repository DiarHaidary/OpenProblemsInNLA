"""K4 (exact over F_P, illustrative): the explicit 2(p+q)-point decomposition
   sum_{eps=+-1} sum_{a^(p+q) = eps^(q-1)} eps (a x + y)^(p+1) (eps a u + v)^(q+1) = C x^p y u^q v
realised over F_P with 2(p+q) | P-1 and P > p+q+2; checks C != 0, distinct points, and that every inequality
in the lower-bound proof is an equality there: h_Z(1,q) = 2q+2, h_Z(p,1) = 2p+2, rank of the Gram matrix
V1^T W V2 = 4, n = h + h - 4. (The upper bound itself is proved in ../tr29gen/REPORT.md §2, check U1.)
"""
from math import comb
from common import rank_mod

def is_prime(m):
    return m > 1 and all(m % d for d in range(2, int(m**0.5) + 1))

ok = True
for p, q in [(1, 1), (1, 4), (2, 2), (3, 3), (4, 4), (4, 5), (5, 5), (2, 7), (6, 6), (7, 4)]:
    A, B, N = p + 1, q + 1, 2 * (p + q)
    P = next(m for m in range(N + 1, 10**6, N) if is_prime(m) and m > p + q + 2)
    pts, w = [], []
    for eps in (1, P - 1):
        rhs = pow(eps, q - 1, P)
        for a in range(1, P):
            if pow(a, p + q, P) == rhs:
                pts.append((a, 1, eps * a % P, 1)); w.append(eps)
    n = len(pts)
    coef = {}
    for (a, b, c, e), wt in zip(pts, w):
        for m in range(A + 1):
            for k in range(B + 1):
                coef[(m, k)] = (coef.get((m, k), 0) + wt * comb(A, m) * pow(a, m, P) * comb(B, k) * pow(c, k, P)) % P
    Cc = coef[(p, q)]
    only = all(v == 0 for key, v in coef.items() if key != (p, q))
    # C * x^p y u^q v has coefficient vector entry comb(A,p) comb(B,q) * C0 at (p,q); we only need C != 0
    distinct = len(set(pts)) == n
    def ev(i, k, pt):
        a, b, c, e = pt
        return [pow(a, s, P) * pow(b, i - s, P) * pow(c, t, P) * pow(e, k - t, P) % P for s in range(i + 1) for t in range(k + 1)]
    V1 = [ev(1, q, pt) for pt in pts]; V2 = [ev(p, 1, pt) for pt in pts]
    h1, h2 = rank_mod(V1, P), rank_mod(V2, P)
    G = [[sum(V1[j][r] * w[j] * V2[j][c] for j in range(n)) % P for c in range(len(V2[0]))] for r in range(len(V1[0]))]
    rG = rank_mod(G, P)
    good = (n == N and Cc != 0 and only and distinct and h1 == 2 * q + 2 and h2 == 2 * p + 2 and rG == 4 and n == h1 + h2 - 4)
    ok &= good
    print(f"(p,q)=({p},{q}) P={P}: n={n} C={Cc} only-target={only} distinct={distinct} h(1,q)={h1} h(p,1)={h2} rank Gram={rG} equality={n == h1 + h2 - rG} -> {'OK' if good else 'FAIL'}")
print("ALL OK" if ok else "SOME FAILURE")
