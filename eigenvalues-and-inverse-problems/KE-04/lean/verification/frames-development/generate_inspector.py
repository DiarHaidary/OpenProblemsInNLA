#!/usr/bin/env python3
"""Generate assumption-free expected types and actual proof-graph inspection.

Traversal structure adapted from this agent's IE05 Witness diagnostic, not from
any unverified mathematical theorem. No reference proof is created or imported.
"""
from pathlib import Path
import hashlib
import json
import re

E = Path(__file__).resolve().parent
P = E.parents[1]
challenge = (P / 'Challenge.lean').read_text()
source = (P / 'NLA/KE04/Frames.lean').read_text()
contracts = ['real_matrix_semantics', 'krylovBasis_exists', 'frameProjection_semantics',
    'compression_semantics', 'compressedQuadratic_semantics']
roots = ['NLA.KE04._proved.' + n for n in re.findall(r'^theorem (\w+)', source, re.M)]
headers = {}
defs = []
for n in contracts:
    h = re.search(r'^theorem ' + n + r'\b(.*?) := by sorry$', challenge, re.M | re.S).group(1)
    headers[n] = h
    binders, target = h.rsplit(' :\n', 1)
    defs.append('def ' + n + ' : Prop :=\n  ∀' + binders + ',\n' + target)
required = ['NLA.KE04._proved.' + n for n in [
    'act_mul', 'act_one', 'inner_eq_sum', 'inner_act_transpose', 'inner_act_left',
    'inner_columns', 'frame_iff_orthonormal', 'act_eq_column_sum',
    'columnSpace_eq_range_act', 'act_transpose_act', 'frameProjection_act',
    'frameProjection_fixed_iff', 'submodule_frame_exists']]
required += ['NLA.KE04.' + n for n in ['column', 'act', 'columnSpace', 'krylov',
    'FullBlockDimension', 'IsKrylovBasis', 'frameProjection', 'compression',
    'compressedQuadratic', 'quadraticMatrix', 'form']]
required += ['Matrix.toLpLin', 'Matrix.toLpLin_mul_same', 'Matrix.toLpLin_one',
    'stdOrthonormalBasis', 'OrthonormalBasis.reindex', 'Orthonormal.comp_linearIsometry',
    'Submodule.map_span', 'Module.Basis.span_eq',
    'Matrix.PosSemidef.mul_mul_conjTranspose_same', 'Matrix.isHermitian_conjTranspose_mul_mul']

body = '''/- Frames author inspection: expected types are exact frozen propositions,
not admitted reference proofs. All actual roots are inspected independently. -/
import NLA.KE04.Frames
import Lean.Util.FoldConsts
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.KE04.FramesExpected
'''
body += '\n\n'.join(defs) + '\nend NLA.KE04.FramesExpected\n\n'
body += '''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [''' + ',\n    '.join('(``NLA.KE04._proved.' + n + ', ``NLA.KE04.FramesExpected.' + n + ')' for n in contracts) + ''']
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual theorem {actual}"
    let some b := env.find? reference | throwError "Missing expected type {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Actual export is not a theorem {actual}"
    let some expected := b.value? | throwError "Expected type has no value {reference}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type expected do
        throwError "Frozen signature mismatch {actual}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  let mut pending := [''' + ', '.join('``' + n for n in roots) + ''']
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.KE04.FramesExpected." then
          throwError "Actual proof reached diagnostic type {name}"
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing declaration {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial declaration {name}"
        let axioms ← liftCoreM <| collectAxioms name
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Forbidden transitive axiom {name}: {ax}"
        logInfo m!"ACTUAL_AXIOMS {name}: {axioms.toList}"
        let body ← match ci.value? (allowOpaque := true) with
          | some b => pure b.getUsedConstants.toList
          | none => match ci with
            | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
            | _ => throwError "Unexplained bodyless declaration {name}"
        let deps := ci.type.getUsedConstants.toList ++ body
        used := deps ++ used
        let follow := deps.filter isProject
        logInfo m!"PROJECT_EDGE {name}: {follow}"
        pending := follow ++ pending
  unless pending.isEmpty do throwError "Incomplete traversal"
  let required := [''' + ',\n    '.join('``' + n for n in required) + ''']
  let mut missing : List Name := []
  for need in required do
    if used.contains need then
      logInfo m!"RETAINED_DEPENDENCY {need}"
    else
      missing := need :: missing
  unless missing.isEmpty do throwError "Missing material dependencies {missing}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

'''
for n in roots:
    body += '#assert_trust kernel ' + n + '\n#print axioms ' + n + '\n'
for n in ['act', 'column', 'columnSpace', 'frameProjection', 'compression', 'compressedQuadratic']:
    body += 'set_option pp.all true in\n#print NLA.KE04.' + n + '\n'
for n in contracts + ['submodule_frame_exists']:
    body += 'set_option pp.proofs true in\n#print NLA.KE04._proved.' + n + '\n'
target = E / 'Inspect.lean'
target.write_text(body)
(E / 'expected-type-extraction.json').write_text(json.dumps({
    'frozen_challenge_sha256': hashlib.sha256(challenge.encode()).hexdigest(),
    'headers': headers, 'expected_types_are_Props_without_admissions': True,
    'actual_roots': roots, 'required_dependencies': required,
    'inspector_sha256': hashlib.sha256(body.encode()).hexdigest()}, indent=2) + '\n')
print(json.dumps({'contracts': len(contracts), 'roots': len(roots), 'required': len(required),
    'inspector_sha256': hashlib.sha256(body.encode()).hexdigest()}))
