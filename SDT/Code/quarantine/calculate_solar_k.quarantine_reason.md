# Quarantine Reason: calculate_solar_k.py

**Moved**: 2026-03-23
**Violation**: Uses `G = 6.67430e-11`, `M_sun = 1.989e30`, and `R_s = 2*G*M_sun/c²` (Schwarzschild radius) as primary computational inputs.

**SDT Rules Violated**: R1 (G as input), R2 (M as input), R9 (Schwarzschild radius)

**Replacement**: `calculate_solar_k_sdt.py` — derives solar κ from observed orbital velocities using `κ = c/v`, no G or M required.
