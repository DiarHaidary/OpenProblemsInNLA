#!/usr/bin/env python3
"""Read-only final checks. Recognize four exact non-address path tokens only."""
from pathlib import Path
import hashlib, json, re, zipfile

E=Path(__file__).resolve().parent
P=E.parents[1];G=P.parents[2]
REPORT=P/'reviews/linux-operational-referee-2026-09-13.md'

def checks():
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    b=json.loads((E/'source-binding.json').read_text())
    root=json.loads((P/'verification/root-candidate-2026-09-13/ROOT-CHECKS.json').read_text())
    for n,v in root['exact_hash_bound_whitespace_exceptions'].items():
        assert h(G/n)==v['sha256']
        assert b['candidate_inputs'][str((G/n).relative_to(P))]['sha256']==v['sha256']
    assert len(root['exact_hash_bound_whitespace_exceptions'])==14
    assert (E/'commands/021-id-checker-source/stdout').read_bytes()==(G/'tools/validate_problem_ids.py').read_bytes()
    allowed={
        b'/opt/homebrew/opt/python@3.13':'Homebrew versioned Python directory',
        b'actions_checkout@11d5960a326750d5838078e36cf38b85af677262.txt':'Pinned checkout action log filename',
        b'actions_setup-go@924ae3a1cded613372ab5595356fb5720e22ba16.txt':'Pinned setup-go action log filename',
        b'leanprover_lean-action@96e06131c0e9943c780388fd166f55d1e2fa0433.txt':'Pinned lean-action log filename'
    }
    workflow=(G/'.github/workflows/lean-verification.yml').read_bytes()
    for token in list(allowed)[1:]:
        action=token[:-4].replace(b'_',b'/',1)
        assert action in workflow
    assert b'/opt/homebrew/opt/python@3.13/bin/python3.13' in (E/'remaining-artifacts-retrieval.json').read_bytes()
    regex=re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
    occurrences=[];archive_members=0
    paths=[p for p in E.rglob('*') if p.is_file() and p!=E/'EVIDENCE-MANIFEST.json']+[REPORT]
    def inspect(data,name):
        for match in regex.finditer(data):
            token=match.group()
            assert token in allowed,('unrecognized address-shaped token; values not displayed',name)
            occurrences.append({'file':name,'token_sha256':hashlib.sha256(token).hexdigest(),'kind':allowed[token]})
    for path in paths:
        name=str(path.relative_to(P))
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as z:
                for item in z.infolist():
                    if not item.is_dir():
                        archive_members+=1;inspect(z.read(item),name+'::'+item.filename)
        else:inspect(path.read_bytes(),name)
    return {'status':'FINAL_SUPPLEMENTAL_AND_PRIVACY_PASS',
            'fourteen_whitespace_exception_hashes':{n:v['sha256'] for n,v in root['exact_hash_bound_whitespace_exceptions'].items()},
            'candidate_Git_ID_checker_sha256':h(G/'tools/validate_problem_ids.py'),
            'private_email_addresses_added':0,'unrecognized_address_shaped_tokens':0,
            'exact_non_address_forms_allowed':len(allowed),'recognized_path_occurrences':occurrences,
            'scanned_review_files':len(paths),'scanned_archive_members':archive_members}

if __name__=='__main__':
    r=checks();print(json.dumps({k:v for k,v in r.items() if k!='recognized_path_occurrences'},indent=2))
