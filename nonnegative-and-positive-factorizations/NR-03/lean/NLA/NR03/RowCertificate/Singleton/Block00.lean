/-
Generated NR-03 literal-row certificates; see row-certificates/INTERFACES.md.
Each row uses its own closed kernel decision. The predecessor import makes
heavy row reductions sequential during ordinary Lake dependency builds.
No earlier probe source is imported. This source awaits full verification.
-/
import NLA.NR03.FamilyDefs
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace NLA.NR03.RowCertificate.Singleton

theorem row0 : ∀ b : Mask7,
    singletonSum (0 : Mask7) b = singletonClosed (0 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row0

theorem row1 : ∀ b : Mask7,
    singletonSum (1 : Mask7) b = singletonClosed (1 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row1

theorem row2 : ∀ b : Mask7,
    singletonSum (2 : Mask7) b = singletonClosed (2 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row2

theorem row3 : ∀ b : Mask7,
    singletonSum (3 : Mask7) b = singletonClosed (3 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row3

theorem row4 : ∀ b : Mask7,
    singletonSum (4 : Mask7) b = singletonClosed (4 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row4

theorem row5 : ∀ b : Mask7,
    singletonSum (5 : Mask7) b = singletonClosed (5 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row5

theorem row6 : ∀ b : Mask7,
    singletonSum (6 : Mask7) b = singletonClosed (6 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row6

theorem row7 : ∀ b : Mask7,
    singletonSum (7 : Mask7) b = singletonClosed (7 : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.Singleton.row7

end NLA.NR03.RowCertificate.Singleton
