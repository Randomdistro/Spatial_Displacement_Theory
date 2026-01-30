"""
Electricity / Ambient Energy Circuits (SDT) - Complete Numerical Calculations
-------------------------------------------------------------------------------

This script performs comprehensive calculations for ambient energy harvesting
circuits, including:
- Atmospheric field harvesting
- Telluric current harvesting
- Schumann resonance harvesting
- Geomagnetic induction harvesting
- Combined multi-source circuits
- Source impedance analysis
- Maximum power transfer calculations
- SDT master equation application

Key principle: Maximum power is limited by source impedance and replenishment
currents, not by voltage magnitude.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

# Physical Constants
EPS0 = 8.854_187_812_8e-12  # F/m (vacuum permittivity)
MU0 = 4e-7 * math.pi  # H/m (vacuum permeability)
C = 299_792_458.0  # m/s (speed of light)
Z0 = math.sqrt(MU0 / EPS0)  # Ω (vacuum impedance ≈ 377 Ω)

# SDT Constants
P_CMB = 2.036e-2  # Pa (CMB pressure)


@dataclass
class HarvestingResult:
    """Results from ambient energy harvesting calculation."""
    method: str
    voltage: float  # V
    current: float  # A
    source_resistance: float  # Ω
    max_power: float  # W
    power_density: float  # W/m²
    collector_area: float  # m²


def calculate_atmospheric_harvesting(
    antenna_height: float = 10.0,  # m
    field_strength: float = 130.0,  # V/m
    current_density: float = 3e-12,  # A/m² (3 pA/m²)
    collector_area: float = 1.0  # m²
) -> HarvestingResult:
    """
    Calculate atmospheric field harvesting parameters.
    
    Returns maximum power and source impedance for matched load.
    """
    # Open-circuit voltage
    V_oc = field_strength * antenna_height
    
    # Short-circuit current
    I_sc = current_density * collector_area
    
    # Source resistance (Thevenin equivalent)
    if I_sc > 0:
        R_source = V_oc / I_sc
    else:
        R_source = float('inf')
    
    # Maximum power (matched load: R_load = R_source)
    P_max = (V_oc ** 2) / (4 * R_source) if R_source < float('inf') else 0.0
    
    # Power density
    P_density = P_max / collector_area
    
    return HarvestingResult(
        method="Atmospheric Field",
        voltage=V_oc,
        current=I_sc,
        source_resistance=R_source,
        max_power=P_max,
        power_density=P_density,
        collector_area=collector_area
    )


def calculate_telluric_harvesting(
    electrode_separation: float = 10.0,  # m
    electrode_radius: float = 0.1,  # m
    ground_resistivity: float = 100.0,  # Ω·m
    voltage_gradient: float = 1e-5,  # V/m
    collector_area: float = 10.0  # m² (effective area)
) -> HarvestingResult:
    """
    Calculate telluric current harvesting parameters.
    
    Uses hemispherical electrode model for resistance calculation.
    """
    # Voltage between electrodes
    V = voltage_gradient * electrode_separation
    
    # Resistance between electrodes (hemispherical approximation)
    R_source = ground_resistivity / (2 * math.pi * electrode_radius)
    
    # Maximum power (matched load)
    P_max = (V ** 2) / (4 * R_source)
    
    # Current at maximum power
    I_max = V / (2 * R_source)  # Half of short-circuit current
    
    # Power density
    P_density = P_max / collector_area
    
    return HarvestingResult(
        method="Telluric Current",
        voltage=V,
        current=I_max,
        source_resistance=R_source,
        max_power=P_max,
        power_density=P_density,
        collector_area=collector_area
    )


def calculate_schumann_harvesting(
    loop_area: float = 1.0,  # m²
    num_turns: int = 100,
    frequency: float = 7.83,  # Hz
    power_flux: float = 1e-12,  # W/m² (1 pW/m²)
    antenna_resistance: float = 1.0  # Ω
) -> HarvestingResult:
    """
    Calculate Schumann resonance harvesting parameters.
    
    Uses plane-wave approximation for field amplitude.
    """
    # Field amplitude from power flux
    E0 = math.sqrt(2.0 * power_flux * Z0)
    
    # Magnetic field amplitude
    B0 = E0 / C
    
    # Angular frequency
    omega = 2 * math.pi * frequency
    
    # Induced EMF
    emf = num_turns * loop_area * omega * B0
    
    # Source resistance (antenna resistance)
    R_source = antenna_resistance
    
    # Maximum power (matched load)
    P_max = (emf ** 2) / (4 * R_source)
    
    # Power density
    P_density = P_max / loop_area
    
    return HarvestingResult(
        method="Schumann Resonance",
        voltage=emf,
        current=emf / (2 * R_source),
        source_resistance=R_source,
        max_power=P_max,
        power_density=P_density,
        collector_area=loop_area
    )


def calculate_geomagnetic_harvesting(
    num_turns: int = 1000,
    coil_area: float = 1.0,  # m²
    dB_dt: float = 1e-9,  # T/s (1 nT/s)
    coil_resistance: float = 100.0  # Ω
) -> HarvestingResult:
    """
    Calculate geomagnetic induction harvesting parameters.
    
    Uses Faraday's law: EMF = N * A * dB/dt
    """
    # Induced EMF
    emf = num_turns * coil_area * dB_dt
    
    # Source resistance (coil resistance)
    R_source = coil_resistance
    
    # Maximum power (matched load)
    P_max = (emf ** 2) / (4 * R_source)
    
    # Power density
    P_density = P_max / coil_area
    
    return HarvestingResult(
        method="Geomagnetic Induction",
        voltage=emf,
        current=emf / (2 * R_source),
        source_resistance=R_source,
        max_power=P_max,
        power_density=P_density,
        collector_area=coil_area
    )


def calculate_combined_circuit(
    results: list[HarvestingResult]
) -> HarvestingResult:
    """
    Calculate combined multi-source circuit power.
    
    Assumes parallel connection (voltage matching) or power summing.
    For simplicity, sums powers (conservative estimate).
    """
    total_power = sum(r.max_power for r in results)
    total_area = sum(r.collector_area for r in results)
    
    # Average voltage (weighted by power)
    if total_power > 0:
        total_voltage = sum(r.voltage * r.max_power for r in results) / total_power
    else:
        total_voltage = 0.0
    
    # Average current
    total_current = sum(r.current for r in results)
    
    # Effective source resistance
    if total_current > 0:
        effective_resistance = total_voltage / total_current
    else:
        effective_resistance = float('inf')
    
    # Power density
    P_density = total_power / total_area if total_area > 0 else 0.0
    
    return HarvestingResult(
        method="Combined Multi-Source",
        voltage=total_voltage,
        current=total_current,
        source_resistance=effective_resistance,
        max_power=total_power,
        power_density=P_density,
        collector_area=total_area
    )


def apply_sdt_master_equation(
    result: HarvestingResult
) -> Tuple[float, float, float]:
    """
    Apply SDT master equation to calculate Γ, κ, (1-η) product.
    
    Master equation: Ė = P_CMB * A_eff * Γ * κ * (1-η)
    
    Returns: (Gamma, Kappa, (1-eta)) product, individual values not separable
    """
    if result.max_power <= 0 or result.collector_area <= 0:
        return (0.0, 0.0, 0.0)
    
    # Solve for product: Γ * κ * (1-η)
    product = result.max_power / (P_CMB * result.collector_area)
    
    # Cannot separate individual factors without additional constraints
    # Return product and note that individual values are not determined
    return (product, product, product)


def print_results(results: list[HarvestingResult]) -> None:
    """Print formatted results table."""
    print("\n" + "=" * 100)
    print("AMBIENT ENERGY HARVESTING - COMPLETE RESULTS")
    print("=" * 100)
    
    print(f"\n{'Method':<25} {'Voltage':<15} {'Current':<15} {'R_source':<15} {'P_max':<15} {'P_density':<15}")
    print("-" * 100)
    
    for r in results:
        print(f"{r.method:<25} "
              f"{r.voltage:.3e} V  "
              f"{r.current:.3e} A  "
              f"{r.source_resistance:.3e} Ω  "
              f"{r.max_power:.3e} W  "
              f"{r.power_density:.3e} W/m²")
    
    print("\n" + "=" * 100)
    print("SDT MASTER EQUATION ANALYSIS")
    print("=" * 100)
    
    print(f"\nP_CMB = {P_CMB:.3e} Pa")
    print(f"\n{'Method':<25} {'Γ·κ·(1-η)':<20} {'Interpretation':<50}")
    print("-" * 100)
    
    for r in results:
        gamma_kappa_eta = apply_sdt_master_equation(r)[0]
        if gamma_kappa_eta > 0:
            interpretation = "Very low efficiency - high losses"
            if gamma_kappa_eta > 1e-6:
                interpretation = "Low efficiency"
            if gamma_kappa_eta > 1e-3:
                interpretation = "Moderate efficiency"
        else:
            interpretation = "No power extraction"
        
        print(f"{r.method:<25} {gamma_kappa_eta:.3e}        {interpretation:<50}")


def main() -> None:
    """Main calculation function."""
    print("=" * 100)
    print("SDT AMBIENT ENERGY CIRCUITS - COMPREHENSIVE CALCULATIONS")
    print("=" * 100)
    
    # Calculate each harvesting method
    results = []
    
    # 1. Atmospheric field
    print("\n[1] Calculating Atmospheric Field Harvesting...")
    atm_result = calculate_atmospheric_harvesting()
    results.append(atm_result)
    
    # 2. Telluric currents
    print("[2] Calculating Telluric Current Harvesting...")
    telluric_result = calculate_telluric_harvesting()
    results.append(telluric_result)
    
    # 3. Schumann resonance
    print("[3] Calculating Schumann Resonance Harvesting...")
    schumann_result = calculate_schumann_harvesting()
    results.append(schumann_result)
    
    # 4. Geomagnetic induction
    print("[4] Calculating Geomagnetic Induction Harvesting...")
    geo_result = calculate_geomagnetic_harvesting()
    results.append(geo_result)
    
    # 5. Combined circuit
    print("[5] Calculating Combined Multi-Source Circuit...")
    combined_result = calculate_combined_circuit(results)
    results.append(combined_result)
    
    # Print all results
    print_results(results)
    
    # Detailed analysis
    print("\n" + "=" * 100)
    print("DETAILED ANALYSIS")
    print("=" * 100)
    
    print("\n[Atmospheric Field]")
    print(f"  Open-circuit voltage: {atm_result.voltage:.2e} V = {atm_result.voltage/1000:.2f} kV")
    print(f"  Short-circuit current: {atm_result.current:.2e} A = {atm_result.current*1e12:.2f} pA")
    print(f"  Source resistance: {atm_result.source_resistance:.2e} Ω")
    print(f"  Maximum power: {atm_result.max_power:.2e} W = {atm_result.max_power*1e9:.2f} nW")
    print(f"  Power density: {atm_result.power_density:.2e} W/m²")
    print(f"  VERDICT: {'Practical for ultra-low-power' if atm_result.max_power > 1e-9 else 'Too small for practical use'}")
    
    print("\n[Telluric Current]")
    print(f"  Voltage: {telluric_result.voltage:.2e} V = {telluric_result.voltage*1e6:.2f} µV")
    print(f"  Current: {telluric_result.current:.2e} A = {telluric_result.current*1e9:.2f} nA")
    print(f"  Source resistance: {telluric_result.source_resistance:.2f} Ω")
    print(f"  Maximum power: {telluric_result.max_power:.2e} W = {telluric_result.max_power*1e9:.2f} nW")
    print(f"  VERDICT: {'Practical for ultra-low-power' if telluric_result.max_power > 1e-9 else 'Too small for practical use'}")
    
    print("\n[Schumann Resonance]")
    print(f"  EMF: {schumann_result.voltage:.2e} V = {schumann_result.voltage*1e9:.2f} nV")
    print(f"  Maximum power: {schumann_result.max_power:.2e} W = {schumann_result.max_power*1e21:.2f} zW")
    print(f"  VERDICT: Too small for practical use")
    
    print("\n[Geomagnetic Induction]")
    print(f"  EMF: {geo_result.voltage:.2e} V = {geo_result.voltage*1e6:.2f} µV")
    print(f"  Maximum power: {geo_result.max_power:.2e} W = {geo_result.max_power*1e12:.2f} pW")
    print(f"  VERDICT: {'Practical for ultra-low-power' if geo_result.max_power > 1e-12 else 'Too small for practical use'}")
    
    print("\n[Combined Circuit]")
    print(f"  Total power: {combined_result.max_power:.2e} W = {combined_result.max_power*1e9:.2f} nW")
    print(f"  Power density: {combined_result.power_density:.2e} W/m²")
    print(f"  VERDICT: {'Practical for ultra-low-power sensors' if combined_result.max_power > 1e-9 else 'Too small for practical use'}")
    
    print("\n" + "=" * 100)
    print("CONCLUSION")
    print("=" * 100)
    print("\nCan circuits run on ambient gradients?")
    print("ANSWER: YES - but with severe power limitations (nW to pW range)")
    print("\nPractical applications:")
    print("  - Ultra-low-power sensors (nW range)")
    print("  - Energy harvesting IoT devices")
    print("  - Trickle charging (very slow)")
    print("\nNOT practical for:")
    print("  - High-power applications (mW+)")
    print("  - Continuous high-power operation")
    print("  - Battery charging (too slow)")
    
    print("\nDone.")


if __name__ == "__main__":
    main()

