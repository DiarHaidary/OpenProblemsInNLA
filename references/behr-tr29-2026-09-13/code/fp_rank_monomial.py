"""K6 (exhaustive, exact over F_P): finite-field sanity check of Theorem B (§4 of REPORT.md) in a case with
equal generator degrees, not covered by the W-theorem: F = x^2 y^2 (Ann = (a0^3, a1^3), r = s = 3, R(F) = 3),
G = u^2 v (r' = 2, s' = 3, lowest generator b1^2 not squarefree). Theorem B predicts R(F (x) G) >= 9.
Tests every n-subset Z of P^1 x P^1(F_P) for T = x^a y^(A-a) u^c v^(B-c) in span nu_(A,B)(Z).
usage: fp_rank_monomial.py P A a B c n     (e.g. 5 4 2 3 2 8: x^2y^2 (x) u^2 v, 8-subsets over F_5)
This is a finite-field check, not a proof over C.
"""
import sys, itertools, time
import numpy as np
from math import comb
P, A, a0, B, c0, n = map(int, sys.argv[1:7])
assert P > max(A, B)
pts = [(a, 1) for a in range(P)] + [(1, 0)]
grid = [(l, m) for l in pts for m in pts]
def nu(l, m):
    a, b = l; c, e = m
    L = [comb(A, i) * pow(a, i, P) * pow(b, A - i, P) for i in range(A + 1)]
    M = [comb(B, k) * pow(c, k, P) * pow(e, B - k, P) for k in range(B + 1)]
    return (np.outer(L, M) % P).ravel()
NU = np.array([nu(l, m) for l, m in grid], dtype=np.int64)
D = NU.shape[1]
target = np.zeros(D, dtype=np.int64); target[a0 * (B + 1) + c0] = 1
INV = np.array([0] + [pow(i, P - 2, P) for i in range(1, P)], dtype=np.int64)
def batch_in_span(Mat):
    Mat = Mat % P; N, R, C = Mat.shape
    row = np.zeros(N, dtype=np.int64); ar = np.arange(N)
    for col in range(C - 1):
        mask = (Mat[:, :, col] != 0) & (np.arange(R)[None, :] >= row[:, None])
        has = mask.any(axis=1)
        if not has.any():
            continue
        piv = np.argmax(mask, axis=1)
        idx = ar[has]; pr = piv[has]; rr = row[has]
        tmp = Mat[idx, pr, :].copy(); Mat[idx, pr, :] = Mat[idx, rr, :]; Mat[idx, rr, :] = tmp
        pv = INV[Mat[idx, rr, col]]
        Mat[idx, rr, :] = (Mat[idx, rr, :] * pv[:, None]) % P
        f = Mat[idx, :, col].copy(); f[np.arange(len(idx)), rr] = 0
        Mat[idx, :, :] = (Mat[idx, :, :] - f[:, :, None] * Mat[idx, rr, :][:, None, :]) % P
        row[has] += 1
    zero_coef = (Mat[:, :, :C - 1] == 0).all(axis=2)
    bad = (zero_coef & (Mat[:, :, C - 1] != 0)).any(axis=1)
    return ~bad
rng = np.random.default_rng(2)
S = np.array([rng.choice(len(grid), n, replace=False) for _ in range(300)])
Wt = rng.integers(0, P, size=(300, n)); cols = NU[S]
tg = (np.einsum('bn,bnd->bd', Wt, cols)) % P
st = batch_in_span(np.concatenate([cols.transpose(0, 2, 1), tg[:, :, None]], axis=2)).all()
print(f"P={P} target x^{a0} y^{A-a0} u^{c0} v^{B-c0}, n={n}; self-test: {st}")
t0 = time.time(); found = 0; total = 0
it = itertools.combinations(range(len(grid)), n)
while True:
    chunk = list(itertools.islice(it, 20000))
    if not chunk:
        break
    S = np.array(chunk, dtype=np.int64)
    Mat = np.concatenate([NU[S].transpose(0, 2, 1), np.broadcast_to(target, (len(S), D))[:, :, None]], axis=2)
    hit = batch_in_span(Mat); found += int(hit.sum()); total += len(S)
print(f"subsets tested: {total}; subsets whose span contains the target: {found}; time {time.time()-t0:.1f}s")
