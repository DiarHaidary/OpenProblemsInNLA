import NLA.KE04.Krylov

/-!
# KE-04: the genuine nonzero Krylov intersection

Original argument: Matthew J. Colbrook. AI-assisted formalization by George
Stepaniants, Department of Computing and Mathematical Sciences, California
Institute of Technology, Pasadena, California, USA.
-/

noncomputable section
set_option leancert.trust "kernel"
namespace NLA.KE04._proved

theorem krylov_intersection_nonzero {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 1 ≤ k) (hfull : FullBlockDimension A V k)
    (hprev : FullBlockDimension A V (k - 1)) (E : Submodule ℝ (Vec n))
    (hE : E ≤ krylov A V k) (hdim : Module.finrank ℝ E = p + 1) :
    ∃ x : Vec n, x ≠ 0 ∧ x ∈ E ∧ x ∈ krylov A V (k - 1) := by
  have hsum := Submodule.finrank_sup_add_finrank_inf_eq E (krylov A V (k - 1))
  have hsup : E ⊔ krylov A V (k - 1) ≤ krylov A V k :=
    sup_le hE (krylov_mono A V (Nat.sub_le k 1))
  have hsupdim := Submodule.finrank_mono hsup
  have hprod : k * p = (k - 1) * p + p := by
    calc
      k * p = ((k - 1) + 1) * p := by rw [Nat.sub_add_cancel hk]
      _ = (k - 1) * p + p := by rw [Nat.add_mul, Nat.one_mul]
  change Module.finrank ℝ (krylov A V k) = k * p at hfull
  change Module.finrank ℝ (krylov A V (k - 1)) = (k - 1) * p at hprev
  have hpos : 0 < Module.finrank ℝ ↥(E ⊓ krylov A V (k - 1)) := by omega
  obtain ⟨x, hx⟩ := (Module.finrank_pos_iff_exists_ne_zero.mp hpos)
  refine ⟨x.val, ?_, x.property.1, x.property.2⟩
  intro hz
  apply hx
  exact Subtype.ext hz

#assert_trust kernel krylov_intersection_nonzero
#print axioms krylov_intersection_nonzero
end NLA.KE04._proved
