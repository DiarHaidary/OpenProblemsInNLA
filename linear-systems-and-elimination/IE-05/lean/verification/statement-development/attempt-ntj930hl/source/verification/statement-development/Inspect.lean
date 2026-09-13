import NLA.IE05.Definitions
import LeanCert.Tactic.Verification

/- Definition-only checks. No Challenge import and no proof of a proposed theorem. -/
set_option leancert.trust "kernel"

#check InnerProductSpace.gramSchmidtNormed
#check InnerProductSpace.gramSchmidt_orthonormal
#check InnerProductSpace.gramSchmidt_inv_triangular
#check InnerProductSpace.gramSchmidt_ne_zero
#check InnerProductSpace.gramSchmidt_def
#check Matrix.det_mul
#check Matrix.det_transpose
#check Matrix.det_one
#check Finset.le_sup
#check Finset.sup_le
#check le_csSup
#check csSup_le
#check Real.sq_sqrt
#check Real.sqrt_pos

#print NLA.IE05.euclideanColumns
#print NLA.IE05.normalizedQRQ
#print NLA.IE05.PositiveQR
#print NLA.IE05.schurStep
#print NLA.IE05.trajectory
#print NLA.IE05.AdmissiblePivot
#print NLA.IE05.FirstAvailablePivot
#print NLA.IE05.firstPivotIndex
#print NLA.IE05.firstPath
#print NLA.IE05.entryMaxNN
#print NLA.IE05.activeMaxNN
#print NLA.IE05.growth
#print NLA.IE05.orthogonalGrowthSet
#print NLA.IE05.orthogonalGrowthSup
#print NLA.IE05.OrthogonalExtremizerConjecture
#print NLA.IE05.tailProduct

#assert_trust kernel NLA.IE05.normalizedQRQ
#print axioms NLA.IE05.normalizedQRQ
#assert_trust kernel NLA.IE05.PositiveQR
#print axioms NLA.IE05.PositiveQR
#assert_trust kernel NLA.IE05.schurStep
#print axioms NLA.IE05.schurStep
#assert_trust kernel NLA.IE05.trajectory
#print axioms NLA.IE05.trajectory
#assert_trust kernel NLA.IE05.firstPivotIndex
#print axioms NLA.IE05.firstPivotIndex
#assert_trust kernel NLA.IE05.firstPath
#print axioms NLA.IE05.firstPath
#assert_trust kernel NLA.IE05.growth
#print axioms NLA.IE05.growth
#assert_trust kernel NLA.IE05.orthogonalGrowthSet
#print axioms NLA.IE05.orthogonalGrowthSet
#assert_trust kernel NLA.IE05.orthogonalGrowthSup
#print axioms NLA.IE05.orthogonalGrowthSup
#assert_trust kernel NLA.IE05.OrthogonalExtremizerConjecture
#print axioms NLA.IE05.OrthogonalExtremizerConjecture
#assert_trust kernel NLA.IE05.normalizedInteger
#print axioms NLA.IE05.normalizedInteger
#assert_trust kernel NLA.IE05.tailProduct
#print axioms NLA.IE05.tailProduct
