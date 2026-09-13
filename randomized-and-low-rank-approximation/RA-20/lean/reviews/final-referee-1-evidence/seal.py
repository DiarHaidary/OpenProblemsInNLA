#!/usr/bin/env python3
"""One-shot independent final review seal; only its exact own outer path is excluded."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
E=Path(__file__).resolve().parent;P=E.parent.parent;M=E/'EVIDENCE-MANIFEST.json'
assert not M.exists(),'Never regenerate an existing final seal'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((E/'validated-results.json').read_text());assert v['status']=='PASS'
c=json.loads((E/'owned-prefix-cleanup.json').read_text());assert c['postcheck_absent']
report=P/'reviews/final-referee-1.md'
assert '**APPROVE the complete frozen mathematical proof.**' in report.read_text()
final={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/ra20_final_referee1',
       'verdict':'APPROVE','role':'Independent final mathematical referee; no statement/proof authorship',
       'report_sha256':sha(report),'validation_sha256':sha(E/'validated-results.json'),
       'proof_freeze_sha256':sha(P/'verification/proof-freeze.json'),
       'successful_Lean_commands':13,'exact_export_types':12,'all_project_declarations':236,
       'actual_project_closure':214,'material_dependencies':39,'printed_standard_three_axiom_reports':69,
       'source_kernel_assertions':61,'diagnostic_kernel_assertions':12,
       'owned_objects_hashed_then_removed':26,'actual_Linux_Comparator':'Pending separate gate',
       'required_mathematical_corrections':[],'nonblocking_documentation_precisions':[
          'abcLocalChart uses ordinary localization, not an adic completion.',
          'Nondegenerate Hessians are proved; no separate scheme-theoretic multiplicity theorem is exported.']}
(E/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
f=json.loads((P/'verification/proof-freeze.json').read_text())
frozen={(P/n).resolve() for n in f['files']}|{(P/'verification/proof-freeze.json').resolve()}
own={p.resolve() for p in E.rglob('*') if p.is_file() and p!=M}
files=frozen|own|{report.resolve()}
assert len(frozen)==522 and len(files)==len(frozen)+len(own)+1
inventory={os.path.relpath(p,E):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)}
m={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/ra20_final_referee1',
   'scope':'Complete independent final mathematical review evidence, exact frozen proof closure and all nested manifests',
   'file_count':len(inventory),'own_evidence_files':len(own),'frozen_files_including_freeze':522,
   'adjacent_report_files':1,'original_source_files':f['source_files'],'original_source_git_blobs':f['source_git_blobs'],
   'inventory_rule':'Every own file, the complete 521-file frozen project plus its freeze, and adjacent report. All nested manifests included. Original source bytes are bound through their retained snapshots.',
   'exact_self_exclusion':'EVIDENCE-MANIFEST.json','files':inventory}
M.write_text(json.dumps(m,indent=2)+'\n')
subprocess.run([sys.executable,str(E/'verify_seal.py')],check=True)
