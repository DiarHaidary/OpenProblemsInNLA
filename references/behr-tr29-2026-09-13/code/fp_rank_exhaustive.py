"""K3 (exhaustive, exact over F_P): black-box sanity check of the Theorem over F_P for small (p,q).
Tests every n-subset Z of P^1 x P^1(F_P) and decides whether T = x^p y u^q v lies in the F_P-span of nu(Z)
(zero weights allowed, so this covers all decompositions of length <= n with F_P-rational points).
The written proof is valid over any field of characteristic > max(p,q)+1, so for n = 2(p+q)-1 the count must be 0.
Control: n = 2(p+q) (count reported; must be > 0 when F_P-rational decompositions of that length exist).
This is a finite-field check, not a proof over C.
usage: fp_rank_exhaustive.py P p q n
"""
import sys, itertools, time
import numpy as np
from math import comb
P, p, q, n = map(int, sys.argv[1:5])
assert P > max(p, q) + 1
A, B = p + 1, q + 1
pts = [(a, 1) for a in range(P)] + [(1, 0)]
grid = [(l, m) for l in pts for m in pts]
def nu(l, m):
    a, b = l; c, e = m
    L = [comb(A, i) * pow(a, i, P) * pow(b, A - i, P) for i in range(A + 1)]
    M = [comb(B, k) * pow(c, k, P) * pow(e, B - k, P) for k in range(B + 1)]
    return (np.outer(L, M) % P).ravel()
NU = np.array([nu(l, m) for l, m in grid], dtype=np.int64)
D = NU.shape[1]
target = np.zeros(D, dtype=np.int64); target[p * (B + 1) + q] = 1
INV = np.array([0] + [pow(i, P - 2, P) for i in range(1, P)], dtype=np.int64)

def batch_in_span(Mat):
    """Mat: (N, D, n+1), last column = target. True where target in span of first n columns."""
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

# self-test: random spans that contain the target must be recognised; random targets usually not
rng = np.random.default_rng(1)
S = np.array([rng.choice(len(grid), n, replace=False) for _ in range(300)])
Wt = rng.integers(0, P, size=(300, n))
cols = NU[S]                                     # (300, n, D)
tg = (np.einsum('bn,bnd->bd', Wt, cols)) % P
st = batch_in_span(np.concatenate([cols.transpose(0, 2, 1), tg[:, :, None]], axis=2)).all()
print(f"P={P} p={p} q={q} n={n}; |grid|={len(grid)}; self-test (300 constructed in-span targets recognised): {st}")
t0 = time.time(); found = 0; total = 0; examples = []
it = itertools.combinations(range(len(grid)), n)
CH = 20000
while True:
    chunk = list(itertools.islice(it, CH))
    if not chunk:
        break
    S = np.array(chunk, dtype=np.int64)
    Mat = np.concatenate([NU[S].transpose(0, 2, 1), np.broadcast_to(target, (len(S), D))[:, :, None]], axis=2)
    hit = batch_in_span(Mat)
    found += int(hit.sum()); total += len(S)
    if hit.any() and len(examples) < 3:
        examples += [[grid[j] for j in S[k]] for k in np.nonzero(hit)[0][:3 - len(examples)]]
print(f"subsets tested: {total}; subsets whose span contains T: {found}; time {time.time()-t0:.1f}s")
for ex in examples:
    print("  example support:", ex)
