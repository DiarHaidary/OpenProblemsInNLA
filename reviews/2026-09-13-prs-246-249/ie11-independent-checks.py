#!/usr/bin/env python3
"""Independent primary-polynomial and CP-path checks; supplied proof code is not imported."""
from html.parser import HTMLParser
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,re,random
p=argparse.ArgumentParser();p.add_argument('--package',required=True);p.add_argument('--primary-html',required=True);p.add_argument('--output',required=True);a=p.parse_args();root=Path(a.package)
class Parser(HTMLParser):
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='math' and d.get('id')=='S2.E15.m1.m1': self.poly=d['alttext']
q=Parser();src=Path(a.primary_html);q.feed(src.read_text());s=q.poly.split('=',1)[1].replace(r'\end{aligned}','').replace(r'\quad','').replace('\\','').replace('&','');s=''.join(s.split())
terms=list(re.finditer(r'([+-]\d+)(g(?:\^\{(\d+)\})?)?',s));assert ''.join(t.group(0) for t in terms)==s
coeff={int(t.group(3) or ('1' if t.group(2) else '0')):int(t.group(1)) for t in terms};assert len(terms)==len(coeff)==62 and set(coeff)==set(range(62))
ref=root/'data/reference_P5_ascending.txt';assert [coeff[i] for i in range(62)]==list(map(int,ref.read_text().split()))
d=json.loads((root/'data/rational_witness.json').read_text());A=[[F(int(x),int(d['denominator'])) for x in row] for row in d['numerators']]
def cp(A):
 B=[r[:] for r in A];peaks=[];pivots=[]
 for k in range(5):
  positions=[(i,j) for i in range(k,5) for j in range(k,5)];top=max(abs(B[i][j]) for i,j in positions);winners=[(i,j) for i,j in positions if abs(B[i][j])==top];assert len(winners)==1
  i,j=winners[0];B[k],B[i]=B[i],B[k]
  for row in B:row[k],row[j]=row[j],row[k]
  pivot=B[k][k];assert pivot;peaks.append(top);pivots.append(abs(pivot))
  for i in range(k+1,5):
   multiplier=B[i][k]/pivot
   for j in range(k+1,5):B[i][j]-=multiplier*B[k][j]
   B[i][k]=F(0)
 return max(peaks)/peaks[0],pivots
ratio,pivs=cp(A);assert ratio>F(d['strict_lower_bound']) and ratio==pivs[-1]
rng=random.Random(24911)
for k in range(80):
 rows=rng.sample(range(5),5);cols=rng.sample(range(5),5);signs=[rng.choice((-1,1)) for _ in range(5)];cs=[rng.choice((-1,1)) for _ in range(5)];scale=F(rng.randint(1,9),rng.randint(1,9))
 B=[[scale*signs[i]*cs[j]*A[rows[i]][cols[j]] for j in range(5)] for i in range(5)];r,ps=cp(B);assert r==ratio and ps==[scale*x for x in pivs]
# The advertised relaxation upper value must be visibly weaker than the known bound.
assert F(81,16)>F('4.84')>ratio
out={'passed':True,'source':'https://arxiv.org/html/2602.20390v1#S2.E15','source_html_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'primary_coefficients_compared':62,'reference_file_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'independent_complete_pivoting_executions':81,'permutations_row_column_signs_and_positive_scalings_preserve_growth':True,'all_pivot_choices_strict':True,'fifth_pivot_exceeds_advertised_rational_lower_bound':True,'global_optimality_proved':False}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
