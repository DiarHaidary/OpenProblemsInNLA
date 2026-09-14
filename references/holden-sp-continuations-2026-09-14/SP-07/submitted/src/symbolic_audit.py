#!/usr/bin/env python3
"""Separate SymPy reconstruction of small completion examples and model algebra."""
import argparse,json,time
from pathlib import Path
import sympy as s


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    arg=parser.parse_args();start=time.perf_counter();checks=[];examples=[]
    x=s.symbols('x')
    for lam,expected,label in [(-s.Rational(1,3),x*(x-s.Rational(4,3))**2*(x-s.Rational(4,9))**2,'compressed-optimal'),
                               (-s.Rational(1,2),x*(x-1)**4,'completion-optimal')]:
        D=s.zeros(5);U=s.zeros(5)
        for j in range(3):D[(j+1)%3,j]=1
        D[4,3]=-1;U[0,0]=1
        for j in [1,2]:
            k=2+j;U[j,j]=lam;U[k,k]=-lam;U[j,k]=U[k,j]=s.sqrt(1-lam**2)
        H=D*U+U*D;G=s.simplify(H.T*H)
        for ok,name in [(U.T==U,'reflection symmetry'),(s.simplify(U*U)==s.eye(5),'reflection involution'),
                        (s.simplify(H*U-U*H)==s.zeros(5),'pinching commutation'),
                        (s.expand(G.charpoly(x).as_expr()-expected)==0,'exact Gram characteristic polynomial'),
                        (D*D.T!=D.T*D,'complementary normality is not assumed')]:
            require(ok,label+': '+name);checks.append(label+': '+name)
        examples.append({'name':label,'Gram_characteristic_polynomial':str(s.factor(expected))})
    t,B,d,z=s.symbols('t B d z',real=True)
    sx=s.Matrix([[0,1],[1,0]]);sz=s.diag(1,-1)
    M=t*sx+s.I*(B*s.eye(2)+d*sz);G=s.expand(M.conjugate().T*M)
    expected=(z-(t*t+B*B+d*d))**2-4*d*d*(t*t+B*B)
    cp=G.charpoly(z)
    # SymPy may replace an assumed symbol by a fresh polynomial generator.
    require(s.expand(cp.as_expr().subs(cp.gen,z)-expected)==0,'Pauli singular-value identity failed')
    checks.append('Pauli singular-value polynomial')
    b,c,u=s.symbols('b c u',real=True)
    q=s.expand((1+u*u-2*c*u)**2-b*b*(1+u*u)**2)
    qlist=(1-b*b)-4*c*u+(2+4*c*c-2*b*b)*u*u-4*c*u**3+(1-b*b)*u**4
    require(s.expand(q-qlist)==0,'Quartic substitution failed');checks.append('Rationalized integral quartic')
    ss,cc,zz=s.symbols('ss cc zz',real=True)
    Q=1-ss**2+2*cc*(ss-zz)-cc**2*(1-zz**2)
    g=ss-zz-cc*(1-zz**2)
    expr=s.diff(Q**s.Rational(-1,2),cc,2)*Q**s.Rational(5,2)
    require(s.simplify(expr-3*g*g-(1-zz**2)*Q)==0,'Strict-convexity identity failed')
    checks.append('Height-balance strict-convexity identity')
    out={'status':'PASS','checks':checks,'check_count':len(checks),'examples':examples,
         'seconds':time.perf_counter()-start,'sympy_version':s.__version__,
         'scope':'Independent symbolic reconstruction; not an external referee audit'}
    if arg.output:arg.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
