# Volume 01: Foundations and Spation Primitives — Book 01: Foundational Axioms and Core Principles

This book is the narrative backbone of SDT’s first principles. Every chapter is an explicit extraction of
the foundation papers, rendered in a continuous, professional voice and supported by the actual numeric
constants and equations that anchor SDT. The tone is direct and explanatory; the mathematics is present,
visible, and used.

---

## Chapter 01: Foundational Principles

### Abstract

SDT begins by naming what exists and refusing what does not. Space is the matrix, matter is boundary,
movement is the class of change, and now is the ordering of change. From those four primitives we build
the pressure field, the occlusion function, and the geometric parameters that appear throughout the
entire theory. The chapter is a deliberate construction: definitions first, then equations, then
dimensional closure, then numerical constants, then consequences.

### Introduction

The common habit is to treat empty space as a rule-bound vacuum. SDT refuses this. If rules exist and
distance is coherent, then a substrate exists. SDT names that substrate the **matrix** and defines the
discrete unit of the matrix as the **spation**. What follows is not philosophical garnish; it is the
mathematical scaffolding that produces every later equation.

### Definitions

We keep the primitives explicit:

- **Space:** the matrix, a continuous medium that supports pressure propagation at speed `c`.
- **Matter:** boundary geometry that excludes matrix volume.
- **Movement:** the total class of change within the matrix and its boundaries.
- **Now:** the ordering of change as realized in the present configuration.

### Mathematical Grounding

The pressure field is the first principle:

$$
\Pi(\mathbf{r}) = \int_{4\pi} I_{\text{CMB}}(\hat{\mathbf{n}})\left[1 - E(\mathbf{r},\hat{\mathbf{n}})\right]\, d\Omega
$$

The constants are not rhetorical; they are numeric anchors:

$$
P_{\text{CMB}} = 2.036 \times 10^{-2}\ \text{Pa}, \qquad
K_{\text{bulk}} = 4.6 \times 10^{113}\ \text{Pa}, \qquad
c = 2.99792458 \times 10^8\ \text{m/s}.
$$

The spation scale is tied to the Planck length:

$$
d_P = 1.616255 \times 10^{-35}\ \text{m}.
$$

The force is the pressure gradient acting on displacement volume:

$$
\mathbf{F} = -V_{\text{disp}} \nabla \Pi(\mathbf{r}).
$$

### Results

From these definitions we extract the immediate consequences:

- Pressure gradients are the origin of interaction.
- Occlusion encodes interaction strength via angular deficit.
- Every later constant is derived, not inserted.

### Discussion

SDT’s premise is strict: no entity enters the theory without a geometric role. That is why the pressure
field and occlusion function appear before any discussion of “forces,” and why every force becomes a
geometric limit of the same equation.

### Conclusion

The chapter establishes SDT’s basic grammar: the matrix exists, the spation is its discrete unit, and the
pressure field is the continuous mechanism that connects all later derivations.

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Foundational_Principles/Foundational_Principles.md`

---

## Chapter 02: SDT-Navier Field Theory

### Abstract

The SDT-Navier field theory converts the master equation into local field dynamics. It defines the field
state, enforces incompressibility, and derives flow, curvature, and slip evolution directly from the
pressure field.

### Introduction

The master equation is global; it must be localized for multi-body interaction and simulation. That is
the purpose of SDT-Navier: it is the field form of SDT, built from the same primitives and closed by
dimensional verification.

### Field Definitions

The field state is

$$
\mathbf{U}(\mathbf{x},t) = (P, \mathbf{v}, \kappa, \eta, e)^T.
$$

Local energy throughput is

$$
\dot{e}(\mathbf{x},t) = P(\mathbf{x},t)\,\sigma(\mathbf{x},t),
$$

with

$$
\sigma(\mathbf{x},t) = \Gamma(\mathbf{x},t)\,\kappa(\mathbf{x},t)\,(1-\eta(\mathbf{x},t)).
$$

### Flow and Constraints

Incompressibility gives

$$
\nabla \cdot \mathbf{v} = 0.
$$

The flow equation is

$$
\rho_s \left(\frac{\partial\mathbf{v}}{\partial t} + (\mathbf{v}\cdot\nabla)\mathbf{v}\right)
= -\nabla P - \alpha \nabla\kappa - \beta \eta \mathbf{v}.
$$

Curvature and slip evolve as

$$
\frac{\partial \kappa}{\partial t} + (\mathbf{v}\cdot\nabla)\kappa
  = \mathcal{C}(\kappa,\mathbf{v}) - \mathcal{D}(\kappa,\eta),
$$

$$
\frac{\partial \eta}{\partial t} + (\mathbf{v}\cdot\nabla)\eta
  = \mathcal{S}_{\text{strain}}(\kappa,\mathbf{v}) - \mathcal{S}_{\text{healing}}(\kappa).
$$

### Results

The SDT-Navier system provides a closed field formulation of SDT and supplies the equations used in
simulation and validation pipelines.

### Discussion

This is not an analogy to Navier–Stokes; it is a direct consequence of SDT primitives. Pressure is the
driver, curvature and slip are geometry, and the field equations are the only consistent way to carry the
master equation into local dynamics.

### Conclusion

The SDT-Navier field theory is the local, computationally viable form of SDT, and it retains the same
geometric roots as the global derivations.

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/SDT_Navier_Field_Theory/SDT_Navier_Field_Theory.md`

---

## Chapter 03: Core Engine Mathematical Proof

### Abstract

We derive the master equation from pressure, boundary geometry, circulation, curvature, and slip. Every
term is derived, not assumed.

### Derivation

Pressure force on a boundary:

$$
F_{\text{pressure}} = P_{\text{CMB}} A_{\text{eff}}.
$$

Circulation modifies throughput:

$$
P_{\text{flow}} = P_{\text{CMB}} \Gamma.
$$

Curvature enhances capture:

$$
P_{\text{curved}} = P_{\text{flow}} \kappa = P_{\text{CMB}} \Gamma \kappa.
$$

Slip reduces coupling:

$$
P_{\text{effective}} = P_{\text{curved}} (1-\eta).
$$

Energy throughput is pressure times area times characteristic velocity:

$$
\dot{E} = P_{\text{effective}} A_{\text{eff}} v_{\text{char}}.
$$

For toroidal systems, $v_{\text{char}} = c$, giving

$$
\boxed{\dot{E} = P_{\text{CMB}} A_{\text{eff}} \Gamma \kappa (1-\eta)}.
$$

### Dimensional Closure

$$
[\dot{E}] = \text{Pa}\cdot\text{m}^2\cdot\text{m}^{-1}\cdot\text{m}\cdot\text{s}^{-1}
= \text{kg}\cdot\text{m}^2\cdot\text{s}^{-3}.
$$

### Numerical Template

$$
\dot{E} = (2.036 \times 10^{-2})\,A_{\text{eff}}\,\Gamma\,\kappa\,(1-\eta)\ \text{W}.
$$

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Core_Engine_Mathematical_Proof/Core_Engine_Mathematical_Proof.md`

---

## Chapter 04: Unified Physics from the Master Equation

### Abstract

The same equation produces electromagnetism, gravitation, thermodynamics, and atomic structure by
changing geometric regime.

### Regime Examples

Electromagnetic limit:

$$
F_{\text{EM}} = \frac{\kappa_1 \kappa_2}{4\pi K_{\text{bulk}} r^2}.
$$

Gravitational limit:

$$
G = \frac{c^4}{4\pi K_{\text{bulk}}^2}, \qquad
F_{\text{grav}} = G\frac{m_1 m_2}{r^2}.
$$

Temperature from shunt statistics:

$$
k_B T = h\langle \nu \rangle.
$$

### Discussion

The unification is geometric: there is one pressure field, one occlusion function, and one master
equation. The rest is regime selection.

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Unified_Physics_from_Master_Equation/Unified_Physics_from_Master_Equation.md`

---

## Chapter 05: Topology from Spation Structure

### Abstract

Topology is the geometric memory of the matrix: winding numbers, surface invariants, and topological
phases are all pressure-geometry invariants.

### Core Equations

Winding number:

$$
w = \frac{1}{2\pi} \oint \nabla \phi \cdot d\mathbf{l}.
$$

Surface invariant:

$$
C = \frac{1}{2\pi} \int \mathbf{F}\cdot d\mathbf{S}.
$$

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Topology_from_Spation_Structure/Topology_from_Spation_Structure.md`

---

## Chapter 06: Symmetry Breaking from Geometric Instability

### Abstract

Symmetry breaks when geometry becomes unstable. The matrix reorganizes into lower-symmetry minima.

### Instability Criterion

$$
\frac{\partial^2 E}{\partial \phi^2} < 0.
$$

### Interpretation

The system selects new minima, and the lowest-cost modes are the residual sliding directions of the new
geometry.

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Symmetry_Breaking_from_Geometric_Instability/Symmetry_Breaking_from_Geometric_Instability.md`

---

## Chapter 07: Information Theory from Spation States

### Abstract

Information is a property of spation configuration probability. Entropy is geometric counting.

### Core Equations

$$
I = -\log_2 P, \qquad
S = -k_B \sum_i P_i \ln P_i.
$$

Channel capacity:

$$
C = \max_{P(X)} I(X;Y).
$$

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Information_Theory_from_Spation_States/Information_Theory_from_Spation_States.md`

---

## Chapter 08: Renormalization from Scale Hierarchy

### Abstract

Renormalization is scale transition in the matrix hierarchy. Couplings run because occlusion geometry
changes with scale.

### Scale Dependence

$$
\alpha(\mu) = \alpha(\mu_0) + \beta \ln(\mu/\mu_0).
$$

Effective description:

$$
\mathcal{L}_{\text{eff}} = \langle \mathcal{L}_{\text{micro}} \rangle_{\mu}.
$$

### References

- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/00_Foundations/Renormalization_from_Scale_Hierarchy/Renormalization_from_Scale_Hierarchy.md`
