#!/usr/bin/env python3
"""Validate the draft's source binding and recorded statement-only checks.

This is a reproducible integrity diagnostic, not a freeze, independent review,
mathematical proof, or Linux Comparator run.
"""
import hashlib,json,pathlib,re,subprocess

P=pathlib.Path(__file__).resolve().parents[2]
GIT=pathlib.Path('/tmp/nla-lean-ra09-worktree')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    original=json.loads((P/'verification/original-source-inventory.json').read_text())
    for rel,expected in original['files'].items():
        local=P/'verification/original-sources'/rel
        assert sha(local)==expected['sha256'] and local.stat().st_size==expected['bytes']
        data=subprocess.check_output(['git','-C',str(GIT),'show',original['base']+':'+rel])
        assert data==local.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==expected['git_blob']
    development=P/'verification/statement-development'
    latest=json.loads((development/'latest.json').read_text())
    attempt=development/latest['attempt']
    assert sha(attempt/'result.json')==latest['result_sha256']
    result=json.loads((attempt/'result.json').read_text())
    assert result['pass'] and result['own_prefix_removed']
    assert len(result['commands'])==3 and all(c['exit_code']==0 for c in result['commands'])
    assert result['pins_before']==result['pins_after'] and len(result['pins_after'])==10
    prior_attempts=[]
    for old in sorted(development.glob('attempt-*')):
        if (old/'result.json').exists():
            old_result=json.loads((old/'result.json').read_text())
            assert old_result['own_prefix_removed'] and not pathlib.Path(old_result['prefix']).exists()
            prior_attempts.append({'attempt':old.name,'kind':'source check',
                                  'pass':old_result['pass'],'commands':len(old_result['commands'])})
        else:
            failure=json.loads((old/'preflight-failure.json').read_text())
            assert not failure['mathematical_compile_started']
            assert all(not pathlib.Path(x['path']).exists() for x in failure['cleanup'])
            prior_attempts.append({'attempt':old.name,'kind':'preflight','pass':False,'commands':0})
    for rel,expected in result['inputs'].items():
        assert sha(P/rel)==expected['sha256']
        assert sha(attempt/'source'/rel)==expected['sha256']
    for command in result['commands']:
        assert sha(attempt/command['log'])==command['log_sha256']
    assert not (attempt/'Definitions.log').read_text()
    assert (attempt/'Challenge.log').read_text().count('declaration uses `sorry`')==17
    inspector=(attempt/'Inspect.log').read_text()
    axioms=re.findall(r"'NLA\.IE05\.[^']+' depends on axioms: \[([^]]*)\]",inspector)
    assert len(axioms)==12
    assert all({x.strip() for x in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for a in axioms)
    assert 'error:' not in inspector and 'error(' not in inspector
    definitions=(P/'NLA/IE05/Definitions.lean').read_text()
    challenge=(P/'Challenge.lean').read_text()
    names=re.findall(r'^theorem (\w+)',challenge,re.M)
    config=json.loads((P/'comparator.json').read_text())
    assert config['theorem_names']==['NLA.IE05.'+n for n in names] and len(names)==17
    assert config['definition_names']==[]
    assert set(config['permitted_axioms'])=={'propext','Classical.choice','Quot.sound'}
    assert len(re.findall(r'\bby sorry\b',challenge))==17
    # Lexical guards supplement, and do not replace, human/agent semantic review.
    assert not re.search(r'^\s*(axiom|opaque|unsafe|theorem|lemma)\b',definitions,re.M)
    assert not re.search(r'\b(sorry|admit|native_decide|ofReduceBool)\b',definitions)
    assert not re.search(r'^\s*(axiom|opaque|unsafe)\b',challenge,re.M)
    assert not (P/'Solution.lean').exists() and not (P/'NLA/IE05/Proof.lean').exists()
    assert not (P/'formalization.yaml').exists()
    assert not (P/'.lake').exists()
    assert not list(P.rglob('*.olean')) and not list(P.rglob('*.ilean'))
    recon=json.loads((development/'reconstruction.json').read_text())
    assert recon['source_sha256']==sha(P/'NLA/IE05/Definitions.lean')
    assert recon['script_sha256']==sha(development/'reconstruct.py')
    assert recon['all_checks_pass'] and recon['witness_initial_count']==64 and recon['candidate_active_count']==204
    assert recon['positive_squared_gap']=='117335164/1147041'
    evidence={'phase':'unfrozen statement draft validation','pass':True,
        'source_base':original['base'],'original_source_files':len(original['files']),
        'latest_attempt':latest['attempt'],'latest_result_sha256':latest['result_sha256'],
        'successful_fresh_commands':3,'definition_only_kernel_assertions':12,
        'definition_only_standard_three_reports':12,'challenge_placeholders':17,
        'comparator_export_names':config['theorem_names'],'definition_exceptions':[],
        'ten_pins_clean_unchanged':True,'reconstruction_sha256':sha(development/'reconstruction.json'),
        'witness_input_inequalities':64,'candidate_active_inequalities':204,
        'local_platform_only':True,'all_own_object_prefixes_cleaned':True,
        'all_retained_attempts':prior_attempts,
        'coordinator_review_not_independent_approval':True,'statement_approvals':0,
        'proof_implementation_started':False,'linux_comparator_ran':False,
        'canonical_or_git_mutations':False,'no_formalization_yaml':True}
    (development/'validation.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence))

if __name__=='__main__':main()
