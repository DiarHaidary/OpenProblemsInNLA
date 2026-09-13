#!/usr/bin/env python3
"""One-shot packaging-author seal. Reviewers use verify_inventory.py read-only."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
E = Path(__file__).resolve().parent
P = E.parents[1]
OUTER = 'verification/candidate-inputs.json'

def main():
    target = P / OUTER
    if target.exists():
        raise RuntimeError('Refusing to overwrite a candidate seal; preserve this phase and make an explicit later-phase record')
    spec = importlib.util.spec_from_file_location('ie05_candidate_inventory', E / 'verify_inventory.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    checked = verifier.verify(preseal=True)
    files = {p.relative_to(P).as_posix(): verifier.record(p)
             for p in sorted(P.rglob('*')) if p.is_file() and p.relative_to(P).as_posix() != OUTER}
    selection = json.dumps(files, sort_keys=True, separators=(',', ':')).encode()
    result = {
        'root': '.', 'path_convention': 'project-relative POSIX paths',
        'phase': 'completed mathematical proof candidate; packaging-author handoff before independent package and actual Linux gates',
        'author': 'OpenAI Codex /root/ie05_final_math_referee1 in subsequent packaging-author role',
        'exact_self_exclusion': OUTER,
        'scope': 'Every regular candidate-project file except exactly verification/candidate-inputs.json; includes all historical inventories, prior attempts, accepted reviews, old wrapper archives and new package-author checks',
        'no_other_exclusions': True,
        'file_count': len(files), 'selection_sha256': hashlib.sha256(selection).hexdigest(),
        'original_accepted_files': checked['original_accepted_files'],
        'historical_inventory_count': checked['historical_inventory_count'],
        'actual_linux_comparator': 'pending', 'independent_packaging_approval': 'pending',
        'canonical_status': 'Solved', 'whole_problem_verified': False,
        'files': files,
    }
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'candidate_manifest': OUTER, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                      'selected_files': len(files), 'selection_sha256': result['selection_sha256']}, indent=2))

if __name__ == '__main__':
    main()
