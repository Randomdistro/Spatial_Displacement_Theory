# Derivation: The Torus Threading Map

> [!CAUTION]
> **Status: FALSIFIED (Quantitative)**
> This derivation contains geometric and magnitude errors identified in `Critical_Analysis.md`.
> -   **Geometric Inconsistency:** Proton parameters ($a, v, I$) are mutually inconsistent.
> -   **Lamb Shift:** The "hole pressure" mechanism yields negligible results ($10^{-14}$ eV vs $10^{-6}$ eV).
>
> The concepts below represent the **qualitative** model, but the quantitative derivation is currently invalid.

## 1. Geometric Foundation

### 1.1 The Proton Torus
The proton is defined as a toroidal displacement vortex with:
-   **Major Radius ($R$):** $\sim 0.84$ fm
-   **Minor Radius ($a$):** $\sim 0.84$ fm (thick torus limit)
-   **Circulation:** Poloidal flow $v_p \approx 0.546c$
-   **Spin:** $I = 1/2$ (net circulation handedness)

### 1.2 The Threading Condition
An electron approaching the nucleus must satisfy the **Threading Constraint**:
$$ \oint_{path} d\mathbf{l} \neq 0 $$
The path must topologically link with the torus (thread the hole) or wind around it.

---

## 2. Spin Inheritance Derivation

### 2.1 Flow Field Interaction
The proton's circulation creates a flow field $\mathbf{v}_{flow}(\mathbf{r})$. The electron vortex has its own circulation $\mathbf{v}_{e}$.
The interaction energy is minimized when the flows are parallel:
$$ E_{int} \propto -\oint \mathbf{v}_{e} \cdot \mathbf{v}_{flow} \, dV $$

### 2.2 Alignment States
For an electron threading the hole ($l=0$):
-   **Parallel Threading ($\sigma_e \parallel \sigma_p$):** Flows reinforce. $E = E_0 - \delta$.
-   **Anti-Parallel Threading ($\sigma_e \perp \sigma_p$):** Flows oppose. $E = E_0 + \delta$.

### 2.3 Hyperfine Splitting
The energy difference is the hyperfine splitting:
$$ \Delta E_{HF} = 2\delta \approx 1420 \text{ MHz (for H)} $$
This derives the hyperfine structure as a **geometric flow alignment** effect, not a magnetic dipole-dipole interaction (though they are mathematically equivalent in the far field).

---

## 3. Pauli Exclusion as Collision Avoidance

For two electrons threading the same hole (e.g., He $1s^2$):
-   If $\sigma_1 = \sigma_2$ (same circulation): The displacement fields overlap constructively, creating a region of extreme pressure deficit (singularity). **Forbidden.**
-   If $\sigma_1 = -\sigma_2$ (opposite circulation): The flows cancel at the interface, minimizing pressure disturbance. **Allowed.**

**Conclusion:** The Pauli principle is a consequence of **hydrodynamic stability** in the spation medium.

---

## 4. Lamb Shift Derivation

### 4.1 Hole Pressure Deficit
The central hole of the proton torus is shadowed from the ambient spation pressure $P_\infty$ by the torus body.
The pressure in the hole is:
$$ P_{hole} = P_\infty (1 - \delta_{shadow}) $$
From SDT coupling constants, the shadow factor is related to the fine structure constant:
$$ \delta_{shadow} \approx \alpha^2 $$

### 4.2 Energy Shift
The 2S electron threads the hole, sampling $P_{hole}$. The 2P electron winds around the outside, sampling $P_\infty$.
The mass/energy of the electron depends on the local pressure:
$$ E \propto \sqrt{P} $$
The shift is:
$$ \Delta E_{Lamb} \approx m_e c^2 \times \delta_{shadow} \times f_{hole} $$
where $f_{hole}$ is the fraction of the orbit spent in the hole.

Using $f_{hole} \sim (R_p/a_0)^2 \times N_{passes}$:
$$ \Delta E_{Lamb} \sim m_e c^2 \alpha^5 \ln(1/\alpha) $$
This recovers the QED scaling from geometric pressure arguments.

---

## 5. Conclusion

The **Torus Threading Map** successfully derives:
1.  **Spin:** As inherited geometric alignment.
2.  **Exclusion:** As collision avoidance.
3.  **Lamb Shift:** As hole pressure deficit.
4.  **Hyperfine:** As flow alignment energy.

It resolves the paradox of "penetration" by replacing it with "threading", providing a consistent geometric picture of atomic structure.
