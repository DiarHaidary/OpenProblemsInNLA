"""Exact dyadic contraction certificates for the SP-03 polynomial system.
The verifier uses integer arithmetic for every proof inequality.  NumPy is only
used to store data and (in certificate generation) propose approximate inverses.
A successful certificate proves distinct simple zeros, NOT completeness.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction
import numpy as np
import json,sys,time
BASE=Path(__file__).resolve().parent

def dyadic(z, exponent=None):
    z=np.asarray(z,dtype=np.complex128)
    rs=[float(v).as_integer_ratio() for v in z.real.ravel()]
    ims=[float(v).as_integer_ratio() for v in z.imag.ravel()]
    ee=max([b.bit_length()-1 for a,b in rs+ims],default=0)
    if exponent is None:exponent=ee
    if exponent<ee:raise ValueError('Insufficient common binary exponent')
    rr=np.asarray([a << (exponent-(b.bit_length()-1)) for a,b in rs],dtype=object).reshape(z.shape)
    ii=np.asarray([a << (exponent-(b.bit_length()-1)) for a,b in ims],dtype=object).reshape(z.shape)
    return rr,ii,exponent

def cdot(ar,ai,br,bi):return ar@br-ai@bi,ar@bi+ai@br

def exact_system(x,u,n):
    both=np.concatenate([x.ravel(),u.ravel()]);rr,ii,e=dyadic(both)
    m=n//2;xr=rr[:n*n].reshape(n,n);xi=ii[:n*n].reshape(n,n)
    ur=rr[n*n:].reshape(n,n);ui=ii[n*n:].reshape(n,n)
    jr=np.concatenate([xr[m:],-xr[:m]],axis=0);ji=np.concatenate([xi[m:],-xi[:m]],axis=0)
    kr=np.concatenate([-xr[:,m:],xr[:,:m]],axis=1);ki=np.concatenate([-xi[:,m:],xi[:,:m]],axis=1)
    cr,ci=cdot(xr.T,xi.T,jr,ji)
    vr,vi=cdot((ur-xr).T,(ui-xi).T,kr,ki)
    fr=np.empty(n*n,dtype=object);fi=np.empty_like(fr)
    ar=np.zeros((n*n,n*n),dtype=object);ai=np.zeros_like(ar);row=0
    for i in range(n):
        for j in range(i+1,n):
            fr[row]=cr[i,j]-(1<<(2*e) if i<m and j==i+m else 0);fi[row]=ci[i,j]
            for a in range(n):
                ar[row,a*n+i]+=jr[a,j];ai[row,a*n+i]+=ji[a,j]
                ar[row,a*n+j]-=jr[a,i];ai[row,a*n+j]-=ji[a,i]
            row+=1
    for i in range(n):
        for j in range(i,n):
            fr[row]=vr[i,j]+vr[j,i];fi[row]=vi[i,j]+vi[j,i]
            bj=j+m if j<m else j-m;bi=i+m if i<m else i-m
            sj=-1 if j<m else 1;si=-1 if i<m else 1
            for a in range(n):
                ar[row,a*n+i]-=kr[a,j];ai[row,a*n+i]-=ki[a,j]
                ar[row,a*n+j]-=kr[a,i];ai[row,a*n+j]-=ki[a,i]
                ar[row,a*n+bj]+=sj*(ur[a,i]-xr[a,i]);ai[row,a*n+bj]+=sj*(ui[a,i]-xi[a,i])
                ar[row,a*n+bi]+=si*(ur[a,j]-xr[a,j]);ai[row,a*n+bi]+=si*(ui[a,j]-xi[a,j])
            row+=1
    return fr,fi,ar,ai,e

def pow2(e):return Fraction(1<<e,1) if e>=0 else Fraction(1,1<<(-e))

def check_one(x,u,Y,n):
    fr,fi,ar,ai,e=exact_system(x,u,n);yr,yi,ey=dyadic(Y)
    er,ei=cdot(yr,yi,fr,fi)
    eta=Fraction(int(max(abs(er)+abs(ei))),1<<(ey+2*e))
    br,bi=cdot(yr,yi,ar,ai)
    for j in range(n*n):br[j,j]-=1<<(e+ey)
    z0=Fraction(int(max(np.sum(abs(br)+abs(bi),axis=1))),1<<(e+ey))
    yn=Fraction(int(max(np.sum(abs(yr)+abs(yi),axis=1))),1<<ey)
    z2=4*n*yn
    r=pow2(eta.numerator.bit_length()-eta.denominator.bit_length()+3) if eta else pow2(-80)
    contraction=z0+z2*r
    inclusion=eta+z0*r+z2*r*r/2
    ok=contraction<1 and inclusion<r
    return ok,r,eta,z0,z2

def disjoint(roots,radii):
    if len(roots)<2:return True,None
    rr,ii,e=dyadic(roots);ints=np.concatenate([rr,ii],axis=1)
    vals=np.concatenate([roots.real,roots.imag],axis=1)
    bound=2*max(radii)*(1<<e);best=None
    for i in range(len(roots)):
        for j in range(i):
            ix=int(np.argmax(abs(vals[i]-vals[j])))
            gap=abs(int(ints[i,ix]-ints[j,ix]))
            if gap*bound.denominator<=bound.numerator:return False,(i,j)
            if best is None or gap<best:best=gap
    return True,float(Fraction(best,1<<e))

def verify(path):
    path=Path(path);z=np.load(path,allow_pickle=False);roots=z['roots'];Y=z['inverses'];U=z['U']
    if roots.ndim!=2 or not len(roots):raise ValueError('Expected a nonempty matrix of centers')
    n=int(round(np.sqrt(roots.shape[1])))
    if n<2 or n%2 or n*n!=roots.shape[1]:raise ValueError('Centers must represent even square matrices')
    if U.size!=n*n or Y.shape!=(len(roots),n*n,n*n):raise ValueError('Inconsistent certificate shapes')
    if not all(v.dtype==np.dtype('complex128') for v in (roots,Y,U)):raise ValueError('Certificates must use complex binary64 arrays')
    if not all(np.isfinite(v).all() for v in (roots,Y,U)):raise ValueError('Nonfinite certificate entries')
    U=U.ravel()
    radii=[];eta=[];z0=[];z2=[];start=time.time()
    for i in range(len(roots)):
        ok,r,a,b,c=check_one(roots[i],U,Y[i],n)
        if not ok:raise AssertionError(f'Contraction certificate {i} failed')
        radii.append(r);eta.append(float(a));z0.append(float(b));z2.append(float(c))
    separated,gap=disjoint(roots,radii)
    if not separated:raise AssertionError(f'Non-disjoint certified balls: {gap}')
    report=dict(m=n//2,certified_distinct_simple_roots=len(roots),completeness_proved=False,arithmetic='exact Python integers and fractions',maximum_radius=float(max(radii)),maximum_eta=max(eta),maximum_z0=max(z0),maximum_z2=max(z2),minimum_selected_coordinate_separation=gap,verification_seconds=time.time()-start)
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Verify exact dyadic existence, simplicity, and distinctness certificates. This is not a completeness test.')
    parser.add_argument('files',nargs='+',type=Path)
    parser.add_argument('--out',type=Path,help='Optional JSON summary destination')
    args=parser.parse_args()
    results=[]
    for file in args.files:
        result=verify(file)
        result['certificate_file']=file.name
        results.append(result)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(results,indent=2)+'\n')
