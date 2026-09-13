#!/usr/bin/env python3
"""Propose point and uniform local certificates; verify.py checks them independently."""
import json,sys,math
from pathlib import Path
from fractions import Fraction
import mpmath as mp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from verify import verify
sys.path.insert(0,str(HERE.parent/'prior_work'/'src'))
from ie28 import inverse_similar,determinant_coefficients,refine_ansatz
mp.mp.dps=120

def m(s):
 q=Fraction(s);return mp.mpf(q.numerator)/q.denominator

def propose(e):
 n=len(e['nodes'])
 cc=([Fraction(i,n) for i in range(1,n+1)] if 'equally spaced' in e['label']
      else list(map(Fraction,e['nodes'])))
 c=list(map(m,cc))
 sol=refine_ansatz(c,e['alphas'],dps=100,maxiter=100)
 d=sol['diagonal'];M=inverse_similar(c);L=M*mp.diag(d);I=mp.eye(n);P=I;J=mp.zeros(n)
 ee=determinant_coefficients(L)
 for k in range(1,n+1):
  PM=P*M
  for i in range(n):J[k-1,i]=PM[i,i]
  P=ee[k]*I-L*P
 R=J**-1
 data={'label':e['label'],'precision_bits':320,'node_box':[[str(z),str(z)] for z in cc],
       'center':[mp.nstr(z,75) for z in d], 'radius':'1e-30',
       'preconditioner':[[mp.nstr(R[i,j],75) for j in range(n)] for i in range(n)],
       'claim':'For every node vector in node_box there is one and only one solution inside center +/- radius. No global uniqueness claim.'}
 assert verify(data,True)['passed']
 point=data.copy();point['label']+=' (point certificate)'
 # Try increasingly small node neighborhoods, then diagonal radii.
 best=None
 for power in range(3,25):
  delta=Fraction(1,10**power)
  box=[[str(z-delta),str(z+delta)] for z in cc[:-1]]+[[str(cc[-1]),str(cc[-1])]]
  if cc[0]-delta<=0 or any(cc[i]+2*delta>=cc[i+1] for i in range(n-1)):continue
  for rp in range(max(2,power-7),power):
   trial=data.copy();trial['node_box']=box;trial['radius']=str(Fraction(1,10**rp))
   try: ans=verify(trial)
   except ValueError: continue
   if ans['passed']:
    trial['node_center']=[str(z) for z in cc];trial['node_half_width']=str(delta)
    trial['label']+=' (uniform node neighborhood)'
    best=trial;verify(trial,True);break
  if best:break
 if best is None:raise RuntimeError('no neighborhood certified')
 return point,best

def main():
 import argparse
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--input',type=Path,default=HERE.parent/'prior_work'/'results'/'numerical_checks.json')
 ap.add_argument('--out-dir',type=Path,default=HERE)
 args=ap.parse_args();args.out_dir.mkdir(parents=True,exist_ok=True)
 old=json.loads(args.input.read_text());points=[];local=[]
 for e in old['examples']:
  if len(e['nodes'])<4:continue
  p,l=propose(e);points.append(p);local.append(l)
  (args.out_dir/'point_certificates.json').write_text(json.dumps(points,indent=2)+'\n')
  (args.out_dir/'neighborhood_certificates.json').write_text(json.dumps(local,indent=2)+'\n')
if __name__=='__main__':main()
