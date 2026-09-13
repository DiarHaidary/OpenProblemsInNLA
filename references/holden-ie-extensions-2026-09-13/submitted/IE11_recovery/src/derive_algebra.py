#!/usr/bin/env python3
"""Exact reconstruction of the candidate polynomial, not global optimality."""
from pathlib import Path
import json,time
import sympy as sp
from sympy.polys.fields import field
from math import comb
from candidate import parameters,make_candidate,eliminate,constraints,ACTIVE
ROOT=Path(__file__).resolve().parents[1]

def run():
    if not __debug__:raise RuntimeError('Run without -O; assertions are proof checks')
    start=time.time();K,g,z=field('g,z',sp.QQ);gs,zs=sp.symbols('g z')
    v=parameters(g,z);x,y,p,d,c,r,s,t,e=[v[a] for a in ['x','y','p','d','c','r','s','t','e']]
    X=1+z*z/y+e;Y=2-(z+x)*c;R=-z*(1+x);H=1+y*z+z*(1+x)-t*r
    assert 2*H==g and H*(d-R)==d*d-R*Y
    F=sp.Poly((g/2-Y-X).numer.as_expr(),gs,zs)
    assert F.degree(gs)==7 and F.degree(zs)==10
    stages=eliminate([[K(a) for a in row] for row in make_candidate(g,z)]);cs=dict(constraints(stages));ident=0
    for label in ACTIVE:
        if not cs[label]:ident+=1
        else:assert sp.Poly(cs[label].numer.as_expr(),gs,zs).rem(F).is_zero
    assert ident==21
    assert sp.Poly((stages[-1][0][0]-g).numer.as_expr(),gs,zs).rem(F).is_zero
    assert stages[3][0][0]==g/2 and stages[3][0][1]==g/2
    disc=sp.discriminant(F.as_expr(),zs);factors=sp.factor_list(disc)
    P5=sp.Poly(next(v for v,m in factors[1] if sp.degree(v,gs)==61),gs)
    assert P5.LC()==59049
    expected=-sp.Integer(295147905179352825856)*(gs-6)*(gs-4)**32*(gs-2)**6*(gs**2-12*gs+40)*P5.as_expr()
    assert sp.Poly(disc-expected,gs).is_zero
    pp=list(reversed(P5.all_coeffs()))
    reference=[int(a) for a in (ROOT/'data'/'reference_P5_ascending.txt').read_text().split()]
    assert [int(a) for a in pp]==reference, 'Mismatch with source Eq. 2.15'
    q=[0]*62
    for i,ci in enumerate(pp):
        for j in range(i+1):
            a=int(ci)*comb(i,j)*4**(i-j)*5**j
            for k in range(62-i):q[j+k]+=a*comb(61-i,k)
    signs=[1 if t>0 else -1 for t in q if t];variations=sum(a!=b for a,b in zip(signs,signs[1:]))
    assert variations==1 and P5.eval(4)<0 and P5.eval(5)>0
    Q11=zs**11-6*zs**10+15*zs**9-16*zs**8+7*zs**7-22*zs**6+81*zs**5-60*zs**4+8*zs**3-56*zs**2+144*zs+32
    assert sp.Poly(F.as_expr().subs(gs,4+zs-zs**2)+zs**5*(zs-1)**4*(zs**4-2*zs**3+zs**2+4)*Q11,zs).is_zero
    bb=[0]*12
    for i,ci in enumerate(reversed(sp.Poly(Q11,zs).all_coeffs())):
        for k in range(12-i):bb[i+k]+=int(ci)*comb(11-i,k)
    assert all(v>0 for v in bb)
    data=dict(F_terms=[dict(g=int(a),z=int(b),c=str(c)) for (a,b),c in F.terms()],P5_ascending=[str(c) for c in pp],
        source='Chen, Edelman, Urschel, arXiv:2602.20390v1; reconstructed from the active family in Eq. 2.1.')
    (ROOT/'data'/'polynomials.json').write_text(json.dumps(data,indent=2)+'\n')
    (ROOT/'data'/'F.txt').write_text(str(F.as_expr())+'\n');(ROOT/'data'/'P5.txt').write_text(str(P5.as_expr())+'\n')
    result=dict(status='PASS',global_solution=False,F_degrees=[7,10],P5_degree=61,active_equalities_identical=ident,
        active_equalities_modulo_F=23-ident,final_pivot_equals_g_modulo_F=True,discriminant_verified=True,
        unique_root_in_4_5=True,reference_coefficients_match=True,descartes_variations=variations,descartes_coefficients=[str(c) for c in q],
        extraneous_branch_positive_coefficients=bb,seconds=time.time()-start)
    (ROOT/'results'/'algebra_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    return F,P5,result
if __name__=='__main__':
    F,P,r=run();print('PASS: exact algebra, discriminant, and unique P5 root in (4,5). Not a global proof.')
