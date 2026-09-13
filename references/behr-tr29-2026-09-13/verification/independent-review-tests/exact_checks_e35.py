"""Independent exact (sympy, over Q) checks of the ingredients of the TR-29 k=2 proof and of Theorem B.
E1  Lemma 2: dim Ann(T)_(i,k) and equality with beta1^2*S (resp alpha1^2*S) in ALL bidegrees i<=1,k<=q
    and k<=1,i<=p; failure exactly at k = q+1 (shows the range restriction is sharp).
E2  rank Cat_(1,q)(T) = rank Cat_(p,1)(T) = 4, and image = <x^{p-1}y, x^p> (x) <u,v>.
E3  Lemma 4 needs nonzero weights: explicit example where adding zero-weight points breaks the inequality.
E4  Lemma 4 on random rational decompositions of random F (not T): Gram = V1^T W V2 identity and inequality.
E5  Theorem B ingredients (a),(b) for non-monomial forms; Hilbert function of CI at r-1, s'-1."""
import itertools, random
from math import comb, factorial
import sympy as sp
a0, a1, b0, b1, x, y, u, v = sp.symbols('a0 a1 b0 b1 x y u v')
def contract(g, F):
    g = sp.Poly(sp.expand(g), a0, a1, b0, b1); out = 0
    for (e0, e1, f0, f1), c in g.terms():
        out += c * sp.diff(F, x, e0, y, e1, u, f0, v, f1)
    return sp.expand(out)
def monos(i, k):
    return [a0**s * a1**(i - s) * b0**t * b1**(k - t) for s in range(i + 1) for t in range(k + 1)]
def rmonos(i, k):
    return [x**s * y**(i - s) * u**t * v**(k - t) for s in range(i + 1) for t in range(k + 1)]
def catmat(F, A, B, i, k):
    cols = monos(i, k); rows = rmonos(A - i, B - k)
    M = sp.zeros(len(rows), len(cols))
    for c, g in enumerate(cols):
        h = sp.Poly(contract(g, F), x, y, u, v) if contract(g, F) != 0 else None
        if h is None: continue
        for r, m in enumerate(rows):
            M[r, c] = h.coeff_monomial(m)
    return M, cols
def ann_space(F, A, B, i, k):
    M, cols = catmat(F, A, B, i, k)
    return [sum(vec[j] * cols[j] for j in range(len(cols))) for vec in M.nullspace()], M
# E3: zero weights break Lemma 4
def evalvec(i, k, P):
    aa, bb, cc, ee = P
    return [aa**s * bb**(i - s) * cc**t * ee**(k - t) for s in range(i + 1) for t in range(k + 1)]
def hZ(Z, i, k):
    return sp.Matrix([evalvec(i, k, P) for P in Z]).rank()
# F = x^3 u^3 (one point), split (1,1)/(2,2); add m generic points with weight 0
A, B = 3, 3
Zg = [(1, 0, 1, 0)]
extra = [(1, 2, 1, 3), (1, 5, 1, 7), (1, -3, 1, 11), (2, 1, 3, 1), (1, 7, 2, 9)]
F0 = x**3 * u**3
M, _ = catmat(F0, A, B, 1, 1); rkc = M.rank()
for m in range(0, 6):
    Z = Zg + extra[:m]
    lhs = len(Z); rhs = hZ(Z, 1, 1) + hZ(Z, 2, 2) - rkc
    print('E3 F=x^3u^3 with %d zero-weight extra points: n=%d, h(1,1)+h(2,2)-rank Cat=%d -> %s'
          % (m, lhs, rhs, 'VIOLATED (nonzero weights needed)' if lhs < rhs else 'holds'))
# E5 Theorem B ingredients for non-monomial F, G
def binary_ann_degrees(Fb, var0, var1, d0, d1, deg):
    # returns (r, basis of Ann in degree r) for a binary form in variables var0,var1 with derivations d0,d1
    for j in range(0, deg + 2):
        cols = [d0**s * d1**(j - s) for s in range(j + 1)]
        rows = [var0**s * var1**(deg - j - s) for s in range(deg - j + 1)] if j <= deg else []
        if j > deg: return j, cols
        M = sp.zeros(max(len(rows), 1), len(cols))
        for c, g in enumerate(cols):
            e = sp.Poly(g, d0, d1).monoms()[0]
            h = sp.expand(sp.diff(Fb, var0, e[0], var1, e[1]))
            if h == 0: continue
            hp = sp.Poly(h, var0, var1)
            for rr, m in enumerate(rows): M[rr, c] = hp.coeff_monomial(m)
        ns = M.nullspace()
        if ns: return j, [sum(vv[t] * cols[t] for t in range(len(cols))) for vv in ns]
cases = [(x**4 * y + y**5, 5, u**2 * v, 3), (x**4 + x**2 * y**2 + y**4, 4, u**2 * v, 3), (x**3 * y**2, 5, u**2 * v, 3),
         (x**3 * y + 2 * x * y**3 + 3 * y**4, 4, u**4 * v + v**5, 5), (x**2 * y**2, 4, u**4 * v + 3 * v**5, 5)]
for Fb, A, Gb, B in cases:
    r, phiF = binary_ann_degrees(Fb, x, y, a0, a1, A); s = A + 2 - r
    rp, phiG = binary_ann_degrees(Gb, u, v, b0, b1, B); sp_ = B + 2 - rp
    T = sp.expand(Fb * Gb)
    M, _ = catmat(T, A, B, r - 1, sp_ - 1); rk = M.rank()
    basis, _ = ann_space(T, A, B, r - 1, sp_ - 1)
    # (b): Ann_(r-1,k) for k<=s'-1 should be phi' * S_(r-1,k-r') : dim r*(k-r'+1)
    bok = all(len(ann_space(T, A, B, r - 1, k)[0]) == (r * (k - rp + 1) if k >= rp and rp < sp_ else 0)
              for k in range(0, sp_))
    fac = [sp.factor_list(sp.Poly(ph, a0, a1).as_expr()) for ph in phiF]
    print('E5 F=%s (r=%d,s=%d, phi=%s) G=%s (r\'=%d,s\'=%d, phi\'=%s): rank Cat_(r-1,s\'-1)=%d (r r\'=%d), (b) %s, bound rs\'+sr\'-rr\'=%d, R(F)R(G)=%d'
          % (Fb, r, s, [sp.factor(t) for t in phiF] if len(phiF) == 1 else 'pencil', Gb, rp, sp_,
             [sp.factor(t) for t in phiG] if len(phiG) == 1 else 'pencil', rk, r * rp, bok,
             r * sp_ + s * rp - r * rp, s * sp_))
