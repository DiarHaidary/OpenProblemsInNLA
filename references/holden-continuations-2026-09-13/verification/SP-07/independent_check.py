import json,itertools,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
p=Path(sys.argv[1])
d=json.loads(p.read_text()); z=[(F(x),F(y)) for x,y in d['z']]; n=len(z); X=[[F(x) for x in row] for row in d['X']];r=len(X[0])
def tr(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def inverse(A):
 R=[a+b for a,b in zip(A,eye(len(A)))]; m=len(A)
 for j in range(m):
  k=next(k for k in range(j,m) if R[k][j]); R[k],R[j]=R[j],R[k]
  v=R[j][j];R[j]=[a/v for a in R[j]]
  for k in range(m):
   if k!=j:
    v=R[k][j];R[k]=[a-v*b for a,b in zip(R[k],R[j])]
 return [row[m:] for row in R]
Y=eye(r)+X;P=mm(mm(Y,inverse(mm(tr(Y),Y))),tr(Y));S=[[F(i==j)-2*P[i][j] for j in range(n)] for i in range(n)]
assert mm(tr(S),S)==eye(n)
D=[[[z[i][part]*F(i==j) for j in range(n)] for i in range(n)] for part in range(2)]
M=[[[D[k][i][j]+mm(mm(S,D[k]),S)[i][j] for j in range(n)] for i in range(n)] for k in range(2)]
# Independent realification of the full complex matrix; use Schur elimination
# on t^2 I - R(M)^T R(M), avoiding Gaussian-complex LDL code in package.
R=[M[0][i]+[-a for a in M[1][i]] for i in range(n)]+[M[1][i]+M[0][i] for i in range(n)]
G=mm(tr(R),R);t=F(d['norm_upper_bound']);q=F(d['ratio_lower_bound'])
H=[[t*t*F(i==j)-G[i][j] for j in range(2*n)] for i in range(2*n)];piv=[]
while H:
 v=H[0][0];assert v>0;piv.append(str(v))
 H=[[H[i][j]-H[i][0]*H[0][j]/v for j in range(1,len(H))] for i in range(1,len(H))]
cost=[[(x+u)**2+(y+v)**2 for u,v in z] for x,y in z]
best=min(max(cost[i][j] for i,j in enumerate(pi)) for pi in itertools.permutations(range(n)))
assert best>q*q*t*t
out={'status':'PASS','method':'independent Fraction realification, positive Schur pivots, exhaustive 5040 matchings','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'squared_matching':str(best),'positive_real_gram_pivots':len(piv),'strict_ratio_lower_bound':str(q),'strict_norm_upper_bound':str(t)}
Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
