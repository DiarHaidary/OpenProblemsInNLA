"""K2 (exhaustive, exact over F_P): finite-field test of Lemma 3.
For every nonzero form g of bidegree (1,q) over F_P (up to scalar) let Z_g = set of F_P-rational points of
P^1 x P^1 on V(g). Lemma 3 (whose proof is valid over any field of characteristic > max(p,q)+1) says that
T = x^p y u^q v is NOT in the span of nu(Z_g) (nu = (p+1,q+1) Segre-Veronese). Same for bidegree (p,1).
Since every Z contained in V(g) has span(nu(Z)) inside span(nu(Z_g)), this is exactly Lemma 3 over F_P
for F_P-rational point sets.
Controls: (i) the full grid P^1 x P^1(F_P) must support T when it spans; (ii) for P = 1 mod 2(p+q) the
(2,2)-curve (a0 b1 - a1 b0)(a0 b1 + a1 b0) containing the explicit 2(p+q)-point decomposition must support T.
usage: fp_curves_exhaustive.py P p q [both|1q]
"""
import sys, itertools
import numpy as np
from math import comb
P, p, q = map(int, sys.argv[1:4]); mode = sys.argv[4] if len(sys.argv) > 4 else 'both'
assert P > max(p, q) + 1
A, B = p + 1, q + 1
pts = [(a, 1) for a in range(P)] + [(1, 0)]
grid = [(l, m) for l in pts for m in pts]

def nu(l, m):
    a, b = l; c, e = m
    L = [comb(A, i) * pow(a, i, P) * pow(b, A - i, P) for i in range(A + 1)]
    M = [comb(B, k) * pow(c, k, P) * pow(e, B - k, P) for k in range(B + 1)]
    return (np.outer(L, M) % P).ravel()
NU = np.array([nu(l, m) for l, m in grid], dtype=np.int64)          # (#grid, (A+1)(B+1))
target = np.zeros((A + 1) * (B + 1), dtype=np.int64); target[p * (B + 1) + q] = 1

def rank_mod(M):
    M = M.copy() % P; R, C = M.shape; r = 0
    for c in range(C):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        j = r + nz[0]; M[[r, j]] = M[[j, r]]
        M[r] = (M[r] * pow(int(M[r, c]), P - 2, P)) % P
        f = M[:, c].copy(); f[r] = 0
        M = (M - np.outer(f, M[r])) % P
        r += 1
        if r == R:
            break
    return r

def supports(mask):
    V = NU[mask]
    if V.shape[0] == 0:
        return False
    r0 = rank_mod(V.T)
    r1 = rank_mod(np.column_stack([V.T, target]))
    return r0 == r1

def monos(i, k):
    return [(s, t) for s in range(i + 1) for t in range(k + 1)]

def test_bidegree(i, k):
    mon = monos(i, k)
    # evaluation matrix E[point, monomial] = a^s b^(i-s) c^t e^(k-t)
    E = np.array([[pow(l[0], s, P) * pow(l[1], i - s, P) * pow(m[0], t, P) * pow(m[1], k - t, P) % P
                   for (s, t) in mon] for l, m in grid], dtype=np.int64)
    seen = {}; nforms = 0; bad = 0
    D = len(mon)
    # enumerate forms up to scalar: first nonzero coefficient = 1
    for lead in range(D):
        for rest in itertools.product(range(P), repeat=D - lead - 1):
            g = np.zeros(D, dtype=np.int64); g[lead] = 1; g[lead + 1:] = rest
            vals = (E @ g) % P
            key = np.packbits(vals == 0).tobytes()
            nforms += 1
            if key not in seen:
                seen[key] = supports(vals == 0)
            if seen[key]:
                bad += 1
    return nforms, len(seen), bad

print(f"P={P} p={p} q={q}: grid size {len(grid)}")
full = supports(np.ones(len(grid), dtype=bool))
print("control (i): full grid supports T:", full, "(grid spans:", rank_mod(NU.T) == (A + 1) * (B + 1), ")")
if (P - 1) % (2 * (p + q)) == 0:
    D = [(l, m) for l, m in grid if (l[0] * m[1] - l[1] * m[0]) * (l[0] * m[1] + l[1] * m[0]) % P == 0]
    mask = np.array([(g in D) for g in grid])
    print("control (ii): (2,2)-curve through the explicit decomposition supports T:", supports(mask),
          f"({mask.sum()} points)")
res = test_bidegree(1, q)
print(f"bidegree (1,{q}): {res[0]} forms, {res[1]} distinct zero sets, forms whose zero set supports T: {res[2]}")
ok = res[2] == 0
if mode == 'both':
    res = test_bidegree(p, 1)
    print(f"bidegree ({p},1): {res[0]} forms, {res[1]} distinct zero sets, forms whose zero set supports T: {res[2]}")
    ok &= res[2] == 0
print("Lemma 3 over F_P:", "CONFIRMED (no curve supports T)" if ok else "VIOLATED")
