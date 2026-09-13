#!/usr/bin/env python3
"""One-shot independent RA20 operational evidence seal, excluding exact self only."""
import datetime,json,os
from verify_inventory import E,P,REPORT,SELF,HEAD,load,scope,sha,verify
from privacy_and_supplemental import checks as privacy_checks

assert not SELF.exists() and not (E/'FINAL.json').exists()
privacy=privacy_checks()
(E/'privacy-final.json').write_text(json.dumps(privacy,indent=2)+'\n')
final={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict':'APPROVE actual RA20 Ubuntu operational verification','candidate':HEAD,
    'workflow_run':34743832047,'RA20_job':103687982518,'checker_controls_job':103687982272,
    'reviewer':'/root/ra20_final_referee2','report':str(REPORT.relative_to(P)),
    'report_sha256':sha(REPORT),'source_binding_sha256':sha(E/'source-binding.json'),
    'runtime_verification_sha256':sha(E/'runtime-verification.json'),
    'artifact_verification_sha256':sha(E/'artifact-verification.json'),
    'whole_run_verification_sha256':sha(E/'whole-run-verification.json'),
    'candidate_Git_and_Linux_inputs':1092,'all_jobs':17,'all_original_artifact_ZIPs':16,
    'all_workflow_log_members':217,'exports':12,'source_kernel_assertions':61,'source_axiom_occurrences':57,
    'new_local_Lean_or_Linux_execution':False,'new_mathematical_approval':False,
    'canonical_status':'Solved, unchanged','root_operational_acceptance_and_publication':'pending'}
(E/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
files=scope()
assert SELF not in files
assert {p.resolve() for p in P.rglob('*') if p.is_file()}=={p for p in files if p.is_relative_to(P)}
own={p.resolve() for p in E.rglob('*') if p.is_file() and p.resolve()!=SELF}
manifest={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict':'APPROVE actual RA20 Ubuntu operational verification','candidate':HEAD,
    'reviewer':'/root/ra20_final_referee2','file_count':len(files),
    'own_evidence_files_excluding_outer':len(own),'exact_self_exclusion':'EVIDENCE-MANIFEST.json',
    'scope':'All 1092 committed candidate inputs, every prior nested-manifest input including live originals/check scripts, additional actual repository infrastructure, this report, every own raw command/API/archive/member snapshot/checker source/diagnostic/result. Only this exact outer self path is excluded. Later root acceptance/publication files outside this directory are outside this phase seal.',
    'historical_mapping':{'exact_original_project_path':'README.md',
        'only_expected_sha256':'7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50',
        'exact_archive_project_path':'verification/pre-candidate-README.md'},
    'files':{os.path.relpath(p,E):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)}}
verify(manifest)
with SELF.open('x') as f:f.write(json.dumps(manifest,indent=2)+'\n')
result=verify()
result.update(manifest_sha256=sha(SELF),report_sha256=sha(REPORT),
              source_binding_sha256=sha(E/'source-binding.json'),runtime_verification_sha256=sha(E/'runtime-verification.json'),
              final_sha256=sha(E/'FINAL.json'))
print(json.dumps(result,indent=2))
