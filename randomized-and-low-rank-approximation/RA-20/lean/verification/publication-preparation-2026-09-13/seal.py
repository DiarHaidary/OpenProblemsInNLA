#!/usr/bin/env python3
"""One-shot publication author seal; not an independent publication approval."""
from pathlib import Path
import datetime,hashlib,json,os
from verify_inventory import E,P,R,SELF,load,sha,sealed_scope
assert not SELF.exists()
v=load(E/'VALIDATION.json');assert v['status']=='PUBLICATION_PRESEAL_PASS'
scope=sealed_scope();b=load(E/'PREFLIGHT.json')
files={os.path.relpath(q,E):{'sha256':sha(q),'bytes':q.stat().st_size} for q in sorted(scope)}
m={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PUBLICATION_AUTHOR_SEALED; independent publication review pending',
 'author':'/root/ra20_final_referee1','role':'Candidate-document and publication author; no independent review of own publication',
 'candidate':v['candidate'],'actual_accepted_Ubuntu_run':34743832047,
 'root_gate_sha256':b['anchors']['verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json'],
 'file_count':len(files),'own_evidence_files_excluding_outer':sum(q.is_relative_to(E) for q in scope),
 'project_files_excluding_outer':sum(q.is_relative_to(P) for q in scope),
 'other_repository_files':sum(not q.is_relative_to(P) for q in scope),
 'project_baseline_count':1580,'other_prepublication_inputs':17,'changed_existing_paths':v['changed_existing_paths'],
 'accepted_prior_inventories':v['accepted_prior_inventories'],'rejected_diagnostic_manifest_retained':v['rejected_diagnostic_manifest_retained'],
 'inventory_rule':'Complete prior project baseline, accepted root operational scope including every nested manifest and rejected diagnostic bytes, all new publication outputs/archives/evidence, all canonical/index inputs and actual renderer/check sources. Only this exact outer self path excluded. Later independent reviewer additions outside this directory are separate evidence.',
 'historical_mapping_rule':'Only exact original repository path plus exact expected old SHA256 in ARCHIVES.json, together with the earlier exact project-README/7eb951... mapping. All other expectations unchanged; no historical seal edited.',
 'exact_self_exclusion':'EVIDENCE-MANIFEST.json','files':files}
SELF.write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'status':m['status'],'files':len(files),'own_evidence_files_excluding_outer':m['own_evidence_files_excluding_outer'],'outer_sha256':sha(SELF)}))
