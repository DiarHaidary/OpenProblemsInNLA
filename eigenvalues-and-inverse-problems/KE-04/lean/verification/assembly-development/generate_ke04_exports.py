from pathlib import Path
import hashlib, json, re

P = Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean')
E = P / 'verification/assembly-development'
E.mkdir(exist_ok=False)
C = (P / 'Challenge.lean').read_text()
assert hashlib.sha256(C.encode()).hexdigest() == 'a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e'
headers = re.findall(r'^theorem (\w+)(.*?) := by sorry', C, re.M | re.S)
assert len(headers) == 24
out = '''import NLA.KE04.Completion

/-!
# KE-04: the complete approved theorem boundary

Every signature is copied from the independently approved original Challenge.
The implementation imports only completed proofs, never the reference Challenge.
Original mathematical proof: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA,
with substantial AI assistance. Final independent review remains a separate gate.
-/

noncomputable section
open scoped BigOperators
set_option leancert.trust "kernel"
namespace NLA.KE04

'''
records = []
for name, sig in headers:
    depth = 0
    boundary = None
    for i, char in enumerate(sig):
        if char in '({[':
            depth += 1
        elif char in ')}]':
            depth -= 1
        elif char == ':' and depth == 0:
            boundary = i
            break
    assert boundary is not None
    binders = sig[:boundary]
    args = []
    depth = 0
    start = None
    for i, char in enumerate(binders):
        if char in '({[':
            if depth == 0:
                start = i + 1
            depth += 1
        elif char in ')}]':
            depth -= 1
            if depth == 0:
                b = binders[start:i]
                assert ':' in b
                new = b.split(':', 1)[0].split()
                assert all(re.fullmatch(r'\w+', x) for x in new)
                args += new
    assert depth == 0
    implementation = '@_proved.' + name + (' ' + ' '.join(args) if args else '')
    out += 'theorem ' + name + sig + ' := by\n  exact ' + implementation + '\n\n'
    records.append({'name': name, 'frozen_signature': sig,
                    'arguments_in_source_order': args, 'implementation': implementation})
out += '\n'.join('#assert_trust kernel ' + name + '\n#print axioms ' + name for name, _ in headers)
out += '\n\nend NLA.KE04\n'
assert not (P / 'NLA/KE04/Proof.lean').exists()
(P / 'NLA/KE04/Proof.lean').write_text(out)
assert not (P / 'Solution.lean').exists()
(P / 'Solution.lean').write_text('import NLA.KE04.Proof\n')
(E / 'export-extraction.json').write_text(json.dumps({'challenge_sha256': hashlib.sha256(C.encode()).hexdigest(),
    'contracts': records, 'proof_sha256': hashlib.sha256(out.encode()).hexdigest()}, indent=2) + '\n')
(E / 'generate_ke04_exports.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'exports': len(records), 'proof_sha256': hashlib.sha256(out.encode()).hexdigest()}))
