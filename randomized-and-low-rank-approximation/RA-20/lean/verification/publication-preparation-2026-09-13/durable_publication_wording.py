#!/usr/bin/env python3
"""Coordinator-requested durable publication prose, before the first author seal."""
from pathlib import Path
import json,shutil,yaml
E=Path(__file__).resolve().parent;P=E.parents[1]
assert not (E/'EVIDENCE-MANIFEST.json').exists()
d=E/'before-durable-wording';d.mkdir()
for n in ['README.md','formalization.yaml']:shutil.copyfile(P/n,d/n)
for n in ['DOCUMENT-CHECKS.json','final_document_checks.py']:shutil.copyfile(E/n,d/n)
f=P/'README.md';s=f.read_text()
a='''support **Lean verified** status. This publication is prepared for a separate
independent publication review; its new upstream pull request is still pending.'''
b='''support **Lean verified** status. Publication review and upstream integration
are separate from these accepted mathematical and Linux checks. This document
does not claim an upstream merge.'''
assert a in s;s=s.replace(a,b)
a='''the complete rejection/control suite. The concrete canonical Markdown/TeX/PDF,
metadata and indexes receive a separate publication review before the new
individual pull request to upstream main. No upstream acceptance is claimed.'''
b='''the complete rejection/control suite. Publication of the canonical
Markdown/TeX/PDF, metadata and indexes is reviewed separately from the immutable
proof. Submission and upstream merging do not follow from kernel acceptance
alone; no upstream merge is claimed here.'''
assert a in s;f.write_text(s.replace(a,b))
f=P/'formalization.yaml';m=yaml.safe_load(f.read_text())
m['repository']['note']='Immutable proof and Linux-checked candidate revision; publication wrappers archive its exact metadata and README. Publication commits and upstream integration are separate; this metadata does not claim an upstream merge.'
m['status']['scope']='Complete twelve-export negative proof of the full original joint generic smooth critical-count conjecture, using its allowed n=s=3 case. Two independent statement approvals preceded implementation; two final mathematical approvals, independent candidate packaging, and actual Ubuntu default-kernel/Comparator/control verification were accepted by the coordinator. Canonical Lean verified publication preserves that immutable proof. Publication review and upstream integration are separate from accepted mathematical and runtime verification.'
m['review']['status']='agent-reviewed; mathematical-packaging-operational-reviews-accepted; actual-Linux-kernel-and-Comparator-pass'
m['review']['publication']['status']='Dated preparation state on 2026-09-13, before the independent publication handoff: the concrete publication was prepared, while its independent publication review, new publication commit, push and pull request were pending. This is a historical preparation record, not a continuing assertion of GitHub status.'
m['review']['publication']['preparation_record_date']='2026-09-13'
class Dumper(yaml.SafeDumper):
 def ignore_aliases(self,v):return True
f.write_text('# yaml-language-server: $schema=../../../docs/lean/schema/v0.4.schema.json\n'+yaml.dump(m,Dumper=Dumper,sort_keys=False,allow_unicode=True,width=104))
f=E/'final_document_checks.py';s=f.read_text()
for name in ['schema-final','diff-check','tracked-change-scope']:
 s=s.replace("'"+name+"'","'"+name+"-2'")
f.write_text(s)
(E/'durable-wording-change.json').write_text(json.dumps({'requester':'/root coordinator','before_first_seal':True,'change':'Use durable current README status and explicitly date YAML pending-publication statements as the 2026-09-13 preparation state','prior_wrappers_and_checks_preserved':'before-durable-wording/','canonical_Markdown_TeX_PDF_changed':False,'proof_or_CI_claims_changed':False},indent=2)+'\n')
print('Durable publication prose installed before sealing; prior wrapper and check bytes retained.')
