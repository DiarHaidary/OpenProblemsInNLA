from pathlib import Path
import hashlib,json,datetime
E=Path(__file__).resolve().parent;P=E.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
freeze=P/'reviews/proof-freeze.json';d=json.loads(freeze.read_text())
assert sha(freeze.read_bytes())=='394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4'
assert len(d['files'])==3503
for rel,h in d['files'].items():assert sha((P/rel).read_bytes())==h,rel
ss=json.loads((P/'reviews/statement-freeze.json').read_text());assert len(ss['files'])==1598
for rel,h in ss['files'].items():assert sha((P/rel).read_bytes())==h,rel
assert d['source_files']==ss['source_files'] and len(d['source_files'])==17
own=json.loads((E/'accepted-compiled-result.json').read_text());assert own['success'] and own['exact_types']==24
report=P/'reviews/final-referee-2.md'
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'APPROVE','role':'Independent final mathematical referee 2, no KE04 contribution','freeze_sha256':sha(freeze.read_bytes()),'frozen_files_preserved':3503,'statement_files_preserved':1598,'distinct_original_git_records':17,'fresh_Lean_commands':13,'exact_types':24,'kernel_and_axiom_checks':101,'final_target_project_closure':105,'all_exports_project_closure':147,'fresh_compiled_result_sha256':sha((E/'accepted-compiled-result.json').read_bytes()),'source_audit_result_sha256':sha((E/'source-audit/result.json').read_bytes()),'report_sha256':sha(report.read_bytes()),'mathematical_findings':[],'resolved_provenance_finding':'Initial convenience source maps collapsed two pairs; corrected distinct snapshot keys, all original bytes retained.','later_gates':['Refresh historical README/Lake default and create truthful v0.4 YAML','Actual Ubuntu default-kernel/Comparator/negative controls','Independent operational acceptance and publication review'],'local_macOS_only':True}
(E/'FINAL.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
outer=E/'EVIDENCE-MANIFEST.json';files={};excluded=[]
for q in sorted(P.rglob('*')):
    if not q.is_file():continue
    rel=str(q.relative_to(P))
    if q==outer:continue
    if rel=='reviews/final-referee-1.md' or rel.startswith('reviews/final-referee-1-evidence/'):
        excluded.append(rel);continue
    b=q.read_bytes();files[rel]={'sha256':sha(b),'bytes':len(b)}
assert all(rel in files for rel in d['files'])
nested=[r for r in files if Path(r).name=='EVIDENCE-MANIFEST.json']
manifest={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/leancert_examples','base':str(P),'report_sha256':sha(report.read_bytes()),'exact_self_exclusion':str(outer.relative_to(P)),'concurrent_sibling_exclusion':['reviews/final-referee-1.md','reviews/final-referee-1-evidence/'],'actual_sibling_files_excluded':excluded,'all_nested_manifests_included':nested,'files':files,'file_count':len(files),'rule':'Every project file at seal time, except only this exact outer self and the named concurrent sibling review scope. No basename exemptions.'}
outer.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'report_sha256':sha(report.read_bytes()),'outer_sha256':sha(outer.read_bytes()),'files':len(files),'nested_manifests':len(nested),'final_sha256':sha((E/'FINAL.json').read_bytes())},indent=2))
