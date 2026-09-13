"""Exact helpers: bihomogeneous forms, contraction, ranks over Q (Fractions) and over F_P."""
from fractions import Fraction
from math import comb
import itertools

def ff(n, r):
    """falling factorial n(n-1)...(n-r+1); 0 if r > n."""
    if r > n:
        return 0
    out = 1
    for t in range(r):
        out *= n - t
    return out

def contract_mono(i, s, k, t, A, B, m, n):
    """alpha0^s alpha1^(i-s) beta0^t beta1^(k-t) applied to x^m y^(A-m) u^n v^(B-n).
    Returns (coef, (m-s, n-t)) or (0, None)."""
    if s > m or i - s > A - m or t > n or k - t > B - n:
        return 0, None
    c = ff(m, s) * ff(A - m, i - s) * ff(n, t) * ff(B - n, k - t)
    return c, (m - s, n - t)

def cat_matrix(F, A, B, i, k):
    """F: dict {(m,n): coef} for x^m y^(A-m) u^n v^(B-n). Matrix of g -> g∘F, g in S_(i,k)
    (basis alpha0^s alpha1^(i-s) beta0^t beta1^(k-t)), rows = monomials of R_(A-i,B-k)."""
    cols = [(s, t) for s in range(i + 1) for t in range(k + 1)]
    rows = [(m, n) for m in range(A - i + 1) for n in range(B - k + 1)]
    ridx = {r: j for j, r in enumerate(rows)}
    M = [[0] * len(cols) for _ in rows]
    for c, (s, t) in enumerate(cols):
        for (m, n), f in F.items():
            cf, mono = contract_mono(i, s, k, t, A, B, m, n)
            if cf:
                M[ridx[mono]][c] += cf * f
    return M, cols, rows

def rank_Q(M):
    M = [[Fraction(x) for x in row] for row in M]
    if not M:
        return 0
    R, C = len(M), len(M[0]); r = 0
    for c in range(C):
        piv = next((j for j in range(r, R) if M[j][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for j in range(R):
            if j != r and M[j][c] != 0:
                f = M[j][c] / M[r][c]
                M[j] = [a - f * b for a, b in zip(M[j], M[r])]
        r += 1
        if r == R:
            break
    return r

def nullspace_Q(M):
    """basis of {x : M x = 0} over Q."""
    M = [[Fraction(x) for x in row] for row in M]
    R, C = len(M), (len(M[0]) if M else 0)
    piv_cols = []; r = 0
    for c in range(C):
        piv = next((j for j in range(r, R) if M[j][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]; M[r] = [a / pv for a in M[r]]
        for j in range(R):
            if j != r and M[j][c] != 0:
                f = M[j][c]; M[j] = [a - f * b for a, b in zip(M[j], M[r])]
        piv_cols.append(c); r += 1
        if r == R:
            break
    free = [c for c in range(C) if c not in piv_cols]
    basis = []
    for fc in free:
        v = [Fraction(0)] * C; v[fc] = Fraction(1)
        for row, pc in enumerate(piv_cols):
            v[pc] = -M[row][fc]
        basis.append(v)
    return basis

def rank_mod(M, P):
    M = [[x % P for x in row] for row in M]
    if not M:
        return 0
    R, C = len(M), len(M[0]); r = 0
    for c in range(C):
        piv = next((j for j in range(r, R) if M[j][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [(a * inv) % P for a in M[r]]
        for j in range(R):
            if j != r and M[j][c]:
                f = M[j][c]; M[j] = [(a - f * b) % P for a, b in zip(M[j], M[r])]
        r += 1
        if r == R:
            break
    return r

def T_dict(p, q):
    return {(p, q): 1}      # x^p y^1 u^q v^1 with A = p+1, B = q+1
