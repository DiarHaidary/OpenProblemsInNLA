"""Exact finite checks of the zero-coupling specialization theorem."""
from pathlib import Path
import sys,json,itertools,time
import sympy as sp
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from stein_normal_form import evaluate,induced_matrix

def main():
    started=time.perf_counter();checks=[]
    for m in range(1,6):
        a=list(range(5,5+m));d=sp.diag(*[sp.Rational(16,x*x) for x in a])
        count=0
        for signs in itertools.product((-1,1),repeat=m):
            C=sp.diag(*[s*x-1 for s,x in zip(signs,a)])
            Y=(C+sp.eye(m)).inv().T
            assert 16*Y*Y==d
            lam=list(C.diagonal())
            Delta=sp.prod(lam[i]*lam[j]-1 for i in range(m) for j in range(i,m))
            assert Delta!=0
            # Exact nonsingularity of H -> YH+HY, after an invertible
            # inverse-transpose change of coordinates.
            square_derivative_det=sp.prod(Y[i,i]+Y[j,j] for i in range(m) for j in range(m))
            assert square_derivative_det!=0
            count+=1
        # A non-diagonal test of the exact epsilon^2 scaling law.
        G=sp.eye(m)
        for i in range(m-1):G[i,i+1]=1
        C=G*sp.diag(*list(range(3,3+m)))*G.inv()
        b=sp.Matrix(m,m,lambda i,j:sp.Rational((i+2)*(j+1)-2,3))
        c=sp.Matrix(m,m,lambda i,j:sp.Rational(i-2*j+3,5))
        z=sp.zeros(m);eps=sp.Rational(3,5)
        _,g,S,T=evaluate(C,b,c,z)
        _,gs,Ss,Ts=evaluate(C,eps*b,eps*c,z)
        _,gn,Sn,Tn=evaluate(C,-eps*b,-eps*c,z)
        base=16*((C+sp.eye(m)).inv().T)**2
        assert Ss==eps*S and Ts==eps*T
        assert gs==base+eps**2*(g-base)
        assert gn==gs
        checks.append({'rank':m,'regular_zero_coupling_roots_checked':count,
                       'expected':2**m,'all_simple_and_in_domain':True,
                       'non_diagonal_scaling_identity':True})
    out={'all_passed':True,'checks':checks,'seconds':time.perf_counter()-started,
         'scope':'exact finite checks supporting the written all-rank argument'}
    (BASE/'results'/'zero_coupling_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
