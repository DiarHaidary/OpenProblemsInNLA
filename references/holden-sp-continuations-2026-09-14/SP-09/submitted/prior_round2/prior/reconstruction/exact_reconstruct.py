"""Exact Q(sqrt(-3)) reconstruction of the Krause tracial certificate."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from fractions import Fraction as F
from math import lcm
import numpy as np
from moments import basis, canon, reduce
Z=(F(0),F(0)); O=(F(1),F(0))
def fc(x=0,y=0):return F(x),F(y)
def fa(a,b):return a[0]+b[0],a[1]+b[1]
def fn(a):return -a[0],-a[1]
def fs(a,b):return fa(a,fn(b))
def fm(a,b):return a[0]*b[0]-3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def fj(a):return a[0],-a[1]
def fi(a):
 d=a[0]*a[0]+3*a[1]*a[1]
 return a[0]/d,-a[1]/d

def mm(A,B):
 return [[sumf(fm(x,y) for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def sumf(vals):
 s=Z
 for v in vals:s=fa(s,v)
 return s

def eye(n):return [[O if i==j else Z for j in range(n)] for i in range(n)]
def ma(A,B):return [[fa(a,b) for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]
def mscale(A,c):return [[fm(a,c) for a in row] for row in A]
def kernel(M):
 M=[row.copy() for row in M];m=len(M);n=len(M[0]);piv=[];i=0
 for j in range(n):
  p=next((p for p in range(i,m) if M[p][j]!=Z),None)
  if p is None:continue
  M[i],M[p]=M[p],M[i];v=fi(M[i][j]);M[i]=[fm(v,a) for a in M[i]]
  for q in range(m):
   if q==i or M[q][j]==Z:continue
   v=M[q][j];M[q]=[fs(a,fm(v,b)) for a,b in zip(M[q],M[i])]
  piv.append(j);i+=1
  if i==m:break
 free=[j for j in range(n) if j not in piv]
 N=[[Z for _ in free] for _ in range(n)]
 for k,j in enumerate(free):
  N[j][k]=O
  for row,p in enumerate(piv):N[p][k]=fn(M[row][j])
 den=lcm(*(x.denominator for row in N for z in row for x in z))
 KR=np.array([[int(z[0]*den) for z in row] for row in N],dtype=np.int64)
 KI=np.array([[int(z[1]*den) for z in row] for row in N],dtype=np.int64)
 return KR,KI,den,free,piv

def exact_example():
 w=[F(5,8),F(1,4),F(1,8)]
 R=[[fc((1 if i==j else 0)-2*w[j]) for j in range(3)] for i in range(3)]
 P1=[[O if i==j==0 else Z for j in range(3)] for i in range(3)]
 P2=[[O if i==j==1 else Z for j in range(3)] for i in range(3)]
 Ps=[P1,P2,mm(mm(R,P1),R),mm(mm(R,P2),R)]
 D=mscale(eye(3),fc(F(-2,13),F(4,13)))
 for i in [0,2]:D=ma(D,mscale(Ps[i],fc(F(14,13),F(-2,13))))
 for i in [1,3]:D=ma(D,mscale(Ps[i],fc(F(5,13),F(3,13))))
 Dc=[[fj(z) for z in row] for row in D]
 h1=ma(mscale(eye(3),fc(F(27,13))),mscale(mm(Dc,D),fc(-1)))
 h2=ma(mscale(eye(3),fc(F(27,13))),mscale(mm(D,Dc),fc(-1)))
 return Ps,h1,h2

def exact_kernels():
 Ps,h1,h2=exact_example();Bs=[basis(4),basis(3),basis(3)];Ks=[]
 def ev(w):
  M=eye(3)
  for j in w:M=mm(M,Ps[j])
  return M
 W=[[ev(w) for w in bs] for bs in Bs]
 E0=[[M[i][j] for M in W[0]] for i in range(3) for j in range(3)]
 Es=[E0]
 for h,Ws in zip([h1,h2],W[1:]):
  row=next(r for r in h if any(x!=Z for x in r))
  Es.append([[sumf(fm(row[k],M[k][j]) for k in range(3)) for M in Ws] for j in range(3)])
 for E in Es:Ks.append(kernel(E))
 for i,(R,I,den,free,piv) in enumerate(Ks):print('K',i,R.shape,'den',den,'max',max(abs(R).max(),abs(I).max()),'pivots',piv,flush=True)
 return Ks

# Integer-pair polynomial arithmetic, with s^2=-3.
def imul(a,b):return a[0]*b[0]-3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def iadd(a,b):return a[0]+b[0],a[1]+b[1]
def iadj(p):return {w[::-1]:(a,-b) for w,(a,b) in p.items()}
def ipmul(p,q):
 out={}
 for u,a in p.items():
  for v,b in q.items():
   w=reduce(u+v)
   if w is not None:out[w]=iadd(out.get(w,(0,0)),imul(a,b))
 return out

def exact_moments():
 dp={():(-2,4),(0,):(14,-2),(1,):(5,3),(2,):(14,-2),(3,):(5,3)}
 h1={w:(-a,-b) for w,(a,b) in ipmul(iadj(dp),dp).items()};h1[()]=iadd(h1[()],(351,0))
 h2={w:(-a,-b) for w,(a,b) in ipmul(dp,iadj(dp)).items()};h2[()]=iadd(h2[()],(351,0))
 mats=[(basis(4),{():(169,0)}),(basis(3),h1),(basis(3),h2)]
 fixed={():3,(0,):1,(1,):1,(2,):1,(3,):1};keys={}
 for bs,p in mats:
  for u in bs:
   for v in bs:
    for w in p:
     c,sgn=canon(u[::-1]+w+v)
     if c is not None and c not in fixed:
      keys[(c,'r')]=0
      if reduce(c[::-1],True)!=c:keys[(c,'i')]=0
 keys={key:j+1 for j,key in enumerate(sorted(keys))};Fblocks=[]
 for bs,p in mats:
  TR=np.zeros((len(keys)+1,len(bs),len(bs)),dtype=np.int64);TI=TR.copy()
  for i,u in enumerate(bs):
   for j,v in enumerate(bs):
    for w,(a,b) in p.items():
     c,sgn=canon(u[::-1]+w+v)
     if c is None:continue
     if c in fixed:TR[0,i,j]+=a*fixed[c];TI[0,i,j]+=b*fixed[c]
     else:
      ix=keys[(c,'r')];TR[ix,i,j]+=3*a;TI[ix,i,j]+=3*b
      if (c,'i') in keys:
       ix=keys[(c,'i')];TR[ix,i,j]+=-9*b*sgn;TI[ix,i,j]+=3*a*sgn
  assert np.array_equal(TR,TR.transpose(0,2,1))
  assert np.array_equal(TI,-TI.transpose(0,2,1))
  Fblocks.append((TR,TI))
 return Fblocks,keys

def coordvec(R,I):
 n=len(R);i,j=np.triu_indices(n,1)
 return np.r_[R.diagonal(),2*R[i,j],6*I[i,j]]

def int_congruence(KR,KI,MR,MI):
 A=MR@KR-3*MI@KI;B=MR@KI+MI@KR
 return KR.T@A+3*KI.T@B,KR.T@B-KI.T@A

def build_exact_system():
 Ks=exact_kernels();Fs,keys=exact_moments();Cs=[]
 for (KR,KI,den,free,piv),(FR,FI) in zip(Ks,Fs):
  vals=[]
  for R,I in zip(FR,FI):
   RR,II=int_congruence(KR,KI,R,I)
   vals.append(coordvec(RR,II))
  Cs.append(np.array(vals,dtype=np.int64))
 C=np.concatenate(Cs,axis=1)
 qr=np.zeros((29,1),dtype=np.int64);qi=qr.copy();qr[:5,0]=[-114,372,381,372,381];qi[:5,0]=[-18,120,-93,120,-93]
 rhs=[]
 for R,I in zip(*Fs[1]):
  r,im=int_congruence(qr,qi,R,I);assert im[0,0]==0;rhs.append(-r[0,0])
 rhs=np.array(rhs,dtype=np.int64)
 print('system',C.shape,'max',abs(C).max(),'rhsmax',abs(rhs).max(),flush=True)
 out={'C':C,'rhs':rhs,'qr':qr,'qi':qi}
 for j,(R,I,den,free,piv) in enumerate(Ks):out.update({f'KR{j}':R,f'KI{j}':I,f'den{j}':den,f'free{j}':free})
 np.savez('exact_system.npz',**out)
 return out

if __name__=='__main__':build_exact_system()
