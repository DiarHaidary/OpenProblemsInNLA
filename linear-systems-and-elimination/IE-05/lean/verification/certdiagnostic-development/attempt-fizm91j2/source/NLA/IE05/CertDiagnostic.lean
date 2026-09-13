import NLA.IE05.Definitions
import LeanCert.Tactic.Verification
namespace NLA.IE05
set_option pp.universes true
#synth Decidable ((1 : ℤ) = 1)
#synth Decidable (integerH false 0 0 = 1)
#synth Decidable (∀ i : Fin 8, integerLower false i i = 1)
set_option trace.Meta.synthInstance true in
#synth Decidable ((integerH false).transpose * integerH false = Matrix.diagonal (integerD false))
set_option trace.Meta.synthInstance true in
#synth Decidable (integerLower false 0 0 = 1)
end NLA.IE05
