"""
SDT Participation Functional Calculation - Pure Phi-Overlap Method
================================================================
Author: Claude Opus 4.5 (Anthropic AI)
Date: January 2, 2026

CORRECTED VERSION: No E_b imports, pure geometry-based O_i calculation
"""

import numpy as np
from scipy import integrate
from scipy.special import sph_harm
import json
from pathlib import Path

# Physical constants (CODATA 2018)
HBAR = 1.054571817e-34  # J·s
M_E = 9.1093837015e-31   # kg
E_CHARGE = 1.602176634e-19  # C
EPSILON_0 = 8.8541878128e-12  # F/m
C = 2.99792458e8         # m/s
A_0 = 5.29177210903e-11  # m (Bohr radius)
N_A = 6.02214076e23      # mol⁻¹

# Phase-7 locking threshold
O_THRESHOLD = 0.45  # From SDT contact mechanics


def generate_phi_radial(n, l, r, a_n=None, lambda_nl=None):
    """
    Generate radial profile R_{nℓ}(r) from SDT toroidal vortex geometry.
    
    Parameters:
    -----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    r : array
        Radial coordinates (m)
    a_n : float, optional
        Characteristic radius (default: n² a_0)
    lambda_nl : float, optional
        Decay length (default: n × a_0 × f_ℓ)
    
    Returns:
    --------
    R : array
        Radial profile R_{nℓ}(r)
    """
    if a_n is None:
        a_n = n**2 * A_0
    
    if lambda_nl is None:
        # Angular momentum factor
        f_l = {0: 1.0, 1: 0.8, 2: 0.3, 3: 0.15}.get(l, 0.1)
        lambda_nl = n * A_0 * f_l
    
    # Radial profile: R_{nl}(r) = Phi_0 (r/a_n)^l exp(-r/lambda_{nl})
    phi_0 = 1.0  # Normalization constant
    R = phi_0 * (r / a_n)**l * np.exp(-r / lambda_nl)
    
    return R, a_n, lambda_nl


def compute_gradient_radial(n, l, r, a_n, lambda_nl):
    """
    Compute radial component of gradient |grad Phi|.
    
    For spherical symmetry (s-states), this is the full gradient.
    For p/d states, this is the radial part (angular part handled separately).
    """
    phi_0 = 1.0
    
    # d/dr [R_{nℓ}(r)]
    if l == 0:
        dR_dr = -phi_0 / lambda_nl * np.exp(-r / lambda_nl)
    else:
        dR_dr = phi_0 * (l * (r / a_n)**(l-1) / a_n * np.exp(-r / lambda_nl) 
                        - (r / a_n)**l / lambda_nl * np.exp(-r / lambda_nl))
    
    return np.abs(dR_dr)


def compute_participation_functional(n, l, r_WS, a_n=None, lambda_nl=None):
    """
    Compute participation functional O_i for electron state (n, ℓ).
    
    O_i = (boundary flux) / (total flux in WS cell)
    
    Parameters:
    -----------
    n, l : int
        Quantum numbers
    r_WS : float
        Wigner-Seitz radius (m)
    a_n, lambda_nl : float, optional
        Characteristic scales (computed if not provided)
    
    Returns:
    --------
    O_i : float
        Participation functional value
    """
    # Generate radial profile
    r_points = np.linspace(0, r_WS, 1000)
    R, a_n, lambda_nl = generate_phi_radial(n, l, r_points, a_n, lambda_nl)
    
    # Compute gradient
    grad_r = compute_gradient_radial(n, l, r_points, a_n, lambda_nl)
    
    # Boundary flux (surface integral at r = r_WS)
    # Integral_boundary |grad Phi . n| dA
    # For spherical WS cell: 4*pi*r_WS^2 * |grad_r| at boundary
    grad_at_boundary = grad_r[-1]  # |dR/dr| at r = r_WS
    
    # Angular factor for non-s states (reduces effective boundary flux)
    if l == 0:
        angular_factor = 1.0  # Spherical, no reduction
    elif l == 1:
        angular_factor = 0.8  # p-state, moderate reduction
    elif l == 2:
        angular_factor = 0.3  # d-state, strong reduction from nodes
    else:
        angular_factor = 0.1  # f and higher
    
    # Surface integral: boundary_flux = 4*pi*r_WS^2 * |grad_r| * angular_factor
    boundary_flux_surface = 4 * np.pi * r_WS**2 * grad_at_boundary * angular_factor
    
    # Total flux magnitude in WS cell
    # Integral_WS |grad Phi| d^3r = Integral_0^{r_WS} |dR/dr| 4*pi*r^2 dr
    volume_integral = integrate.simpson(grad_r * 4 * np.pi * r_points**2, r_points)
    
    # Participation functional: ratio of boundary flux to total flux
    if volume_integral > 1e-30:  # Avoid division by zero
        O_i = boundary_flux_surface / volume_integral
    else:
        O_i = 0.0
    
    return O_i, {
        'boundary_flux_surface': float(boundary_flux_surface),
        'volume_integral': float(volume_integral),
        'angular_factor': angular_factor,
        'lambda_nl': float(lambda_nl),
        'a_n': float(a_n),
        'grad_at_boundary': float(grad_at_boundary)
    }


def calculate_Z_eff(element_config, r_WS):
    """
    Calculate effective participating electron count Z_eff.
    
    Parameters:
    -----------
    element_config : dict
        Electron configuration, e.g.:
        {'Al': [(1,0,2), (2,0,2), (2,1,6), (3,0,2), (3,1,1)]}
        Format: (n, l, count)
    r_WS : float
        Wigner-Seitz radius (m)
    
    Returns:
    --------
    Z_eff : int
        Number of participating electrons
    results : dict
        Detailed results for each shell
    """
    Z_eff = 0
    results = {}
    
    for n, l, count in element_config:
        O_i, details = compute_participation_functional(n, l, r_WS)
        participates = O_i > O_THRESHOLD
        
        if participates:
            Z_eff += count
        
        results[f"{n}{'spdf'[l]}"] = {
            'n': n,
            'l': l,
            'count': count,
            'O_i': float(O_i),
            'participates': participates,
            'details': details
        }
    
    return Z_eff, results


def calculate_plasma_frequency(n_e):
    """
    Calculate plasma frequency from electron density.
    
    ω_p = √(n_e e² / (ε₀ m_e))
    """
    omega_p = np.sqrt(n_e * E_CHARGE**2 / (EPSILON_0 * M_E))
    E_p = HBAR * omega_p / E_CHARGE  # Convert to eV
    return omega_p, E_p


# ==============================================================================
# Application to Metals
# ==============================================================================

def analyze_aluminum():
    """Analyze aluminum using pure Phi-overlap method."""
    print("="*80)
    print("ALUMINUM - Pure Phi-Overlap Method")
    print("="*80)
    
    # Structural data
    Z = 13
    A = 26.98e-3  # kg/mol
    rho = 2700  # kg/m³
    r_WS = (3 * A / (4 * np.pi * rho * N_A))**(1/3)
    
    print(f"\nStructural parameters:")
    print(f"  Z = {Z}")
    print(f"  r_WS = {r_WS*1e10:.2f} Å")
    
    # Electron configuration: 1s²2s²2p⁶3s²3p¹
    config = [
        (1, 0, 2),  # 1s²
        (2, 0, 2),  # 2s²
        (2, 1, 6),  # 2p⁶
        (3, 0, 2),  # 3s²
        (3, 1, 1),  # 3p¹
    ]
    
    Z_eff, results = calculate_Z_eff(config, r_WS)
    
    print(f"\nParticipation functional results:")
    for shell, data in results.items():
        status = "[PASS] PARTICIPATES" if data['participates'] else "[FAIL] Excluded"
        print(f"  {shell}: O_i = {data['O_i']:.3f} {status}")
    
    print(f"\nZ_eff = {Z_eff}")
    
    # Plasma frequency
    n_atom = rho * N_A / A
    n_e = Z_eff * n_atom
    omega_p, E_p = calculate_plasma_frequency(n_e)
    
    print(f"\nPlasma frequency:")
    print(f"  n_e = {n_e:.2e} m^-3")
    print(f"  ω_p = {omega_p:.2e} rad/s")
    print(f"  E_p = {E_p:.2f} eV")
    
    # Experimental
    E_p_exp = 15.3  # eV
    error = abs(E_p - E_p_exp) / E_p_exp * 100
    
    print(f"\nComparison:")
    print(f"  E_p(SDT) = {E_p:.2f} eV")
    print(f"  E_p(exp) = {E_p_exp:.2f} eV")
    print(f"  Error = {error:.2f}%")
    
    return {
        'element': 'Al',
        'Z_eff': Z_eff,
        'E_p_sdt': float(E_p),
        'E_p_exp': E_p_exp,
        'error_pct': float(error),
        'results': results
    }


def analyze_gold():
    """Analyze gold using pure Phi-overlap method."""
    print("\n" + "="*80)
    print("GOLD - Pure Phi-Overlap Method")
    print("="*80)
    
    # Structural data
    Z = 79
    A = 196.97e-3  # kg/mol
    rho = 19300  # kg/m³
    r_WS = (3 * A / (4 * np.pi * rho * N_A))**(1/3)
    
    print(f"\nStructural parameters:")
    print(f"  Z = {Z}")
    print(f"  r_WS = {r_WS*1e10:.2f} Å")
    
    # Electron configuration: [Xe]4f¹⁴5d¹⁰6s¹
    # Focus on valence: 5d¹⁰6s¹
    config = [
        (5, 2, 10),  # 5d¹⁰
        (6, 0, 1),   # 6s¹
    ]
    
    Z_eff, results = calculate_Z_eff(config, r_WS)
    
    print(f"\nParticipation functional results:")
    for shell, data in results.items():
        status = "[PASS] PARTICIPATES" if data['participates'] else "[FAIL] Excluded"
        print(f"  {shell}: O_i = {data['O_i']:.3f} {status}")
    
    print(f"\nZ_eff = {Z_eff}")
    
    # Plasma frequency
    n_atom = rho * N_A / A
    n_e = Z_eff * n_atom
    omega_p, E_p = calculate_plasma_frequency(n_e)
    
    print(f"\nPlasma frequency:")
    print(f"  n_e = {n_e:.2e} m^-3")
    print(f"  ω_p = {omega_p:.2e} rad/s")
    print(f"  E_p = {E_p:.2f} eV")
    
    # Experimental
    E_p_exp = 9.0  # eV
    error = abs(E_p - E_p_exp) / E_p_exp * 100
    
    print(f"\nComparison:")
    print(f"  E_p(SDT) = {E_p:.2f} eV")
    print(f"  E_p(exp) = {E_p_exp:.2f} eV")
    print(f"  Error = {error:.2f}%")
    
    return {
        'element': 'Au',
        'Z_eff': Z_eff,
        'E_p_sdt': float(E_p),
        'E_p_exp': E_p_exp,
        'error_pct': float(error),
        'results': results
    }


def main():
    """Run corrected participation functional calculations."""
    print("SDT PARTICIPATION FUNCTIONAL - CORRECTED VERSION")
    print("No E_b imports - Pure Phi-overlap method")
    print("="*80)
    
    results = {}
    
    # Aluminum
    results['Al'] = analyze_aluminum()
    
    # Gold
    results['Au'] = analyze_gold()
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nThreshold O_* = {O_THRESHOLD}")
    print(f"\nResults:")
    for element, data in results.items():
        print(f"  {element}: Z_eff = {data['Z_eff']}, "
              f"E_p = {data['E_p_sdt']:.2f} eV, "
              f"Error = {data['error_pct']:.2f}%")
    
    # Save results
    output_file = Path(__file__).parent / "participation_functional_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            'method': 'Pure Phi-overlap (no E_b imports)',
            'threshold': O_THRESHOLD,
            'results': results
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
