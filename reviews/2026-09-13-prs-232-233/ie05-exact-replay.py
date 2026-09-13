"""Independent integer/rational replay, reading only active Lean literals."""
import ast
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path

root = Path('/private/tmp/nla-audit-232/linear-systems-and-elimination/IE-05/lean')
source = (root / 'NLA/IE05/Definitions.lean').read_text()

def arrays(name):
    text = source.split('def ' + name + ' :', 1)[1].split('\ndef ', 1)[0]
    return {b: ast.literal_eval(re.search(r'\| ' + b + r' => (.*?)(?=\n  \| |\Z)', text, re.S).group(1).replace('!', '').strip()) for b in ['false', 'true']}

H, D, T = (arrays(n) for n in ['integerH', 'integerD', 'integerT'])

def matmul(a, b):
    return [[sum(a[i][r] * b[r][j] for r in range(8)) for j in range(8)] for i in range(8)]

results = {}
for flag in ['false', 'true']:
    h, d, t = H[flag], D[flag], T[flag]
    lower = [[1 if i == j else -1 if i > j else 0 for j in range(8)] for i in range(8)]
    if flag == 'true':
        lower[7][1] = 0
    assert matmul(list(map(list, zip(*h))), h) == [[d[i] if i == j else 0 for j in range(8)] for i in range(8)]
    assert matmul(lower, t) == h
    assert all(d[j] > 0 and t[j][j] > 0 for j in range(8))
    assert all(t[i][j] == 0 for i in range(8) for j in range(i))
    # Direct exact elimination on H; fixed positive column normalization cancels
    # in each multiplier and does not affect which row is largest in one column.
    state = [[F(x) for x in row] for row in h]
    stages, ties, active_count = [], [], 0
    for k in range(8):
        colmax = max(abs(state[i][k]) for i in range(k, 8))
        tied = [i for i in range(k, 8) if abs(state[i][k]) == colmax]
        assert colmax > 0 and tied[0] == k
        ties.append(tied)
        values = []
        for i in range(k, 8):
            for j in range(k, 8):
                tail = sum(lower[i][r] * t[r][j] for r in range(k, 8))
                assert state[i][j] == tail
                values.append(F(state[i][j] ** 2, d[j]))
                active_count += 1
                if flag == 'false':
                    assert tail ** 2 <= 5462 * d[j]
        stages.append(max(values))
        pivot = state[k][k]
        state = [[state[i][j] - state[i][k] / pivot * state[k][j] if i > k and j > k else F(0) for j in range(8)] for i in range(8)]
    assert all(x == 0 for row in state for x in row)
    if flag == 'true':
        assert all(5272 * h[i][j] ** 2 <= 3969 * d[j] for i in range(8) for j in range(8))
        assert stages == [F(x*x, 5272) for x in [63,94,173,338,672,1342,2683,5272]]
        assert max(stages) / stages[0] == F(5272, 63) ** 2
    else:
        assert stages == [F(2601, 3286)] + [F(x*x, 5462) for x in [96,176,344,684,1366,2731,5462]]
        assert max(stages) / stages[0] == F(17948132, 2601)
    results[flag] = {'label': 'witness' if flag == 'true' else 'candidate', 'gram_and_lu': 'PASS', 'active_entries_checked': active_count, 'first_available_ties_zero_based': ties, 'squared_stage_maxima': list(map(str, stages)), 'squared_growth': str(max(stages)/stages[0])}

gap = F(results['true']['squared_growth']) - F(results['false']['squared_growth'])
assert gap == F(117335164,1147041) and gap > 0

# Inventory the actual local import graph, excluding historical source copies.
todo, seen, imports = ['Solution'], {}, {}
while todo:
    name = todo.pop()
    if name in seen:
        continue
    file = root / (name.replace('.', '/') + '.lean')
    body = file.read_text()
    # All active files use unnested prose comments. Strip comments before scanning.
    clean = re.sub(r'/\-.*?\-/', '', body, flags=re.S)
    clean = re.sub(r'--[^\n]*', '', clean)
    assert not re.search(r'\b(sorry|axiom|native_decide|unsafe|partial|run_elab|implemented_by)\b', clean)
    imps = re.findall(r'^import\s+(\S+)', clean, flags=re.M)
    assert 'Challenge' not in imps
    imports[name] = imps
    seen[name] = hashlib.sha256(file.read_bytes()).hexdigest()
    todo.extend(i for i in imps if (root / (i.replace('.', '/') + '.lean')).exists())

def statements(filename):
    content = (root / filename).read_text()
    content = re.sub(r'/\-.*?\-/', '', content, flags=re.S)
    return {name: re.sub(r'\s+', ' ', signature).strip() for name, signature in re.findall(r'\btheorem\s+(\w+)(.*?)\s*:=', content, flags=re.S)}

challenge = statements('Challenge.lean')
proof = statements('NLA/IE05/Proof.lean')
assert len(challenge) == len(proof) == 17 and challenge == proof
expected = json.loads((root / 'comparator.json').read_text())['theorem_names']
assert expected == ['NLA.IE05.' + name for name in proof]
assert len(seen) == 13

report = {'result': 'PASS', 'reviewed_head': '5ce3e36cacbebcafda267eb6a9f2a42c461b189b', 'method': 'Independent Python integer/Fraction arithmetic and active-source inspection; not Lean compilation or CI authentication', 'source_hashes': seen, 'active_import_graph': imports, 'statement_text_matches': len(proof), 'arithmetic': results, 'squared_growth_gap': str(gap), 'total_active_entries': sum(r['active_entries_checked'] for r in results.values()), 'canonical_pdf_sha256': hashlib.sha256((root.parent / 'problem.pdf').read_bytes()).hexdigest()}
Path('/private/tmp/nla-pr232-independent-exact-checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'result':'PASS','source_modules':len(seen),'matching_exports':len(proof),'active_entries':report['total_active_entries'],'squared_growth_gap':str(gap)}))
