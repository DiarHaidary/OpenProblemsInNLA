"""Active family from Chen--Edelman--Urschel (2026), equation 2.1.
Not a parameterization of all completely pivoted matrices.
"""
from __future__ import annotations
INITIAL_ACTIVE=[(1,1,2,1),(1,2,4,-1),(1,2,5,1),(1,3,1,-1),(1,3,4,-1),
 (1,3,5,-1),(1,4,3,1),(1,4,4,1),(1,4,5,1),(1,5,2,-1),(1,5,3,1),(1,5,4,-1),(1,5,5,1)]
LATER_ACTIVE=[(2,3,2,1),(2,3,4,-1),(2,4,3,1),(2,5,2,-1),(3,3,5,-1),
 (3,4,3,1),(3,5,4,-1),(4,4,5,1),(4,5,4,-1),(4,5,5,1)]
ACTIVE=INITIAL_ACTIVE+LATER_ACTIVE

def parameters(g,z):
    x=(8+4*z-8*z*z-g*(2+z-z*z))/(4*z)
    d0=2*x*x*z+x*z*z+x*z-2*x-2
    y=(g-4)*d0/(2*z*(z-1))-1
    p=1+z;d=2-z*(x+z);a=-z/y;c=z*(x+z)/(1+x)
    r=(-1+x*z)/p;s=(1-x*c)/p
    t=(y*(z+c)+z*(1+x)-d)/(r-s);e=p*(p-d)/t
    return dict(g=g,z=z,x=x,y=y,p=p,d=d,a=a,c=c,r=r,s=s,t=t,e=e)

def make_candidate(g,z):
    v=parameters(g,z);x,y,a,c,d,t,e=(v[s] for s in ['x','y','a','c','d','t','e'])
    return [[1,1,a,-z,c],[x,1+x+z,x*a+e,-1,1],[-1,z,d-a+e,-1,-1],
            [y,y+t,1,1,1],[z,-1,1,-1,1]]

def eliminate(A):
    S=[list(row) for row in A];stages=[]
    while S:
        stages.append(S);p=S[0][0]
        S=[[S[i][j]-S[i][0]*S[0][j]/p for j in range(1,len(S))] for i in range(1,len(S))]
    return stages

def constraints(stages):
    out=[]
    for k,S in enumerate(stages[:-1],start=1):
        for i in range(len(S)):
            for j in range(len(S)):
                if i==j==0:continue
                for sign in [1,-1]:out.append(((k,k+i,k+j,sign),S[0][0]-sign*S[i][j]))
    return out

def value_and_jacobian(A,zero,one):
    S=[list(row) for row in A]
    J=[[[zero for _ in range(24)] for _ in range(5)] for _ in range(5)]
    for t in range(24):
        i,j=divmod(t+1,5);J[i][j][t]=one
    c=[];CJ=[];labels=[];pivots=[]
    for k in range(5):
        p=S[k][k];pivots.append(p)
        if k<4:
            for i in range(k,5):
                for j in range(k,5):
                    if i==j==k:continue
                    for sign in [1,-1]:
                        labels.append((k+1,i+1,j+1,sign));c.append(p-sign*S[i][j])
                        CJ.append([J[k][k][t]-sign*J[i][j][t] for t in range(24)])
        for i in range(k+1,5):
            for j in range(k+1,5):
                a,b=S[i][k],S[k][j]
                new=[J[i][j][t]-(J[i][k][t]*b+a*J[k][j][t])/p+a*b*J[k][k][t]/(p*p) for t in range(24)]
                S[i][j]-=a*b/p;J[i][j]=new
    return S[4][4],J[4][4],c,CJ,labels,pivots
