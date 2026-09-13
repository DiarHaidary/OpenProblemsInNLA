/-
NR-03 unconditional certificate assembly.

The generic algebra is isolated in CertificateBridge for inexpensive bounded
diagnostics. Every conditional premise is supplied below by the complete
original core and family identities. Development only: final authoritative
LeanCert, Comparator, kernel and sandbox checks remain pending.
-/
import NLA.NR03.CertificateBridge
import NLA.NR03.FamilyIdentities
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

theorem full_identity (a b : Mask7) :
    fullSum a b = sourceD b * natTarget a b := by
  exact CertificateBridge.full_identity_of_components
    (fun a b => core_identity a b)
    singleton_identity pair_identity four_identity
    closed_family_identity a b

#print axioms full_identity

theorem generic_scaled_identity (a b : BoolVec 7) :
    (castNatMatrix genericW * castNatMatrix genericV) a b =
      (genericD b : ℝ) * cMatrix 7 a b := by
  exact CertificateBridge.scaled_identity_of_full
    (fun a b => full_identity a b) a b

#print axioms generic_scaled_identity

end NLA.NR03
