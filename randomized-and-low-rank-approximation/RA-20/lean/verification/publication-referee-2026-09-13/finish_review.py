#!/usr/bin/env python3
"""Create this referee's own review records and seal, after recorded checks.

This is a one-time evidence writer, not the read-only reproduction command.
It writes exclusively inside this referee directory. The adjacent report is
written separately before sealing. Do not rerun after sealing.
"""
from pathlib import Path
import datetime, hashlib, json, os

E=Path(__file__).resolve().parent
P=E.parents[1]
R=P.parents[2]
A=P/'verification/publication-preparation-2026-09-13'
SELF=E/'EVIDENCE-MANIFEST.json'
REPORT=P/'reviews/publication-referee-2026-09-13.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def write(name, value):
    p=E/name
    assert not p.exists(),name
    p.write_text(json.dumps(value,indent=2)+'\n')

assert not SELF.exists() and REPORT.is_file()
result=json.loads((E/'receipts/independent-preservation-final.stdout').read_text())
assert result['status']=='INDEPENDENT_RA20_PUBLICATION_PRESERVATION_PASS'
assert result['original_Linux_input_map_equals_all_1092_Git_inputs']
pages=[]
observations=[
    'Title, Lean verified status, dated negative resolution, full formalization affiliation, original credit, twelve exports and scope paragraph readable. No clipped text, overlap or missing glyph.',
    'Ubuntu evidence, exact pins, reproduction commands, full original statement and all four formulas readable. All formulas and common parameter range remain together on this page. No clipping or overlap.',
    'Numerical significance, complete reference and historical scope/status paragraph readable. Footer and page number separated from content. Deliberate trailing whitespace; no clipping or overlap.'
]
for i in range(1,4):
    p=E/f'pages/page-{i}.png'
    pages.append({'page':i,'file':str(p.relative_to(E)),'sha256':sha(p),
                  'visually_inspected_by':'OpenAI Codex agent /root/ie05_statement_referee2',
                  'method':'independent 125 DPI Poppler rendering, viewed with tools.view_image',
                  'observation':observations[i-1]})
write('VISUAL-REVIEW.json',{'verdict':'INDEPENDENT_PUBLICATION_VISUAL_PASS',
      'PDF_sha256':sha(P.parent/'problem.pdf'),'pages':pages,'page_count':3,
      'source_PDF_modified':False,'new_render_command':'receipts/pdf-render.json',
      'metadata_command':'receipts/pdf-info.json','extracted_text_command':'receipts/pdf-text.json'})
write('SOURCE-RECEIPTS.json',{
    'receipt_recorder':{'file':'record.py','sha256':sha(E/'record.py')},
    'initial_successful_preservation_command':{
        'receipt':'receipts/independent-preservation.json',
        'actual_source_snapshot':'verify_publication-initial.py',
        'sha256':sha(E/'verify_publication-initial.py'),
        'note':'Initial source snapshot retained before adding an extra direct equality check against the original Ubuntu artifact input map.'},
    'final_preservation_command':{
        'receipt':'receipts/independent-preservation-final.json',
        'source':'verify_publication.py','sha256':sha(E/'verify_publication.py')},
    'navigation_stdin_disclosure':'Three initial diagnostic commands used inline Python passed on stdin. Their exact command source is retained in navigation-stdin.json from the tool-call text. The recorder captured their actual stdout/stderr/exits, but did not itself capture stdin at runtime. They are navigation only; the standalone final preservation verifier rechecks all material assertions.',
    'read_scope':'The complete final wrappers, canonical Markdown/TeX and all three PDF pages were read. Original proof, Definitions, Challenge, Solution exports, correspondence, standards, author handoff/verifier/archive mapping, actual publication inspector/render drivers, accepted operational report/gate and original artifact receipt were inspected. Prior proofs were not recompiled or independently reapproved by this publication review.'})
receipts=[]
for p in sorted((E/'receipts').glob('*.json')):
    d=json.loads(p.read_text())
    assert d['exit_code']==0,(p,d['exit_code'])
    assert sha(p.with_suffix('.stdout'))==d['stdout_sha256']
    assert sha(p.with_suffix('.stderr'))==d['stderr_sha256']
    receipts.append({'file':str(p.relative_to(E)),'sha256':sha(p),'exit_code':d['exit_code']})
write('RESULT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'verdict':'APPROVE final RA-20 publication package',
      'phase':'independent publication review', 'reviewer':'/root/ie05_statement_referee2','AI_agent':True,
      'independent_of_RA20_mathematics_and_publication_authors':True,
      'publication_author_seal_sha256':sha(A/'EVIDENCE-MANIFEST.json'),
      'report_sha256':sha(REPORT),'preservation_result':'receipts/independent-preservation-final.stdout',
      'preservation_result_sha256':sha(E/'receipts/independent-preservation-final.stdout'),
      'all_actual_recorded_command_receipts':receipts,'retained_current_review_failed_commands':0,
      'historical_failed_diagnostics':'All retained and hash-bound; rejected root initial scope diagnostic is not an accepted inventory.',
      'visual_review':'VISUAL-REVIEW.json','schema_pass':True,
      'required_publication_changes':[], 'read_only_reproduction':'PYTHONDONTWRITEBYTECODE=1 python3 verify_publication.py --check-own-seal',
      'new_mathematical_approval':False,'new_Lean_or_Linux_execution':False,
      'Git_commit_push_PR':False,'upstream_merge_claim':False,
      'limitation':'Evidence preservation and publication review, not new kernel execution or live HTTP verification of every external URL. Root acceptance and subsequent Git/publication operations remain separate.'})
outer=json.loads((A/'EVIDENCE-MANIFEST.json').read_text())
inputs={(A/n).resolve() for n in outer['files']}|{(A/'EVIDENCE-MANIFEST.json').resolve()}
inputs|={(R/n).resolve() for n in result['status_input_snapshots']}
own={q.resolve() for q in E.rglob('*') if q.is_file() and q.resolve()!=SELF.resolve()}|{REPORT.resolve()}
files=inputs|own
assert SELF.resolve() not in files
write('EVIDENCE-MANIFEST.json',{
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer':'/root/ie05_statement_referee2','verdict':'APPROVE final RA-20 publication package',
    'exact_self_exclusion':'EVIDENCE-MANIFEST.json',
    'scope':'All 1791 exact sealed author inputs and the author outer itself; all 217 canonical README inputs independently counted; this adjacent report and every own evidence file. Only this exact outer path is excluded. Earlier and concurrent separate publication actions outside this fixed scope are not silently added.',
    'file_count':len(files),'own_files_including_adjacent_report':len(own),'input_files':len(inputs),
    'files':{os.path.relpath(p,E):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)}})
print(json.dumps({'report_sha256':sha(REPORT),'outer_sha256':sha(SELF),
      'result_sha256':sha(E/'RESULT.json'),'files':len(files),'own_files_including_report':len(own),
      'read_only_verifier_sha256':sha(E/'verify_publication.py')},indent=2))
