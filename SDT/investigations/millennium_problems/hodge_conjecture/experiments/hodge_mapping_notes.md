# Hodge Classes → SDT Field Dictionary

SDT treats every algebraic construct as a concrete spation configuration. This
note translates the Hodge-conjecture vocabulary into SDT fields so the upcoming
simulation harness can be parameterized without guesswork.

## 1. Dictionary of Objects

| Hodge-theory term | SDT interpretation | Governing field(s) |
| --- | --- | --- |
| Smooth projective variety \(X\subset\mathbb{CP}^N\) | Displacement surface carved out of the spation lattice; locally a nested stack of turbine shells | Pressure \(P\), curvature density \(\kappa\), slip \(\eta\) |
| Harmonic \((p,q)\)-form | Static pressure/flow pattern with \(p\) spatial curls and \(q\) temporal curls | Flow field \(\mathbf{v}\), divergence-free constraint |
| Hodge class | Equilibrium configuration with \(\dot e = 0\) and master-equation throughput set by the occlusion profile of \(X\) | \(P_\infty \Gamma \kappa (1-\eta)\) |
| Algebraic cycle | Fundamental turbine cell (single or linked toroidal radius) embedded in \(X\) | Local boosts in \(\kappa\), suppressed \(\eta\), prescribed \(\Gamma\) |
| Rational linear combination | Superposition coefficients inherited from count ratios of turbine cells and their occlusion factors | Dimensionless weights derived from PCMB-normalized areas |

Key SDT principle: the master equation already yields a linear decomposition of
any pressure pattern into turbine contributions
\[
\dot e(\mathbf{x}) = P(\mathbf{x}) \Gamma(\mathbf{x}) \kappa(\mathbf{x}) (1-\eta(\mathbf{x})) = \sum_i r_i \, P_\infty A_i \Gamma_i \kappa_i (1-\eta_i),
\]
where the \(r_i\) are rational because the occluded solid angles and turbine
counts are ratios of integer lattice counts.

## 2. Concrete Test Variety

We will prototype on a **complex 2-torus \(T^2 = \mathbb{C}^2 / \Lambda\)**, which
admits both algebraic and non-algebraic representatives. In SDT terms:

- Represent \(T^2\) as a **four-layer toroidal sheet** floating in the lattice.
- Each fundamental 1-cycle corresponds to a proton-style turbine loop.
- The full \(T^2\) Hodge decomposition (1,1)-forms map to **paired circulation
  streams** with mutually orthogonal slip suppressions.

### Field parameters for the simulation grid

| Parameter | Value | Rationale |
| --- | --- | --- |
| Grid (`nx=ny=32, nz=8`) | Enough resolution to wrap two independent cycles; thin thickness in z | Minimizes runtime while preserving topology |
| Grid spacing (`dx=dy=2.0 fm`, `dz=1.0 fm`) | Keeps timestep sane for SDT-Navier while still resolving nuclear-scale curvature | Matches proton radius scale |
| \(P_\infty\) | `2.036e-2 Pa` | CMB pressure from SDT fundamentals |
| Base \(\kappa\) | `0` background, `2.0e3 m⁻¹` on torus sheet (clamped ≤ `5.0e3 m⁻¹`) | Prevents runaway curvature while preserving toroidal signature |
| Base \(\eta\) | `0.55` outside, `0.08` on algebraic cycles (down to `0.04` where they overlap) | Low slip encodes traction but stays within numerical stability window |
| \(\Gamma\) | `0.04` for single cycles, `0.08` where cycles intersect | Circulation doubles when cycles overlap |
| Occlusion factor | `O=0.35` inside torus | Captures 35% pressure drop due to displacement surface |

### Algebraic cycle seeding

1. **Cycle \(a\)** (longitude): place a ring of turbine sources at \(z=0\) with
   radius `r_a = 6 dx`.  
2. **Cycle \(b\)** (meridian): second ring orthogonal to the first, sharing the
   same center but lifted to `z = 1 dz`.
3. **Combination cycle \(a+b\)**: cells where both rings overlap receive
   doubled \(\Gamma\) and halved \(\eta\), plus curvature clamp at `5.0e3 m⁻¹`.

These three seeds correspond to a basis of \(H_2(T^2,\mathbb{Q})\). Every Hodge
class on the torus will be supplied to the solver as a tuple of rational weights
on \((a, b, a+b)\).

## 3. Encoding Procedures

1. **Displacement surface mask**  
   Create a boolean array \(M\) marking torus cells. Set \(P = P_\infty (1 -
   O)\) where \(O\) is the occlusion fraction derived from the mask.

2. **Curvature & slip fields**  
   Use `add_turbine_source` to punch in curvature around each algebraic cycle.
   After injection, clamp \(\eta\) using:
   \[
   \eta_\text{target} = \eta_\text{ambient} - r_i(1-\eta_\text{ambient}),
   \]
   ensuring the rational coefficient \(r_i\) directly tunes traction.

3. **Hodge-class pressure pattern**  
   For a target class \(c = \alpha [a] + \beta [b]\) with \(\alpha,\beta\in
   \mathbb{Q}\), set a slip modulation
   \[
   \Delta \eta = \alpha \cdot \delta\eta_a + \beta \cdot \delta\eta_b
   \]
   before recomputing energy density.

4. **Measurement outputs**  
   - Per-cycle throughput \(E_i = \int_{\text{cycle}_i} P \Gamma \kappa (1-\eta)\).
   - Residual slip outside the span of the seeded cycles.
   - Divergence norm to verify harmonicity.

These steps lock the simulation harness to explicit SDT field values, providing
the foundation for the code in `run_hodge_pressure_basis.py`.

