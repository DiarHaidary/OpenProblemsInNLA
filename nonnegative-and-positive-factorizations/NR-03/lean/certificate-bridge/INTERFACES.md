# NR-03 lightweight certificate bridge: interfaces before bodies

Base: `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`. The actual full-graph run passed all 384 rows and three full-family identities, then Certificate timed out with empty stdout/stderr. No particular failing declaration or cause is known. This plan isolates generic algebra for fast development feedback; it is not a new problem statement or a verification claim.

## Original data and positivity, moved without semantic changes

A new `NLA.NR03.CertificateBridge` module imports Index and Mathlib.Tactic only. Index imports FamilyDefs, Encoding and the frozen Definitions. It imports neither FamilyIdentities nor any RowCertificate/Probe module.

The following existing declarations move from Certificate into that lightweight module, in their original namespace and with the exact original definition bodies. The positivity proof will also be copied unchanged from the current reviewed source.

```lean
namespace NLA.NR03

def genericW : Matrix (BoolVec 7) (Fin 127) ℕ :=
  fun a k => sourceW (maskOfVector a) k

def genericV : Matrix (Fin 127) (BoolVec 7) ℕ :=
  fun k b => sourceV k (maskOfVector b)

def genericD : BoolVec 7 → ℕ :=
  fun b => sourceD (maskOfVector b)

theorem genericD_positive : ∀ b : BoolVec 7, 0 < genericD b
```

The original frozen Definitions.lean, Challenge.lean and all ten public target signatures stay byte-identical. Relocating the four implementation declarations changes no global name, type, numerical value, or proof body.

## Exact generic helper interfaces

```lean
namespace CertificateBridge

theorem full_sum_decomposition (a b : Mask7) :
    fullSum a b = coreSum a b + singletonSum a b + pairSum a b + fourSum a b

theorem full_identity_of_components
    (hcore : ∀ a b : Mask7, coreSum a b = coreClosed a b)
    (hsingleton : ∀ a b : Mask7, singletonSum a b = singletonClosed a b)
    (hpair : ∀ a b : Mask7, pairSum a b = pairClosed a b)
    (hfour : ∀ a b : Mask7, fourSum a b = fourClosed a b)
    (hclosed : ∀ a b : Mask7,
      coreClosed a b + singletonClosed a b + pairClosed a b + fourClosed a b =
        sourceD b * natTarget a b) :
    ∀ a b : Mask7, fullSum a b = sourceD b * natTarget a b

theorem scaled_identity_of_full
    (hfull : ∀ a b : Mask7, fullSum a b = sourceD b * natTarget a b) :
    ∀ a b : BoolVec 7,
      (castNatMatrix genericW * castNatMatrix genericV) a b =
        (genericD b : ℝ) * cMatrix 7 a b

end CertificateBridge
end NLA.NR03
```

All helper parameters above are explicit universally quantified theorem hypotheses, not new axioms, constants, input restrictions, or additions to the public problem boundary. The diagnostic establishes these conditional algebraic lemmas only. Every hypothesis has a specified existing proof at final integration.

## Exact discharge graph and unchanged final types

The final Certificate module imports the lightweight bridge and the existing successfully compiled FamilyIdentities chain. It retains these original theorem types:

```lean
namespace NLA.NR03

theorem full_identity (a b : Mask7) :
    fullSum a b = sourceD b * natTarget a b

theorem generic_scaled_identity (a b : BoolVec 7) :
    (castNatMatrix genericW * castNatMatrix genericV) a b =
      (genericD b : ℝ) * cMatrix 7 a b

end NLA.NR03
```

For `full_identity`, instantiate `full_identity_of_components` with `fun a b => core_identity a b`, `singleton_identity`, `pair_identity`, `four_identity`, and `closed_family_identity`, then apply to a and b. For `generic_scaled_identity`, instantiate `scaled_identity_of_full` with `fun a b => full_identity a b`, then apply to its two Boolean vectors. Thus both original final theorems have no additional hypotheses. Their consumers in Rank and Solution retain the same ten public statements.

## Proof and diagnostic plan

After interface review, prove decomposition with the existing `fin127_sum_split` and four explicitly scoped finite-sum congruences using the matching Index lemmas. Derive the natural identity from the five explicit hypotheses. Prove the real matrix identity using only definitional matrix entry expansion, finite-sum/multiplication casts, the supplied full natural identity, and `natTarget_cast`. This removes broad simplifier search as a proposed optimization; it is not asserted to be the measured timeout cause.

Retain the original Certificate bytes and the exact timeout evidence separately. Add raw diagnostics after genericD_positive and each helper so a later failure has a concrete last completed declaration. The lightweight development graph is Definitions → Encoding → FamilyDefs → Index → CertificateBridge; it avoids the 920.535 measured seconds of successful row-module work on each algebra iteration. The final graph still imports and discharges the complete row-family proofs, and still requires full canonical verification afterward.

Every direct module keeps 4096 MiB, one thread and 120 seconds. The workflow remains 30 minutes. No source or workflow change is live, no local Lean/Lake process or cache download is permitted, and no run is authorized by freezing these interfaces. Root and independent statement review precede proof bodies. No canonical status, public assumption, or campaign count change is proposed.
