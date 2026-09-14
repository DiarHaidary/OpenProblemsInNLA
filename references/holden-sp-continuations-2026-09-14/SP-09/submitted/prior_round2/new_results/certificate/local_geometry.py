"""Exact geometry used by the local-openness argument, over Q(s), s^2=-3."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json,sys
import numpy as np
PRIOR=Path(__file__).resolve().parents[2]/'prior'/'certificate'
sys.path.insert(0,str(PRIOR))
from verify_certificate import require,words,normal_word,mm,load_matrix
from verify_witness_and_rigidity import zero,ident,scale_pair,add_pair,trace_pair,exact_rank

def sub(A,B):return A[0]-B[0],A[1]-B[1]
def comm(A,B):return sub(mm(A,B),mm(B,A))
def real(A):return A,zero(len(A),A.shape[1])
def weighted_star(A,W,Wi):return Wi@A[0].T@W,-Wi@A[1].T@W

def model():
 w=[F(5,8),F(1,4),F(1,8)];I=ident(3);W=zero(3);Wi=zero(3)
 for i in range(3):W[i,i]=w[i];Wi[i,i]=1/w[i]
 R=np.array([[F(i==j)-2*w[j] for j in range(3)] for i in range(3)],dtype=object)
 P1=zero(3);P1[0,0]=F(1);P2=zero(3);P2[1,1]=F(1)
 Ps=[P1,P2,R@P1@R,R@P2@R]
 ar=zero(3);ai=zero(3)
 for j,(x,y) in enumerate([(1,0),(F(4,13),F(5,13)),(F(-1,13),F(2,13))]):ar[j,j]=F(x);ai[j,j]=F(y)
 A=ar,ai;C=R@ar@R,R@ai@R;D=add_pair(A,C);Ds=weighted_star(D,W,Wi);H=mm(Ds,D)
 E=scale_pair(add_pair(scale_pair(H,(13,0)),(-4*I,zero(3))),(F(1,23),0))
 h1=add_pair(scale_pair(H,(-1,0)),(F(27,13)*I,zero(3)))
 h2=add_pair(scale_pair(mm(D,Ds),(-1,0)),(F(27,13)*I,zero(3)))
 return dict(w=w,I=I,W=W,Wi=Wi,R=R,Ps=Ps,A=A,C=C,D=D,E=E,h1=h1,h2=h2)

def directions(m):
 w=m['w'];ans=[]
 for i in range(3):
  X=zero(3);X[i,i]=F(1);ans.append((zero(3),X))
 for i in range(3):
  for j in range(i+1,3):
   X=zero(3);X[i,j]=w[j];X[j,i]=-w[i];ans.append((X,zero(3)))
 for i in range(3):
  for j in range(i+1,3):
   X=zero(3);X[i,j]=w[j];X[j,i]=w[i];ans.append((zero(3),X))
 for X in ans:require(np.array_equal(add_pair(X,weighted_star(X,m['W'],m['Wi']))[0],zero(3)) and np.array_equal(add_pair(X,weighted_star(X,m['W'],m['Wi']))[1],zero(3)))
 return ans

def evaluate(w,Ps):
 X=ident(3)
 for i in w:X=X@Ps[i]
 return X

def moment_keys():
 cyclic=set()
 for u in words(4):
  for v in words(4):
   w=normal_word(u[::-1]+v,True)
   if w is not None:cyclic.add(w)
 keys=[((),'r')]
 for w in sorted(cyclic):
  if len(w)<=1:continue
  wr=normal_word(w[::-1],True)
  if w>wr:continue
  keys.append((w,'r'))
  if w!=wr:keys.append((w,'s'))
 require(len(keys)==109)
 return keys

def geometry_checks(certificate:Path|None=None):
 c=json.loads((certificate or PRIOR/'krause_certificate.json').read_text());m=model();Xlist=directions(m);E=m['E'];D=m['D'];Ds=weighted_star(D,m['W'],m['Wi']);face=[]
 for X in Xlist:
  dD=comm(X,m['C']);dDs=weighted_star(dD,m['W'],m['Wi']);dH=add_pair(mm(Ds,dD),mm(dDs,D));F0=mm(mm(E,dH),E);face.append(np.r_[F0[0].ravel(),F0[1].ravel()])
 face=np.column_stack(face);face_rank=exact_rank(face);require(face_rank==3,'The active-face tangent map does not have rank three.')
 # Explicit unique KKT density: eigenvalues 5/28 and 23/28 on the
 # two-dimensional top singular space. This avoids numerical positivity.
 Pv=real((m['I']-m['R'])/2);Etail=sub(E,Pv)
 for J in (E,Pv,Etail):
  require(np.array_equal(sub(mm(J,J),J)[0],zero(3)) and np.array_equal(sub(mm(J,J),J)[1],zero(3)))
  require(np.array_equal(sub(weighted_star(J,m['W'],m['Wi']),J)[0],zero(3)) and np.array_equal(sub(weighted_star(J,m['W'],m['Wi']),J)[1],zero(3)))
 require(trace_pair(Pv)==(1,0) and trace_pair(Etail)==(1,0))
 require(np.array_equal(mm(Pv,Etail)[0],zero(3)) and np.array_equal(mm(Pv,Etail)[1],zero(3)))
 rho=add_pair(scale_pair(Pv,(F(5,28),0)),scale_pair(Etail,(F(23,28),0)))
 require(trace_pair(rho)==(1,0))
 for X in Xlist:
  dD=comm(X,m['C']);dH=add_pair(mm(Ds,dD),mm(weighted_star(dD,m['W'],m['Wi']),D))
  require(trace_pair(mm(rho,dH))==(0,0),'The exact KKT density is not stationary.')
 keys=moment_keys();moment=zero(len(keys),len(Xlist))
 for row,(w,typ) in enumerate(keys):
  if not w:continue
  G=zero(3)
  for j,letter in enumerate(w):
   if letter<2:continue
   rest=w[j+1:]+w[:j];T=evaluate(rest,m['Ps']);Q=m['Ps'][letter];G+=Q@T-T@Q
  for col,X in enumerate(Xlist):
   z=trace_pair(mm(X,real(G)));moment[row,col]=z[0 if typ=='r' else 1]/3
 moment_rank=exact_rank(moment);joint_rank=exact_rank(np.concatenate([moment,face],axis=0))
 require(moment_rank==4,'The tracial moment map does not have rank four.')
 require(joint_rank==4,'The active-face tangent map does not factor through the four orbit directions.')
 # A nongauge tangent with zero compressed singular-value derivative.
 tangent=np.array([F(0),F(0),F(0),F(-3,5),F(2,5),F(1),F(0),F(0),F(0)],dtype=object)
 require(all(x==0 for x in face@tangent),'The explicit tangent leaves the active face.')
 mdot=moment@tangent
 require(mdot[keys.index(((0,2),'r'))]==F(-1,48),'The explicit tangent has an incorrect nonzero moment derivative.')
 require(mdot[0]==0)
 B,L=words(4),words(3);EL=np.column_stack([evaluate(w,m['Ps']).ravel() for w in L]);require(exact_rank(EL)==9)
 qr=[F(int(x),388) for x in c['q_real']];qi=[F(int(x),388) for x in c['q_s']]
 require(all(x==0 for x in qr[5:]+qi[5:]),'The distinguished q is not degree one.')
 q=(sum((x*evaluate(w,m['Ps']) for x,w in zip(qr,L)),zero(3)),sum((x*evaluate(w,m['Ps']) for x,w in zip(qi,L)),zero(3)))
 require(trace_pair(q)==(3,0),'The distinguished q does not have normalized model trace one.')
 require(qr[0]+sum(qr[1:5])/3==1 and qi[0]+sum(qi[1:5])/3==0,'The degree-one trace is not universally one.')
 hq=mm(m['h1'],q);require(np.array_equal(hq[0],zero(3)) and np.array_equal(hq[1],zero(3)),'The distinguished q is not in the right local kernel.')
 for j,h in [(1,m['h1']),(2,m['h2'])]:
  K=(load_matrix(c['blocks'][j]['kernel_real']),load_matrix(c['blocks'][j]['kernel_s']))
  require(np.array_equal(K[0][3:,:],4992*ident(26)) and np.array_equal(K[1][3:,:],zero(26)))
  values=(EL@K[0],EL@K[1])
  for col in range(26):
   Z=mm(h,(values[0][:,col].reshape(3,3),values[1][:,col].reshape(3,3)))
   require(np.array_equal(Z[0],zero(3)) and np.array_equal(Z[1],zero(3)),f'Local kernel block {j} fails.')
  # First three word images span the rank-three left multiplication range.
  hs=[mm(h,real(evaluate(w,m['Ps']))) for w in L[:3]]
  T=np.column_stack([np.r_[z[0].ravel(),z[1].ravel()] for z in hs])
  require(exact_rank(T)==3,'First three local images are not independent over R.')
  # Their complex independence is checked by including s multiples.
  TC=np.column_stack([np.r_[z[0].ravel(),z[1].ravel()] for z in hs]+[np.r_[(-3*z[1]).ravel(),z[0].ravel()] for z in hs])
  require(exact_rank(TC)==6,'First three local images are not independent over Q(s).')
 print('PASS: active-face tangent rank = 3; tracial moment tangent rank = 4; joint rank = 4.')
 print('PASS: the unique KKT density has positive eigenvalues 5/28 and 23/28; an explicit nongauge flat tangent is verified.')
 print('PASS: both local kernels have full complex dimension 26; degree-one local evaluation rank = 3.')
 return {'result':'PASS','active_face_tangent_rank':face_rank,'moment_tangent_rank':moment_rank,'joint_tangent_rank':joint_rank,'local_kernel_dimensions':[26,26],'degree_one_local_complex_rank':3,'coefficient_space_real_dimension':109,'unique_KKT_density_eigenvalues':['5/28','23/28'],'explicit_flat_tangent_coefficients':[str(x) for x in tangent],'flat_tangent_P1Q1_trace_derivative':'-1/48'}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--json-report',type=Path);a=p.parse_args();r=geometry_checks()
 if a.json_report:a.json_report.write_text(json.dumps(r,indent=2)+'\n')
