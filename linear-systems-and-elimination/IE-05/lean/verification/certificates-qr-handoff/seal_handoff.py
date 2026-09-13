#!/usr/bin/env python3
"""One-time own handoff/seal writer; use verify_handoff.py for read-only checks."""
from pathlib import Path
import datetime,hashlib,json
from verify_handoff import verify
E=Path(__file__).resolve().parent;P=E.parents[1]
M=E/'EVIDENCE-MANIFEST.json';R=P/'reviews/certificates-qr-completion.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not M.exists() and R.is_file()
result=verify(True)
sources={n:sha(P/n) for n in ['NLA/IE05/ExactCertificates.lean','NLA/IE05/IntegerQR.lean','NLA/IE05/Scaling.lean','NLA/IE05/QR.lean','NLA/IE05/Definitions.lean','Challenge.lean']}
handoff={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'HELPER_COMPLETION_READY_FOR_ASSEMBLY','owner_of_mathematical_helpers':'/root',
 'certificate_fix_contributor':'/root/formal_review_standards',
 'completion_inspector':'/root/ie05_statement_referee2','independent_final_review':False,
 'actual_Linux_Comparator':False,'source_sha256':sources,'report_sha256':sha(R),
 'checked_result':result,'actual_fresh_attempt':'attempt-eod4mx91',
 'actual_audit':'AUDIT-RESULT.json','read_only_verifier_sha256':sha(E/'verify_handoff.py'),
 'exact_APIs':['NLA.IE05._proved.integer_factor_certificates','NLA.IE05._proved.integer_entry_certificates',
              'NLA.IE05._proved.numerical_gap_positive','NLA.IE05._proved.normalizedQRQ_of_gram_lu'],
 'no_mathematical_sources_edited':True,'concurrent_Witness_scope':'not inspected or bound',
 'root_note_preserved_sha256':sha(E/'ROOT-NOTE.json')}
(E/'HANDOFF.json').write_text(json.dumps(handoff,indent=2)+'\n')
bound=set(json.loads((E/'INPUTS.json').read_text())['files'])
own={str(p.relative_to(P)) for p in E.rglob('*') if p.is_file() and p!=M}
names=bound|own|{str(R.relative_to(P))}
assert str(M.relative_to(P)) not in names
seal={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'All fixed1210 frozen/prior/stable helper inputs, every own evidence file including root-owned ROOT-NOTE, and adjacent completion report; concurrent Witness additions outside this scope are not bound.',
 'exact_self_exclusion':str(M.relative_to(P)),'file_count':len(names),
 'complete_evidence_directory_files_excluding_outer':len(own),
 'stable_input_files':len(bound),'files':{n:{'sha256':sha(P/n),'bytes':(P/n).stat().st_size} for n in sorted(names)}}
M.write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'report_sha256':sha(R),'handoff_sha256':sha(E/'HANDOFF.json'),
 'outer_sha256':sha(M),'sealed_files':len(names),'evidence_directory_files_excluding_outer':len(own),
 'verifier_sha256':sha(E/'verify_handoff.py')},indent=2))
