/- Independent diagnostic only. No Challenge import and no theorem proofs. -/
import NLA.KE04.Definitions
import LeanCert
import Lean.Util.FoldConsts
set_option leancert.trust "kernel"
set_option maxHeartbeats 2000000
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let original : List Name := [``NLA.KE04.Vec,
    ``NLA.KE04.Rect,
    ``NLA.KE04.Mat,
    ``NLA.KE04.column,
    ``NLA.KE04.act,
    ``NLA.KE04.columnSpace,
    ``NLA.KE04.FullColumnRank,
    ``NLA.KE04.krylovColumns,
    ``NLA.KE04.krylov,
    ``NLA.KE04.krylovCombination,
    ``NLA.KE04.FullBlockDimension,
    ``NLA.KE04.LastFullBlockIteration,
    ``NLA.KE04.IsKrylovBasis,
    ``NLA.KE04.frameProjection,
    ``NLA.KE04.compression,
    ``NLA.KE04.orderedEigenvalues,
    ``NLA.KE04.orderedEigenbasis,
    ``NLA.KE04.eigenvalueAt,
    ``NLA.KE04.ritzValues,
    ``NLA.KE04.ritzValueAt,
    ``NLA.KE04.monicQuadratic,
    ``NLA.KE04.quadraticMatrix,
    ``NLA.KE04.compressedQuadratic,
    ``NLA.KE04.form,
    ``NLA.KE04.IterationOccupancy,
    ``NLA.KE04.FullPrefixBlockLanczosClaim,
    ``NLA.KE04.BlockLanczosConjecture]
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." || n.toString.startsWith "_private.NLA.KE04."
  let mut pending := original
  let mut visited : List Name := []
  for _ in [:10000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless visited.contains name do
        visited := name :: visited
        let some ci := env.find? name | throwError "Missing concrete definition {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial definition {name}"
        let some value := ci.value? (allowOpaque := true) | throwError "Bodyless definition {name}"
        let axioms ← liftCoreM <| collectAxioms name
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonfoundational axiom {name}: {ax}"
        let deps := ci.type.getUsedConstants.toList ++ value.getUsedConstants.toList
        for dep in deps do
          if [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler].contains dep then
            throwError "Forbidden actual dependency {name}: {dep}"
        let projectDeps := deps.filter isProject
        let externalDeps := deps.filter (fun n => !isProject n)
        logInfo m!"DEFINITION_CLOSURE {name}: axioms={axioms.toList}; project={projectDeps}; imported={externalDeps}"
        pending := projectDeps ++ pending
  unless pending.isEmpty do throwError "Incomplete definition closure"
  logInfo m!"DEFINITION_CLOSURE_COMPLETE {visited.length}"

#assert_trust kernel NLA.KE04.Vec
#print axioms NLA.KE04.Vec
set_option pp.all true in
#print NLA.KE04.Vec

#assert_trust kernel NLA.KE04.Rect
#print axioms NLA.KE04.Rect
set_option pp.all true in
#print NLA.KE04.Rect

#assert_trust kernel NLA.KE04.Mat
#print axioms NLA.KE04.Mat
set_option pp.all true in
#print NLA.KE04.Mat

#assert_trust kernel NLA.KE04.column
#print axioms NLA.KE04.column
set_option pp.all true in
#print NLA.KE04.column

#assert_trust kernel NLA.KE04.act
#print axioms NLA.KE04.act
set_option pp.all true in
#print NLA.KE04.act

#assert_trust kernel NLA.KE04.columnSpace
#print axioms NLA.KE04.columnSpace
set_option pp.all true in
#print NLA.KE04.columnSpace

#assert_trust kernel NLA.KE04.FullColumnRank
#print axioms NLA.KE04.FullColumnRank
set_option pp.all true in
#print NLA.KE04.FullColumnRank

#assert_trust kernel NLA.KE04.krylovColumns
#print axioms NLA.KE04.krylovColumns
set_option pp.all true in
#print NLA.KE04.krylovColumns

#assert_trust kernel NLA.KE04.krylov
#print axioms NLA.KE04.krylov
set_option pp.all true in
#print NLA.KE04.krylov

#assert_trust kernel NLA.KE04.krylovCombination
#print axioms NLA.KE04.krylovCombination
set_option pp.all true in
#print NLA.KE04.krylovCombination

#assert_trust kernel NLA.KE04.FullBlockDimension
#print axioms NLA.KE04.FullBlockDimension
set_option pp.all true in
#print NLA.KE04.FullBlockDimension

#assert_trust kernel NLA.KE04.LastFullBlockIteration
#print axioms NLA.KE04.LastFullBlockIteration
set_option pp.all true in
#print NLA.KE04.LastFullBlockIteration

#assert_trust kernel NLA.KE04.IsKrylovBasis
#print axioms NLA.KE04.IsKrylovBasis
set_option pp.all true in
#print NLA.KE04.IsKrylovBasis

#assert_trust kernel NLA.KE04.frameProjection
#print axioms NLA.KE04.frameProjection
set_option pp.all true in
#print NLA.KE04.frameProjection

#assert_trust kernel NLA.KE04.compression
#print axioms NLA.KE04.compression
set_option pp.all true in
#print NLA.KE04.compression

#assert_trust kernel NLA.KE04.orderedEigenvalues
#print axioms NLA.KE04.orderedEigenvalues
set_option pp.all true in
#print NLA.KE04.orderedEigenvalues

#assert_trust kernel NLA.KE04.orderedEigenbasis
#print axioms NLA.KE04.orderedEigenbasis
set_option pp.all true in
#print NLA.KE04.orderedEigenbasis

#assert_trust kernel NLA.KE04.eigenvalueAt
#print axioms NLA.KE04.eigenvalueAt
set_option pp.all true in
#print NLA.KE04.eigenvalueAt

#assert_trust kernel NLA.KE04.ritzValues
#print axioms NLA.KE04.ritzValues
set_option pp.all true in
#print NLA.KE04.ritzValues

#assert_trust kernel NLA.KE04.ritzValueAt
#print axioms NLA.KE04.ritzValueAt
set_option pp.all true in
#print NLA.KE04.ritzValueAt

#assert_trust kernel NLA.KE04.monicQuadratic
#print axioms NLA.KE04.monicQuadratic
set_option pp.all true in
#print NLA.KE04.monicQuadratic

#assert_trust kernel NLA.KE04.quadraticMatrix
#print axioms NLA.KE04.quadraticMatrix
set_option pp.all true in
#print NLA.KE04.quadraticMatrix

#assert_trust kernel NLA.KE04.compressedQuadratic
#print axioms NLA.KE04.compressedQuadratic
set_option pp.all true in
#print NLA.KE04.compressedQuadratic

#assert_trust kernel NLA.KE04.form
#print axioms NLA.KE04.form
set_option pp.all true in
#print NLA.KE04.form

#assert_trust kernel NLA.KE04.IterationOccupancy
#print axioms NLA.KE04.IterationOccupancy
set_option pp.all true in
#print NLA.KE04.IterationOccupancy

#assert_trust kernel NLA.KE04.FullPrefixBlockLanczosClaim
#print axioms NLA.KE04.FullPrefixBlockLanczosClaim
set_option pp.all true in
#print NLA.KE04.FullPrefixBlockLanczosClaim

#assert_trust kernel NLA.KE04.BlockLanczosConjecture
#print axioms NLA.KE04.BlockLanczosConjecture
set_option pp.all true in
#print NLA.KE04.BlockLanczosConjecture
