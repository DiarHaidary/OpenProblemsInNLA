import NLA.IE05.Definitions
import Mathlib.Tactic.NormNum
import LeanCert.Tactic.Verification
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000
namespace NLA.IE05._proved
example : (integerH false).transpose * integerH false = Matrix.diagonal (integerD false) := by
  decide +kernel
example : UnitLower (integerLower false) := by
  unfold UnitLower
  decide +kernel
example : UpperTriangular (integerT false) := by
  unfold UpperTriangular
  decide +kernel
example : integerH false = integerLower false * integerT false := by
  decide +kernel
end NLA.IE05._proved
