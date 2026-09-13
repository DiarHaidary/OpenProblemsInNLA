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
ok = True
# E1, E2
for p in range(1, 6):
    for q in range(1, 6):
        A, B = p + 1, q + 1; T = x**p * y * u**q * v
        for i in range(0, 2):
            for k in range(0, q + 2):
                basis, M = ann_space(T, A, B, i, k)
                expect = 2 * 0 if k < 2 else (i + 1) * (k - 1)   # dim beta1^2 S_(i,k-2)
                divis = all(sp.rem(sp.Poly(g, b1), sp.Poly(b1**2, b1)).is_zero for g in basis)
                if k <= q:
                    if len(basis) != expect or not divis:
                        ok = False; print('E1 FAIL', p, q, i, k, len(basis), expect)
                else:  # k = q+1: beta0^{q+1} type elements appear -> not all divisible by beta1^2
                    if divis: ok = False; print('E1 sharpness not seen', p, q, i, k)
        for k in range(0, 2):
            for i in range(0, p + 2):
                basis, M = ann_space(T, A, B, i, k)
                expect = 0 if i < 2 else (i - 1) * (k + 1)
                divis = all(sp.rem(sp.Poly(g, a1), sp.Poly(a1**2, a1)).is_zero for g in basis)
                if i <= p and (len(basis) != expect or not divis):
                    ok = False; print('E1b FAIL', p, q, i, k)
                if i == p + 1 and divis:
                    ok = False; print('E1b sharpness not seen', p, q)
        M1, _ = catmat(T, A, B, 1, q); M2, _ = catmat(T, A, B, p, 1)
        if M1.rank() != 4 or M2.rank() != 4:
            ok = False; print('E2 FAIL', p, q)
        img = set(sp.Poly(contract(g, T), x, y, u, v).monoms()[0] for g in monos(1, q) if contract(g, T) != 0)
        # image monomials of Cat_(1,q): x^{p-1}y u, x^{p-1} y v, x^p u, x^p v  (exponents (x,y,u,v))
        want = {(p - 1, 1, 1, 0), (p - 1, 1, 0, 1), (p, 0, 1, 0), (p, 0, 0, 1)}
        if img != want: ok = False; print('E2 image FAIL', p, q, img)
print('E1/E2 Lemma 2 + Cat ranks + sharpness at k=q+1, p,q<=5:', 'OK' if ok else 'FAIL')
# E3: zero weights break Lemma 4
def evalvec(i, k, P):
    aa, bb, cc, ee = P
    return [aa**s * bb**(i - s) * cc**t * ee**(k - t) for s in range(i + 1) for t in range(k + 1)]
def hZ(Z, i, k):
    return sp.Matrix([evalvec(i, k, P) for P in Z]).rank()
p, q = 1, 1; A, B = 2, 2
# T = xy uv = (1/16) sum_{e1,e2=+-1} e1 e2 (x+e1 y)^2 (u+e2 v)^2
Z0 = [(1, e1, 1, e2) for e1 in (1, -1) for e2 in (1, -1)]
extra = [(1, 2, 1, 3), (1, 5, 1, 7), (1, -3, 1, 11), (2, 1, 3, 1), (1, 7, 2, 9)]
Z = Z0 + extra
lhs = len(Z); rhs = hZ(Z, 1, 1) + hZ(Z, 1, 1) - 4
print('E3 zero-weight example (xy⊗uv, 4 genuine + 5 zero-weight points): n =', lhs, ' h+h-rank =', rhs,
      '-> inequality', 'FAILS (so nonzero weights are needed)' if lhs < rhs else 'holds')
# check the 4-term identity
Tdec = sum(e1 * e2 * (x + e1 * y)**2 * (u + e2 * v)**2 for e1 in (1, -1) for e2 in (1, -1))
print('   4-term identity:', sp.expand(Tdec - 16 * x * y * u * v) == 0)
# E4: Lemma 4 on random decompositions of random F
rng = random.Random(7); bad = 0; cnt = 0
for trial in range(60):
    A = rng.randint(1, 4); B = rng.randint(1, 4); nn = rng.randint(1, 9)
    Z = [(rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)) for _ in range(nn)]
    Z = [P for P in Z if (P[0], P[1]) != (0, 0) and (P[2], P[3]) != (0, 0)]
    if not Z: continue
    W = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in Z]
    F = sp.expand(sum(w * (P[0] * x + P[1] * y)**A * (P[2] * u + P[3] * v)**B for w, P in zip(W, Z)))
    if F == 0: continue
    for i in range(A + 1):
        for k in range(B + 1):
            M, _ = catmat(F, A, B, i, k)
            r = M.rank()
            if len(Z) < hZ(Z, i, k) + hZ(Z, A - i, B - k) - r: bad += 1
            cnt += 1
print('E4 Lemma 4 on random decompositions: %d (decomposition, bidegree) cases, %d violations' % (cnt, bad))
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
cases = [(x**4 * y + y**5, 5, u**2 * v, 2), (x**4 + x**2 * y**2 + y**4, 4, u**2 * v, 2),
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
