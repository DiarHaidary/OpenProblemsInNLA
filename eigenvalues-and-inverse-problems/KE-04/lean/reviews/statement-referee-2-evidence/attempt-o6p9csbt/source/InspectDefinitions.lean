import NLA.KE04.Definitions
import LeanCert.Tactic.Verification
import Lean.Util.FoldConsts
set_option leancert.trust "kernel"
set_option maxHeartbeats 1200000
#assert_trust kernel NLA.KE04.Vec
#print axioms NLA.KE04.Vec
#assert_trust kernel NLA.KE04.Rect
#print axioms NLA.KE04.Rect
#assert_trust kernel NLA.KE04.Mat
#print axioms NLA.KE04.Mat
#assert_trust kernel NLA.KE04.column
#print axioms NLA.KE04.column
#assert_trust kernel NLA.KE04.act
#print axioms NLA.KE04.act
#assert_trust kernel NLA.KE04.columnSpace
#print axioms NLA.KE04.columnSpace
#assert_trust kernel NLA.KE04.FullColumnRank
#print axioms NLA.KE04.FullColumnRank
#assert_trust kernel NLA.KE04.krylovColumns
#print axioms NLA.KE04.krylovColumns
#assert_trust kernel NLA.KE04.krylov
#print axioms NLA.KE04.krylov
#assert_trust kernel NLA.KE04.krylovCombination
#print axioms NLA.KE04.krylovCombination
#assert_trust kernel NLA.KE04.FullBlockDimension
#print axioms NLA.KE04.FullBlockDimension
#assert_trust kernel NLA.KE04.LastFullBlockIteration
#print axioms NLA.KE04.LastFullBlockIteration
#assert_trust kernel NLA.KE04.IsKrylovBasis
#print axioms NLA.KE04.IsKrylovBasis
#assert_trust kernel NLA.KE04.frameProjection
#print axioms NLA.KE04.frameProjection
#assert_trust kernel NLA.KE04.compression
#print axioms NLA.KE04.compression
#assert_trust kernel NLA.KE04.orderedEigenvalues
#print axioms NLA.KE04.orderedEigenvalues
#assert_trust kernel NLA.KE04.orderedEigenbasis
#print axioms NLA.KE04.orderedEigenbasis
#assert_trust kernel NLA.KE04.eigenvalueAt
#print axioms NLA.KE04.eigenvalueAt
#assert_trust kernel NLA.KE04.ritzValues
#print axioms NLA.KE04.ritzValues
#assert_trust kernel NLA.KE04.ritzValueAt
#print axioms NLA.KE04.ritzValueAt
#assert_trust kernel NLA.KE04.monicQuadratic
#print axioms NLA.KE04.monicQuadratic
#assert_trust kernel NLA.KE04.quadraticMatrix
#print axioms NLA.KE04.quadraticMatrix
#assert_trust kernel NLA.KE04.compressedQuadratic
#print axioms NLA.KE04.compressedQuadratic
#assert_trust kernel NLA.KE04.form
#print axioms NLA.KE04.form
#assert_trust kernel NLA.KE04.IterationOccupancy
#print axioms NLA.KE04.IterationOccupancy
#assert_trust kernel NLA.KE04.FullPrefixBlockLanczosClaim
#print axioms NLA.KE04.FullPrefixBlockLanczosClaim
#assert_trust kernel NLA.KE04.BlockLanczosConjecture
#print axioms NLA.KE04.BlockLanczosConjecture

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let roots : List Name := [``NLA.KE04.Vec, ``NLA.KE04.Rect, ``NLA.KE04.Mat, ``NLA.KE04.column, ``NLA.KE04.act, ``NLA.KE04.columnSpace, ``NLA.KE04.FullColumnRank, ``NLA.KE04.krylovColumns, ``NLA.KE04.krylov, ``NLA.KE04.krylovCombination, ``NLA.KE04.FullBlockDimension, ``NLA.KE04.LastFullBlockIteration, ``NLA.KE04.IsKrylovBasis, ``NLA.KE04.frameProjection, ``NLA.KE04.compression, ``NLA.KE04.orderedEigenvalues, ``NLA.KE04.orderedEigenbasis, ``NLA.KE04.eigenvalueAt, ``NLA.KE04.ritzValues, ``NLA.KE04.ritzValueAt, ``NLA.KE04.monicQuadratic, ``NLA.KE04.quadraticMatrix, ``NLA.KE04.compressedQuadratic, ``NLA.KE04.form, ``NLA.KE04.IterationOccupancy, ``NLA.KE04.FullPrefixBlockLanczosClaim, ``NLA.KE04.BlockLanczosConjecture]
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  let mut pending := roots
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:4000] do
    match pending with
    | [] => pure ()
    | n :: rest =>
      pending := rest
      unless seen.contains n do
        seen := n :: seen
        let some ci := env.find? n | throwError "Missing actual definition {n}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial definition {n}"
        let axioms ← liftCoreM <| collectAxioms n
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonstandard definition axiom {n}: {ax}"
        let some v := ci.value? (allowOpaque := true) | throwError "Bodyless definition {n}"
        let ds := ci.type.getUsedConstants.toList ++ v.getUsedConstants.toList
        used := ds ++ used
        pending := ds.filter isProject ++ pending
        logInfo m!"DEFINITION_CLOSURE {n}: axioms={axioms.toList}; dependencies={ds}"
  unless pending.isEmpty do throwError "Incomplete definition traversal"
  for bad in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains bad then throwError "Forbidden definition dependency {bad}"
  logInfo m!"DEFINITION_COUNTS roots={roots.length}, closure={seen.length}"
set_option pp.all true
#print NLA.KE04.Vec
#print NLA.KE04.Rect
#print NLA.KE04.Mat
#print NLA.KE04.column
#print NLA.KE04.act
#print NLA.KE04.columnSpace
#print NLA.KE04.FullColumnRank
#print NLA.KE04.krylovColumns
#print NLA.KE04.krylov
#print NLA.KE04.krylovCombination
#print NLA.KE04.FullBlockDimension
#print NLA.KE04.LastFullBlockIteration
#print NLA.KE04.IsKrylovBasis
#print NLA.KE04.frameProjection
#print NLA.KE04.compression
#print NLA.KE04.orderedEigenvalues
#print NLA.KE04.orderedEigenbasis
#print NLA.KE04.eigenvalueAt
#print NLA.KE04.ritzValues
#print NLA.KE04.ritzValueAt
#print NLA.KE04.monicQuadratic
#print NLA.KE04.quadraticMatrix
#print NLA.KE04.compressedQuadratic
#print NLA.KE04.form
#print NLA.KE04.IterationOccupancy
#print NLA.KE04.FullPrefixBlockLanczosClaim
#print NLA.KE04.BlockLanczosConjecture
