#!/usr/bin/env python3
"""Integer interval certificate of root, feasibility, STRICT LOCAL maximum.
Not a certificate of global optimality. Run derive_algebra.py first.
"""
from fractions import Fraction
from math import factorial
from pathlib import Path
import json,time
from intervals import I,BITS,solve_interval
from candidate import make_candidate,value_and_jacobian,ACTIVE
ROOT=Path(__file__).resolve().parents[1]

def derivative_terms(terms,dg=0,dz=0):
    out=[]
    for t in terms:
        a,b,c=int(t['g']),int(t['z']),int(t['c'])
        if a>=dg and b>=dz:out.append(dict(g=a-dg,z=b-dz,c=c*factorial(a)//factorial(a-dg)*factorial(b)//factorial(b-dz)))
    return out

def evaluate_terms(terms,g,z):
    if not terms:return 0*g
    dz=max(t['z'] for t in terms);dg=max(t['g'] for t in terms)
    d={(t['g'],t['z']):int(t['c']) for t in terms};total=0*g
    for b in range(dz,-1,-1):
        coefficient=0*g
        for a in range(dg,-1,-1):coefficient=coefficient*g+d.get((a,b),0)
        total=total*z+coefficient
    return total

def run():
    if not __debug__:raise RuntimeError('Run without -O')
    start=time.time();data=json.loads((ROOT/'data'/'polynomials.json').read_text());center=json.loads((ROOT/'data'/'root_centers.json').read_text())
    assert center['precision_bits']==BITS
    cc=[Fraction(center['g']),Fraction(center['z'])];radius=Fraction(2)**center['box_radius_power_of_two']
    X=[I.bounds(t-radius,t+radius) for t in cc];C0=[I.point(t) for t in cc]
    assert X[0].lower()>4 and X[0].upper()<5
    leading_terms=[dict(g=t['g'],z=0,c=t['c']) for t in data['F_terms'] if t['z']==10]
    leading=evaluate_terms(leading_terms,X[0],X[1]);assert not leading.contains_zero()
    T={key:derivative_terms(data['F_terms'],*key) for key in [(0,0),(1,0),(0,1),(1,1),(0,2)]}
    def ev(key,xx):return evaluate_terms(T[key],xx[0],xx[1])
    def jac(xx):return [[ev((1,0),xx),ev((0,1),xx)],[ev((1,1),xx),ev((0,2),xx)]]
    m=[[a.midpoint() for a in row] for row in jac(C0)];det=m[0][0]*m[1][1]-m[0][1]*m[1][0];assert det!=0
    R=[[m[1][1]/det,-m[0][1]/det],[-m[1][0]/det,m[0][0]/det]];RI=[[I.point(a) for a in row] for row in R]
    JX=jac(X);E=[[I.point(int(i==j))-sum((RI[i][k]*JX[k][j] for k in range(2)),I.point(0)) for j in range(2)] for i in range(2)]
    contraction=max(sum(v.abs_upper() for v in row) for row in E);assert contraction<1
    f0=[ev((0,0),C0),ev((0,1),C0)]
    K=[C0[i]-sum((RI[i][j]*f0[j] for j in range(2)),I.point(0))+sum((E[i][j]*(X[j]-C0[j]) for j in range(2)),I.point(0)) for i in range(2)]
    assert all(k.strict_inside(x) for k,x in zip(K,X))
    fg=ev((1,0),X);fzz=ev((0,2),X);assert not fg.contains_zero()
    curvature=-fzz/fg;assert curvature.hi<0
    A=[[I.coerce(v) for v in row] for row in make_candidate(X[0],X[1])]
    growth,grad,cons,J,labels,pivots=value_and_jacobian(A,I.point(0),I.point(1))
    assert len(labels)==100 and len(ACTIVE)==23
    index={lab:i for i,lab in enumerate(labels)};active_indices=[index[lab] for lab in ACTIVE]
    inactive=[v for lab,v in zip(labels,cons) if lab not in ACTIVE];assert len(inactive)==77
    assert all(v.lo>0 for v in inactive) and all(p.lo>0 for p in pivots)
    assert all(pivots[-1].lo>p.hi for p in pivots[:-1])
    columns=[j for j in range(24) if j!=19] # A_51 coordinate after omitting A_11.
    JA=[J[i] for i in active_indices];M=[[JA[j][col] for j in range(23)] for col in columns]
    multipliers,checked_pivots=solve_interval(M,[-grad[col] for col in columns])
    assert all(v.lo>0 for v in multipliers)
    # The omitted stationarity equation follows by dotting with the exact
    # active-curve tangent, with A_51 component 1 and growth derivative 0.
    result=dict(status='PASS: strict LOCAL maximum',global_solution=False,
        arithmetic='512-bit dyadic outward-rounded intervals; integer arithmetic only',
        root_g_enclosure=X[0].decimal_bounds(68),root_z_enclosure=X[1].decimal_bounds(68),
        contraction_upper_fraction=str(contraction),contraction_less_than_1e_50=contraction<Fraction(1,10**50),
        krawczyk_g=K[0].decimal_bounds(100),krawczyk_z=K[1].decimal_bounds(100),
        Fg=fg.decimal_bounds(),Fzz=fzz.decimal_bounds(),F_leading_z_coefficient=leading.decimal_bounds(),curve_second_derivative=curvature.decimal_bounds(),
        inactive_count=77,inactive_slack_lower_bound=I.point(min(v.lower() for v in inactive)).decimal_bounds()[0],
        active_jacobian_rank=23,kkt_multipliers=[dict(constraint=list(lab),enclosure=v.decimal_bounds()) for lab,v in zip(ACTIVE,multipliers)],
        pivots=[p.decimal_bounds() for p in pivots],matrix=[[a.decimal_bounds() for a in row] for row in A],seconds=time.time()-start)
    (ROOT/'results'/'local_certificate.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    r=run();print(r['status']);print('alpha:',r['root_g_enclosure']);print('curvature:',r['curve_second_derivative']);print('Not a global proof.')
