#!/usr/bin/env python3
"""Initialize an own fresh source build from the sealed generic driver."""
from pathlib import Path
import hashlib

P = Path(__file__).resolve().parents[2]
old = P / 'verification/spectral-window-development/run-attempt.py'
assert hashlib.sha256(old.read_bytes()).hexdigest() == 'c8635ed81b2415a42f6595afcc4fc7b1ef52ebd6f15a97510d5b10976200bf01'
s = old.read_text().replace('spectral-window-development', 'completion-development')
s = s.replace('ke04-spectral-window-', 'ke04-completion-')
start = s.index('    imported_seals = {')
end = s.index('    def imported(phase):', start)
s = s[:start] + '''    imported_seals = {
        'verification/spectral-window-development/EVIDENCE-MANIFEST.json': '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c'}
    fixed_sources = {
        'NLA/KE04/Krylov.lean': '4912fc18fe64afafdb77a3dd19647ad623b05ee87d63ce56c4fbdad933d99ef3',
        'NLA/KE04/Transport.lean': 'f8bbd7a8095c333efe899bc71aae896dd6731002f89cefa2296f09aba7ecddbb',
        'NLA/KE04/Intersection.lean': '85acdc5925c94da8c48f5840bfce5055b6660ed11529a5554953f8acd598cb95',
        'NLA/KE04/Nonannihilation.lean': 'fec6e511329419a04ba4de0bd5c69b1366e851b3ade713a78ab90cd058a866e2'}
''' + s[end:]
s = s.replace('        union = {}', '        union = dict(fixed_sources)\n        for r, expected in fixed_sources.items():\n            assert sha(P / r) == expected, r')
old_prefix = "    sources = ['NLA/KE04/Definitions.lean', 'NLA/KE04/Frames.lean', 'NLA/KE04/Spectral.lean', 'NLA/KE04/SpectralWindow.lean',"
new_prefix = "    sources = ['NLA/KE04/Definitions.lean', 'NLA/KE04/Krylov.lean', 'NLA/KE04/Frames.lean', 'NLA/KE04/Spectral.lean', 'NLA/KE04/SpectralWindow.lean', 'NLA/KE04/Transport.lean', 'NLA/KE04/Intersection.lean', 'NLA/KE04/Nonannihilation.lean', 'NLA/KE04/Completion.lean',"
assert old_prefix in s
s = s.replace(old_prefix, new_prefix)
start = s.index('    modules = [')
end = s.index('    if args.inspect:', start)
names = ['Definitions', 'Krylov', 'Frames', 'Spectral', 'SpectralWindow',
         'Transport', 'Intersection', 'Nonannihilation', 'Completion']
s = s[:start] + '    modules = [' + ',\n               '.join(
    "('NLA/KE04/" + n + ".lean', 'NLA/KE04/" + n + "')" for n in names) + ']\n' + s[end:]
target = P / 'verification/completion-development/run-attempt.py'
assert not target.exists()
target.write_text(s)
print(hashlib.sha256(target.read_bytes()).hexdigest())
