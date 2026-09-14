#!/usr/bin/env python3
"""Exact arithmetic audit of the all-odd-order polygon formulas.

The general result is proved in REPORT.pdf. These finite exact algebra checks
supplement, rather than replace, that proof; no floating-point inequality is used.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,sys,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from rational_quadrature import require


def audit_order(p):
    require(isinstance(p,int) and p>=3 and p%2==1,'p must be odd and >=3')
    lam=[(-1)**j*(1-F(2*j,p)) for j in range(p)]
    require(lam[0]==1 and all(-1<=x<=1 for x in lam),'Invalid compressed optimizer')
    sums=[lam[j]+lam[(j+1)%p] for j in range(p)]
    require(all(sums[j]==(-1)**j*F(2,p) for j in range(p)),'Cyclic sum identity failed')
    require(sum(((-1)**j*sums[j] for j in range(p)),F(0))==2,'Odd telescoping failed')
    require(all(lam[j]==lam[p-j] for j in range(1,p)),'Real-circulant symmetry failed')
    # Angles represented as rational multiples of gamma=pi/(2p).
    angles=[0]+[(p-j if j%2 else j) for j in range(1,p)]
    require(angles[1]==angles[-1]==p-1,'Endpoint angles failed')
    require(all(0<=t<=p for t in angles),'Angle range failed')
    require(all(angles[j]+angles[j+1]==p+(-1)**(j+1) for j in range(1,p-1)),
            'Internal equioscillation angles failed')
    alt=[(-1)**(j+1) for j in range(1,p-1)]
    coefficients=[0]*p
    for j,sign in zip(range(1,p-1),alt):
        coefficients[j]+=sign;coefficients[j+1]+=sign
    require(coefficients[1]==coefficients[-1]==1 and all(x==0 for x in coefficients[2:-1]),
            'Endpoint telescoping coefficients failed')
    require(sum(alt)==1 and len(alt)==p-2,'Angle inequality count failed')
    # For the compressed optimizer, A-B=1/(sqrt(q+p)+sqrt(q)), q>=0.
    for j in range(1,p-1):
        q=j*(p-j-1);aa=(p-j)*(j+1)
        require(q>=0 and aa==q+p,'Internal square-root difference identity failed')
    require((1+lam[1])/2==F(1,p) and (1+lam[-1])/2==F(1,p),'Endpoint norm squares failed')
    return {'p':p,'compressed_norm_over_R':str(F(2,p)),
            'completed_norm_squared_over_R_squared':str(F(4,p))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path);parser.add_argument('--max-order',type=int,default=1001)
    a=parser.parse_args();require(3<=a.max_order<=10001,'Invalid maximum audit order')
    start=time.perf_counter();rows=[audit_order(p) for p in range(3,a.max_order+1,2)]
    out={'status':'PASS','arithmetic':'integers and fractions only','orders_checked':len(rows),
         'first_order':rows[0],'last_order':rows[-1],'seconds':time.perf_counter()-start,
         'scope':'Exact formula checks; general completion proof is in the report'}
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,ArithmeticError,OSError) as exc:
        print('VERIFICATION FAILED: '+str(exc),file=sys.stderr);raise SystemExit(1)
