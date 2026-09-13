#!/usr/bin/env python3
"""Read-only RA-20 publication preservation audit. No network/build/cache writes.

Run in a checkout containing the original Git objects and complete evidence:
  PYTHONDONTWRITEBYTECODE=1 python3 verify_publication.py [--check-own-seal]
This checks preserved evidence; it does not execute Lean or grant a new
mathematical/kernel/operational approval. Visual review is recorded separately.
"""
from pathlib import Path
import argparse, collections, hashlib, json, os, re, subprocess

E = Path(__file__).resolve().parent
P = E.parents[1]
R = P.parents[2]
A = P / 'verification/publication-preparation-2026-09-13'
OUTER = A / 'EVIDENCE-MANIFEST.json'
SELF = E / 'EVIDENCE-MANIFEST.json'
REPORT = P / 'reviews/publication-referee-2026-09-13.md'
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
CANDIDATE = '43603b173beb294c2588d83f936a8a96246fd5f0'
OLD_README = '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
DIAGNOSTIC = 'verification/root-linux-acceptance-2026-09-13/initial-scope-diagnostic/EVIDENCE-MANIFEST.json'
PIN = {'EVIDENCE-MANIFEST.json': '3a2dbd0aa48277f7b5d87bd3b2f1e4e5a2abec571215de85783b10063bcb629a',
       'HANDOFF.md': 'd73c0ef739f1e86fb80b721be7b0d1978c486ffb98c8e607a62d751076762f4e',
       'VALIDATION.json': '7b90acaf9c5a989dd93ce5f1569ff290ded6a807655a50db3773d014e730680c',
       'PREFLIGHT.json': 'ca08a0e2f2525dd009ee41e7fe99fd0e8d55d54f26884508334c3702bf555b16'}

def unique(pairs):
    d = {}
    for k, v in pairs:
        assert k not in d, ('duplicate key', k)
        d[k] = v
    return d

def load(p):
    return json.loads(p.read_text(), object_pairs_hook=unique)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def sha(p):
    assert p.is_file() and not p.is_symlink(), ('not regular file', str(p))
    return digest(p.read_bytes())

def canonical(p):
    assert not p.is_symlink(), ('symlink input', str(p))
    q = p.resolve()
    assert q.is_relative_to(R), ('outside repository', str(p))
    return q

def command(args, data=None):
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    r = subprocess.run(['git', '-c', 'core.fsmonitor=false'] + args, input=data,
                       cwd=R, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert r.returncode == 0, (args, r.returncode, r.stderr.decode())
    return r.stdout

def verify(check_own=False):
    for n, h in PIN.items():
        assert sha(A/n) == h, ('supplied pin mismatch', n)
    outer = load(OUTER)
    baseline = load(A/'PREFLIGHT.json')
    validation = load(A/'VALIDATION.json')
    archives = load(A/'ARCHIVES.json')['archives']
    mapping = {(canonical(R/x['original_repository_path']), x['expected_sha256']):
               canonical(P/x['archive_project_path']) for x in archives}
    assert len(mapping) == len(archives) == 19
    mapping[(P/'README.md', OLD_README)] = P/'verification/pre-candidate-README.md'
    assert len(mapping) == 20
    mapped = collections.Counter()
    checked = set()

    def file(p, value, historical=False):
        h = value if isinstance(value, str) else value['sha256']
        q = canonical(p)
        if historical and (q, h) in mapping:
            mapped[(str(q.relative_to(R)), h, str(mapping[(q,h)].relative_to(R)))] += 1
            q = mapping[(q, h)]
        assert sha(q) == h, ('hash mismatch', str(p), h)
        if isinstance(value, dict) and 'bytes' in value:
            assert q.stat().st_size == value['bytes'], ('size mismatch', str(q))
        checked.add(q)
        return q

    bound = {canonical(A/n) for n in outer['files']}
    assert len(bound) == len(outer['files']) == outer['file_count'] == 1791
    assert OUTER not in bound and outer['exact_self_exclusion'] == 'EVIDENCE-MANIFEST.json'
    for n, v in outer['files'].items():
        file(A/n, v)
    prior = {canonical(P/n) for n in baseline['project_baseline']}
    own_author = {canonical(q) for q in A.rglob('*') if q.is_file() and q != OUTER}
    assert len(prior) == 1580 and len(own_author) == 164
    assert {q for q in bound if q.is_relative_to(P)} == prior | own_author
    assert len(prior | own_author) == 1744
    root_outer = P/'verification/root-linux-acceptance-2026-09-13/EVIDENCE-MANIFEST.json'
    external = {canonical(root_outer.parent/n) for n in load(root_outer)['files']}
    external |= {canonical(R/n) for n in baseline['other_publication_inputs']}
    external |= {R/n for n in ['tools/render_problems.py', 'tools/update_catalog.py',
                              'tools/format_math.py', 'tools/problem-template.tex',
                              'tools/github_math.lua', 'tests/test_problem_ids.py']}
    external = {q for q in external if not q.is_relative_to(P)}
    assert len(external) == 47 and {q for q in bound if not q.is_relative_to(P)} == external
    changed = []
    for base, entries in [(P, baseline['project_baseline']), (R, baseline['other_publication_inputs'])]:
        for n, v in entries.items():
            file(base/n, v, True)
            if sha(base/n) != v['sha256']:
                changed.append(str((base/n).relative_to(R)))
    assert sorted(changed) == validation['changed_existing_paths'] and len(changed) == 9
    for (old, h), archive in mapping.items():
        file(archive, h)

    manifests = validation['accepted_prior_inventories']
    discovered = {n for n in baseline['project_baseline']
                  if n.endswith('/EVIDENCE-MANIFEST.json') or n == 'reviews/statement-package-manifest.json'}
    assert discovered == {v['file'] for v in manifests} | {DIAGNOSTIC}
    assert len(manifests) == 19
    nested = []
    for item in manifests:
        p = P/item['file']
        file(p, item['sha256'])
        m = load(p)
        base = P if p.name == 'statement-package-manifest.json' else p.parent
        assert len(m['files']) == item['entries']
        if 'file_count' in m:
            assert m['file_count'] == len(m['files'])
        mbound = {canonical(base/n) for n in m['files']}
        assert len(mbound) == len(m['files']) and p not in mbound
        for n, v in m['files'].items():
            assert file(base/n, v, True) in bound, ('nested target not in author seal', item['file'], n)
        if p.name == 'statement-package-manifest.json':
            expected = set(load(P/'reviews/statement-freeze.json')['files'])
            expected |= {'reviews/statement-freeze.json', 'reviews/statement-handoff.md'}
            assert set(m['files']) == expected and len(expected) == 70
            own_count = 70
        else:
            actual_own = {q for q in prior if q.is_relative_to(p.parent) and q != p}
            assert {q for q in mbound if q.is_relative_to(p.parent)} == actual_own
            assert {canonical(q) for q in p.parent.rglob('*') if q.is_file() and q != p} == actual_own
            own_count = len(actual_own)
        nested.append(dict(item, complete_frozen_own_membership=own_count))
    diagnostic = P/DIAGNOSTIC
    failure = load(diagnostic.parent/'observed-failure.json')
    assert diagnostic in bound and len(load(diagnostic)['files']) == 1596
    assert failure['observed_tool_exit_code'] == 1 and 'incomplete and is not counted' in failure['reason']
    assert canonical(diagnostic.parent/'observed-failure.json') in bound

    freezes = [(load(P/'verification/proof-freeze.json'), 521),
               (load(P/'reviews/statement-freeze.json'), 68)]
    for m, count in freezes:
        assert len(m['files']) == count
        for n, h in m['files'].items():
            file(P/n, h, True)
    proof, statement = freezes[0][0], freezes[1][0]
    assert proof['source_files'] == statement['source_files'] and len(proof['source_files']) == 16
    original_records = []
    for n, h in proof['source_files'].items():
        data = command(['show', BASE+':'+n])
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest(data) == h and blob == proof['source_git_blobs'][n]
        file(R/n, h, True)
        file(P/'verification/original-sources'/n, h)
        original_records.append({'path':n,'sha256':h,'git_blob':blob})

    binding = load(P/'verification/linux-run-2026-09-13/source-binding.json')
    assert binding['candidate'] == CANDIDATE and len(binding['candidate_inputs']) == 1092
    prefix = str(P.relative_to(R))+'/'
    tree = command(['ls-tree', '-rz', CANDIDATE, '--', prefix]).split(b'\0')
    rows = []
    for row in tree:
        if not row:
            continue
        head, path = row.split(b'\t',1)
        mode, kind, oid = head.decode().split()
        n = path.decode()
        assert mode == '100644' or mode == '100755'
        assert kind == 'blob' and n.startswith(prefix)
        rows.append((n,oid))
    assert len(rows) == 1092 and {n[len(prefix):] for n,_ in rows} == set(binding['candidate_inputs'])
    data = command(['cat-file', '--batch'], ''.join(oid+'\n' for _,oid in rows).encode())
    offset = 0
    for n, oid in rows:
        end = data.index(b'\n',offset)
        actual_oid, kind, size = data[offset:end].decode().split()
        size = int(size)
        raw = data[end+1:end+1+size]
        offset = end+2+size
        v = binding['candidate_inputs'][n[len(prefix):]]
        assert kind == 'blob' and actual_oid == oid == v['git_blob']
        assert size == v['bytes'] and digest(raw) == v['sha256'] and data[offset-1:offset] == b'\n'
        assert file(R/n,v,True).read_bytes() == raw
    assert offset == len(data)

    config = load(P/'comparator.json')
    runtime = load(P/'verification/linux-run-2026-09-13/runtime-verification.json')
    ax = load(P/'verification/linux-run-2026-09-13/axiom-verification.json')
    gate = load(P/'verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json')
    assert gate['fully_verified'] and gate['verdict'] == 'ACCEPT complete-target Lean verification'
    assert runtime['candidate'] == CANDIDATE and runtime['run'] == 34743832047 and runtime['run_attempt'] == 1
    assert runtime['all17_jobs_and_steps_successful'] is True
    assert len(config['theorem_names']) == 12 and len(set(config['theorem_names'])) == 12
    assert config['definition_names'] == [] and set(config['permitted_axioms']) == {'propext','Classical.choice','Quot.sound'}
    assert runtime['actual_exports'] == config['theorem_names']
    assert runtime['source_kernel_assertions'] == 61
    assert runtime['actual_printed_standard_three_axiom_occurrences'] == len(ax['records']) == 57
    assert runtime['distinct_printed_names'] == 45 and runtime['official_matching_Mathlib_cache_files'] == 8690
    source_texts = [(P/'Solution.lean').read_text()] + [q.read_text() for q in sorted((P/'NLA/RA20').glob('*.lean'))]
    assert sum(len(re.findall(r'^#assert_trust kernel ',t,re.M)) for t in source_texts) == 61
    assert sum(len(re.findall(r'^#print axioms ',t,re.M)) for t in source_texts) == 57
    for n in config['theorem_names']:
        short = n.rsplit('.',1)[1]
        assert '`'+short+'`' in (P/'README.md').read_text() and '`'+short+'`' in (P.parent/'README.md').read_text()

    canonical_now = (P.parent/'README.md').read_bytes()
    canonical_old = command(['show', BASE+':'+str((P.parent/'README.md').relative_to(R))])
    assert canonical_now[canonical_now.index(b'## Statement\n'):] == canonical_old[canonical_old.index(b'## Statement\n'):]
    ids = load(R/'problem_ids.json')
    assert len(ids) == 217 and load(R/'problem_ids.json') == json.loads(command(['show', BASE+':problem_ids.json']))
    statuses = collections.Counter()
    status_inputs = {}
    for problem, n in ids.items():
        q = R/n
        assert q.is_file() and q.read_text().startswith('# '+problem+' '), ('ID/path/title mismatch', problem)
        text = q.read_text()
        match = re.search(r'^\*\*Status:\*\* (.+)$',text,re.M)
        assert match, ('no status',n)
        statuses[match.group(1).strip()] += 1
        status_inputs[n] = {'sha256':sha(q),'bytes':q.stat().st_size}
    assert statuses['Lean verified'] == 17
    assert '17 Lean verified' in (R/'README.md').read_text() and '17 Lean verified' in (R/'CATALOG.md').read_text()
    assert '22 Lean verified' not in (R/'README.md').read_text()

    document_checks = load(A/'DOCUMENT-CHECKS.json')
    for n,v in document_checks['outputs'].items():
        file(R/n,v)
    for item in document_checks['relative_paths_and_links']:
        assert canonical(R/item['target']).is_file()
        if 'sha256' in item:
            file(R/item['target'], item['sha256'])
    commands = []
    for d in sorted((A/'commands').iterdir()):
        result = load(d/'result.json')
        assert result['exit_code'] == 0
        assert sha(d/'stdout') == result['stdout_sha256']
        assert sha(d/'stderr') == result['stderr_sha256']
        command_record = load(d/'command.json')
        assert all(result[k] == v for k,v in command_record.items())
        commands.append({'directory':str(d.relative_to(P)), 'command':result['command'], 'exit_code':0})
    for d in sorted((A/'pdf-build').iterdir()):
        assert load(d/'result.json')['exit_code'] == 0
    assert (A/'pdf-build/xelatex-2/problem.pdf').read_bytes() == (P.parent/'problem.pdf').read_bytes()
    assert (A/'pdf-build/xelatex-2/problem.tex').read_bytes() == (P.parent/'problem.tex').read_bytes()
    assert 'RA-20: OK' in (A/'commands/canonical-render/stdout').read_text()
    assert not re.search(r'Overfull \\[hv]box|Missing character:',(A/'pdf-build/xelatex-2/problem.log').read_text())
    for p in [P/'README.md', P/'formalization.yaml', P.parent/'README.md']:
        t = ' '.join(p.read_text().split())
        assert all(x in t for x in ['George Stepaniants','Department of Computing and Mathematical Sciences',
                                   'California Institute of Technology','Codex','Kubjas','Sodomaco','Tsigaridas'])
    email = re.compile(rb'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
    privacy_scope = own_author | {R/n for n in changed}
    assert not [str(q.relative_to(R)) for q in privacy_scope if email.search(q.read_bytes())]

    own_count = None
    if check_own:
        seal = load(SELF)
        own = {canonical(q) for q in E.rglob('*') if q.is_file() and q != SELF} | {REPORT}
        expected = own | bound | {OUTER} | {R/n for n in status_inputs}
        actual = {canonical(E/n) for n in seal['files']}
        assert expected == actual and SELF not in actual
        assert seal['exact_self_exclusion'] == 'EVIDENCE-MANIFEST.json'
        assert len(actual) == len(seal['files']) == seal['file_count']
        for n,v in seal['files'].items():
            file(E/n,v)
        own_count = len(own)
    return {'status':'INDEPENDENT_RA20_PUBLICATION_PRESERVATION_PASS',
            'reviewer':'/root/ie05_statement_referee2', 'candidate':CANDIDATE,
            'publication_author_outer_sha256':sha(OUTER), 'complete_author_files':1791,
            'author_project_files':1744,'author_other_repository_files':47,
            'accepted_nested_inventories':nested, 'rejected_diagnostic_retained_not_accepted':DIAGNOSTIC,
            'original_Git_source_identities':original_records, 'proof_inputs':521,'statement_inputs':68,
            'actual_tested_candidate_Git_inputs_checked':1092,
            'archive_resolution_records':[{'original_path':n,'expected_sha256':h,'archive_path':a,'uses':count}
                                          for (n,h,a),count in sorted(mapped.items())],
            'changed_existing_paths':sorted(changed),'canonical_statement_tail_byte_identical':True,
            'permanent_IDs':217,'isolated_branch_status_counts':dict(statuses),
            'status_input_snapshots':status_inputs,
            'author_commands_with_verified_raw_streams':commands,
            'accepted_runtime_claims_preserved':{'run':34743832047,'attempt':1,'jobs':17,'exports':12,
                'source_kernel_assertions':61,'source_axiom_occurrences':57,'distinct_printed_names':45,
                'official_matching_dependency_cache_files':8690},
            'publication_email_like_matches':0,'own_seal_verified':check_own,'own_files_including_report':own_count,
            'new_Lean_build':False,'new_Linux_execution':False,'new_mathematical_approval':False,
            'publication_commit_push_PR_performed':False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-own-seal',action='store_true')
    print(json.dumps(verify(parser.parse_args().check_own_seal),indent=2))
