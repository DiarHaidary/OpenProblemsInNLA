import random, itertools
import numpy as np, sympy as sp
from math import comb, factorial
exec(open('ref_check.py').read().split('print("== Lemma 2')[0])  # reuse helpers
rng=np.random.default_rng(7)
def nrank(M):
    sv=np.linalg.svd(np.asarray(M,dtype=complex),compute_uv=False)
    return int((sv>1e-9*max(sv[0],1e-300)).sum())
def evalmat(pts,i,k):
    return np.array([[P[0]**m[0]*P[1]**m[1]*P[2]**m[2]*P[3]**m[3] for m in monos(i,k)] for P in pts],dtype=complex)
def coeffvec(pts,w,A,B):
    ms=monos(A,B)  # index (A-s,s,B-t,t) coefficient of x^{A-s}y^s u^{B-t} v^t
    return np.array([comb(A,m[0])*comb(B,m[2])*sum(wj*P[0]**m[0]*P[1]**m[1]*P[2]**m[2]*P[3]**m[3] for P,wj in zip(pts,w)) for m in ms]),ms

print("== explicit decomposition (numeric), h_Z, Gram rank ==")
for p in range(1,7):
    for q in range(1,7):
        A,B=p+1,q+1;N=p+q;pts=[];w=[]
        for eps in (1,-1):
            c=eps**(q-1); a00=1 if c==1 else np.exp(1j*np.pi/N)
            for t in range(N):
                a=a00*np.exp(2j*np.pi*t/N); pts.append((a,1,eps*a,1)); w.append(eps)
        cv,ms=coeffvec(pts,w,A,B)
        big=[ms[j] for j in range(len(ms)) if abs(cv[j])>1e-8]
        V1=evalmat(pts,1,q);V2=evalmat(pts,p,1);W=np.diag(w)
        h1,h2,g=nrank(V1),nrank(V2),nrank(V1.T@W@V2)
        flag = (big==[(p,1,q,1)] and h1==2*q+2 and h2==2*p+2 and g==4)
        print(f"p={p} q={q} n={len(pts)} support={big} h1={h1} h2={h2} rankGram={g} ok={flag}")

print("== Lemma 4 random test ==")
bad=0
for trial in range(300):
    p=int(rng.integers(1,5));q=int(rng.integers(1,5));A,B=p+1,q+1
    n=int(rng.integers(1,(A+1)*(B+1)+2))
    pts=[tuple(rng.normal(size=4)+1j*rng.normal(size=4)) for _ in range(n)]
    if rng.random()<0.5:  # force structure: points on few lines
        pts=[(P[0],P[1],1.0,float(rng.integers(0,2))) for P in pts]
    w=rng.normal(size=n)+1j*rng.normal(size=n)
    i=int(rng.integers(0,A+1));k=int(rng.integers(0,B+1))
    Gm=evalmat(pts,i,k).T@np.diag(w)@evalmat(pts,A-i,B-k)
    # Gram rank equals rank Cat (check via explicit Cat from coefficient tensor)
    lhs=nrank(Gm); rhs=nrank(evalmat(pts,i,k))+nrank(evalmat(pts,A-i,B-k))-n
    if lhs<rhs: bad+=1
print("Lemma 4 violations:",bad)

print("== variant tensors: where does the argument break? ==")
def analyze(name,F,p,q,known_ub):
    A,B=p+1,q+1
    rep=[]
    for (i,k) in sorted(set([(i,k) for i in (0,1) for k in range(q+1)]+[(i,k) for k in (0,1) for i in range(p+1)])):
        r,forms=kernel_forms(F,i,k,A,B)
        if not forms: continue
        sf=None
        for f in forms:
            if squarefree(f): sf=f;break
        if sf is None:
            for _ in range(6):
                g=random_comb(forms)
                if squarefree(g): sf=g;break
        if sf is not None: rep.append(((i,k),sp.factor(sf)))
    rc,_=kernel_forms(F,1,q,A,B)
    print(f"{name} (p={p},q={q}): rank Cat_(1,q)={rc}; naive bound 2q+2+2p+2-rankCat={2*q+2+2*p+2-rc}; known rank <= {known_ub}")
    print("   squarefree low annihilators (Lemma 2/3 fail):", rep[:4] if rep else "NONE")
for p,q in [(2,1),(2,2),(3,2)]:
    analyze("x^{p+1} (x) u^q v", x**(p+1)*u**q*v, p,q, q+1)
    analyze("x^p y (x) u^{q+1}", x**p*y*u**(q+1), p,q, p+1)
    analyze("(x^p y+y^{p+1}) (x) u^q v", (x**p*y+y**(p+1))*u**q*v, p,q, (p if p>=3 else 2)*(q+1))
    analyze("tangent x^p y u^{q+1}+x^{p+1}u^q v", x**p*y*u**(q+1)+x**(p+1)*u**q*v, p,q, "?")
    analyze("x^p y (x) (u^q v + v^{q+1})", x**p*y*(u**q*v+v**(q+1)), p,q, "(p+1)*R(G)")
