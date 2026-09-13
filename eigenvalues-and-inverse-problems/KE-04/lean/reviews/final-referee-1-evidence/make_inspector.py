"""Independent KE-04 review diagnostics. Never imported by the implementation."""
from pathlib import Path
import hashlib, json, re
P = Path(__file__).resolve().parents[2]
E = Path(__file__).resolve().parent
names = json.loads((P/'comparator.json').read_text())['theorem_names']
assert len(names) == 24
common = '''blockLanczosConjecture strictIntervalOccupancy fullPrefix_implies_canonical
interval_index_validity orderedSpectrum_semantics spectral_gap_quadratic_psd
spectral_window_subspace orthonormal_span_form_nonpos quadratic_apply_eigenvector
compressedQuadratic_semantics fullBlockDimension_prefix krylov_intersection_nonzero
psd_zero_form_iff_kernel quadratic_forms_agree later_quadratic_identity
fullRank_quadratic_nonannihilation fullRank_krylov_eigenvector_zero
blockShift_eq_smul_extend krylovCombination_extend krylovCombination_shift
compressed_form_expansion compressed_action_identity quadratic_form_expansion
quadratic_action_expansion compression_action_coordinates frame_coordinates
frame_inner frameProjection_fixed_iff columnSpace_eq_range_act
act_mem_krylov_succ krylov_mono fullBlockDimension_iff_columns
quadratic_semantics'''.split()
extra = '''lastFullBlockIteration_exists fullBlockDimension_index_le
fullBlockDimension_mul_le fullColumnRank_iff_first krylovBasis_exists
submodule_frame_exists compression_basis_independent frameProjection_semantics
compression_semantics real_matrix_semantics krylov_range_semantics
fullBlockDimension_iff_independent krylov_nesting_and_shift'''.split()
library = ['LinearMap.IsSymmetric.eigenvalues_antitone',
 'LinearMap.IsSymmetric.apply_eigenvectorBasis',
 'LinearMap.IsSymmetric.roots_charpoly_eq_eigenvalues',
 'Matrix.PosSemidef.dotProduct_mulVec_zero_iff',
 'Matrix.isPositive_toEuclideanLin_iff',
 'LinearMap.posSemidef_toMatrix_iff',
 'Submodule.finrank_sup_add_finrank_inf_eq',
 'linearIndependent_iff_injective_fintypeLinearCombination',
 'finrank_span_eq_card']
extra_library = ['stdOrthonormalBasis',
 'LinearMap.IsSymmetric.eigenvalues_eq_eigenvalues_iff']
defs = ['NLA.KE04.'+x for x in re.findall(r'^(?:def|abbrev) (\w+)',
    (P/'NLA/KE04/Definitions.lean').read_text(), re.M)]
source_names = list(names) + defs
for f in sorted((P/'NLA/KE04').glob('*.lean')):
    if f.name in {'Definitions.lean', 'Proof.lean'}: continue
    source_names += ['NLA.KE04._proved.'+x for x in
        re.findall(r'^(?:theorem|def|abbrev) (\w+)', f.read_text(), re.M)]
assert len(source_names) == len(set(source_names))
quote = lambda ns: '['+',\n    '.join('``'+s for s in ns)+']'
text = '''/- Independent KE-04 final mathematical referee 1 diagnostic.
The reference retains the exact frozen signatures and 24 deliberate admitted
bodies, changed only into a new namespace. It is never imported by Solution.
All real type/body closures must reject that namespace and every axiom outside
the standard three. This local check is not the authoritative Linux Comparator.
-/
import Solution
import reviews.«final-referee-1-evidence».Reference
import Lean.Util.FoldConsts

set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs : List (Name × Name) := [
'''+',\n'.join('    (``'+n+', ``NLA.KE04.FinalReferee1Reference.'+n.split('.')[-1]+')' for n in names)+''']
  for (realName, refName) in pairs do
    let some realInfo := env.find? realName | throwError "Missing implementation {realName}"
    let some refInfo := env.find? refName | throwError "Missing reference {refName}"
    match realInfo with
    | .thmInfo _ => pure ()
    | _ => throwError "Expected actual theorem {realName}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq realInfo.type refInfo.type do
        throwError "Actual signature differs from frozen contract: {realName}"
    let refAxioms ← liftCoreM <| collectAxioms refName
    unless refAxioms.contains ``sorryAx do
      throwError "Reference no longer contains its declared admission: {refName}"
    logInfo m!"EXACT_ELABORATED_SIGNATURE {realName} = {refName}"
    logInfo m!"EXPORTED_TYPE {realName}: {realInfo.type}"
  let exports := '''+quote(names)+'''
  let sources := '''+quote(source_names)+'''
  let common := '''+quote(['NLA.KE04._proved.'+s for s in common]+library)+'''
  let extra := '''+quote(['NLA.KE04._proved.'+s for s in extra]+extra_library)+'''
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  for (label, starts) in [("FINAL", [``NLA.KE04.blockLanczosConjecture]),
      ("ALL", exports), ("SOURCE", sources)] do
    let mut todo := starts
    let mut seen : List Name := []
    let mut allDeps : List Name := []
    for _ in [:10000] do
      match todo with
      | [] => pure ()
      | name :: rest =>
        todo := rest
        unless seen.contains name do
          if name.toString.startsWith "NLA.KE04.FinalReferee1Reference." then
            throwError "Real proof reached admitted reference {name}"
          seen := name :: seen
          let some ci := env.find? name | throwError "Missing actual dependency {name}"
          if ci.isUnsafe || ci.isPartial then
            throwError "Unsafe/partial actual project dependency {name}"
          let axs ← liftCoreM <| collectAxioms name
          for ax in axs do
            unless [``propext, ``Quot.sound, ``Classical.choice].contains ax do
              throwError "Forbidden actual transitive axiom {name}: {ax}"
          let valueDeps ← match ci.value? (allowOpaque := true) with
            | some body => pure body.getUsedConstants.toList
            | none => match ci with
              | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
              | _ => throwError "Unexplained bodyless declaration {name}"
          let ds := ci.type.getUsedConstants.toList ++ valueDeps
          allDeps := ds ++ allDeps
          let following := ds.filter isProject
          todo := following ++ todo
          logInfo m!"ACTUAL_EDGE {label} {name}: {following}"
          logInfo m!"ACTUAL_AXIOMS {label} {name}: {axs.toList}"
    unless todo.isEmpty do throwError "Incomplete traversal {label}"
    let must := common ++ if label == "FINAL" then [] else extra
    for need in must do
      unless allDeps.contains need do
        throwError "Required material bridge absent in {label}: {need}"
      logInfo m!"MATERIAL_BRIDGE {label}: {need}"
    logInfo m!"INDEPENDENT_COUNTS {label}: project={seen.length}, material={must.length}"
'''
for n in names + defs:
    text += '\n#assert_trust kernel '+n+'\n#print axioms '+n+'\n'
for n in names:
    text += '\nset_option pp.all true in\n#check '+n+'\n'
for n in ['IterationOccupancy','FullPrefixBlockLanczosClaim','BlockLanczosConjecture',
          'krylovColumns','krylov','krylovCombination','FullColumnRank','FullBlockDimension',
          'LastFullBlockIteration','IsKrylovBasis','orderedEigenvalues','orderedEigenbasis',
          'eigenvalueAt','frameProjection','compression','compressedQuadratic','form']:
    text += '\nset_option pp.all true in\n#print NLA.KE04.'+n+'\n'
(E/'Inspect.lean').write_text(text)
(E/'inspection-requirements.json').write_text(json.dumps({
    'exports': names, 'source_declarations': source_names, 'definitions': defs,
    'common_material_bridges': ['NLA.KE04._proved.'+s for s in common]+library,
    'additional_material_bridges': ['NLA.KE04._proved.'+s for s in extra]+extra_library,
    'required_type_matches':24,'reference_edges_allowed':0,
    'kernel_assertions':len(names+defs),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
},indent=2)+'\n')
