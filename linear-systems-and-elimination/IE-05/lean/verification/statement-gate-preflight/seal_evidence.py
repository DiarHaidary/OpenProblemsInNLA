#!/usr/bin/env python3
"""Seal/verify only the coordinator-helper's new evidence, never historical inputs."""
import hashlib,json,pathlib,sys
E=pathlib.Path(__file__).resolve().parent
P=E.parent.parent
OUTER=E/'EVIDENCE-SEAL.json'
def ident(p):
    assert p.is_file() and not p.is_symlink()
    b=p.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def members():
    out={}
    for p in sorted(E.rglob('*')):
        assert not p.is_symlink()
        if p.is_file() and p!=OUTER:out[p.relative_to(P).as_posix()]=ident(p)
    return out
def validate_receipts():
    for n in [1,2]:
        receipt=json.loads((E/f'attempt-{n}-command.json').read_text())
        assert receipt['exit_code']==(1 if n==1 else 0)
        assert receipt['script_sha256']==ident(E/f'attempt-{n}-verifier.py')['sha256']
        for channel,suffix in [('stdout','json'),('stderr','log')]:
            assert receipt[channel+'_sha256']==ident(E/f'attempt-{n}.{channel}.{suffix}')['sha256']
        result=json.loads((E/f'attempt-{n}.stdout.json').read_text())
        assert result['pass']==(n==2)
        assert not result['proof_authorized'] and not result['is_statement_freeze'] and not result['new_Lean_compile']
        for c in result['actual_commands']:
            assert c['exit_code']==0
            for channel in ['stdout','stderr']:
                assert hashlib.sha256(c[channel].encode()).hexdigest()==c[channel+'_sha256']
    result=json.loads((E/'attempt-2.stdout.json').read_text())
    binding=json.loads((E/'proposed-input-binding.json').read_text())
    assert binding==result['proposed_input_binding'] and len(binding['files'])==718
    assert ident(E/'verify_preflight.py')==ident(E/'attempt-2-verifier.py')
    for rel,meta in binding['files'].items():assert ident(P/rel)==meta
    summary=json.loads((E/'preflight-result.json').read_text())
    assert summary['successful_raw_result']==ident(E/'attempt-2.stdout.json')
    assert summary['proposed_input_binding']==ident(E/'proposed-input-binding.json')
    assert summary['pass'] and not summary['proof_authorized']
validate_receipts()
if sys.argv[1:] == ['--verify']:
    d=json.loads(OUTER.read_text())
    assert d['excluded_paths']==[OUTER.relative_to(P).as_posix()]
    assert d['files']==members()
    print(json.dumps({'pass':True,'members_excluding_exact_outer':len(d['files']),
      'seal':ident(OUTER),'preflight_result':ident(E/'preflight-result.json'),
      'proposed_input_binding':ident(E/'proposed-input-binding.json'),
      'portable_verifier':ident(E/'verify_preflight.py'),'proof_authorized':False},indent=2))
else:
    assert sys.argv[1:]==[] and not OUTER.exists()
    OUTER.write_text(json.dumps({'phase':'coordinator-helper evidence seal; not statement freeze',
      'proof_authorized':False,'historical_referee_reports_and_seals_unchanged':True,
      'scope':'verification/statement-gate-preflight/**',
      'excluded_paths':[OUTER.relative_to(P).as_posix()],
      'exclusion_rule':'Only the exact outer path is excluded; every nested receipt/result/snapshot is included.',
      'files':members()},sort_keys=True,indent=2)+'\n')
    print('Own preflight evidence sealed; historical reports and seals untouched.')
