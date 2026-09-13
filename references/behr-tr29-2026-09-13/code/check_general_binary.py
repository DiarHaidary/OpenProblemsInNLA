"""K5 (exact over Q): ingredients of Theorem B (REPORT.md §4) for monomial factors F = x^a y^b (a >= b >= 1),
G = u^c v^d (c >= d >= 1), A = a+b, B = c+d, all exponents <= 5.
Ann(F) = (alpha1^(b+1), alpha0^(a+1)): r = b+1, s = a+1; Ann(G): r' = d+1, s' = c+1.
Checks, for T = F (x) G:
 (i)  for 0 <= i <= r-1 and 0 <= k <= s'-1: Ann(T)_(i,k) = beta1^(d+1) * S_(i,k-d-1)   (dimension + containment);
 (ii) for 0 <= i <= s-1 and 0 <= k <= r'-1: Ann(T)_(i,k) = alpha1^(b+1) * S_(i-b-1,k);
 (iii) rank Cat_(r-1,s'-1)(T) = r r'  and (A-(r-1), B-(s'-1)) = (s-1, r'-1);
 and reports the resulting bound r s' + s r' - r r' = (a+1)(c+1) - (a-b)(c-d).
"""
from common import cat_matrix, rank_Q
ok = True; rows = []
for a in range(1, 6):
    for b in range(1, a + 1):
        for c in range(1, 6):
            for d in range(1, c + 1):
                A, B = a + b, c + d
                T = {(a, c): 1}          # x^a y^(A-a) u^c v^(B-c)
                r, s, r2, s2 = b + 1, a + 1, d + 1, c + 1
                for i in range(0, r):
                    for k in range(0, s2):
                        M, cols, _ = cat_matrix(T, A, B, i, k)
                        dimAnn = (i + 1) * (k + 1) - rank_Q(M)
                        if dimAnn != (i + 1) * max(k - d, 0):
                            ok = False; print("FAIL (i)", a, b, c, d, i, k, dimAnn)
                        for cc, (ss, tt) in enumerate(cols):          # beta1-degree k-tt >= d+1 must annihilate
                            if k - tt >= d + 1 and any(row[cc] for row in M):
                                ok = False; print("FAIL (i) containment", a, b, c, d, i, k)
                for i in range(0, s):
                    for k in range(0, r2):
                        M, cols, _ = cat_matrix(T, A, B, i, k)
                        dimAnn = (i + 1) * (k + 1) - rank_Q(M)
                        if dimAnn != (k + 1) * max(i - b, 0):
                            ok = False; print("FAIL (ii)", a, b, c, d, i, k, dimAnn)
                        for cc, (ss, tt) in enumerate(cols):
                            if i - ss >= b + 1 and any(row[cc] for row in M):
                                ok = False; print("FAIL (ii) containment", a, b, c, d, i, k)
                rc = rank_Q(cat_matrix(T, A, B, r - 1, s2 - 1)[0])
                if rc != r * r2 or (A - (r - 1), B - (s2 - 1)) != (s - 1, r2 - 1):
                    ok = False; print("FAIL (iii)", a, b, c, d, rc)
                rows.append((a, b, c, d, r * s2 + s * r2 - r * r2, (a + 1) * (c + 1) - (a - b) * (c - d)))
assert all(x[4] == x[5] for x in rows)
print("checked", len(rows), "monomial pairs; sample bounds (a,b,c,d -> bound):",
      [(x[:4], x[4]) for x in rows if x[:4] in [(1,1,1,1),(2,1,2,1),(3,1,3,1),(4,1,4,1),(2,2,2,1),(3,2,2,1),(3,2,3,1),(2,2,2,2)]])
print("ALL OK" if ok else "SOME FAILURE")
