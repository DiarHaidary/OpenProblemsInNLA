import NLA.RA20.Definitions
import LeanCert.Tactic.Verification

/-! Root independent definition/statement boundary inspection; no Challenge import or theorem proof. -/

#print NLA.RA20.variety
#assert_trust kernel NLA.RA20.variety
#print axioms NLA.RA20.variety

#print NLA.RA20.definingIdeal
#assert_trust kernel NLA.RA20.definingIdeal
#print axioms NLA.RA20.definingIdeal

#print NLA.RA20.SmoothPoint
#assert_trust kernel NLA.RA20.SmoothPoint
#print axioms NLA.RA20.SmoothPoint

#print NLA.RA20.TangentVector
#assert_trust kernel NLA.RA20.TangentVector
#print axioms NLA.RA20.TangentVector

#print NLA.RA20.fullFrobeniusDistance
#assert_trust kernel NLA.RA20.fullFrobeniusDistance
#print axioms NLA.RA20.fullFrobeniusDistance

#print NLA.RA20.SmoothCriticalPoint
#assert_trust kernel NLA.RA20.SmoothCriticalPoint
#print axioms NLA.RA20.SmoothCriticalPoint

#print NLA.RA20.HasCriticalCount
#assert_trust kernel NLA.RA20.HasCriticalCount
#print axioms NLA.RA20.HasCriticalCount

#print NLA.RA20.HasGenericCriticalCount
#assert_trust kernel NLA.RA20.HasGenericCriticalCount
#print axioms NLA.RA20.HasGenericCriticalCount

#print NLA.RA20.predictedCount
#assert_trust kernel NLA.RA20.predictedCount
#print axioms NLA.RA20.predictedCount

#print NLA.RA20.criticalCountConjecture
#assert_trust kernel NLA.RA20.criticalCountConjecture
#print axioms NLA.RA20.criticalCountConjecture

#print Algebra.IsSmoothAt
#print Algebra.smoothLocus
#check MvPolynomial.vanishingIdeal
#check MvPolynomial.pointToPoint
#check Matrix.rank
#check fderiv
#check Cardinal.mk
#synth IsAlgClosed ℂ
#synth FiniteDimensional ℂ (NLA.RA20.Mat 3)
#reduce (NLA.RA20.predictedCount 3 1, NLA.RA20.predictedCount 3 2, NLA.RA20.predictedCount 3 3, NLA.RA20.predictedCount 4 4)
