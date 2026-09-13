#!/usr/bin/env python3
"""Adapt the sealed receipt verifier to the exact final completion evidence."""
from pathlib import Path
import hashlib

P = Path(__file__).resolve().parents[2]
old = P / 'verification/spectral-window-development/verify_seal.py'
assert hashlib.sha256(old.read_bytes()).hexdigest() == '1094ec38f7cdefdec5207b471400dc9060a846bfd4ceca6be58517f6ce6821f9'
s = old.read_text().replace('spectral-window-development', 'completion-development')
s = s.replace('SpectralWindow.lean', 'Completion.lean').replace('NLA-KE04-SpectralWindow', 'NLA-KE04-Completion')
s = s.replace('SpectralWindowExpected', 'CompletionExpected')
s = s.replace('c59a80ed6a6dff4e879fb6b8ca602a1d0946ef29b61ff400ffba0122bc86760f',
    '4014011a7c6435c362ce4cf304aed8d7a8ad2e32ffb03448fbf43223c59a3f97')
s = s.replace('b7ad5ff8b97294567ccec35990803a6e94c22cbb2cb5a8208fa07492af9d4382',
    '317c5228a570227cfe4afe5b5a27240fd817a91a167c7a8bd75d94ea8cc9d3ed')
start = s.index('PRIOR = {')
end = s.index('ALLOWED = ', start)
s = s[:start] + '''PRIOR = {
    'verification/spectral-window-development/EVIDENCE-MANIFEST.json': '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c',
    'verification/transport-intersection-handoff/EVIDENCE-MANIFEST.json': 'b3232d8adb072dc44447a2a1f6f806f709bc55b4201b85d680d557645d9d72e8',
    'verification/nonannihilation-development/EVIDENCE-MANIFEST.json': 'd57bb205a29e51eefa1e1d67f662f052875a58961c750f6930028408251def68'}
BUILD_SEALS = {'verification/spectral-window-development/EVIDENCE-MANIFEST.json':
    '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c'}
TARGETS = ['strictIntervalOccupancy', 'blockLanczosConjecture']
ROOTS = TARGETS + ['psd_form_nonneg']
ATTEMPTS = [('attempt-c7o2c3cd', True, 9), ('attempt-700n3s8e', True, 10)]
''' + s[end:]
s = s.replace("r'\\b(.*?):=\\s*by'", "r'\\b(.*?):='")
s = s.replace('assert len(prior) == 2245', 'assert len(prior) == 3047')
s = s.replace("'seals': PRIOR, 'all_match': True, 'bound_files': 2245", "'seals': BUILD_SEALS, 'all_match': True, 'bound_files': 2764")
s = s.replace("assert sha(a / 'inputs' / r) == expected, (name, r)", "assert sha(a / 'inputs' / r) == expected, (name, r)\n            if r in prior:\n                assert prior[r] == expected, (name, r)")
s = s.replace('== 43 and set(axes)', '== 104 and set(axes)')
s = s.replace('== 37\n', '== 89\n')
s = s.replace('== 25 and set(required)', '== 22 and set(required)')
s = s.replace('PROJECT_COUNTS declarations=43, required=25', 'PROJECT_COUNTS declarations=104, required=22')
start = s.index("    api = E / 'api-sources'")
end = s.index('    bound = None', start)
s = s[:start] + '''    capture = E / 'imported-helper-checks'
    assert read(capture / 'before.json') == read(capture / 'after.json')
    binding = read(capture / 'before.json')
    assert binding['seals'] == PRIOR and binding['files'] == prior
    assert binding['file_count'] == 3047
    commands = read(capture / 'commands.json')
    assert len(commands) == 3
    for i, c in enumerate(commands):
        assert c['exit'] == 0 and c['read_only_branch'] is True
        assert not (capture / c['stderr']).read_bytes()
        assert sha(capture / ('executed-verifier-' + str(i) + '.py')) == c['executed_verifier_sha256']
        original = Path(c['argv'][1])
        relative = str(original).split('/next-ke04-statements-draft/lean/', 1)[1]
        assert sha(P / relative) == c['executed_verifier_sha256']
    assert read(capture / '0.stdout')['status'] == 'SEALED_KE04_SPECTRAL_WINDOW_PASS'
    assert read(capture / '1.stdout')['pass'] is True
    assert read(capture / '2.stdout')['status'] == 'VERIFIED'
    assert commands[2]['argv'][-1] == '--verify'
    final_warnings = []
    reports = 0
    for log in a.glob('compile-*.stdout'):
        content = log.read_text()
        assert 'error:' not in content and 'sorryAx' not in content
        reports += len(re.findall(r"^'[^']+' depends on axioms:", content, re.M))
        final_warnings.extend((log.name, line) for line in content.splitlines() if 'warning:' in line)
    assert len(final_warnings) == 1
    assert final_warnings[0][0] == 'compile-NLA-KE04-Krylov.stdout'
    assert 'Krylov.lean:107:25: warning: This simp argument is unused:' in final_warnings[0][1]
    assert reports == 56
''' + s[end:]
s = s.replace('KE04_SPECTRAL_WINDOW_PREFLIGHT_PASS', 'KE04_COMPLETION_PREFLIGHT_PASS')
s = s.replace('SEALED_KE04_SPECTRAL_WINDOW_PASS\',\n', 'SEALED_KE04_COMPLETION_PASS\',\n')
# Only the final response status changes; the imported helper status remains exact.
s = s.replace("else 'SEALED_KE04_SPECTRAL_WINDOW_PASS'", "else 'SEALED_KE04_COMPLETION_PASS'")
s = s.replace("'scope': 'bounded author helper completion'", "'scope': 'complete target proof author assembly; final verification gates remain' ")
s = s.replace("'final_fresh_Lean_commands': 5, 'warnings': 0, 'actual_project_closure': 43", "'final_fresh_Lean_commands': 10, 'new_source_and_inspector_warnings': 0,\n        'inherited_Krylov_warnings': 1, 'actual_project_closure': 104")
s = s.replace("'required_material_dependencies': 25", "'required_material_dependencies': 22")
s = s.replace("'fresh_attempts': 4, 'historical_failed_new_module_compiles': 2", "'fresh_attempts': 2, 'historical_failed_new_module_compiles': 0")
s = s.replace("'preserved_imported_seal_files': 2245", "'preserved_imported_seal_files': 3047")
s = s.replace("'new_API_Git_bindings': 6", "'actual_imported_read_only_checks': 3, 'final_actual_axiom_reports': 56")
target = P / 'verification/completion-development/verify_seal.py'
assert not target.exists()
target.write_text(s)
print(hashlib.sha256(target.read_bytes()).hexdigest())
