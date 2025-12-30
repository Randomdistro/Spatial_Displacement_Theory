# Ionization Energy from Solid Angle Occlusion Calculations
## Complete Geometric Derivation - WORK IN PROGRESS

**Date:** December 2025  
**Status:** Need to actually calculate solid angles, not just change words

---

## The Problem

I need to:
1. Calculate the actual solid angle occlusion from a nucleus with $Z$ protons
2. Show how this scales with $Z$ and nuclear radius $R_N$
3. Derive the force from pressure deficit
4. Integrate to get ionization energy
5. Verify it matches observations

**NOT just change "charge" to "occlusion" - actually do the math.**

---

## Step 1: Solid Angle from Single Sphere

For a sphere of radius $R$ at distance $r$:

$$\Omega = 2\pi(1 - \cos(\theta_e))$$

where $\sin(\theta_e/2) = R/r$.

For small angles: $\cos(\theta_e) \approx 1 - \theta_e^2/2$ and $\theta_e \approx 2R/r$:

$$\Omega \approx 2\pi \left(1 - \left(1 - \frac{2R^2}{r^2}\right)\right) = 4\pi \frac{R^2}{r^2}$$

Occlusion fraction: $E = \Omega/(4\pi) = R^2/r^2$

SDT convention: $E = R^2/(4r^2)$

---

## Step 2: Solid Angle from Nucleus with Z Protons

**Question:** If I have $Z$ protons packed in a nucleus of radius $R_N$, what is the total solid angle occlusion?

**Option A:** The nucleus is a single sphere, so:
$$E_N = \frac{R_N^2}{4r^2}$$

But $R_N \propto A^{1/3} \propto Z^{1/3}$, so $E_N \propto Z^{2/3}/r^2$.

**Option B:** Each proton creates occlusion, but they overlap. Need to calculate total occlusion accounting for overlaps.

**Option C:** The occlusion is geometric ($R_N^2/(4r^2)$), but the "field strength" or "pressure" scales with $Z$ in addition.

**Which is correct?** I need to actually calculate this from the physics.

---

## Step 3: Pressure Field from Nucleus

From the multi-electron paper, the binding pressure is:

$$P_{\text{eff}} = P_{\text{CMB}} \left(\frac{R_N}{r}\right)^3 [1 - E]$$

This scales as $(R_N/r)^3$, not $(R_N/r)^2$.

And the binding energy scales as $Z^2 \Xi_{n\ell}/n^2$.

So there's a $Z^2$ factor that comes from somewhere other than just the geometric occlusion $R_N^2/(4r^2)$.

---

## Step 4: What I Need to Calculate

1. **Total solid angle occlusion from Z protons packed in radius R_N**
2. **How this scales with Z and R_N**
3. **The pressure deficit force from this occlusion**
4. **The work integral for ionization energy**
5. **Verification against experimental data**

**I haven't done this yet. I just changed words.**

---

## Next Steps

I need to:
1. Actually calculate the solid angle occlusion for a multi-proton nucleus
2. Account for how protons are packed (not just treat as a single sphere)
3. Calculate the pressure field properly
4. Derive the force from first principles
5. Integrate to get ionization energy
6. Verify the scaling matches $I_1 \propto A/r_{\text{atomic}}^2$

**This is real work, not word substitution.**

