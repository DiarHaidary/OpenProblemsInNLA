"""Audit the retained successful Lean batch; preserve its initial parser failure.

The original run's Python final assertion rejected pp.universes decorations,
not an axiom Name. Actual Lean collectAxioms checks compare Names and all passed.
This script records corrected diagnostics without altering or rerunning sources,
the earlier result, commands, logs, source snapshots, or deleted object receipts.
"""
from pathlib import Path
import hashlib,json,re,datetime
E=Path(__file__).resolve().parent;P=E.parents[1];A=E/'attempt-m7jifjwc'
sha=lambda b:hashlib.sha256(b).hexdigest()
R=json.loads((A/'result.json').read_text())
assert len(R['errors'])==1 and "assert all(set(r['axioms'])" in R['errors'][0]
commands=R['commands'];assert all(c['exit_code']==0 for c in commands)
lean=[c for c in commands if c['argv'][0].endswith('/lean') and '-o' in c['argv']]
assert len(lean)==13
for c in commands:
    assert sha((A/c['stdout']).read_bytes())==c['stdout_sha256']
    assert sha((A/c['stderr']).read_bytes())==c['stderr_sha256']
il=(A/'12-Inspector.stdout').read_text();assert il.count('EXACT_FROZEN_TYPE ')==24
assert il.count('REFERENCE_ONLY_PLACEHOLDER ')==24
reports=[];warnings=[]
for c in lean:
    log=(A/c['stdout']).read_text()
    reports.extend({'log':c['stdout'],'declaration':n,'printed_axioms':a,'axioms':[re.sub(r'\.\{[^}]*\}','',x.strip()) for x in a.split(',') if x.strip()]} for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log))
    warnings.extend({'log':c['stdout'],'line':line} for line in log.splitlines() if 'warning:' in line)
assert len(reports)==101 and all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in reports)
closures=re.findall(r'CLOSURE_TOTAL (\w+) reached=(\d+) required=(\d+)',il)
assert closures==[('FINAL_TARGET','105','31'),('ALL_EXPORTS','147','40')]
source_asserts=sum((A/'source'/('Solution.lean' if m=='Solution' else 'NLA/KE04/'+m+'.lean')).read_text().count('#assert_trust kernel') for m in ['Definitions','Krylov','Frames','Spectral','SpectralWindow','Transport','Intersection','Nonannihilation','Completion','Proof','Solution'])
assert source_asserts==77
assert (A/'source/Inspector.lean').read_text().count('#assert_trust kernel')==24
imported=json.loads((A/'actual-imported-objects.json').read_text());assert imported
assert len(imported)==len(re.findall(r'^IMPORTED_MODULE (\S+)',il,re.M))
for o in imported:
    q=Path(o['path'])
    if o['origin']=='own fresh prefix':assert not q.exists()
    else:assert q.is_file() and sha(q.read_bytes())==o['sha256']
assert R['own_prefix_removed'] and not Path(R['object_prefix']).exists() and len(R['own_objects'])==13
assert len(R['before_pins'])==len(R['after_pins'])==10 and R['before_pins']==R['after_pins']
f=P/'reviews/proof-freeze.json';d=json.loads(f.read_text());assert sha(f.read_bytes())=='394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4'
assert len(d['files'])==3503
for rel,h in d['files'].items():assert sha((P/rel).read_bytes())==h,rel
for rel,r in R['source_inputs'].items():
    assert sha((A/'source'/rel).read_bytes())==r['sha256']
    if rel not in ['Reference.lean','Inspector.lean','executed-runner.py.txt']:assert sha((P/rel).read_bytes())==r['sha256'],rel
(E/'accepted-compiled-result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'success':True,'scope':'Fresh macOS source and independent actual-type/body/axiom review; no actual Linux Comparator or external default-kernel replay.','original_result_sha256':sha((A/'result.json').read_bytes()),'original_python_postprocess_error_preserved':R['errors'][0],'correction':'Strip only printed universe decorations for report counting; actual compiled Name comparisons required the exact three allowed axioms and passed before this correction.','lean_source_commands':lean,'exact_types':24,'source_kernel_assertions':source_asserts,'inspector_kernel_assertions':24,'axiom_reports':reports,'closure_counts':closures,'imported_modules':len(imported),'imported_object_manifest_sha256':sha((A/'actual-imported-objects.json').read_bytes()),'imported_object_bytes':sum(x['bytes'] for x in imported),'read_only_external_objects_rehashed':sum(x['origin']!='own fresh prefix' for x in imported),'local_elaboration_trust_level':re.findall(r'LOCAL_ELABORATION_TRUST_LEVEL (\d+)',il),'warnings':warnings,'all_3503_frozen_inputs_unchanged':True,'all_10_pins_clean_unchanged':True,'cleaned_own_object_count':13,'raw_logs_retained':True},indent=2,sort_keys=True)+'\n')
print(json.dumps({'accepted_fresh_Lean':'PASS','Lean_commands':len(lean),'types':24,'axiom_reports':len(reports),'kernel_assertions':101,'closures':closures,'imported_modules':len(imported),'warnings':len(warnings)}))
