"""Compare the exact certificate equations/Jacobian with symbolic differentiation.

SymPy constructs the matrix identities directly, differentiates them, and
checks every Jacobian entry at an exact dyadic point. This is separate from
the hand-coded Jacobian construction used by the integer reference verifier.
The quadratic monomial coefficients also check the global Hessian bound.
Finite examples support, but do not replace, the all-rank written proof.
"""
from pathlib import Path
import sys,json,time
import numpy as np
import sympy as sp
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'verify'))
from reference import exact_system

def exact_complex(v):
    a,b=float(v.real).as_integer_ratio();c,d=float(v.imag).as_integer_ratio()
    return sp.Rational(a,b)+sp.I*sp.Rational(c,d)

def one(m):
    n=2*m;size=n*n
    symbols=sp.symbols(f'x0:{size}')
    X=sp.Matrix(n,n,symbols)
    I=sp.eye(m);Z=sp.zeros(m)
    J=Z.row_join(I).col_join((-I).row_join(Z))
    rng=np.random.default_rng(615723+m)
    x=(rng.integers(-8,9,size=size)+1j*rng.integers(-8,9,size=size))/4
    u=(rng.integers(-8,9,size=size)+1j*rng.integers(-8,9,size=size))/8
    U=sp.Matrix(n,n,[exact_complex(v) for v in u])
    V=X.T*J*X-J
    R=(U-X).T*X*J
    equations=[sp.expand(V[i,j]) for i in range(n) for j in range(i+1,n)]
    equations += [sp.expand(R[i,j]+R[j,i]) for i in range(n) for j in range(i,n)]
    # Substitution in a linear derivative is done termwise to keep it exact
    # and avoid repeatedly traversing a large simultaneous-substitution tree.
    values=[exact_complex(v) for v in x]
    def evaluate_polynomial(poly):
        out=sp.S.Zero
        for powers,coefficient in poly.terms():
            term=coefficient
            for j,e in enumerate(powers):
                if e:term*=values[j]**e
            out+=term
        return sp.expand(out)
    fr,fi,ar,ai,E=exact_system(x,u,n)
    q_bounds=[]
    for row,f in enumerate(equations):
        polynomial=sp.Poly(f,*symbols)
        f_exact=sp.Rational(int(fr[row]),1<<(2*E))+sp.I*sp.Rational(int(fi[row]),1<<(2*E))
        assert evaluate_polynomial(polynomial)==f_exact,(m,row,'equation')
        for j,symbol in enumerate(symbols):
            derivative=sp.Poly(sp.diff(f,symbol),*symbols)
            a_exact=sp.Rational(int(ar[row,j]),1<<E)+sp.I*sp.Rational(int(ai[row,j]),1<<E)
            assert evaluate_polynomial(derivative)==a_exact,(m,row,j,'Jacobian')
        bound=sp.S.Zero
        for powers,coefficient in polynomial.terms():
            if sum(powers)==2:bound+=2*abs(coefficient)
        allowed=2*n if row<n*(n-1)//2 else 4*n
        assert bound<=allowed,(m,row,bound,allowed)
        q_bounds.append(int(bound))
    return {'rank':m,'equations_checked':size,'Jacobian_entries_checked':size*size,
            'all_exact_equations_and_derivatives_agree':True,
            'quadratic_Hessian_bounds_checked':True,
            'maximum_quadratic_bound':max(q_bounds),'allowed_global_bound':4*n}

if __name__=='__main__':
    started=time.perf_counter();checks=[]
    for m in range(1,5):
        result=one(m);checks.append(result);print(json.dumps(result),flush=True)
    report={'all_passed':True,'checks':checks,'seconds':time.perf_counter()-started,
            'scope':'finite exact implementation checks; not an all-rank formal proof'}
    (BASE/'results'/'polynomial_symbolic_checks.json').write_text(json.dumps(report,indent=2)+'\n')
