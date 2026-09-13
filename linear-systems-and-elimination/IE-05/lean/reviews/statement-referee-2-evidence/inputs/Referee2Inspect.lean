import NLA.IE05.Definitions
import LeanCert.Tactic.Verification

set_option leancert.trust "kernel"

#print NLA.IE05.Mat
#print axioms NLA.IE05.Mat
#assert_trust kernel NLA.IE05.Mat

#print NLA.IE05.IntMat
#print axioms NLA.IE05.IntMat
#assert_trust kernel NLA.IE05.IntMat

#print NLA.IE05.PivotPath
#print axioms NLA.IE05.PivotPath
#assert_trust kernel NLA.IE05.PivotPath

#print NLA.IE05.Orthogonal
#print axioms NLA.IE05.Orthogonal
#assert_trust kernel NLA.IE05.Orthogonal

#print NLA.IE05.UpperTriangular
#print axioms NLA.IE05.UpperTriangular
#assert_trust kernel NLA.IE05.UpperTriangular

#print NLA.IE05.UnitLower
#print axioms NLA.IE05.UnitLower
#assert_trust kernel NLA.IE05.UnitLower

#print NLA.IE05.prescribedLower
#print axioms NLA.IE05.prescribedLower
#assert_trust kernel NLA.IE05.prescribedLower

#print NLA.IE05.euclideanColumns
#print axioms NLA.IE05.euclideanColumns
#assert_trust kernel NLA.IE05.euclideanColumns

#print NLA.IE05.normalizedQRQ
#print axioms NLA.IE05.normalizedQRQ
#assert_trust kernel NLA.IE05.normalizedQRQ

#print NLA.IE05.candidateQ
#print axioms NLA.IE05.candidateQ
#assert_trust kernel NLA.IE05.candidateQ

#print NLA.IE05.candidateR
#print axioms NLA.IE05.candidateR
#assert_trust kernel NLA.IE05.candidateR

#print NLA.IE05.PositiveQR
#print axioms NLA.IE05.PositiveQR
#assert_trust kernel NLA.IE05.PositiveQR

#print NLA.IE05.rowSwap
#print axioms NLA.IE05.rowSwap
#assert_trust kernel NLA.IE05.rowSwap

#print NLA.IE05.schurStep
#print axioms NLA.IE05.schurStep
#assert_trust kernel NLA.IE05.schurStep

#print NLA.IE05.trajectory
#print axioms NLA.IE05.trajectory
#assert_trust kernel NLA.IE05.trajectory

#print NLA.IE05.AdmissiblePivot
#print axioms NLA.IE05.AdmissiblePivot
#assert_trust kernel NLA.IE05.AdmissiblePivot

#print NLA.IE05.FirstAvailablePivot
#print axioms NLA.IE05.FirstAvailablePivot
#assert_trust kernel NLA.IE05.FirstAvailablePivot

#print NLA.IE05.AdmissiblePath
#print axioms NLA.IE05.AdmissiblePath
#assert_trust kernel NLA.IE05.AdmissiblePath

#print NLA.IE05.FirstAvailablePath
#print axioms NLA.IE05.FirstAvailablePath
#assert_trust kernel NLA.IE05.FirstAvailablePath

#print NLA.IE05.firstPivotIndex
#print axioms NLA.IE05.firstPivotIndex
#assert_trust kernel NLA.IE05.firstPivotIndex

#print NLA.IE05.firstTrajectory
#print axioms NLA.IE05.firstTrajectory
#assert_trust kernel NLA.IE05.firstTrajectory

#print NLA.IE05.firstPath
#print axioms NLA.IE05.firstPath
#assert_trust kernel NLA.IE05.firstPath

#print NLA.IE05.noSwapPath
#print axioms NLA.IE05.noSwapPath
#assert_trust kernel NLA.IE05.noSwapPath

#print NLA.IE05.entryMaxNN
#print axioms NLA.IE05.entryMaxNN
#assert_trust kernel NLA.IE05.entryMaxNN

#print NLA.IE05.entryMax
#print axioms NLA.IE05.entryMax
#assert_trust kernel NLA.IE05.entryMax

#print NLA.IE05.activeMaxNN
#print axioms NLA.IE05.activeMaxNN
#assert_trust kernel NLA.IE05.activeMaxNN

#print NLA.IE05.activeMax
#print axioms NLA.IE05.activeMax
#assert_trust kernel NLA.IE05.activeMax

#print NLA.IE05.growth
#print axioms NLA.IE05.growth
#assert_trust kernel NLA.IE05.growth

#print NLA.IE05.firstGrowth
#print axioms NLA.IE05.firstGrowth
#assert_trust kernel NLA.IE05.firstGrowth

#print NLA.IE05.orthogonalGrowthSet
#print axioms NLA.IE05.orthogonalGrowthSet
#assert_trust kernel NLA.IE05.orthogonalGrowthSet

#print NLA.IE05.orthogonalGrowthSup
#print axioms NLA.IE05.orthogonalGrowthSup
#assert_trust kernel NLA.IE05.orthogonalGrowthSup

#print NLA.IE05.OrthogonalExtremizerConjecture
#print axioms NLA.IE05.OrthogonalExtremizerConjecture
#assert_trust kernel NLA.IE05.OrthogonalExtremizerConjecture

#print NLA.IE05.scaledColumns
#print axioms NLA.IE05.scaledColumns
#assert_trust kernel NLA.IE05.scaledColumns

#print NLA.IE05.tailProduct
#print axioms NLA.IE05.tailProduct
#assert_trust kernel NLA.IE05.tailProduct

#print NLA.IE05.integerLower
#print axioms NLA.IE05.integerLower
#assert_trust kernel NLA.IE05.integerLower

#print NLA.IE05.integerH
#print axioms NLA.IE05.integerH
#assert_trust kernel NLA.IE05.integerH

#print NLA.IE05.integerD
#print axioms NLA.IE05.integerD
#assert_trust kernel NLA.IE05.integerD

#print NLA.IE05.integerT
#print axioms NLA.IE05.integerT
#assert_trust kernel NLA.IE05.integerT

#print NLA.IE05.castIntegerMatrix
#print axioms NLA.IE05.castIntegerMatrix
#assert_trust kernel NLA.IE05.castIntegerMatrix

#print NLA.IE05.normalizedInteger
#print axioms NLA.IE05.normalizedInteger
#assert_trust kernel NLA.IE05.normalizedInteger

#print NLA.IE05.witnessQ
#print axioms NLA.IE05.witnessQ
#assert_trust kernel NLA.IE05.witnessQ

#print InnerProductSpace.gramSchmidtNormed
#check InnerProductSpace.gramSchmidtNormed_orthonormal
#check InnerProductSpace.gramSchmidt_ne_zero
#check InnerProductSpace.gramSchmidt_inv_triangular
#check PiLp.inner_apply
#check Real.sqrt_pos
#check Real.sq_sqrt
#check le_csSup
#check csSup_le
