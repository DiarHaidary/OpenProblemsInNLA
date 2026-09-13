"""Numerical Newton continuation in the confluent determinant regularization.

Convergence flags are numerical stopping tests, not exact certificates.
No termination or existence guarantee for arbitrary target nodes is claimed.
"""
from __future__ import annotations
import sys,time,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'cluster'))
from confluent import seed,complete_homogeneous
from math import factorial,comb
import mpmath as mp

def pencil_matrices(c):
 n=len(c);z=[1-t for t in c];T=mp.zeros(n);Bs=[mp.zeros(n) for _ in range(n)]
 for k in range(n):
  h=complete_homogeneous(z[:k+1],2*n)
  def hh(m):return h[m] if m>=0 else mp.mpf(0)
  for j in range(1,n+1):
   T[k,j-1]=-j*hh(j-1-k)
   for r in range(n):Bs[r][k,j-1]=-(r+1)*(hh(r+j-k)-hh(r-k))
 Ti=T**-1
 return [Ti*b for b in Bs]

def FJ(a,Bs,withJ=True):
 n=len(a);I=mp.eye(n);K=mp.zeros(n)
 for j in range(n):K+=a[j]*Bs[j]
 Q=I;F=mp.zeros(n,1);J=mp.zeros(n)
 for k in range(1,n+1):
  if withJ:
   for r in range(n):J[k-1,r]=-sum(Q[i,j]*Bs[r][j,i] for i in range(n) for j in range(n))
  KQ=K*Q;f=-sum(KQ[i,i] for i in range(n))/k;F[k-1]=f-(-1)**k*comb(n,k)
  Q=KQ+f*I
 return F,J

def values(c,a):
 return [sum(-(j+1)*a[j]*(1-t)**j for j in range(len(a))) for t in c]

def newton(c,a,tol=None):
 n=len(a);Bs=pencil_matrices(c);a=mp.matrix(a);tol=tol or mp.mpf(10)**(-mp.mp.dps//2)
 for it in range(25):
  F,J=FJ(a,Bs);err=max(abs(t) for t in F)
  if err<tol:return a,it,err
  da=mp.lu_solve(J,-F);r=mp.mpf(1)
  for ls in range(20):
   aa=a+r*da
   if min(values(c,aa))>0:
    FF,_=FJ(aa,Bs,False)
    if max(abs(t) for t in FF)<err:break
   r/=2
  else:raise ValueError('line search failed')
  a=aa
 raise ValueError('Newton iteration limit')

def continuation(c,verbose=False):
 if len(c)<2 or any(not mp.isfinite(t) or t<=0 for t in c):
  raise ValueError('at least two finite positive nodes required')
 if any(x>=y for x,y in zip(c,c[1:])) or c[-1]>1:
  raise ValueError('nodes must be strictly increasing and at most one')
 n=len(c);a=mp.matrix(seed(n));s=mp.mpf(0);ds=mp.mpf('.05');steps=[]
 while s<1:
  sn=min(1,s+ds);cc=[1-sn*(1-t) for t in c]
  try:
   aa,it,err=newton(cc,a)
   if min(values(cc,aa))<=0:raise ValueError('not positive')
  except (ValueError,ZeroDivisionError) as ex:
   ds/=2
   if verbose:print('reject',mp.nstr(sn,6),str(ex),flush=True)
   if ds<mp.mpf('1e-7'):return {'pass':False,'at':str(s),'error':str(ex),'a':[str(t) for t in a]}
   continue
  a=aa;s=sn;steps.append({'s':str(s),'iterations':it,'residual':str(err)})
  if verbose:print('accepted',n,mp.nstr(s,5),it,mp.nstr(err,3),flush=True)
  ds=min(mp.mpf('.2'),ds*mp.mpf('1.5'))
 d=[1/t for t in values(c,a)]
 return {'pass':True,'scope':'Numerical stopping tests only; not an exact certificate.','nodes':[str(t) for t in c],'a':[str(t) for t in a],'d':[str(t) for t in d],'steps':steps}

def main():
 import argparse
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--stages',type=int,default=8)
 ap.add_argument('--dps',type=int,default=60)
 ap.add_argument('--out',type=Path)
 args=ap.parse_args()
 if args.stages<2 or args.dps<40:ap.error('use at least two stages and 40 decimal digits')
 mp.mp.dps=args.dps;n=args.stages
 c=[mp.mpf(i)/n for i in range(1,n+1)]
 t=time.time();out=continuation(c,True);out['seconds']=time.time()-t
 print(json.dumps(out,indent=2),flush=True)
 if args.out:
  args.out.parent.mkdir(parents=True,exist_ok=True)
  args.out.write_text(json.dumps(out,indent=2)+'\n')
 if not out['pass']:raise SystemExit(1)
if __name__=='__main__':main()
