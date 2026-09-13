"""Generate input for spansearch: all points of P1xP1(F_P), vectors nu(P) in the monomial basis
x^i y^(A-i) u^k v^(B-k), target F (x) G.  Usage:
  gen.py P A B n F G [planted]
F, G: comma-separated coefficient lists f_0..f_A (coef of x^i y^(A-i)) and g_0..g_B (coef of u^k v^(B-k)).
planted=m: replace target by a random combination of m random points with nonzero weights (control)."""
import sys, random
from math import comb
P, A, B, n = map(int, sys.argv[1:5])
f = [int(t) for t in sys.argv[5].split(',')]; g = [int(t) for t in sys.argv[6].split(',')]
assert len(f) == A + 1 and len(g) == B + 1
planted = int(sys.argv[7]) if len(sys.argv) > 7 else 0
p1 = [(1, 0)] + [(t, 1) for t in range(P)]          # (a:b) ; ax+by
pts = [(a, b, c, e) for (a, b) in p1 for (c, e) in p1]
def nu(a, b, c, e):
    return [comb(A, i) * pow(a, i, P) * pow(b, A - i, P) * comb(B, k) * pow(c, k, P) * pow(e, B - k, P) % P
            for i in range(A + 1) for k in range(B + 1)]
V = [nu(*pt) for pt in pts]
T = [f[i] * g[k] % P for i in range(A + 1) for k in range(B + 1)]
if planted:
    rng = random.Random(12345 + planted)
    idx = rng.sample(range(len(pts)), planted)
    T = [0] * len(T)
    for j in idx:
        w = rng.randrange(1, P)
        T = [(t + w * v) % P for t, v in zip(T, V[j])]
    print("planted indices", sorted(idx), file=sys.stderr)
dim = (A + 1) * (B + 1)
print(P, dim, len(pts), n)
for v in V:
    print(*v)
print(*T)
