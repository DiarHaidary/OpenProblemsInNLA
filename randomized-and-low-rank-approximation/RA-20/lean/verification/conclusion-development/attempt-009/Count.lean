import NLA.RA20.Critical
import NLA.RA20.Generic
import Mathlib.SetTheory.Cardinal.Basic

/-!
# RA-20: genuine generic cardinality and the full conjecture's negation

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
Original negative-resolution mathematics: the repository's Codex automated
maintainer audit; conjecture: Kubjas, Sodomaco and Tsigaridas.

The cardinality is that of the actual smooth critical-point subtype. The proved
intersection with every nonempty principal open set excludes any competing
generic count of four, not merely the proposed exceptional polynomial.
-/

noncomputable section
namespace NLA.RA20

theorem critical_count_three (U : Mat 3) (hU : GenericData U) :
    HasCriticalCount 3 3 U 3 := by
  obtain ⟨he, hi⟩ := generic_critical_locus_proved U hU
  change Cardinal.mk (criticalSet 3 3 U) = (3 : Cardinal)
  rw [he, Cardinal.mk_range_eq _ hi]
  rfl

theorem generic_count_three_proved : HasGenericCriticalCount 3 3 3 := by
  refine ⟨genericPolynomial, ?_, ?_⟩
  · refine ⟨hollow 1 1 1, hollow_isSymm 1 1 1, ?_⟩
    norm_num [genericPolynomial, coordinates, hollow]
  · intro U hU hq
    apply critical_count_three U
    refine ⟨hU, ?_⟩
    simpa [genericPolynomial, coordinates] using hq

theorem generic_count_not_four_proved : ¬ HasGenericCriticalCount 3 3 4 := by
  rintro ⟨q, hq, hcount⟩
  obtain ⟨U, hU, hqU⟩ := generic_data_intersection_proved q hq
  have h3 := critical_count_three U hU
  have h4 := hcount U hU.1 hqU
  have hbad : (3 : Cardinal) = (4 : Cardinal) := h3.symm.trans h4
  norm_num at hbad

theorem not_criticalCountConjecture_proved : ¬ criticalCountConjecture := by
  intro h
  have h4 := h 3 3 (by decide) (by decide) (by decide) (by decide)
  apply generic_count_not_four_proved
  simpa [predictedCount] using h4

#assert_trust kernel critical_count_three
#assert_trust kernel generic_count_three_proved
#assert_trust kernel generic_count_not_four_proved
#assert_trust kernel not_criticalCountConjecture_proved
#print axioms critical_count_three
#print axioms generic_count_three_proved
#print axioms generic_count_not_four_proved
#print axioms not_criticalCountConjecture_proved

end NLA.RA20
