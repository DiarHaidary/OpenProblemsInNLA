#!/usr/bin/env python3
"""Specialize the sealed actual-value closure inspector for the complete targets."""
from pathlib import Path
import hashlib

P = Path(__file__).resolve().parents[2]
old = P / 'verification/spectral-window-development/Inspect.lean'
assert hashlib.sha256(old.read_bytes()).hexdigest() == 'b7ad5ff8b97294567ccec35990803a6e94c22cbb2cb5a8208fa07492af9d4382'
s = old.read_text().replace('import NLA.KE04.SpectralWindow\n', 'import NLA.KE04.Completion\n')
s = s.replace('SpectralWindowExpected', 'CompletionExpected')
start = s.index('namespace NLA.KE04.CompletionExpected')
end = s.index('end NLA.KE04.CompletionExpected') + len('end NLA.KE04.CompletionExpected')
s = s[:start] + '''namespace NLA.KE04.CompletionExpected
def strictIntervalOccupancy : Prop := FullPrefixBlockLanczosClaim
def blockLanczosConjecture : Prop := BlockLanczosConjecture
end NLA.KE04.CompletionExpected''' + s[end:]
targets = ['strictIntervalOccupancy', 'blockLanczosConjecture']
roots = targets + ['psd_form_nonneg']
start = s.index('  let pairs := [')
end = s.index('  for (actual, reference)', start)
s = s[:start] + '  let pairs := [\n' + ',\n'.join(
    '    (``NLA.KE04._proved.' + n + ', ``NLA.KE04.CompletionExpected.' + n + ')'
    for n in targets) + ']\n' + s[end:]
s = s.replace('[``NLA.KE04._proved.orthonormal_span_form_nonpos]', '[``NLA.KE04._proved.psd_form_nonneg]')
required = ['NLA.KE04.IterationOccupancy', 'NLA.KE04.FullPrefixBlockLanczosClaim',
    'NLA.KE04.BlockLanczosConjecture', 'NLA.KE04.FullColumnRank', 'NLA.KE04.FullBlockDimension',
    'NLA.KE04.LastFullBlockIteration', 'NLA.KE04._proved.interval_index_validity',
    'NLA.KE04._proved.orderedSpectrum_semantics', 'NLA.KE04._proved.spectral_gap_quadratic_psd',
    'NLA.KE04._proved.compressedQuadratic_semantics', 'NLA.KE04._proved.spectral_window_subspace',
    'NLA.KE04._proved.fullBlockDimension_prefix', 'NLA.KE04._proved.krylov_intersection_nonzero',
    'NLA.KE04._proved.quadratic_forms_agree', 'NLA.KE04._proved.psd_form_nonneg',
    'NLA.KE04._proved.psd_zero_form_iff_kernel', 'NLA.KE04._proved.later_quadratic_identity',
    'NLA.KE04._proved.fullRank_quadratic_nonannihilation', 'NLA.KE04._proved.fullPrefix_implies_canonical',
    'NLA.KE04._proved.strictIntervalOccupancy', 'Matrix.isPositive_toEuclideanLin_iff',
    'LinearMap.IsPositive.inner_nonneg_right']
start = s.index('  let required := [')
end = s.index('  for need in required', start)
s = s[:start] + '  let required := [' + ',\n    '.join('``' + n for n in required) + ']\n' + s[end:]
s = s[:s.index('#assert_trust kernel')]
for name in roots:
    s += '#assert_trust kernel NLA.KE04._proved.' + name + '\n'
    s += '#print axioms NLA.KE04._proved.' + name + '\n'
for name in ['IterationOccupancy', 'FullPrefixBlockLanczosClaim', 'BlockLanczosConjecture',
             'FullBlockDimension', 'FullColumnRank', 'LastFullBlockIteration', 'IsKrylovBasis']:
    s += 'set_option pp.all true in\n#print NLA.KE04.' + name + '\n'
for name in roots:
    s += 'set_option pp.proofs true in\n#print NLA.KE04._proved.' + name + '\n'
target = P / 'verification/completion-development/Inspect.lean'
assert not target.exists()
target.write_text(s)
print(hashlib.sha256(target.read_bytes()).hexdigest())
