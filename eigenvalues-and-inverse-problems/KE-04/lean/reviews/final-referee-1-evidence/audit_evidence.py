"""Audit this referee's own outputs; does not execute old sealed runners."""
from pathlib import Path
import hashlib, json, re
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
R=json.loads((E/'execution.json').read_text())
assert R['status']=='PASS_LOCAL_SOURCE_AND_INSPECTION'
assert len(R['lean_modules'])==13
for c in R['commands']:
    assert c['exit_code'] in c['allowed_exit_codes'] and not c['timed_out'],c['label']
    for field in ['stdout','stderr']:assert sha(E/c[field])==c[field+'_sha256']
for s in R['source_inputs']:
    assert sha(P/s['path'])==s['sha256']==sha(E/s['snapshot'])
assert len(R['pins_before'])==10 and R['pins_before']==R['pins_after']
assert sum(p['used_in_lean_path'] for p in R['pins_before'])==9
assert R['key_objects_before']==R['key_objects_after']
assert R['frozen_before']==R['frozen_after']
for f in R['frozen_before']:
    assert sha(P/f['path'])==f['sha256']
    d=json.loads((P/f['path']).read_text())
    for rel,h in d['files'].items():assert sha(P/rel)==h
standard={'propext','Classical.choice','Quot.sound'}
cfg=json.loads((P/'comparator.json').read_text());names=cfg['theorem_names']
assert len(names)==24 and cfg['definition_names']==[] and set(cfg['permitted_axioms'])==standard
requirements=json.loads((E/'inspection-requirements.json').read_text())
inspection=next(x for x in R['lean_modules'] if x['path'].endswith('/Inspect.lean'))
text=(E/inspection['stdout']).read_text()
matches=re.findall(r'^EXACT_ELABORATED_SIGNATURE (\S+) = (\S+)$',text,re.M)
assert len(matches)==24 and [x for x,y in matches]==names
assert all(y=='NLA.KE04.FinalReferee1Reference.'+x.split('.')[-1] for x,y in matches)
counts=re.findall(r'INDEPENDENT_COUNTS (\w+): project=(\d+), material=(\d+)',text)
assert len(counts)==3 and {x[0] for x in counts}=={'FINAL','ALL','SOURCE'}
actual_axioms=re.findall(r'ACTUAL_AXIOMS (\w+) ([^:]+):\s*\[(.*?)\]',text,re.S)
assert len(actual_axioms)==sum(int(n) for _,n,_ in counts)
for label,name,axs in actual_axioms:
    assert {s.strip() for s in axs.split(',') if s.strip()}<=standard,(name,axs)
    assert 'FinalReferee1Reference' not in name
axiom_reports=[];warnings=[];trust_count=0;decls={}
for module in R['lean_modules']:
    content=(E/module['stdout']).read_text()
    if module['path'].endswith('/Reference.lean'):
        assert module['warning_count']==24
        continue
    source=(P/module['path']).read_text()
    trust_count+=len(re.findall(r'^#assert_trust kernel ',source,re.M))
    for name,axs in re.findall(r"'([^']+)' depends on axioms:\s*\[(.*?)\]",content,re.S):
        allowed={s.strip() for s in axs.split(',') if s.strip()}
        assert allowed<=standard,(name,axs)
        axiom_reports.append({'module':module['path'],'declaration':name,'axioms':sorted(allowed)})
    for name in re.findall(r"'([^']+)' does not depend on any axioms",content):
        axiom_reports.append({'module':module['path'],'declaration':name,'axioms':[]})
    if module['warning_count']:warnings.append({'path':module['path'],'warnings':module['warning_count'],'log':module['stdout']})
    if module['path'].startswith('NLA/') or module['path']=='Solution.lean':
        cleaned=re.sub(r'/\-.*?\-/','',source,flags=re.S)
        cleaned=re.sub(r'--[^\n]*','',cleaned)
        assert not re.search(r'\b(sorry|admit|axiom|unsafe|partial|native_decide)\b',cleaned),module['path']
        assert not re.search(r'^import .*Challenge',cleaned,re.M)
        decls[module['path']]=len(re.findall(r'^(?:def|abbrev|theorem) ',source,re.M))
assert trust_count==len(axiom_reports),(trust_count,len(axiom_reports))
assert inspection['warning_count']==0
reference=(E/'Reference.lean').read_text().replace('namespace NLA.KE04.FinalReferee1Reference\n','namespace NLA.KE04\n').replace('end NLA.KE04.FinalReferee1Reference\n','end NLA.KE04\n')
assert reference==(P/'Challenge.lean').read_text()
report={'success':True,'reviewer':'/root/ra09_final_referee1',
  'actual_source_modules':13,'actual_exact_contract_matches':24,
  'counts':[{'scope':s,'project_declarations':int(n),'material_bridges':int(m)} for s,n,m in counts],
  'actual_project_axiom_rows':len(actual_axioms),'kernel_assertions':trust_count,
  'actual_axiom_reports':axiom_reports,'warnings':warnings,'source_declaration_counts':decls,
  'proof_freeze':R['frozen_before'],'recorded_commands':len(R['commands']),
  'direct_Lean_seconds':sum(c['seconds'] for c in R['commands'] if c['label'].startswith('compile-')),
  'scope':'Independent local source/type/body/axiom evidence; not actual Linux Comparator or external kernel replay',
  'auditor_sha256':sha(__file__)}
(E/'source-and-output-audit.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:report[k] for k in ['success','actual_source_modules','actual_exact_contract_matches','counts','actual_project_axiom_rows','kernel_assertions','recorded_commands','warnings','direct_Lean_seconds']},indent=2))
