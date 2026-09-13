#!/usr/bin/env python3
"""Specialize the sealed declaration-closure inspector to the two frozen contracts."""
from pathlib import Path
import hashlib

P = Path(__file__).resolve().parents[2]
old = P / 'verification/spectral-development/Inspect.lean'
assert hashlib.sha256(old.read_bytes()).hexdigest() == '0eba246cae16b7faae8ab69afc3e626f18a7c2c5cf9616469ef83aeb6a362e39'
text = old.read_text().replace('import NLA.KE04.Spectral\n', 'import NLA.KE04.SpectralWindow\n')
text = text.replace('SpectralExpected', 'SpectralWindowExpected')
start = text.index('namespace NLA.KE04.SpectralWindowExpected')
end = text.index('end NLA.KE04.SpectralWindowExpected') + len('end NLA.KE04.SpectralWindowExpected')
expected = '''namespace NLA.KE04.SpectralWindowExpected

def compression_basis_independent : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian) (Q R : Rect n m),
    Q.transpose * Q = 1 → R.transpose * R = 1 → columnSpace Q = columnSpace R →
    (∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R

def spectral_window_subspace : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian) (Q : Rect n m),
    Q.transpose * Q = 1 → ∀ (i p : ℕ), i + p < m →
    ∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0

end NLA.KE04.SpectralWindowExpected'''
text = text[:start] + expected + text[end:]
roots = ['compression_basis_independent', 'orthonormal_span_form_nonpos', 'spectral_window_subspace']
start = text.index('  let pairs := [')
end = text.index('  for (actual, reference)', start)
text = text[:start] + '  let pairs := [\n' + ',\n'.join(
    '    (``NLA.KE04._proved.' + n + ', ``NLA.KE04.SpectralWindowExpected.' + n + ')'
    for n in [roots[0], roots[2]]) + ']\n' + text[end:]
text = text.replace('[``NLA.KE04._proved.quadratic_apply_eigenvector]',
                    '[``NLA.KE04._proved.orthonormal_span_form_nonpos]')
required = ['NLA.KE04._proved.act_mul', 'NLA.KE04._proved.act_transpose_act',
    'NLA.KE04._proved.inner_act_left', 'NLA.KE04._proved.columnSpace_eq_range_act',
    'NLA.KE04._proved.frameProjection_fixed_iff', 'NLA.KE04._proved.frameProjection_act',
    'NLA.KE04._proved.orderedSpectrum_semantics', 'NLA.KE04._proved.quadratic_apply_eigenvector',
    'NLA.KE04._proved.orthonormal_span_form_nonpos', 'NLA.KE04.compression',
    'NLA.KE04.compressedQuadratic', 'NLA.KE04.ritzValues', 'NLA.KE04.ritzValueAt',
    'NLA.KE04.orderedEigenvalues', 'NLA.KE04.orderedEigenbasis', 'NLA.KE04.columnSpace',
    'Matrix.charpoly_mul_comm', 'Matrix.charpoly_toLin', 'mul_eq_one_comm',
    'LinearMap.IsSymmetric.eigenvalues_eq_eigenvalues_iff',
    'Orthonormal.comp', 'Orthonormal.linearIndependent', 'Orthonormal.inner_sum',
    'finrank_span_eq_card', 'Submodule.mem_span_range_iff_exists_fun']
start = text.index('  let required := [')
end = text.index('  for need in required', start)
text = text[:start] + '  let required := [' + ',\n    '.join('``' + n for n in required) + ']\n' + text[end:]
text = text[:text.index('#assert_trust kernel')]
for name in roots:
    text += '#assert_trust kernel NLA.KE04._proved.' + name + '\n'
    text += '#print axioms NLA.KE04._proved.' + name + '\n'
for name in ['orderedEigenvalues', 'orderedEigenbasis', 'ritzValues', 'ritzValueAt',
             'compression', 'compressedQuadratic']:
    text += 'set_option pp.all true in\n#print NLA.KE04.' + name + '\n'
for name in roots:
    text += 'set_option pp.proofs true in\n#print NLA.KE04._proved.' + name + '\n'
target = P / 'verification/spectral-window-development/Inspect.lean'
assert not target.exists()
target.write_text(text)
print(hashlib.sha256(target.read_bytes()).hexdigest())
