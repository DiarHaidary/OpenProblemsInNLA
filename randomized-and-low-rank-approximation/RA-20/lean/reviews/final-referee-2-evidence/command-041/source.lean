/-
RA-20: actual algebraic smoothness of the reduced union of three planes.
Formalization: George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA, with AI assistance.
Original resolution: the repository's Codex automated maintainer audit.
The exact infinitesimal lifting and localization APIs are from pinned Mathlib.
-/
import NLA.RA20.Definitions
import NLA.RA20.Algebra
import NLA.RA20.SmoothTransport
import Mathlib.RingTheory.Localization.Algebra
import LeanCert.Tactic.Verification
import Mathlib.Tactic.Ring

set_option autoImplicit false
set_option leancert.trust "kernel"

noncomputable section

namespace NLA.RA20

/-- A triple-product hypersurface cannot be formally smooth where every pairwise
product vanishes. The proof uses an actual square-zero thickening, rather than
assuming a Jacobian criterion. -/
theorem triple_product_not_formallySmooth
    {R P A K : Type*} [CommRing R] [CommRing P] [IsDomain P]
    [CommRing A] [CommRing K] [Nontrivial K]
    [Algebra R P] [Algebra R A] [Algebra.FormallySmooth R P]
    (π : P →ₐ[R] A) (hπ : Function.Surjective π)
    (a b c : P) (hf : a * b * c ≠ 0)
    (hker : RingHom.ker π.toRingHom = Ideal.span {a * b * c})
    (e : P →+* K) (hab : e (a * b) = 0) (hac : e (a * c) = 0)
    (hbc : e (b * c) = 0) : ¬ Algebra.FormallySmooth R A := by
  intro hs
  obtain ⟨g, hg⟩ := (Algebra.FormallySmooth.iff_split_surjection π hπ).mp hs
  obtain ⟨a', ha'⟩ := Ideal.Quotient.mk_surjective (g (π a))
  obtain ⟨b', hb'⟩ := Ideal.Quotient.mk_surjective (g (π b))
  obtain ⟨c', hc'⟩ := Ideal.Quotient.mk_surjective (g (π c))
  have preimage (x x' : P)
      (hx : Ideal.Quotient.mk (RingHom.ker π.toRingHom ^ 2) x' = g (π x)) :
      ∃ t : P, x' = x + (a * b * c) * t := by
    have h : π x' = π x := by
      simpa only [AlgHom.kerSquareLift_mk, AlgHom.comp_apply, AlgHom.id_apply]
        using (congrArg π.kerSquareLift hx).trans (AlgHom.congr_fun hg (π x))
    have hm : x' - x ∈ Ideal.span {a * b * c} := by
      rw [← hker, RingHom.mem_ker]
      change π (x' - x) = 0
      rw [map_sub, h, sub_self]
    obtain ⟨t, ht⟩ := Ideal.mem_span_singleton.mp hm
    exact ⟨t, by linear_combination ht⟩
  obtain ⟨u, hu⟩ := preimage a a' ha'
  obtain ⟨v, hv⟩ := preimage b b' hb'
  obtain ⟨w, hw⟩ := preimage c c' hc'
  have hzero : π (a * b * c) = 0 := by
    change π.toRingHom (a * b * c) = 0
    apply RingHom.mem_ker.mp
    rw [hker]
    exact Ideal.mem_span_singleton_self _
  have hm : a' * b' * c' ∈ RingHom.ker π.toRingHom ^ 2 := by
    apply Ideal.Quotient.eq_zero_iff_mem.mp
    rw [map_mul, map_mul, ha', hb', hc', ← map_mul, ← map_mul,
      ← map_mul, ← map_mul, hzero, map_zero]
  rw [hker, Ideal.span_singleton_pow] at hm
  obtain ⟨t, ht⟩ := Ideal.mem_span_singleton.mp hm
  have heq :
      1 + b * c * u + a * c * v + a * b * w +
        (a * b * c) * (c * u * v + b * u * w + a * v * w) +
        (a * b * c)^2 * u * v * w = (a * b * c) * t := by
    apply mul_left_cancel₀ hf
    calc
      a * b * c * _ = a' * b' * c' := by rw [hu, hv, hw]; ring
      _ = (a * b * c)^2 * t := ht
      _ = (a * b * c) * ((a * b * c) * t) := by ring
  have hef : e (a * b * c) = 0 := by rw [map_mul, hab, zero_mul]
  have h01 := congrArg e heq
  simp only [map_add, map_one, map_mul, map_pow, hef, hab, hac, hbc,
    zero_mul, add_zero, zero_pow two_ne_zero] at h01
  exact one_ne_zero h01

#assert_trust kernel triple_product_not_formallySmooth
#print axioms triple_product_not_formallySmooth

/-- Formal smoothness descends along an actual algebra retraction. -/
theorem formallySmooth_of_retraction
    {R P A : Type*} [CommRing R] [CommRing P] [CommRing A]
    [Algebra R P] [Algebra R A] [Algebra.FormallySmooth R P]
    (π : P →ₐ[R] A) (σ : A →ₐ[R] P) (h : π.comp σ = AlgHom.id R A) :
    Algebra.FormallySmooth R A := by
  refine Algebra.FormallySmooth.of_comp_surjective fun B _ _ I hI f ↦ ?_
  obtain ⟨g, hg⟩ := Algebra.FormallySmooth.comp_surjective R P I hI (f.comp π)
  refine ⟨g.comp σ, ?_⟩
  rw [← AlgHom.comp_assoc, hg, AlgHom.comp_assoc, h, AlgHom.comp_id]

/-- The preimage of a point prime in the polynomial presentation. -/
abbrev abcPreimagePrime (p : PrimeSpectrum ABCCoordinateRing) : Ideal ABCPoly :=
  p.asIdeal.comap (Ideal.Quotient.mk abcIdeal)

abbrev ABCPolynomialLocal (p : PrimeSpectrum ABCCoordinateRing) :=
  Localization.AtPrime (abcPreimagePrime p)

abbrev ABCLocal (p : PrimeSpectrum ABCCoordinateRing) :=
  Localization.AtPrime p.asIdeal

theorem abc_complement_map (p : PrimeSpectrum ABCCoordinateRing) :
    (abcPreimagePrime p).primeCompl.map (Ideal.Quotient.mk abcIdeal) = p.asIdeal.primeCompl := by
  change (p.asIdeal.primeCompl.comap (Ideal.Quotient.mk abcIdeal)).map _ = _
  exact Submonoid.map_comap_eq_self_of_surjective Ideal.Quotient.mk_surjective

set_option backward.isDefEq.respectTransparency false in
/-- The actual localized presentation map, before any chart is chosen. -/
def abcLocalizationMap (p : PrimeSpectrum ABCCoordinateRing) :
    ABCPolynomialLocal p →ₐ[ℂ] ABCLocal p where
  __ := IsLocalization.map (ABCLocal p) (Ideal.Quotient.mk abcIdeal)
    (show (abcPreimagePrime p).primeCompl ≤
      p.asIdeal.primeCompl.comap (Ideal.Quotient.mk abcIdeal) from fun _ h ↦ h)
  commutes' r := by
    change IsLocalization.map (ABCLocal p) (Ideal.Quotient.mk abcIdeal) _
      (algebraMap ℂ (ABCPolynomialLocal p) r) = _
    rw [IsScalarTower.algebraMap_apply ℂ ABCPoly (ABCPolynomialLocal p),
      IsLocalization.map_eq]
    simp only [Ideal.Quotient.mk_algebraMap,
      IsScalarTower.algebraMap_apply ℂ ABCCoordinateRing (ABCLocal p)]

@[simp] theorem abcLocalizationMap_algebraMap
    (p : PrimeSpectrum ABCCoordinateRing) (f : ABCPoly) :
    abcLocalizationMap p (algebraMap ABCPoly (ABCPolynomialLocal p) f) =
      algebraMap ABCCoordinateRing (ABCLocal p) (Ideal.Quotient.mk abcIdeal f) := by
  exact IsLocalization.map_eq (Q := ABCLocal p) (S := ABCPolynomialLocal p)
    (g := Ideal.Quotient.mk abcIdeal) (M := (abcPreimagePrime p).primeCompl)
    (T := p.asIdeal.primeCompl) (fun _ h ↦ h) f

theorem abcLocalizationMap_surjective (p : PrimeSpectrum ABCCoordinateRing) :
    Function.Surjective (abcLocalizationMap p) := by
  let : IsLocalization ((abcPreimagePrime p).primeCompl.map
      (Ideal.Quotient.mk abcIdeal)) (ABCLocal p) := by
    rw [abc_complement_map]; infer_instance
  exact IsLocalization.map_surjective_of_surjective
    (abcPreimagePrime p).primeCompl (ABCPolynomialLocal p) (ABCLocal p)
    Ideal.Quotient.mk_surjective

theorem abcLocalizationMap_ker (p : PrimeSpectrum ABCCoordinateRing) :
    RingHom.ker (abcLocalizationMap p).toRingHom =
      Ideal.span {algebraMap ABCPoly (ABCPolynomialLocal p) abcPolynomial} := by
  have h := IsLocalization.ker_map (S := ABCPolynomialLocal p) (ABCLocal p)
    (Ideal.Quotient.mk abcIdeal) (abc_complement_map p)
  change RingHom.ker (IsLocalization.map (ABCLocal p) (Ideal.Quotient.mk abcIdeal)
    (show (abcPreimagePrime p).primeCompl ≤
      p.asIdeal.primeCompl.comap (Ideal.Quotient.mk abcIdeal) from fun _ h ↦ h)) = _
  rw [h, Ideal.mk_ker, abcIdeal, Ideal.map_span, Set.image_singleton]

#assert_trust kernel formallySmooth_of_retraction
#print axioms formallySmooth_of_retraction

theorem abc_prime_mem_iff (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (f : ABCPoly) :
    Ideal.Quotient.mk abcIdeal f ∈ p.asIdeal ↔ MvPolynomial.aeval x f = 0 := by
  change f ∈ abcPreimagePrime p ↔ _
  have h := congrArg PrimeSpectrum.asIdeal hx
  change abcPreimagePrime p = (MvPolynomial.pointToPoint x).asIdeal at h
  rw [h]
  exact MvPolynomial.mem_vanishingIdeal_singleton_iff x f

theorem abc_prime_product_zero (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x) :
    x 0 * x 1 * x 2 = 0 := by
  have hf : Ideal.Quotient.mk abcIdeal abcPolynomial = 0 := by
    apply Ideal.Quotient.eq_zero_iff_mem.mpr
    exact Ideal.mem_span_singleton_self _
  have h := (abc_prime_mem_iff p x hx abcPolynomial).mp (hf ▸ p.asIdeal.zero_mem)
  simpa [abcPolynomial] using h

/-- Evaluation extends to the actual localized polynomial presentation at this point. -/
def abcLocalEvaluation (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x) :
    ABCPolynomialLocal p →ₐ[ℂ] ℂ :=
  IsLocalization.liftAlgHom (M := (abcPreimagePrime p).primeCompl)
    (f := MvPolynomial.aeval x) fun y ↦ by
      apply isUnit_iff_ne_zero.mpr
      intro hy
      exact y.property ((abc_prime_mem_iff p x hx y).mpr hy)

@[simp] theorem abcLocalEvaluation_algebraMap (p : PrimeSpectrum ABCCoordinateRing)
    (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (f : ABCPoly) :
    abcLocalEvaluation p x hx (algebraMap ABCPoly (ABCPolynomialLocal p) f) =
      MvPolynomial.aeval x f := by
  exact IsLocalization.lift_eq _ _

theorem abc_local_product_ne_zero (p : PrimeSpectrum ABCCoordinateRing) :
    algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X 0) *
      algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X 1) *
      algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X 2) ≠ 0 := by
  rw [← map_mul, ← map_mul, ← map_zero (algebraMap ABCPoly (ABCPolynomialLocal p))]
  apply (FaithfulSMul.algebraMap_injective ABCPoly (ABCPolynomialLocal p)).ne
  exact mul_ne_zero (mul_ne_zero (MvPolynomial.X_ne_zero 0) (MvPolynomial.X_ne_zero 1))
    (MvPolynomial.X_ne_zero 2)

/-- The actual localized ring is not formally smooth at any component intersection. -/
theorem abc_local_not_smooth (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (h01 : x 0 * x 1 = 0) (h02 : x 0 * x 2 = 0) (h12 : x 1 * x 2 = 0) :
    ¬ Algebra.FormallySmooth ℂ (ABCLocal p) := by
  let a := algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X 0)
  let b := algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X 1)
  let c := algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X 2)
  apply triple_product_not_formallySmooth (abcLocalizationMap p)
    (abcLocalizationMap_surjective p) a b c (abc_local_product_ne_zero p)
    (by simpa only [abcPolynomial, map_mul] using abcLocalizationMap_ker p)
    (abcLocalEvaluation p x hx).toRingHom
  · simpa [a, b, c] using h01
  · simpa [a, b, c] using h02
  · simpa [a, b, c] using h12

#assert_trust kernel abc_local_not_smooth
#print axioms abc_local_not_smooth

/-- Coordinate elimination on the polynomial presentation. -/
def abcErase (j : Fin 3) : ABCPoly →ₐ[ℂ] ABCPoly :=
  MvPolynomial.aeval (fun i ↦ if i = j then 0 else MvPolynomial.X i)

@[simp] theorem abcErase_X (j i : Fin 3) :
    abcErase j (MvPolynomial.X i) = if i = j then 0 else MvPolynomial.X i := by
  simp [abcErase]

theorem abcErase_relation (j : Fin 3) : abcErase j abcPolynomial = 0 := by
  fin_cases j <;> simp [abcPolynomial]

theorem abc_eval_erase (x : Fin 3 → ℂ) (j : Fin 3) (hj : x j = 0) (f : ABCPoly) :
    MvPolynomial.aeval x (abcErase j f) = MvPolynomial.aeval x f := by
  have h : (MvPolynomial.aeval x).comp (abcErase j) = MvPolynomial.aeval x := by
    apply MvPolynomial.algHom_ext
    intro i
    by_cases hi : i = j
    · subst i; simp [hj]
    · simp [hi]
  exact AlgHom.congr_fun h f

/-- A polynomial chart map factors through the actual relation ideal. -/
def abcChart (p : PrimeSpectrum ABCCoordinateRing) (j : Fin 3) :
    ABCCoordinateRing →ₐ[ℂ] ABCPolynomialLocal p :=
  Ideal.Quotient.liftₐ abcIdeal
    ((IsScalarTower.toAlgHom ℂ ABCPoly (ABCPolynomialLocal p)).comp (abcErase j)) (by
      intro f hf
      obtain ⟨g, rfl⟩ := Ideal.mem_span_singleton.mp hf
      simp [abcErase_relation])

@[simp] theorem abcChart_mk (p : PrimeSpectrum ABCCoordinateRing) (j : Fin 3) (f : ABCPoly) :
    abcChart p j (Ideal.Quotient.mk abcIdeal f) =
      algebraMap ABCPoly (ABCPolynomialLocal p) (abcErase j f) := rfl

theorem abcChart_unit (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (j : Fin 3) (hj : x j = 0) (y : p.asIdeal.primeCompl) :
    IsUnit (abcChart p j y) := by
  obtain ⟨f, hf⟩ := Ideal.Quotient.mk_surjective y.val
  have hm : abcErase j f ∈ (abcPreimagePrime p).primeCompl := by
    intro hz
    have hh := (abc_prime_mem_iff p x hx (abcErase j f)).mp hz
    rw [abc_eval_erase x j hj] at hh
    apply y.property
    rw [← hf]
    exact (abc_prime_mem_iff p x hx f).mpr hh
  rw [← hf, abcChart_mk]
  exact IsLocalization.map_units (ABCPolynomialLocal p) ⟨_, hm⟩

/-- The chart extends to the complete local ring, since it preserves the point. -/
def abcLocalChart (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (j : Fin 3) (hj : x j = 0) : ABCLocal p →ₐ[ℂ] ABCPolynomialLocal p :=
  IsLocalization.liftAlgHom (M := p.asIdeal.primeCompl) (f := abcChart p j)
    (abcChart_unit p x hx j hj)

@[simp] theorem abcLocalChart_algebraMap (p : PrimeSpectrum ABCCoordinateRing)
    (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (j : Fin 3) (hj : x j = 0) (f : ABCCoordinateRing) :
    abcLocalChart p x hx j hj (algebraMap ABCCoordinateRing (ABCLocal p) f) =
      abcChart p j f := by
  exact IsLocalization.lift_eq _ _

theorem abc_local_coordinate_unit (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (i : Fin 3) (hi : x i ≠ 0) :
    IsUnit (abcLocalizationMap p
      (algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X i))) := by
  rw [abcLocalizationMap_algebraMap]
  apply IsLocalization.map_units (M := p.asIdeal.primeCompl) (ABCLocal p)
    ⟨Ideal.Quotient.mk abcIdeal (MvPolynomial.X i), ?_⟩
  intro hm
  have h := (abc_prime_mem_iff p x hx (MvPolynomial.X i)).mp hm
  exact hi (by simpa using h)

theorem abc_local_coordinate_zero (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (j : Fin 3) (hj : ∀ i : Fin 3, i ≠ j → x i ≠ 0) :
    abcLocalizationMap p
      (algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X j)) = 0 := by
  let z : Fin 3 → ABCLocal p := fun i ↦ abcLocalizationMap p
    (algebraMap ABCPoly (ABCPolynomialLocal p) (MvPolynomial.X i))
  have hu (i : Fin 3) (hi : i ≠ j) : IsUnit (z i) :=
    abc_local_coordinate_unit p x hx i (hj i hi)
  have hz : z 0 * z 1 * z 2 = 0 := by
    change abcLocalizationMap p _ * abcLocalizationMap p _ * abcLocalizationMap p _ = 0
    rw [← map_mul, ← map_mul, ← map_mul, ← map_mul,
      abcLocalizationMap_algebraMap]
    have hrel : Ideal.Quotient.mk abcIdeal abcPolynomial = 0 :=
      Ideal.Quotient.eq_zero_iff_mem.mpr (Ideal.mem_span_singleton_self _)
    change algebraMap ABCCoordinateRing (ABCLocal p) (Ideal.Quotient.mk abcIdeal abcPolynomial) = 0
    rw [hrel, map_zero]
  change z j = 0
  fin_cases j
  · exact (hu 1 (by decide)).mul_left_eq_zero.mp
      ((hu 2 (by decide)).mul_left_eq_zero.mp hz)
  · exact (hu 0 (by decide)).mul_right_eq_zero.mp
      ((hu 2 (by decide)).mul_left_eq_zero.mp hz)
  · exact ((hu 0 (by decide)).mul (hu 1 (by decide))).mul_right_eq_zero.mp hz

theorem abcLocalChart_retraction (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (j : Fin 3) (hj : x j = 0) (hother : ∀ i : Fin 3, i ≠ j → x i ≠ 0) :
    (abcLocalizationMap p).comp (abcLocalChart p x hx j hj) = AlgHom.id ℂ (ABCLocal p) := by
  have herase :
      ((abcLocalizationMap p).comp (IsScalarTower.toAlgHom ℂ ABCPoly (ABCPolynomialLocal p))).comp
          (abcErase j) =
      (abcLocalizationMap p).comp (IsScalarTower.toAlgHom ℂ ABCPoly (ABCPolynomialLocal p)) := by
    apply MvPolynomial.algHom_ext
    intro i
    simp only [AlgHom.comp_apply, abcErase_X, IsScalarTower.toAlgHom_apply]
    by_cases hi : i = j
    · subst i
      simp only [ite_true, map_zero, abc_local_coordinate_zero p x hx j hother]
    · simp only [if_neg hi]
  apply AlgHom.coe_ringHom_injective
  apply IsLocalization.ringHom_ext p.asIdeal.primeCompl
  apply RingHom.ext
  intro y
  obtain ⟨f, rfl⟩ := Ideal.Quotient.mk_surjective y
  change abcLocalizationMap p (abcLocalChart p x hx j hj
    (algebraMap ABCCoordinateRing (ABCLocal p) (Ideal.Quotient.mk abcIdeal f))) = _
  rw [abcLocalChart_algebraMap, abcChart_mk]
  change abcLocalizationMap p (algebraMap ABCPoly (ABCPolynomialLocal p) (abcErase j f)) =
    algebraMap ABCCoordinateRing (ABCLocal p) (Ideal.Quotient.mk abcIdeal f)
  have hh := AlgHom.congr_fun herase f
  simpa only [AlgHom.comp_apply, IsScalarTower.toAlgHom_apply, abcLocalizationMap_algebraMap]
    using hh

/-- The smooth side follows from the constructed local algebra retraction. -/
theorem abc_local_smooth (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x)
    (j : Fin 3) (hj : x j = 0) (hother : ∀ i : Fin 3, i ≠ j → x i ≠ 0) :
    Algebra.FormallySmooth ℂ (ABCLocal p) :=
  formallySmooth_of_retraction (abcLocalizationMap p) (abcLocalChart p x hx j hj)
    (abcLocalChart_retraction p x hx j hj hother)

#assert_trust kernel abc_local_smooth
#print axioms abc_local_smooth

/-- Genuine smoothness in the quotient's local ring, including the singular origin and axes. -/
theorem abc_smooth_locus_iff (p : PrimeSpectrum ABCCoordinateRing) (x : Fin 3 → ℂ)
    (hx : PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) p = MvPolynomial.pointToPoint x) :
    p ∈ Algebra.smoothLocus ℂ ABCCoordinateRing ↔ ExactlyOneZero (x 0) (x 1) (x 2) := by
  change Algebra.FormallySmooth ℂ (ABCLocal p) ↔ _
  constructor
  · intro hs
    by_contra hn
    have hz := abc_prime_product_zero p x hx
    have hpairs : x 0 * x 1 = 0 ∧ x 0 * x 2 = 0 ∧ x 1 * x 2 = 0 := by
      by_cases h0 : x 0 = 0 <;> by_cases h1 : x 1 = 0 <;> by_cases h2 : x 2 = 0 <;>
        simp_all [ExactlyOneZero, mul_eq_zero]
    exact abc_local_not_smooth p x hx hpairs.1 hpairs.2.1 hpairs.2.2 hs
  · rintro (⟨h0, h1, h2⟩ | ⟨h0, h1, h2⟩ | ⟨h0, h1, h2⟩)
    · apply abc_local_smooth p x hx 0 h0
      intro i hi; fin_cases i <;> simp_all
    · apply abc_local_smooth p x hx 1 h1
      intro i hi; fin_cases i <;> simp_all
    · apply abc_local_smooth p x hx 2 h2
      intro i hi; fin_cases i <;> simp_all

/-- The point-evaluation map descends through the actual relation ideal. -/
def abcEvaluation (x : Fin 3 → ℂ) (hx : x 0 * x 1 * x 2 = 0) :
    ABCCoordinateRing →ₐ[ℂ] ℂ :=
  Ideal.Quotient.liftₐ abcIdeal (MvPolynomial.aeval x) (by
    intro f hf
    obtain ⟨g, rfl⟩ := Ideal.mem_span_singleton.mp hf
    simp [abcPolynomial, hx])

@[simp] theorem abcEvaluation_mk (x : Fin 3 → ℂ) (hx : x 0 * x 1 * x 2 = 0)
    (f : ABCPoly) :
    abcEvaluation x hx (Ideal.Quotient.mk abcIdeal f) = MvPolynomial.aeval x f := rfl

/-- A concrete prime of the reduced quotient lying over this evaluation point. -/
def abcPoint (x : Fin 3 → ℂ) (hx : x 0 * x 1 * x 2 = 0) :
    PrimeSpectrum ABCCoordinateRing where
  asIdeal := RingHom.ker (abcEvaluation x hx).toRingHom
  isPrime := RingHom.ker_isPrime _

theorem abcPoint_comap (x : Fin 3 → ℂ) (hx : x 0 * x 1 * x 2 = 0) :
    PrimeSpectrum.comap (Ideal.Quotient.mk abcIdeal) (abcPoint x hx) =
      MvPolynomial.pointToPoint x := by
  apply PrimeSpectrum.ext
  ext f
  change abcEvaluation x hx (Ideal.Quotient.mk abcIdeal f) = 0 ↔
    f ∈ MvPolynomial.vanishingIdeal ℂ {x}
  rw [abcEvaluation_mk, MvPolynomial.mem_vanishingIdeal_singleton_iff]

#assert_trust kernel abc_smooth_locus_iff
#print axioms abc_smooth_locus_iff
#assert_trust kernel abcPoint_comap
#print axioms abcPoint_comap

/-- The proved coordinate-preserving isomorphism also commutes on every polynomial. -/
theorem reducedCoordinateEquiv_mk (f : Poly 3) :
    reducedCoordinateEquiv (Ideal.Quotient.mk (definingIdeal 3 3) f) =
      Ideal.Quotient.mk abcIdeal (hollowPullback f) := by
  have h : reducedCoordinateEquiv.toAlgHom.comp (Ideal.Quotient.mkₐ ℂ (definingIdeal 3 3)) =
      (Ideal.Quotient.mkₐ ℂ abcIdeal).comp hollowPullback := by
    apply MvPolynomial.algHom_ext
    rintro ⟨i, j⟩
    simpa [hollowPullback] using reducedCoordinateEquiv_mk_X i j
  exact AlgHom.congr_fun h f

/-- The quotient point is transported to the actual nine-coordinate matrix evaluation prime. -/
theorem reducedPoint_comap (x : Fin 3 → ℂ) (hx : x 0 * x 1 * x 2 = 0) :
    PrimeSpectrum.comap (Ideal.Quotient.mk (definingIdeal 3 3))
        (PrimeSpectrum.comap reducedCoordinateEquiv.toRingHom (abcPoint x hx)) =
      MvPolynomial.pointToPoint (coordinates (hollow (x 0) (x 1) (x 2))) := by
  apply PrimeSpectrum.ext
  ext f
  change abcEvaluation x hx
    (reducedCoordinateEquiv (Ideal.Quotient.mk (definingIdeal 3 3) f)) = 0 ↔
    f ∈ MvPolynomial.vanishingIdeal ℂ {coordinates (hollow (x 0) (x 1) (x 2))}
  rw [reducedCoordinateEquiv_mk, abcEvaluation_mk, aeval_hollowPullback,
    MvPolynomial.mem_vanishingIdeal_singleton_iff]

/-- Complete original matrix-space smooth-locus contract. The coordinate ring,
point prime, localization and formal-smoothness predicate are the actual ones. -/
theorem algebraic_smooth_locus_proved (X : Mat 3) :
    SmoothPoint 3 3 X ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧ ExactlyOneZero (X 0 1) (X 0 2) (X 1 2) := by
  constructor
  · rintro ⟨hX, p, hp, hs⟩
    have hshape := matrix_eq_hollow_of_mem hX
    let x : Fin 3 → ℂ := ![X 0 1, X 0 2, X 1 2]
    have hz : x 0 * x 1 * x 2 = 0 :=
      ((hollow_variety_semantics_proved.2 X).mp hX).2
    have hm : hollow (x 0) (x 1) (x 2) = X := hshape.symm
    have heq : p = PrimeSpectrum.comap reducedCoordinateEquiv.toRingHom (abcPoint x hz) := by
      apply PrimeSpectrum.comap_injective_of_surjective
        (Ideal.Quotient.mk (definingIdeal 3 3)) Ideal.Quotient.mk_surjective
      rw [hp, reducedPoint_comap, hm]
    rw [heq] at hs
    have hs' := (smoothLocus_comap_algEquiv reducedCoordinateEquiv (abcPoint x hz)).mp hs
    exact ⟨hshape, (abc_smooth_locus_iff (abcPoint x hz) x (abcPoint_comap x hz)).mp hs'⟩
  · rintro ⟨hshape, hone⟩
    let x : Fin 3 → ℂ := ![X 0 1, X 0 2, X 1 2]
    have hz : x 0 * x 1 * x 2 = 0 := by
      change X 0 1 * X 0 2 * X 1 2 = 0
      rcases hone with h | h | h
      · simp only [h.1, zero_mul]
      · simp only [h.2.1, mul_zero, zero_mul]
      · simp only [h.2.2, mul_zero]
    have hm : hollow (x 0) (x 1) (x 2) = X := hshape.symm
    refine ⟨(hollow_variety_semantics_proved.2 X).mpr ⟨hshape, hz⟩,
      PrimeSpectrum.comap reducedCoordinateEquiv.toRingHom (abcPoint x hz), ?_, ?_⟩
    · rw [reducedPoint_comap, hm]
    · apply (smoothLocus_comap_algEquiv reducedCoordinateEquiv (abcPoint x hz)).mpr
      exact (abc_smooth_locus_iff (abcPoint x hz) x (abcPoint_comap x hz)).mpr hone

#assert_trust kernel reducedPoint_comap
#print axioms reducedPoint_comap
#assert_trust kernel algebraic_smooth_locus_proved
#print axioms algebraic_smooth_locus_proved

end NLA.RA20
