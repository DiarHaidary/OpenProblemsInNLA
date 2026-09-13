from pathlib import Path
import json,re,subprocess
root=Path('/tmp/nla-lean-ke04-worktree/eigenvalues-and-inverse-problems/KE-04/lean')
comp=json.loads((root/'comparator.json').read_text())
# Ruby already checked formalization pins; parse names by YAML-ish declaration lines
raw=(root/'formalization.yaml').read_text()
yaml_names=re.findall(r'^  - declaration: ([A-Za-z0-9_.]+)$',raw,re.M)
comp_names=comp.get('theorem_names',[])
proof=(root/'NLA/KE04/Proof.lean').read_text()
# Names are fully-qualified; textual exports and assert trust identifiers
short=[x.rsplit('.',1)[-1] for x in comp_names]
exports={name:len(re.findall(r'\b'+re.escape(name)+r'\b',proof)) for name in short}
# Source module scan excluding Challenge and development receipts
source_files=sorted([*root.glob('NLA/KE04/*.lean'),root/'Proof.lean',root/'Solution.lean'])
source_files=[p for p in source_files if p.exists()]
occ=[]
for p in source_files:
 txt=p.read_text()
 occ.append({'file':str(p.relative_to(root)),'bytes':len(txt.encode()),'sorry':len(re.findall(r'\bsorry\b',txt)),'sorryAx':len(re.findall(r'sorryAx',txt)),'native_decide':len(re.findall(r'\bnative_decide\b',txt))})
print(json.dumps({'comparator_theorem_count':len(comp_names),'yaml_decl_count':len(yaml_names),'comparator_names':comp_names,'yaml_names':yaml_names,'sets_match':set(comp_names)==set(yaml_names),'proof_occurrence_counts':exports,'all_exports_textually_present':all(v>0 for v in exports.values()),'permitted_axioms':comp.get('permitted_axioms'),'source_scan':occ},indent=2))
