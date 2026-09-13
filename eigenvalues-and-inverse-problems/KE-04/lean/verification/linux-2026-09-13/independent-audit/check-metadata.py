from pathlib import Path
import hashlib, json, re
root=Path('/tmp/nla-lean-ke04-worktree/eigenvalues-and-inverse-problems/KE-04/lean')
try:
 import yaml
except Exception as e:
 raise SystemExit('PyYAML unavailable: '+str(e))
meta=yaml.safe_load((root/'formalization.yaml').read_text())
man=json.loads((root/'lake-manifest.json').read_text())
pins=meta['toolchain']['dependencies']
# lake-manifest is a package array in this repo; map package name to rev
packages={x['name']:x.get('rev') for x in man.get('packages',[])}
checks={}
for name,val in pins.items():
 if name in ('importGraph',): checks[name]={'metadata':val,'manifest':None,'match':True,'note':'import graph is not a Lake package'}
 else: checks[name]={'metadata':val,'manifest':packages.get(name),'match':packages.get(name)==val}
raw=(root/'formalization.yaml').read_text()
checks['author_name']='George Stepaniants' in raw
checks['affiliation_all']=all(x in raw for x in ['Department of Computing and Mathematical Sciences','California Institute of Technology','Pasadena','California','USA'])
checks['no_email']=not bool(re.search(r'(?i)\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b',raw))
checks['status_truthful']=meta['status']['whole_problem_verified'] is False and meta['status']['actual_linux_comparator']=='pending'
checks['default_solution']='defaultTargets = ["Solution"]' in (root/'lakefile.toml').read_text()
checks['solution_import_proof']=(root/'Solution.lean').read_text().strip()=='import NLA.KE04.Proof'
print(json.dumps({'project':meta.get('project',{}),'pins':checks,'declarations':len(meta['status']['main_results'])},indent=2))
