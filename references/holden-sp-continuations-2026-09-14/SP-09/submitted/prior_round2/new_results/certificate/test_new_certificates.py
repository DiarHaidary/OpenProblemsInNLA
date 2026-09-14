"""Regression checks for exact geometry, coefficient ranks, and corrupted data."""
from __future__ import annotations
from pathlib import Path
from copy import deepcopy
from contextlib import redirect_stdout
import argparse,io,json,tempfile
from local_geometry import PRIOR,geometry_checks
from rank_witness import verify as verify_modular
from exact_minor import run as verify_integer,bareiss
from quantitative_rigidity import verify as verify_stability
from verify_certificate import require


def rejected(fn):
 try:
  with redirect_stdout(io.StringIO()):fn()
 except (ValueError,KeyError,IndexError,TypeError):return True
 return False

def run(report=None):
 root=Path(__file__).resolve().parent;results={}
 with redirect_stdout(io.StringIO()):
  data=json.loads((PRIOR/'krause_certificate.json').read_text());geometry_checks();verify_modular(root/'local_rank_witness.json');verify_integer();verify_stability()
 results['valid_geometry']='PASS';results['valid_modular_rank']='PASS';results['valid_integer_rank']='PASS';results['valid_stability_constant']='PASS'
 w=json.loads((root/'local_rank_witness.json').read_text());corruptions=[]
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'bad.json'
  for name,mutate in [
   ('duplicate_minor_column',lambda x:x['columns'].__setitem__(1,x['columns'][0])),
   ('incorrect_modular_determinant',lambda x:x.__setitem__('minor_determinant_mod_prime',(x['minor_determinant_mod_prime']+1)%x['prime'])),
   ('composite_modulus',lambda x:x.__setitem__('prime',1000005)),
   ('incorrect_coordinate_order',lambda x:x['trace_coordinates'].__setitem__(1,['bad','r']))]:
   bad=deepcopy(w);mutate(bad);p.write_text(json.dumps(bad));ok=rejected(lambda:verify_modular(p));require(ok,'Corruption was accepted: '+name);corruptions.append({'corruption':name,'rejected':ok})
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'bad_certificate.json'
  bad=deepcopy(data);bad['q_real'][5]=int(bad['q_real'][5])+1;p.write_text(json.dumps(bad));ok=rejected(lambda:geometry_checks(p));require(ok,'Higher-degree q corruption was accepted.');corruptions.append({'corruption':'loss_of_degree_one_normalization','rejected':ok})
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'bad_certificate.json'
  bad=deepcopy(data);bad['blocks'][1]['kernel_real'][3][0]=int(bad['blocks'][1]['kernel_real'][3][0])+1;p.write_text(json.dumps(bad));ok=rejected(lambda:geometry_checks(p));require(ok,'Local kernel corruption was accepted.');corruptions.append({'corruption':'changed_local_kernel','rejected':ok})
 for matrix,det in [([[2,3],[5,7]],-1),([[0,1],[1,0]],-1),([[1,2,3],[0,1,4],[5,6,0]],1),([[1,1],[1,1]],0)]:require(bareiss(matrix)==det,'Bareiss regression failed.')
 results['integer_elimination_regressions']='PASS';results['corruption_tests']=corruptions
 print(json.dumps(results,indent=2))
 if report:Path(report).write_text(json.dumps(results,indent=2)+'\n')
 return results
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json-report',type=Path);a=p.parse_args();run(a.json_report)
