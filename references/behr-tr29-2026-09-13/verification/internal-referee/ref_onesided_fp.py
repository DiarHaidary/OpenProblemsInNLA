# Black-box test over F_5 of the referee's one-sided bound R(F⊗G) >= R(F)*br(G) when F satisfies (H_F):
# F = x^2 y (R=3, br=2), G = u^3+v^3 or u^4+v^4 (R=br=2): claim R(F⊗G) >= 6, so no 5-subset of P1xP1(F_5) spans F⊗G.
import itertools, random, time
from math import comb
P=5
P1=[(1,0)]+[(a,1) for a in range(P)]
def vec(pt,A,B):  # coefficients of (ax+by)^A (cu+ev)^B in monomial basis x^{A-i}y^i u^{B-k}v^k
    (a,b),(c,e)=pt
    return [comb(A,i)*pow(a,A-i,P)*pow(b,i,P)*comb(B,k)*pow(c,B-k,P)*pow(e,k,P)%P for i in range(A+1) for k in range(B+1)]
def rank_mod(rows):
    rows=[r[:] for r in rows]; rk=0; L=len(rows[0])
    for col in range(L):
        piv=next((j for j in range(rk,len(rows)) if rows[j][col]%P),None)
        if piv is None: continue
        rows[rk],rows[piv]=rows[piv],rows[rk]; inv=pow(rows[rk][col],P-2,P)
        rows[rk]=[x*inv%P for x in rows[rk]]
        for j in range(len(rows)):
            if j!=rk and rows[j][col]%P:
                f=rows[j][col]; rows[j]=[(x-f*y)%P for x,y in zip(rows[j],rows[rk])]
        rk+=1
    return rk
def run(name,Tdict,A,B,n):
    grid=[(p1,p2) for p1 in P1 for p2 in P1]
    V=[vec(g,A,B) for g in grid]
    T=[Tdict.get((i,k),0)%P for i in range(A+1) for k in range(B+1)]
    # control: random in-span targets of n grid points are recognised
    rnd=random.Random(3); ctrl=True
    for _ in range(50):
        S=rnd.sample(range(len(grid)),n); w=[rnd.randrange(1,P) for _ in S]
        Tc=[sum(wj*V[s][j] for wj,s in zip(w,S))%P for j in range(len(T))]
        if not any(rank_mod([V[s] for s in S2]+[Tc])==rank_mod([V[s] for s in S2]) for S2 in [S]): ctrl=False
    t=time.time(); hits=0; cnt=0
    for S in itertools.combinations(range(len(grid)),n):
        cnt+=1
        M=[V[s] for s in S]
        if rank_mod(M+[T])==rank_mod(M): hits+=1; break
    print(f"{name}: grid={len(grid)} n={n} control={ctrl} subsets tested={cnt} spanning subsets={hits} time={time.time()-t:.0f}s")
# x^2 y ⊗ (u^3+v^3): monomial x^{A-i} y^i u^{B-k} v^k with A=3: x^2y -> i=1; u^3 -> k=0, v^3 -> k=3
run("x^2y⊗(u^3+v^3)",{(1,0):1,(1,3):1},3,3,5)
run("x^2y⊗(u^4+v^4)",{(1,0):1,(1,4):1},3,4,5)
