"""Check Gałązka's Thm 1.5(i) upper-bound construction over F_P (independent of his proof):
Z = V(u^{k1+1} - v^{l1+1}, u^{k0+1} v^{l0-l1} - 1) in the torus, points ((u:1),(v:1)).
Check: |Z| = M, and F = x^{k0} y^{k1} X^{l0} Y^{l1} lies in span nu(Z) over F_P (P chosen so all points rational),
plus h_Z(k1,l0) = (k1+1)(l0+1), h_Z(k0,l1) = (k0+1)(l1+1), equality case of Lemma 4 at (k1,l0)/(k0,l1)."""
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
def isprime(m): return m > 1 and all(m % d for d in range(2, int(m**.5) + 1))
cases = [(2, 1, 2, 1), (3, 1, 2, 1), (3, 2, 2, 1), (2, 1, 3, 1), (4, 1, 3, 2), (3, 2, 4, 1), (5, 2, 3, 1), (4, 3, 4, 2), (3,1,3,1), (4,2,3,1)]
allok = True
for k0, k1, l0, l1 in cases:
    A, B = k0 + k1, l0 + l1
    M = (k0 + 1) * (l1 + 1) + (k1 + 1) * (l0 + 1) - (k1 + 1) * (l1 + 1)
    # the solution group is a subgroup of mu_M x mu_M  (exponent divides M); pick P = 1 mod M, P > A,B
    P = next(m for m in range(max(A, B, M) + 1, 10**6) if isprime(m) and (m - 1) % M == 0)
    Z = [(uu, vv) for uu in range(1, P) for vv in range(1, P)
         if (pow(uu, k1 + 1, P) - pow(vv, l1 + 1, P)) % P == 0 and (pow(uu, k0 + 1, P) * pow(vv, l0 - l1, P) - 1) % P == 0]
    nu = [[comb(A, i) * pow(uu, i, P) * comb(B, k) * pow(vv, k, P) % P for i in range(A + 1) for k in range(B + 1)] for uu, vv in Z]
    Tvec = [1 if (i, k) == (k0, l0) else 0 for i in range(A + 1) for k in range(B + 1)]
    rZ = rank_mod(nu, P); rZT = rank_mod(nu + [Tvec], P)
    def hZ(i, k):  # evaluation of monomials a0^s a1^(i-s) b0^t b1^(k-t) at (uu,1,vv,1)
        return rank_mod([[pow(uu, s, P) * pow(vv, t, P) % P for s in range(i + 1) for t in range(k + 1)] for uu, vv in Z], P)
    h1 = hZ(k1, l0); h2 = hZ(k0, l1)
    ok = (len(Z) == M and rZ == rZT)
    allok &= ok
    print(f"F=x^{k0}y^{k1}u^{l0}v^{l1} P={P}: |Z|={len(Z)} (M={M}), F in span nu(Z): {rZ == rZT}, dim span={rZ}; "
          f"h_Z({k1},{l0})={h1} (full {(k1+1)*(l0+1)}), h_Z({k0},{l1})={h2} (full {(k0+1)*(l1+1)}), "
          f"Lemma-4 RHS = {h1 + h2 - (k1+1)*(l1+1)}")
print("ALL OK" if allok else "SOME FAIL")
