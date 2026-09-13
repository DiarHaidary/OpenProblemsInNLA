from fractions import Fraction as F
from pathlib import Path
import math,json,itertools
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln

# Independent exact Gaussian-rational RPCholesky engine, no submission imports.
def z(a=0,b=0):return(F(a),F(b))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cj(a):return(a[0],-a[1])
def divreal(a,b):return(a[0]/b,a[1]/b)
def tr(A):
 assert all(A[i][i][1]==0 for i in range(len(A)))
 return sum((A[i][i][0] for i in range(len(A))),F(0))
def exact_case(spec,r):
 n=len(spec);v=list(range(1,n+1));vv=sum(x*x for x in v)
 Q=[[F(i==j)-F(2*v[i]*v[j],vv) for j in range(n)] for i in range(n)]
 phases=[z(1),z(0,1),z(F(3,5),F(4,5)),z(F(5,13),F(-12,13))]*3
 A=tuple(tuple(mul(mul(phases[i],cj(phases[j])),z(sum(Q[i][h]*spec[h]*Q[j][h] for h in range(n)))) for j in range(n)) for i in range(n))
 states={0:A};probs={0:F(1)};means=[];checks=0;tau=sum(spec[r:]);alltau=[sum(spec[k:]) for k in range(n+1)]
 e=[F(1)]+[F(0)]*n
 for lam in spec:
  for k in range(n,0,-1):e[k]+=lam*e[k-1]
 for k in range(n+1):
  assert sum(probs.values())==1
  means.append(sum(p*tr(states[s]) for s,p in probs.items()))
  for mask,p in probs.items():assert tr(states[mask])>=alltau[k]
  if k>r:
   m=k-r;M=F(math.factorial(k))*e[k]/(math.prod(alltau[:r])*tau**m)
   # Test every strict tail event threshold realized in the exact distribution.
   thresholds=set(tr(states[s])/tau for s in probs)
   for threshold in thresholds:
    if threshold:
     bad=sum(p for s,p in probs.items() if tr(states[s])>threshold*tau)
     assert bad*threshold**m<=M;checks+=1
  if k==n:break
  nxt={}
  for mask,p in probs.items():
   R=states[mask];T=tr(R);conditional=F(0)
   if T==0:nxt[mask]=nxt.get(mask,F(0))+p;continue
   for j in range(n):
    d=R[j][j][0]
    if d==0:continue
    B=tuple(tuple(sub(R[i][h],divreal(mul(R[i][j],R[j][h]),d)) for h in range(n)) for i in range(n))
    target=mask|(1<<j)
    if target in states:assert states[target]==B
    else:states[target]=B
    nxt[target]=nxt.get(target,F(0))+p*d/T
    conditional+=d/T*tr(B);checks+=1
   frob=sum(a*a+b*b for row in R for a,b in row)
   assert conditional==T-frob/T
  probs=nxt
 warm=min(n,3*r+1)
 assert means[warm]<=F(8,5)*tau
 return {'n':n,'r':r,'complex':True,'all_threshold_events_and_transitions':checks,'warm_start_ratio':str(means[warm]/tau),'exact_means':list(map(str,means))}
ra01=[exact_case([F(31),F(1),F(1,2),F(1,4),F(1,8)],1),exact_case([F(17),F(3)]+[F(1,2**i) for i in range(6)],2)]

# Independent cross-factor adaptive transcript test, with an algorithm that uses
# every earlier factor response to choose next factor/direction.
rng=np.random.default_rng(913235);d,t,k,trials=8,2,3,12000
res=[];known=[]
for trial in range(trials):
 G=rng.normal(size=(k,d,d));W=np.einsum('kji,kjl->kil',G,G)
 U=[[] for _ in range(k)];Y=[[] for _ in range(k)];history=[];counts=[0]*k
 for step in range(k*t):
  eligible=[i for i in range(k) if counts[i]<t]
  chosen=eligible[0] if not history else eligible[int(abs(history[-1].sum())*100)%len(eligible)]
  v=np.eye(d)[0] if not history else np.sin(sum(history))+np.cos(history[-1]*2)
  if U[chosen]:
   V=np.column_stack(U[chosen]);v=v-V@(V.T@v);v=v-V@(V.T@v)
  assert np.linalg.norm(v)>1e-10
  v=v/np.linalg.norm(v);response=W[chosen]@v
  U[chosen].append(v);Y[chosen].append(response);history.append(response);counts[chosen]+=1
 a=[];x=[]
 for i in range(k):
  uu=np.column_stack(U[i]);yy=np.column_stack(Y[i]);aa=np.trace(np.linalg.solve(uu.T@yy,yy.T@yy))
  a.append(aa);x.append(np.trace(W[i])-aa)
 known.append(a);res.append(x)
res=np.array(res);known=np.array(known);nu=(d-t)**2
assert np.all(abs(res.mean(axis=0)/nu-1)<.04)
assert np.all(abs(res.var(axis=0)/(2*nu)-1)<.08)
assert np.max(abs(np.corrcoef(res,rowvar=False)-np.eye(k)))<.04
binned=[]
for i in range(k):
 cuts=np.quantile(known.sum(axis=1),[0,.25,.5,.75,1])
 vals=[float(res[(known.sum(axis=1)>=cuts[j])&(known.sum(axis=1)<=cuts[j+1]),i].mean()) for j in range(4)]
 assert all(abs(val/nu-1)<.05 for val in vals)
 binned.append(vals)
# Analytic numerical quadrature of shifted log-chi-square variance bound at
# degrees of freedom and shifts not covered by the supplied suite.
variances=[]
for nu2 in [2,3,9,36]:
 for aa in [0.,.1,10.,1000.]:
  def pdf(x):return math.exp((nu2/2-1)*math.log(x)-x/2-nu2/2*math.log(2)-gammaln(nu2/2)) if x>0 else 0
  mean=quad(lambda x:math.log(aa+x)*pdf(x),0,np.inf,epsabs=1e-10)[0]
  var=quad(lambda x:(math.log(aa+x)-mean)**2*pdf(x),0,np.inf,epsabs=1e-10)[0]
  bound=2*nu2/(aa+nu2+2)**2
  assert var>=bound*(1-1e-7)
  variances.append({'df':nu2,'shift':aa,'variance':var,'lower_bound':bound})
ra11={'seed':913235,'cross_factor_adaptive_trials':trials,'dimension':d,'queries_per_factor':t,'factors':k,'predicted_df':nu,'residual_means':res.mean(axis=0).tolist(),'residual_variances':res.var(axis=0).tolist(),'cross_factor_residual_correlation':np.corrcoef(res,rowvar=False).tolist(),'known_trace_quartile_conditional_means':binned,'shifted_log_variance_quadrature':variances,'limitation':'Monte Carlo and quadrature diagnostics support but do not prove universal conditional independence or inequalities.'}
Path('/private/tmp/nla-237-adversarial.json').write_text(json.dumps({'pass':True,'cases':ra01},indent=2)+'\n')
Path('/private/tmp/nla-235-adversarial.json').write_text(json.dumps({'pass':True,**ra11},indent=2)+'\n')
print(json.dumps({'pass':True,'ra01_exact_cases':[(x['n'],x['r'],x['all_threshold_events_and_transitions']) for x in ra01],'ra11_residual_means':ra11['residual_means'],'ra11_residual_variances':ra11['residual_variances']}))
