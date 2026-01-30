"""
Electricity / Ambient Energy (SDT) - Numerical sanity checks
------------------------------------------------------------

This script checks the prompt's back-of-envelope calculations using
standard electromagnetism energy relations (which SDT claims to reproduce
in the macroscopic limit) and prints corrected orders of magnitude.

Key point (applies in SDT too if energy conservation holds):
  - Stored energy density u can be nonzero even when harvestable *power* is tiny.
  - Harvestable power is bounded by energy flux into the harvester:
      P_out <= ∫ S · dA  (EM waves) or  P_out <= ∫ J · E dV  (conduction)
    and by source impedance / replenishment currents (quasi-static fields).
"""

from __future__ import annotations

import math


EPS0 = 8.854_187_812_8e-12  # F/m
MU0 = 4e-7 * math.pi  # H/m
C = 299_792_458.0  # m/s
Z0 = math.sqrt(MU0 / EPS0)  # vacuum impedance (Ohms)


def u_electric(E_v_per_m: float) -> float:
    """Electric energy density (J/m^3) for quasi-static field."""
    return 0.5 * EPS0 * E_v_per_m**2


def u_magnetic(B_t: float) -> float:
    """Magnetic energy density (J/m^3) for quasi-static field."""
    return 0.5 * (B_t**2) / MU0


def plane_wave_E_from_flux(S_w_per_m2: float) -> float:
    """
    For a plane wave:
      <S> = (1/2) * E0^2 / Z0  = (1/2) * c * eps0 * E0^2
    Returns E0 (peak) in V/m.
    """
    return math.sqrt(2.0 * S_w_per_m2 * Z0)


def plane_wave_B_from_E(E_v_per_m: float) -> float:
    """For a plane wave in vacuum: B0 = E0 / c."""
    return E_v_per_m / C


def main() -> None:
    print("=" * 78)
    print("SDT Electricity/Ambient Energy — numerical sanity checks")
    print("=" * 78)

    # 1) Atmospheric quasi-static E-field (fair weather)
    E_atm = 130.0  # V/m
    u_atm = u_electric(E_atm)
    print("\nAtmospheric E-field (quasi-static):")
    print(f"  E = {E_atm:.1f} V/m")
    print(f"  u_E = 0.5*eps0*E^2 = {u_atm:.3e} J/m^3")

    # 2) Schumann resonance power density sanity check
    # Prompt claims ~1 pW/m^2 at fundamental.
    S_schumann = 1e-12  # W/m^2
    E0 = plane_wave_E_from_flux(S_schumann)
    B0 = plane_wave_B_from_E(E0)
    print("\nSchumann-scale plane-wave equivalent (if S≈1 pW/m^2):")
    print(f"  <S> = {S_schumann:.1e} W/m^2")
    print(f"  E0 = sqrt(2 S Z0) = {E0:.3e} V/m  ({E0*1e6:.2f} µV/m)")
    print(f"  B0 = E0/c         = {B0:.3e} T    ({B0*1e12:.2f} pT)")

    # Compare energy density implied by that plane wave
    u_wave = u_electric(E0) + u_magnetic(B0)
    # For a plane wave u = <S>/c (time-avg), so this is a good consistency check.
    u_flux = S_schumann / C
    print(f"  u (from fields)   = {u_wave:.3e} J/m^3")
    print(f"  u (from S/c)      = {u_flux:.3e} J/m^3")

    # 3) Geomagnetic field energy density (quasi-static, not harvestable unless time-varying)
    B_earth = 50e-6  # 50 µT
    u_B_earth = u_magnetic(B_earth)
    print("\nEarth's static B-field energy density (not directly harvestable without dB/dt):")
    print(f"  B = {B_earth:.2e} T")
    print(f"  u_B = B^2/(2µ0) = {u_B_earth:.3e} J/m^3")

    # 4) A simple induction example: EMF from dB/dt in a loop
    # epsilon = N A dB/dt
    N = 1000
    A = 1.0  # m^2
    dB_dt = 1e-9  # T/s (1 nT/s)
    emf = N * A * dB_dt
    print("\nInduction sanity check (loop):")
    print(f"  N={N}, A={A} m^2, dB/dt={dB_dt:.1e} T/s -> emf = {emf:.3e} V")

    # 5) Global electric circuit rough bound (order-of-magnitude)
    # Typical downward current density ~ 1–3 pA/m^2 in fair weather.
    # Potential difference ionosphere-ground ~ 250–400 kV.
    J = 2e-12  # A/m^2
    V = 300e3  # V
    P_area = J * V  # W/m^2
    print("\nGlobal electric circuit bound (order-of-magnitude):")
    print(f"  J ≈ {J:.1e} A/m^2, V ≈ {V:.2e} V -> P/A ≈ J*V = {P_area:.3e} W/m^2")
    print("  (This is the replenishment-limited power flow; devices can’t exceed it on average.)")

    print("\nDone.")


if __name__ == "__main__":
    main()


