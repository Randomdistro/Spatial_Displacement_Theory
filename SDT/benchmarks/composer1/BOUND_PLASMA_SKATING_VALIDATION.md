# Bound Plasma Skating: Validation of Predictions

**Date:** January 2, 2026  
**Author:** Claude Opus 4.5 (Anthropic AI)  
**Purpose:** Validate whether framework correctly predicts which elements, excitations, and ionizations engage in bound plasma skating

---

## What is "Bound Plasma Skating"?

**Definition:** Collective electron motion where electrons "skate" on the pressure field - bound (not free) but still collective. This is distinct from:

1. **Free-electron plasma** (metals): Electrons are free, collective oscillations at ω_p
2. **Bound plasma skating** (non-metals, some metals): Electrons are bound but move collectively
3. **Individual atomic transitions**: No collective behavior

**SDT Picture:**
- Electrons "skate" on pressure field gradients
- Bound by nuclear field but can move collectively
- Φ-fields overlap → collective response
- Frequency: Depends on binding strength and collective coupling

---

## Critical Question

**Does the framework correctly predict which elements engage in bound plasma skating?**

---

## Analysis: Li-Ne Elements

### Prediction vs Reality

| Element | Z_eff | Material Type | Free Plasma? | Bound Skating? | Framework Prediction | Correct? |
|---------|-------|---------------|--------------|----------------|---------------------|----------|
| Li | 1 | Metal | ✓ Yes | ✓ Yes | ω_p = 8.0 eV | ✓ |
| Be | 2 | Metal | ✓ Yes | ✓ Yes | ω_p = 18.4 eV | ✓ |
| B | 3 | Metalloid | Partial | ✓ Yes | ω_p = 26.0 eV | ⚠️ |
| C | 4 | Metal (graphite) / Insulator (diamond) | Graphite: Yes | Both: Yes | ω_p = 26.5 eV | ⚠️ |
| N | 5 | Non-metal (N₂) | ✗ No | ✓ Yes (molecular) | ω_p = 18.4 eV | ❌ |
| O | 6 | Non-metal (O₂) | ✗ No | ✓ Yes (molecular) | ω_p = 21.3 eV | ❌ |
| F | 7 | Non-metal (F₂) | ✗ No | ✓ Yes (molecular) | ω_p = 23.0 eV | ❌ |
| Ne | 8 | Noble gas | ✗ No | ✓ Yes (condensed) | ω_p = 21.9 eV | ❌ |

---

## Problem Identified

### Issue 1: Framework Computes Free-Electron Plasma for Non-Metals

**Problem:**
- Framework computes ω_p = √(n_e e²/(ε₀ m_e)) for ALL elements
- This is the **free-electron plasma frequency**
- But N, O, F, Ne are **non-metals** - they don't have free-electron plasma!

**What Should Happen:**
- **Metals (Li, Be, B, C-graphite):** Free-electron plasma at ω_p ✓
- **Non-metals (N, O, F, Ne):** Bound collective modes, NOT free plasma ✗

**Current Framework:**
- Predicts ω_p for all (treats all as free-electron plasma)
- **This is WRONG for non-metals**

### Issue 2: Framework Doesn't Distinguish Metal vs Non-Metal

**Missing Criterion:**
- Framework determines Z_eff (which electrons participate)
- But doesn't determine if material is **metallic** or **insulating**
- Both can have participating electrons, but different collective behavior

**What's Needed:**
- Additional criterion to distinguish:
  - **Metals:** Participating electrons → free plasma (ω_p)
  - **Non-metals:** Participating electrons → bound collective modes (NOT ω_p)

---

## What the Framework DOES Predict Correctly

### ✓ Correct Predictions

1. **Which electrons participate (Z_eff):**
   - Li: Z_eff = 1 (2s¹) ✓
   - Be: Z_eff = 2 (2s²) ✓
   - B: Z_eff = 3 (2s²2p¹) ✓
   - C: Z_eff = 4 (2s²2p²) ✓
   - N: Z_eff = 5 (2s²2p³) ✓
   - O: Z_eff = 6 (2s²2p⁴) ✓
   - F: Z_eff = 7 (2s²2p⁵) ✓
   - Ne: Z_eff = 8 (2s²2p⁶) ✓

2. **Core exclusion:**
   - All: 1s² does NOT participate ✓
   - Correctly identifies core vs valence

3. **Spatial scales:**
   - r_WS, λ_{nℓ}, a_n all computed correctly ✓

### ✗ Incorrect Predictions

1. **Free-electron plasma for non-metals:**
   - N, O, F, Ne: Framework computes ω_p
   - But these are non-metals - no free-electron plasma!
   - **Should predict bound collective modes instead**

2. **Material classification:**
   - Framework doesn't distinguish metal vs non-metal
   - Treats all as if they have free-electron plasma

---

## What "Bound Plasma Skating" Should Mean

### For Metals (Li, Be, B, C-graphite)

**Bound plasma skating:**
- Electrons are "bound" to lattice (not free)
- But can "skate" collectively on pressure field
- **Manifestation:** Free-electron plasma oscillations (ω_p)
- **Framework prediction:** ✓ Correct (computes ω_p)

### For Non-Metals (N, O, F, Ne)

**Bound plasma skating:**
- Electrons are bound (molecular orbitals, band gap)
- Can still "skate" collectively (excitons, bound plasmons)
- **Manifestation:** Bound collective modes, NOT free plasma
- **Framework prediction:** ✗ Wrong (computes free ω_p)

---

## Corrected Interpretation

### What the Framework Actually Predicts

**Z_eff (participating electron count):**
- ✓ Correctly predicts which electrons can participate in collective behavior
- ✓ Correctly excludes core electrons

**ω_p (plasma frequency):**
- ✓ Correct for **metals** (free-electron plasma)
- ✗ **Wrong for non-metals** (should be bound modes, not free plasma)

### What Should Be Predicted

**For metals:**
- Z_eff → n_e → ω_p (free-electron plasma) ✓
- Framework does this correctly

**For non-metals:**
- Z_eff → n_e → **bound collective frequency** (NOT ω_p)
- Framework currently computes ω_p (wrong)
- Should compute bound plasmon/exciton frequency instead

---

## Excitations and Ionizations

### Question: Which Excitations Engage in Bound Plasma Skating?

**Framework Prediction:**
- All participating electrons (Z_eff) can engage in collective behavior
- Core electrons (non-participating) cannot

**Reality Check:**

**Metals (Li, Be, B, C-graphite):**
- ✓ Valence electrons → Free-electron plasma (ω_p)
- ✓ Framework correct

**Non-metals (N, O, F, Ne):**
- ✓ Valence electrons → Bound collective modes
- ✗ Framework computes free ω_p (wrong)
- Should compute bound mode frequency

### Ionizations

**Framework doesn't explicitly predict ionizations, but:**

**First Ionization Energy:**
- Should correlate with binding of participating electrons
- Li: I₁ = 5.39 eV (2s¹) - participating electron
- Be: I₁ = 9.32 eV (2s²) - participating electrons
- N: I₁ = 14.5 eV (2p³) - participating electrons
- **Pattern:** I₁ for participating electrons is lower (easier to remove)

**Framework Implication:**
- Participating electrons (Z_eff) should have lower I₁
- Non-participating (core) should have higher I₁
- **This is consistent** ✓

---

## The Missing Piece: Metal vs Non-Metal Criterion

### What's Needed

**Additional SDT criterion to determine:**
- **Metallic:** Participating electrons → free-electron plasma (ω_p)
- **Non-metallic:** Participating electrons → bound collective modes

**Possible SDT Criteria:**

1. **Band gap from Φ-overlap:**
   - If O_i > O_* AND band gap < k_B T → Metal
   - If O_i > O_* AND band gap > k_B T → Non-metal

2. **Pressure field coupling:**
   - Strong coupling → Free plasma
   - Weak coupling → Bound modes

3. **Lattice structure:**
   - Metallic bonding → Free plasma
   - Covalent/ionic → Bound modes

**Currently missing from framework.**

---

## Validation Summary

### ✓ What Framework Predicts Correctly

1. **Z_eff (participating electron count):**
   - All Li-Ne: Z_eff = Z - 2 ✓
   - Correctly excludes core 1s² ✓

2. **Which electrons participate:**
   - Valence (2s, 2p) → Participate ✓
   - Core (1s) → Do NOT participate ✓

3. **Spatial scales:**
   - r_WS, λ_{nℓ}, a_n all correct ✓

4. **For metals:**
   - Free-electron plasma frequency (ω_p) ✓

### ✗ What Framework Predicts Incorrectly

1. **Free-electron plasma for non-metals:**
   - N, O, F, Ne: Computes ω_p (free plasma)
   - But these are non-metals - should have bound modes ✗

2. **Material classification:**
   - Doesn't distinguish metal vs non-metal
   - Treats all as free-electron plasma ✗

### ⚠️ What's Ambiguous

1. **"Bound plasma skating":**
   - Framework predicts participation (O_i > 0.45)
   - But doesn't specify free vs bound collective behavior
   - For metals: Free plasma (correct)
   - For non-metals: Should be bound modes (currently computes free)

---

## Answer to User's Question

**"Do the calculations correctly predict which elements, excitations and ionizations engage in bound plasma skating?"**

### Answer: **PARTIALLY**

**Correctly predicts:**
- ✓ Which **electrons** participate (Z_eff)
- ✓ Which **elements** have participating electrons (all Li-Ne)
- ✓ **Ionization pattern** (participating electrons have lower I₁)

**Incorrectly predicts:**
- ✗ **Free-electron plasma** for non-metals (N, O, F, Ne)
- ✗ **Material type** (doesn't distinguish metal vs non-metal)

**Missing:**
- ⚠️ Criterion to distinguish free plasma vs bound collective modes
- ⚠️ Explicit prediction of bound plasmon/exciton frequencies for non-metals

### The Core Issue

**Framework predicts participation (O_i > 0.45) correctly, but:**
- For metals: Participation → Free plasma (ω_p) ✓
- For non-metals: Participation → Bound modes (NOT ω_p) ✗

**Framework currently computes ω_p for all, which is wrong for non-metals.**

---

## Recommendation

**Add metal/non-metal criterion to framework:**

1. **Compute band gap from Φ-overlap** (or use structure)
2. **If band gap < threshold:** Free-electron plasma (ω_p)
3. **If band gap > threshold:** Bound collective modes (different frequency)

**Then framework will correctly predict:**
- Which elements have free plasma (metals)
- Which elements have bound skating (non-metals)
- Which excitations engage in each

---

**End of Validation**
