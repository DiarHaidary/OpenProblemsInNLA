#!/usr/bin/env python3
"""Independent raw-output, frozen-closure and source-library checks; no Lean mutations."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess
E=Path(__file__).resolve().parent;P=E.parent.parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda n,x:(E/n).write_text(json.dumps(x,indent=2)+'\n')
freeze=json.loads((P/'verification/proof-freeze.json').read_text())
for n,h in freeze['files'].items():assert sha(P/n)==h,n
for n,h in freeze['source_files'].items():assert sha(R/n)==h,n
nested=[]
for n in freeze['files']:
    if n.endswith('EVIDENCE-MANIFEST.json') or n=='reviews/statement-package-manifest.json':
        f=P/n;m=json.loads(f.read_text());base=P if n=='reviews/statement-package-manifest.json' else f.parent
        for k,v in m['files'].items():
            q=base/k;h=v if isinstance(v,str) else v['sha256'];assert sha(q)==h,(n,k)
            if isinstance(v,dict) and 'bytes' in v:assert q.stat().st_size==v['bytes'],(n,k)
        nested.append({'path':n,'sha256':sha(f),'bound_files':len(m['files'])})
assert len(nested)==12
records=json.loads((E/'commands.json').read_text());assert len(records)==13 and all(r['exit_code']==0 for r in records)
allowed={'propext','Classical.choice','Quot.sound'};reports=[];warnings=[]
for k,r in enumerate(records,1):
    a=E/('attempt-%02d'%k);log=(a/'lean.log').read_text()
    assert sha(a/Path(r['source']).name)==r['source_sha256']==sha(P/r['source'])
    assert 'error:' not in log,(k,'error in successful command')
    for name,axs in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log):
        names={x.strip() for x in axs.split(',') if x.strip()};assert names==allowed,(name,names)
        reports.append({'attempt':k,'name':name,'axioms':sorted(names)})
    warnings.extend({'attempt':k,'line':l} for l in log.splitlines() if 'warning:' in l)
assert len(reports)==69 and len(warnings)==14
s=(E/'attempt-13/lean.log').read_text()
exports=json.loads((P/'comparator.json').read_text())['theorem_names']
got=re.findall(r'^EXACT_FROZEN_TYPE (\S+):',s,re.M);assert got==exports
assert 'ALL_PROJECT_DECLARATIONS 236' in s and 'PROJECT_COUNTS declarations=214, required=39' in s
actual=re.findall(r'^ACTUAL_AXIOMS (\S+):\s*\[([^\]]*)\]',s,re.M)
assert len(actual)==214
for n,axs in actual:assert {x.strip() for x in axs.split(',') if x.strip()}<=allowed,(n,axs)
need=re.findall(r'^RETAINED_DEPENDENCY (\S+)',s,re.M);assert len(need)==39
source_checks=sum(len(re.findall(r'^#assert_trust kernel ',(P/r['source']).read_text(),re.M)) for r in records[:11])
diagnostic_checks=len(re.findall(r'^#assert_trust kernel ',(P/records[-1]['source']).read_text(),re.M))
assert source_checks==61 and diagnostic_checks==12
# The reference is exactly a namespace-only transform, with its twelve admissions isolated.
t=(P/'Challenge.lean').read_text().replace('namespace NLA.RA20','namespace NLA.RA20.Referee1Reference').replace('end NLA.RA20','end NLA.RA20.Referee1Reference')
assert (E/'ReferenceChallenge.lean').read_text()==t and len(re.findall(r'^  sorry$',t,re.M))==12
for r in records[:11]:
    src=(P/r['source']).read_text()
    assert not re.search(r'^\s*(?:axiom|unsafe |partial |sorry\b|admit\b)',src,re.M),r['source']
    assert not re.search(r'^import .*Challenge',src,re.M),r['source']
save('validated-results.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
    'successful_commands':13,'seconds':sum(r['seconds'] for r in records),'exact_raw_expression_and_defeq_matches':got,
    'all_project_declarations_trust_checked':236,'actual_project_closure':214,'material_dependencies':need,
    'source_LeanCert_kernel_assertions':source_checks,'diagnostic_LeanCert_kernel_assertions':diagnostic_checks,
    'printed_axiom_reports':reports,'warnings':warnings,'complete_nested_manifests':nested,
    'proof_freeze_sha256':sha(P/'verification/proof-freeze.json'),'frozen_inputs':521,'original_sources':16,
    'separate_Linux_Comparator':'NOT RUN BY THIS REFEREE; pending authoritative gate'})
print('VALIDATED_RESULTS_PASS: 12 exact types, 236 globals, 214 closure, 39 material dependencies, 69 printed standard-three reports, 12 nested manifests')
