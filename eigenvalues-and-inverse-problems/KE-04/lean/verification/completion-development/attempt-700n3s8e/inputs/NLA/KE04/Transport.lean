import NLA.KE04.Krylov
import NLA.KE04.Frames
import NLA.KE04.Spectral

/-!
# KE-04: exact quadratic transport between arbitrary Krylov frames

Original mathematical argument: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA,
with substantial AI assistance. All statements use the approved actual spaces.
Only a quadratic form is transported through the earlier compression; the later
compression contains the additional power needed for equality of vector actions.
-/

noncomputable section
open scoped BigOperators
set_option leancert.trust "kernel"
namespace NLA.KE04._proved

theorem frame_coordinates {n m : ℕ} (Q : Rect n m) (hQ : Q.transpose * Q = 1)
    (x : Vec n) (hx : x ∈ columnSpace Q) :
    act Q (act Q.transpose x) = x :=
  (frameProjection_act Q x).symm.trans ((frameProjection_fixed_iff Q hQ x).mp hx)

theorem frame_inner {n m : ℕ} (Q : Rect n m) (hQ : Q.transpose * Q = 1)
    (x y : Vec m) : inner ℝ (act Q x) (act Q y) = inner ℝ x y := by
  rw [inner_act_left, act_transpose_act Q hQ]

theorem compression_action_coordinates {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) (x : Vec n) (hx : x ∈ columnSpace Q) :
    act (compression A Q) (act Q.transpose x) = act Q.transpose (act A x) := by
  simp only [compression, Matrix.conjTranspose_eq_transpose_of_trivial, act_mul]
  rw [frame_coordinates Q hQ x hx]

theorem quadratic_action_expansion {m : ℕ} (M : Mat m) (a b : ℝ) (x : Vec m) :
    act (quadraticMatrix M a b) x =
      act M (act M x) - (a + b) • act M x + (a * b) • x := by
  rw [(quadratic_semantics M a b).2.2.2]
  simp only [act, Matrix.toEuclideanLin, map_add, map_sub, map_smul, pow_two,
    Matrix.toLpLin_mul_same, Matrix.toLpLin_one, LinearMap.add_apply,
    LinearMap.sub_apply, LinearMap.smul_apply, LinearMap.comp_apply, LinearMap.id_apply]

theorem quadratic_form_expansion {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ) (x : Vec m) :
    form (quadraticMatrix M a b) x =
      inner ℝ (act M x) (act M x) - (a + b) * inner ℝ x (act M x) +
        (a * b) * inner ℝ x x := by
  have hMt : M.transpose = M := by
    simpa only [Matrix.IsHermitian, Matrix.conjTranspose_eq_transpose_of_trivial] using hM
  simp only [form, quadratic_action_expansion, inner_add_right, inner_sub_right,
    real_inner_smul_right, inner_act_transpose M x (act M x), hMt]

theorem compressed_form_expansion {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) (x : Vec n)
    (hx : x ∈ columnSpace Q) (hAx : act A x ∈ columnSpace Q) (a b : ℝ) :
    form (compressedQuadratic A Q a b) x =
      inner ℝ (act A x) (act A x) - (a + b) * inner ℝ x (act A x) +
        (a * b) * inner ℝ x x := by
  let y := act Q.transpose x
  let C := compression A Q
  have hrep : act Q y = x := frame_coordinates Q hQ x hx
  have hcy : act Q (act C y) = act A x := by
    rw [show act C y = act Q.transpose (act A x) from
      compression_action_coordinates A Q hQ x hx]
    exact frame_coordinates Q hQ (act A x) hAx
  rw [(compressedQuadratic_semantics A Q a b).1 x]
  change form (quadraticMatrix C a b) y = _
  rw [quadratic_form_expansion C (Matrix.isHermitian_conjTranspose_mul_mul Q hA)]
  rw [← frame_inner Q hQ (act C y) (act C y),
    ← frame_inner Q hQ y (act C y), ← frame_inner Q hQ y y, hrep, hcy]

theorem compressed_action_identity {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) (x : Vec n) (hx : x ∈ columnSpace Q)
    (hAx : act A x ∈ columnSpace Q) (hAAx : act A (act A x) ∈ columnSpace Q)
    (a b : ℝ) :
    act (compressedQuadratic A Q a b) x = act (quadraticMatrix A a b) x := by
  simp only [compressedQuadratic, Matrix.conjTranspose_eq_transpose_of_trivial, act_mul]
  rw [quadratic_action_expansion, compression_action_coordinates A Q hQ x hx,
    compression_action_coordinates A Q hQ (act A x) hAx]
  rw [map_add, map_sub, map_smul, map_smul,
    frame_coordinates Q hQ (act A (act A x)) hAAx,
    frame_coordinates Q hQ (act A x) hAx, frame_coordinates Q hQ x hx]
  exact (quadratic_action_expansion A a b x).symm

theorem quadratic_forms_agree {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j)
    (Qk : Rect n (k * p)) (Qj : Rect n (j * p))
    (hQk : IsKrylovBasis A V k Qk) (hQj : IsKrylovBasis A V j Qj)
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (a b : ℝ) :
    form (compressedQuadratic A Qk a b) x =
      form (compressedQuadratic A Qj a b) x := by
  have hxk : x ∈ krylov A V k := krylov_mono A V (Nat.sub_le k 1) hx
  have hAxk : act A x ∈ krylov A V k := by
    simpa only [Nat.sub_add_cancel hk] using act_mem_krylov_succ A V (k - 1) x hx
  have hxj := krylov_mono A V hkj.le hxk
  have hAxj := krylov_mono A V hkj.le hAxk
  rw [← hQk.2] at hxk hAxk
  rw [← hQj.2] at hxj hAxj
  rw [compressed_form_expansion A hA Qk hQk.1 x hxk hAxk,
    compressed_form_expansion A hA Qj hQj.1 x hxj hAxj]

theorem later_quadratic_identity {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j) (Qj : Rect n (j * p))
    (hQj : IsKrylovBasis A V j Qj) (x : Vec n)
    (hx : x ∈ krylov A V (k - 1)) (a b : ℝ) :
    act (compressedQuadratic A Qj a b) x = act (quadraticMatrix A a b) x := by
  have hxk : x ∈ krylov A V k := krylov_mono A V (Nat.sub_le k 1) hx
  have hAxk : act A x ∈ krylov A V k := by
    simpa only [Nat.sub_add_cancel hk] using act_mem_krylov_succ A V (k - 1) x hx
  have hxj := krylov_mono A V hkj.le hxk
  have hAxj := krylov_mono A V hkj.le hAxk
  have hAAxj := krylov_mono A V (Nat.succ_le_of_lt hkj)
    (act_mem_krylov_succ A V k (act A x) hAxk)
  rw [← hQj.2] at hxj hAxj hAAxj
  exact compressed_action_identity A Qj hQj.1 x hxj hAxj hAAxj a b

theorem interval_index_validity (k p i : ℕ) (hk : 1 ≤ k)
    (hi : 1 ≤ i) (hu : i ≤ (k - 1) * p) :
    2 ≤ k ∧ 0 < p ∧ i - 1 < k * p ∧ i + p - 1 < k * p := by
  have hk1 : k ≠ 1 := by
    rintro rfl
    simp only [Nat.sub_self, Nat.zero_mul] at hu
    omega
  have hp : 0 < p := by
    by_contra hn
    have hp0 : p = 0 := by omega
    rw [hp0, Nat.mul_zero] at hu
    omega
  have hprod : k * p = (k - 1) * p + p := by
    calc
      k * p = ((k - 1) + 1) * p := by rw [Nat.sub_add_cancel hk]
      _ = (k - 1) * p + p := by rw [Nat.add_mul, Nat.one_mul]
  omega

theorem fullPrefix_implies_canonical : FullPrefixBlockLanczosClaim → BlockLanczosConjecture := by
  intro h n p A hA V hV s hs
  exact h n p A hA V hV s hs.1

#assert_trust kernel frame_coordinates
#print axioms frame_coordinates
#assert_trust kernel frame_inner
#print axioms frame_inner
#assert_trust kernel compression_action_coordinates
#print axioms compression_action_coordinates
#assert_trust kernel quadratic_action_expansion
#print axioms quadratic_action_expansion
#assert_trust kernel quadratic_form_expansion
#print axioms quadratic_form_expansion
#assert_trust kernel compressed_form_expansion
#print axioms compressed_form_expansion
#assert_trust kernel compressed_action_identity
#print axioms compressed_action_identity
#assert_trust kernel quadratic_forms_agree
#print axioms quadratic_forms_agree
#assert_trust kernel later_quadratic_identity
#print axioms later_quadratic_identity
#assert_trust kernel interval_index_validity
#print axioms interval_index_validity
#assert_trust kernel fullPrefix_implies_canonical
#print axioms fullPrefix_implies_canonical

end NLA.KE04._proved
