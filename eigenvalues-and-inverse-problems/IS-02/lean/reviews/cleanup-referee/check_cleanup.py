#!/usr/bin/env python3
"""Recheck the preserved cleanup mathematical token equivalence, offline."""
from pathlib import Path
import json, re
root = Path(__file__).resolve().parent
mapping = json.loads((root / 'cleanup-record/identifier-mapping.json').read_text())
assert len(mapping) == len(set(mapping.values())) == 35

def strip_comments(s):
    out = []; i = 0; depth = 0
    while i < len(s):
        if depth:
            if s[i:i+2] == '/-': depth += 1; i += 2
            elif s[i:i+2] == '-/': depth -= 1; i += 2
            else: i += 1
        elif s[i:i+2] == '/-': depth = 1; i += 2; out.append(' ')
        elif s[i:i+2] == '--':
            i = s.find('\n', i)
            if i < 0: break
            out.append('\n')
        elif s[i] == '"':
            j = i + 1
            while j < len(s):
                if s[j] == '\\': j += 2
                elif s[j] == '"': j += 1; break
                else: j += 1
            out.append(s[i:j]); i = j
        else: out.append(s[i]); i += 1
    assert depth == 0
    return ''.join(out)

for old_name, new_name in [('Proof.lean', 'NLA/IS02/Proof.lean'), ('Solution.lean','Solution.lean')]:
    old = (root / 'reviewed-source-before' / old_name).read_text()
    new = (root / 'reviewed-source' / new_name).read_text()
    old = re.sub(r'\b[A-Za-z_][A-Za-z_0-9]*\b', lambda m: mapping.get(m.group(), m.group()), old)
    before = strip_comments(old); after = strip_comments(new)
    lines = before.splitlines(); seen = False; retained = []
    for line in lines:
        if line.strip() == 'open Polynomial':
            if seen: continue
            seen = True
        retained.append(line)
    assert ' '.join('\n'.join(retained).split()) == ' '.join(after.split()), old_name
print('PASS: 35 bijective helper renames; identical mathematical tokens after comments, whitespace and redundant opens.')
