from pathlib import Path
import re, json, hashlib, subprocess, math
import sympy as sp

repo = Path('/private/tmp/nla-audit-251')
project = repo / 'nonnegative-and-positive-factorizations/NR-03/lean'

def strip_comments(s):
    out, i, depth, string = [], 0, 0, False
    while i < len(s):
        if depth:
            if s.startswith('/-', i): depth += 1; i += 2
            elif s.startswith('-/', i): depth -= 1; i += 2
            else:
                out.append('\n' if s[i] == '\n' else ' '); i += 1
        elif string:
            out.append(s[i])
            if s[i] == '\\' and i + 1 < len(s):
                i += 1; out.append(s[i])
            elif s[i] == '"': string = False
            i += 1
        elif s.startswith('/-', i): depth = 1; i += 2; out.append(' ')
        elif s.startswith('--', i):
            j = s.find('\n', i)
            i = len(s) if j < 0 else j
        else:
            if s[i] == '"': string = True
            out.append(s[i]); i += 1
    assert depth == 0
    return ''.join(out)

closure, external = {}, set()
def visit(module):
    path = project / (module.replace('.', '/') + '.lean')
    if not path.exists(): external.add(module); return
    if module in closure: return
    raw = path.read_text()
    source = strip_comments(raw)
    closure[module] = source
    for line in re.findall(r'^import\s+(.+)$', source, re.M):
        for child in line.split(): visit(child)

visit('Solution')
assert len(closure) == 58
batch = [m for m in closure if '.RowCertificate.' in m]
assert len(batch) == 48
assert 'Challenge' not in closure
assert 'NLA.NR03.CertificateData' not in closure
for family in ('Singleton', 'Pair', 'Four'):
    assert {f'NLA.NR03.RowCertificate.{family}.Block{i:02}' for i in range(16)} <= closure.keys()

dangerous = re.compile(r'\b(?:sorry|admit|axiom|native_decide|unsafe|implemented_by|sorryAx|run_tac|run_cmd)\b')
hits = [(m, line_no, line.strip()) for m, src in closure.items()
        for line_no, line in enumerate(src.splitlines(), 1) if dangerous.search(line)]
assert not hits, hits
assert all('set_option autoImplicit false' in source for source in closure.values())

def declarations(src):
    return {m.group(1): re.sub(r'\s+', '', m.group(2))
            for m in re.finditer(r'^theorem\s+(\w+)\s*([\s\S]*?):=\s*by', src, re.M)}
challenge = declarations(strip_comments((project / 'Challenge.lean').read_text()))
rank = declarations(closure['NLA.NR03.Rank'])
comparator = json.loads((project / 'comparator.json').read_text())
exported = comparator['theorem_names']
assert len(exported) == 10
for full_name in exported:
    name = full_name.split('.')[-1]
    assert challenge[name] == rank[name], name
    assert sum(len(re.findall(r'^theorem\s+' + re.escape(name) + r'\b', src, re.M))
               for src in closure.values()) == 1
    assert f'#assert_trust kernel {full_name}' in closure['Solution']
    assert f'#print axioms {full_name}' in closure['Solution']
assert set(challenge) == {name.split('.')[-1] for name in exported}
assert comparator['permitted_axioms'] == ['propext', 'Classical.choice', 'Quot.sound']

family_source = closure['NLA.NR03.FamilyIdentities']
for family in ('Singleton', 'Pair', 'Four'):
    rows = re.findall(r'exact RowCertificate\.' + family + r'\.row(\d+)\b', family_source)
    assert list(map(int, rows)) == list(range(128))

manifest = json.loads((project / 'ACTIVE-MODULE-MANIFEST.json').read_text())
actual_paths = {m.replace('.', '/') + '.lean' for m in closure}
assert actual_paths == {record['path'] for record in manifest['active_modules']}
for record in manifest['active_modules']:
    raw = (project / record['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == record['sha256']
    assert len(raw) == record['bytes']

verified = 'f664d07e82aaa60bc9c78dd1946e763168c5c530'
for path in actual_paths | {'Challenge.lean', 'comparator.json', 'lakefile.toml', 'lake-manifest.json', 'lean-toolchain'}:
    relative = str((project / path).relative_to(repo))
    prior = subprocess.check_output(['git', 'show', f'{verified}:{relative}'], cwd=repo)
    assert prior == (project / path).read_bytes(), relative

base = '752218e5417998b7f4d2aee9c447ca5d256fe530'
registry = (repo / 'problem_ids.json').read_bytes()
assert registry == subprocess.check_output(['git', 'show', f'{base}:problem_ids.json'], cwd=repo)
ids = json.loads(registry)
canonical = 'nonnegative-and-positive-factorizations/NR-03/README.md'
now = (repo / canonical).read_text()
old = subprocess.check_output(['git', 'show', f'{base}:{canonical}'], cwd=repo).decode()
heading = '## Context'
assert heading in now and heading in old
assert now[now.index(heading):] == old[old.index(heading):]

# This audit independently checks the closed family polynomial and all finite
# cardinality cases, without loading any submitted numerical verifier/data.
p, t = sp.symbols('p t')
lhs = (p-1)**2*(t-1)**2 - (t-1)**2*(p-t-1)**2
middle = t*(t-1)**2*(2*p-2-t)
rhs = 2*(p-2)*t*(t-1) + 2*(p-t)*t*(t-1)*(t-2) + t*(t-1)*(t-2)*(t-3)
assert sp.expand(lhs-middle) == sp.expand(middle-rhs) == 0
cases = []
for s in range(8):
    for overlap in range(s+1):
        g = (1-overlap)**2 * (1-(s-overlap))**2
        e = 1-overlap if s == 1 else 0
        pair = 4*max(s-2, 0)*math.comb(overlap, 2)
        four = 12*((s-overlap)*math.comb(overlap, 3) + 2*math.comb(overlap, 4))
        d = 1 if s <= 1 else (s-1)**2
        assert d > 0 and min(g, e, pair, four) >= 0
        assert g + e + pair + four == d*(1-overlap)**2
        cases.append([s, overlap, g, e, pair, four, d])
assert len(cases) == 36
result = {
    'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode().strip(),
    'active_module_count': len(closure), 'batch_module_count': len(batch),
    'non_batch_modules': sorted(set(closure)-set(batch)),
    'external_imports': sorted(external), 'forbidden_source_hits': hits,
    'challenge_contracts_identical': exported,
    'aggregate_row_references': {x: 128 for x in ('Singleton','Pair','Four')},
    'manifest_hashes_match': True,
    'active_sources_and_boundary_byte_identical_to_verified_commit': verified,
    'original_context_and_problem_bytes_preserved_from': base,
    'registry_preserved': True, 'registry_count': len(ids),
    'polynomial_identity_symbolically_exact': True,
    'finite_cardinality_cases': cases,
    'scope': 'Independent structural source and exact arithmetic review; no local Lean compilation or remote CI authentication.'
}
Path('/private/tmp/nla-251-structural-check.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'finite_cardinality_cases'}, indent=2))
