#!/usr/bin/env python3
"""Initialize this phase's own fresh-build driver from the sealed generic driver."""
from pathlib import Path
import hashlib

P = Path(__file__).resolve().parents[2]
old = P / 'verification/spectral-development/run-attempt.py'
assert hashlib.sha256(old.read_bytes()).hexdigest() == '0209b0bc754c6521936e0f38d78b6a717588bedc02e98fa0dc7662386c788a4d'
text = old.read_text().replace('spectral-development', 'spectral-window-development')
text = text.replace('ke04-spectral-', 'ke04-spectral-window-')
text = text.replace("'NLA/KE04/Spectral.lean'", "'NLA/KE04/SpectralWindow.lean'")
text = text.replace("'NLA/KE04/Spectral')", "'NLA/KE04/SpectralWindow')")
text = text.replace("sources = ['NLA/KE04/Definitions.lean',", "sources = ['NLA/KE04/Definitions.lean', 'NLA/KE04/Frames.lean', 'NLA/KE04/Spectral.lean',")
text = text.replace("('NLA/KE04/SpectralWindow.lean', 'NLA/KE04/SpectralWindow')", "('NLA/KE04/Frames.lean', 'NLA/KE04/Frames'),\n               ('NLA/KE04/Spectral.lean', 'NLA/KE04/Spectral'),\n               ('NLA/KE04/SpectralWindow.lean', 'NLA/KE04/SpectralWindow')")
block = '''
    imported_seals = {
        'verification/frames-development/EVIDENCE-MANIFEST.json': '73770debb7678e443032c5f30e77ef82365cd32b81d24bba161990e2ac7f8db8',
        'verification/spectral-development/EVIDENCE-MANIFEST.json': '27a8328c569a17db1e6cf671a0a79034e3ce9eb2dc85c4640d13be7624191ca2'}
    def imported(phase):
        union = {}
        for seal, expected in imported_seals.items():
            assert sha(P / seal) == expected, seal
            union[seal] = expected
            d = json.loads((P / seal).read_text())
            for r, v in d['files'].items():
                assert sha(P / r) == v['sha256'], r
                if r in union:
                    assert union[r] == v['sha256'], r
                union[r] = v['sha256']
        write(attempt / ('imported-' + phase + '.json'),
              {'seals': imported_seals, 'all_match': True, 'bound_files': len(union)})
    imported('before')
'''
text = text.replace("    sources = [", block + "    sources = [", 1)
text = text.replace("    after = {r: sha(P / r) for r in sources}", "    imported('after')\n    after = {r: sha(P / r) for r in sources}")
target = P / 'verification/spectral-window-development/run-attempt.py'
assert not target.exists()
target.write_text(text)
print(hashlib.sha256(target.read_bytes()).hexdigest())
