import sys
from math import comb
def rank_mod(M, P):
    M = [r[:] for r in M]; rk = 0; C = len(M[0]) if M else 0
    for c in range(C):
        pv = next((j for j in range(rk, len(M)) if M[j][c] % P), None)
        if pv is None: continue
        M[rk], M[pv] = M[pv], M[rk]; iv = pow(M[rk][c], P - 2, P)
        M[rk] = [t * iv % P for t in M[rk]]
        for j in range(len(M)):
            if j != rk and M[j][c] % P:
                f = M[j][c]; M[j] = [(s - f * t) % P for s, t in zip(M[j], M[rk])]
        rk += 1
    return rk
P = int(sys.argv[1]); f = [int(t) for t in sys.argv[2].split(',')]; A = len(f) - 1
# Cat_j: alpha0^s alpha1^(j-s) applied to x^i y^(A-i) -> ff(i,s) ff(A-i,j-s) x^(i-s) y^(A-i-(j-s))
def ff(n, r):
    o = 1
    for t in range(r): o *= (n - t)
    return o if r <= n else 0
for j in range(A + 2):
    rows = A - j + 1
    if rows <= 0: print('r =', j); break
    M = [[0] * (j + 1) for _ in range(rows)]
    for s in range(j + 1):
        for i in range(A + 1):
            if f[i] and s <= i and j - s <= A - i:
                M[i - s][s] = (M[i - s][s] + f[i] * ff(i, s) * ff(A - i, j - s)) % P
    if rank_mod(M, P) < j + 1:
        print('P=%d f=%s: r = %d, s = %d, dim Ann_r = %d' % (P, f, j, A + 2 - j, j + 1 - rank_mod(M, P))); break
