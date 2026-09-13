import NLA.IE05.Definitions
import Mathlib.Tactic.NormNum
import LeanCert.Tactic.Verification
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000
namespace NLA.IE05._proved
#synth Decidable (∀ i j : Fin 8, j < i → integerT false i j = 0)
set_option trace.Meta.synthInstance true in
example : UpperTriangular (integerT false) := by
  unfold UpperTriangular
  decide +kernel
end NLA.IE05._proved
