from pathlib import Path
from fractions import Fraction as F
import hashlib, json, difflib, itertools, sys, copy
import sympy as s
BASE=Path('/private/tmp/nla-review-253-256/pr254')
SRC=Path('/private/tmp/nla-audit-254/references/holden-continuations-2026-09-13')
checks={}
# Bind the five archives, all original TeX sources, auxiliary tables, and every publication payload.
rows=json.loads((SRC/'source-hashes.json').read_text()); diffs=[]
for r in rows:
 root=BASE/r['id']/r['original_root']; orig=root/r['source_tex']; pub=SRC/r['id']/'report.tex'
 assert hashlib.sha256((SRC/r['id']/'original.zip').read_bytes()).hexdigest()==r['archive_sha256']
 assert hashlib.sha256(orig.read_bytes()).hexdigest()==r['source_tex_sha256']
 diffs.extend(difflib.unified_diff(orig.read_text().splitlines(True),pub.read_text().splitlines(True),fromfile=r['id']+'/original',tofile=r['id']+'/publication'))
manifest=json.loads((SRC/'submission-hashes.json').read_text());actual={str(p.relative_to(SRC)) for p in SRC.rglob('*') if p.is_file() and p.name!='submission-hashes.json'}
assert set(manifest)==actual
for name,h in manifest.items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==h
(BASE/'publication-source-diffs.patch').write_text(''.join(diffs))
for ident,old,new in [('SP-07','paper/generated_data.tex','generated_data.tex'),('SP-14','results/validation_summary.tex','validation_summary.tex'),('SP-14','results/plateau_table.tex','plateau_table.tex')]:
 row=next(r for r in rows if r['id']==ident)
 # SP14 generated files may be regenerated in scratch; use original ZIP bytes.
 import zipfile
 with zipfile.ZipFile(SRC/ident/'original.zip') as z:assert z.read(row['original_root']+'/'+old)==(SRC/ident/new).read_bytes()
checks['archive_hashes']=5;checks['source_hashes']=5;checks['payload_hashes']=len(manifest);checks['auxiliary_tables']=3
# MI20's corrected conjugation: noncommuting rational matrices; no submitted model import.
C=s.Matrix([[3,1,0],[1,4,1],[0,1,3]]);R=s.Matrix([[2,0,1],[0,3,1],[1,1,4]])
U=s.diag(1,1,-1);S=C*C;Q=R*R
A=sum((V*S*V for V in [s.eye(3),U]),s.zeros(3))
B=sum((V*C*V*(V*Q*V)*V*C*V for V in [s.eye(3),U]),s.zeros(3))
expected=C*Q*C+U*C*Q*C*U
assert B==expected and A==S+U*S*U
bad=sum((V*C*V*Q*V*C*V for V in [s.eye(3),U]),s.zeros(3))
assert bad!=expected
checks['mi20_corrected_fourier_conjugation_exact']=True
checks['mi20_omitted_conjugation_negative_control']=True
# SP08: all 512 order-three sign arrays, including nonsymmetric minors selected from a symmetric larger matrix.
x=s.symbols('x'); nonsingular=0
for bits in itertools.product([-1,1],repeat=9):
 T=s.Matrix(3,3,bits);d=T.det()
 if d:
  assert abs(d)==4
  assert (T.T*T).charpoly(x).as_expr().expand()==((x-4)**2*(x-1)).expand()
  nonsingular+=1
checks['sp08_all_3x3_sign_arrays']=512;checks['sp08_nonsingular_minor_singular_values']=nonsingular
# Independent exact Toeplitz products, both boundary contributions, and Jacobi corner signs.
b={-3:s.Rational(2,7),-1:1,0:3,1:s.Rational(1,5),2:s.I/4}
c={-2:s.Rational(1,2),-1:s.I/3,0:2,1:s.Rational(-1,4),3:s.Rational(1,9)}
def T(a,n):return s.Matrix(n,n,lambda i,j:a.get(i-j,0))
conv={k:sum(b.get(j,0)*c.get(k-j,0) for j in b) for k in range(-5,6)}
count=0
for n in range(1,9):
 left=s.Matrix(n,n,lambda i,j:sum(b.get(i+k+1,0)*c.get(-k-j-1,0) for k in range(8)))
 right=s.Matrix(n,n,lambda i,j:sum(b.get(i-n-k,0)*c.get(n+k-j,0) for k in range(8)))
 assert T(b,n)*T(c,n)==T(conv,n)-left-right;count+=1
 for p in [1,2,3]:
  big=T(b,n+p);small=s.Matrix(n,n,lambda i,j:b.get(i-j-p,0));corner=big.inv()[:p,n:n+p]
  assert s.simplify(small.det()-(-1)**(n*p)*big.det()*corner.det())==0;count+=1
checks['sp14_independent_exact_boundaries_and_minors']=count
# SP07 exact negative controls, using only fresh rational inputs and reviewed acceptance code.
sys.path.insert(0,str(BASE/'SP-07/SP07_certified_continuation/code'))
from check_certificate import verify
raw=json.loads((BASE/'SP-07/SP07_certified_continuation/results/certificate_seven.json').read_text())
negative=BASE/'negative-controls';negative.mkdir(exist_ok=True)
for name,key,value in [('ratio','ratio_lower_bound','1.031'),('norm','norm_upper_bound','0.999'),('hall','I',[0,1])]:
 d=copy.deepcopy(raw);d[key]=value;p=negative/(name+'.json');p.write_text(json.dumps(d))
 rejected=False
 try:verify(p,negative/(name+'-unexpected-output.json'))
 except (AssertionError,ValueError):rejected=True
 assert rejected,name
checks['sp07_negative_controls_rejected']=3
(BASE/'independent-checks.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':checks},indent=2))
