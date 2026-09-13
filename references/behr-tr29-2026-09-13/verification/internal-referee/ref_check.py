# Referee checks for PROOF_DRAFT.md (exact integer/rational linear algebra via sympy)
import itertools, random
from math import factorial, comb
import sympy as sp
x,y,u,v = sp.symbols('x y u v'); a0,a1,b0,b1 = sp.symbols('a0 a1 b0 b1')
random.seed(1)

def monos(i,k):
    return [(i-s,s,k-t,t) for s in range(i+1) for t in range(k+1)]

def apply(m, F):
    return sp.diff(F, x, m[0], y, m[1], u, m[2], v, m[3]) if True else None

def dop(m,F):
    G=F
    for var,e in zip((x,y,u,v),m):
        if e: G=sp.diff(G,var,e)
    return sp.expand(G)

def cat_matrix(F,i,k,A,B):
    ms=monos(i,k); tgt=[(A-i-s,s,B-k-t,t) for s in range(A-i+1) for t in range(B-k+1)]
    M=sp.zeros(len(tgt),len(ms))
    for c,m in enumerate(ms):
        P=sp.Poly(dop(m,F),x,y,u,v)
        for r,tm in enumerate(tgt):
            M[r,c]=P.coeff_monomial(x**tm[0]*y**tm[1]*u**tm[2]*v**tm[3])
    return M,ms

def kernel_forms(F,i,k,A,B):
    M,ms=cat_matrix(F,i,k,A,B)
    ns=M.nullspace()
    forms=[sp.expand(sum(vec[j]*a0**m[0]*a1**m[1]*b0**m[2]*b1**m[3] for j,m in enumerate(ms))) for vec in ns]
    return M.rank(), forms

def squarefree(g):
    if g==0: return False
    _,fl=sp.factor_list(g)
    return all(e==1 for _,e in fl)

def random_comb(forms):
    return sp.expand(sum(random.randint(-9,9)*f for f in forms))

print("== Lemma 2 + rank Cat_(1,q), T = x^p y u^q v ==")
ok=True
for p in range(1,6):
    for q in range(1,6):
        A,B=p+1,q+1; T=x**p*y*u**q*v
        bidegs=[(i,k) for i in (0,1) for k in range(q+1)]+[(i,k) for k in (0,1) for i in range(p+1)]
        for (i,k) in set(bidegs):
            r,forms=kernel_forms(T,i,k,A,B)
            if i<=1 and k<=q:
                exp_dim = (i+1)*(k-1) if k>=2 else 0
                div = all(sp.rem(f, b1**2, b1)==0 for f in forms)
                if len(forms)!=exp_dim or not div: ok=False; print("FAIL L2a",p,q,i,k,len(forms),exp_dim)
            if k<=1 and i<=p:
                exp_dim = (k+1)*(i-1) if i>=2 else 0
                div = all(sp.rem(f, a1**2, a1)==0 for f in forms)
                if len(forms)!=exp_dim or not div: ok=False; print("FAIL L2b",p,q,i,k,len(forms),exp_dim)
        r,_=kernel_forms(T,1,q,A,B)
        if r!=4: ok=False; print("FAIL rankCat",p,q,r)
        # also (i,k)=(1,q) vs (p,1) complementary; and symmetric Cat_(p,1) rank
        r2,_=kernel_forms(T,p,1,A,B)
        if r2!=4: ok=False; print("FAIL rankCat(p,1)",p,q,r2)
print("Lemma 2 and rank Cat = 4 for 1<=p,q<=5:", ok)

print("== explicit decomposition (exact, cyclotomic) + h_Z + Gram rank ==")
for p in range(1,5):
    for q in range(1,5):
        A,B=p+1,q+1; N=p+q
        pts=[]
        for eps in (1,-1):
            c = sp.Integer(eps)**(q-1)
            a00 = 1 if c==1 else sp.exp(sp.pi*sp.I/N)
            for t in range(N):
                a=sp.nsimplify(a00*sp.exp(2*sp.pi*sp.I*t/N))
                pts.append((a,1,eps*a,1,eps))
        S=sum(w*(aa*x+bb*y)**A*(cc*u+ee*v)**B for aa,bb,cc,ee,w in pts)
        P=sp.Poly(sp.expand(S),x,y,u,v)
        coeffs={mon:sp.nsimplify(sp.simplify(cf)) for mon,cf in zip(P.monoms(),P.coeffs())}
        nz={m:c for m,c in coeffs.items() if sp.simplify(c)!=0}
        target=(p,1,q,1)
        dist=len(set((sp.nsimplify(aa),sp.nsimplify(cc)) for aa,bb,cc,ee,w in pts))
        def evalmat(i,k):
            return sp.Matrix([[aa**m[0]*bb**m[1]*cc**m[2]*ee**m[3] for m in monos(i,k)] for aa,bb,cc,ee,w in pts])
        V1=evalmat(1,q); V2=evalmat(p,1); W=sp.diag(*[w for *_,w in pts])
        V1n=sp.Matrix(V1).evalf(30); V2n=sp.Matrix(V2).evalf(30)
        import mpmath
        mpmath.mp.dps=30
        def nrank(M):
            Mm=mpmath.matrix(M.tolist()); s=mpmath.svd_r(Mm*0+Mm, compute_uv=False) if False else None
            import numpy as np
            arr=np.array(M.evalf(20).tolist(),dtype=complex)
            sv=np.linalg.svd(arr,compute_uv=False)
            return int((sv>1e-8*sv[0]).sum())
        h1=nrank(V1); h2=nrank(V2); g=nrank(V1.T*W*V2)
        print(f"p={p} q={q}: n={len(pts)} distinct={dist} support={list(nz.keys())} target={target} "
              f"h(1,q)={h1}/{2*q+2} h(p,1)={h2}/{2*p+2} rankGram={g} bound={h1+h2-g}")
