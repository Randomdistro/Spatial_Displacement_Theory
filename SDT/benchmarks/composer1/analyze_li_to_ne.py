"""
SDT Participation Analysis: Lithium to Neon
===========================================
Author: Claude Opus 4.5 (Anthropic AI)
Date: January 2, 2026

Complete SDT framework analysis for all 8 stable atoms Li-Ne:
- WHAT: Z_eff (participating electrons)
- WHERE: Spatial distribution
- WHEN: Temporal dynamics
- VELOCITIES: From Phi structure
- DISTANCES: All spatial scales
- CASCADING EFFECTS: Complete causal chain
"""

import numpy as np
from scipy import integrate
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
O_THRESHOLD = 0.45

# Element data (structure only - no E_b)
ELEMENTS = {
    'Li': {'Z': 3, 'A': 6.941e-3, 'rho': 534, 'config': [(1, 0, 2), (2, 0, 1)]},  # 1s²2s¹
    'Be': {'Z': 4, 'A': 9.012e-3, 'rho': 1848, 'config': [(1, 0, 2), (2, 0, 2)]},  # 1s²2s²
    'B': {'Z': 5, 'A': 10.81e-3, 'rho': 2340, 'config': [(1, 0, 2), (2, 0, 2), (2, 1, 1)]},  # 1s²2s²2p¹
    'C': {'Z': 6, 'A': 12.01e-3, 'rho': 2260, 'config': [(1, 0, 2), (2, 0, 2), (2, 1, 2)]},  # 1s²2s²2p²
    'N': {'Z': 7, 'A': 14.01e-3, 'rho': 1026, 'config': [(1, 0, 2), (2, 0, 2), (2, 1, 3)]},  # 1s²2s²2p³
    'O': {'Z': 8, 'A': 16.00e-3, 'rho': 1429, 'config': [(1, 0, 2), (2, 0, 2), (2, 1, 4)]},  # 1s²2s²2p⁴
    'F': {'Z': 9, 'A': 18.998e-3, 'rho': 1696, 'config': [(1, 0, 2), (2, 0, 2), (2, 1, 5)]},  # 1s²2s²2p⁵
    'Ne': {'Z': 10, 'A': 20.18e-3, 'rho': 1441, 'config': [(1, 0, 2), (2, 0, 2), (2, 1, 6)]},  # 1s²2s²2p⁶
}


class SDTAnalyzer:
    """SDT participation framework analyzer."""
    
    def compute_r_WS(self, rho, A):
        """Compute Wigner-Seitz radius from density and atomic mass."""
        n_atom = rho * N_A / A
        V_WS = 1.0 / n_atom
        r_WS = (3 * V_WS / (4 * np.pi))**(1/3)
        return r_WS, n_atom
    
    def compute_characteristic_scales(self, n, l):
        """Compute a_n and lambda_nl from quantum numbers."""
        a_n = n**2 * A_0
        f_l = {0: 1.0, 1: 0.8, 2: 0.3, 3: 0.15}.get(l, 0.1)
        lambda_nl = n * A_0 * f_l
        return a_n, lambda_nl
    
    def compute_gradient_radial(self, r, n, l, a_n, lambda_nl):
        """Compute |dR/dr|."""
        phi_0 = 1.0
        
        if l == 0:
            dR_dr = -phi_0 / lambda_nl * np.exp(-r / lambda_nl)
        elif l == 1:
            dR_dr = phi_0 * (1.0 / a_n - r / (a_n * lambda_nl)) * np.exp(-r / lambda_nl)
        elif l == 2:
            dR_dr = phi_0 * (2 * r / a_n**2 - r**2 / (a_n**2 * lambda_nl)) * np.exp(-r / lambda_nl)
        else:
            dR_dr = phi_0 * (l * (r / a_n)**(l-1) / a_n - (r / a_n)**l / lambda_nl) * np.exp(-r / lambda_nl)
        
        return np.abs(dR_dr)
    
    def compute_participation_functional(self, n, l, r_WS):
        """Compute O_i for electron state (n, l)."""
        a_n, lambda_nl = self.compute_characteristic_scales(n, l)
        
        # Generate radial grid
        r_points = np.linspace(0, r_WS, 2000)
        
        # Compute gradient
        grad_r = self.compute_gradient_radial(r_points, n, l, a_n, lambda_nl)
        
        # Angular factor
        angular_factor = {0: 1.0, 1: 0.8, 2: 0.3}.get(l, 0.1)
        
        # Boundary flux (at r = r_WS)
        grad_at_boundary = grad_r[-1]
        boundary_flux_surface = 4 * np.pi * r_WS**2 * grad_at_boundary * angular_factor
        
        # Volume integral: ∫ |grad Phi| d³r
        volume_integral = integrate.simpson(grad_r * 4 * np.pi * r_points**2, r_points)
        
        # Participation functional
        if volume_integral > 1e-30:
            O_i = boundary_flux_surface / volume_integral
        else:
            O_i = 0.0
        
        return {
            'O_i': float(O_i),
            'a_n': float(a_n),
            'lambda_nl': float(lambda_nl),
            'boundary_flux': float(boundary_flux_surface),
            'volume_integral': float(volume_integral),
            'angular_factor': angular_factor,
            'participates': O_i > O_THRESHOLD
        }
    
    def compute_velocity(self, lambda_nl):
        """Compute electron velocity from decay length."""
        p = HBAR / lambda_nl
        v = p / M_E
        return v
    
    def compute_plasma_frequency(self, n_e):
        """Compute plasma frequency from electron density."""
        omega_p = np.sqrt(n_e * E_CHARGE**2 / (EPSILON_0 * M_E))
        E_p = HBAR * omega_p / E_CHARGE  # eV
        T_p = 2 * np.pi / omega_p  # s
        return omega_p, E_p, T_p
    
    def compute_penetration_depth(self, omega_p):
        """Compute London penetration depth."""
        delta = C / omega_p
        return delta
    
    def analyze_element(self, symbol, data):
        """Complete analysis of an element."""
        Z = data['Z']
        A = data['A']
        rho = data['rho']
        config = data['config']
        
        print(f"\n{'='*80}")
        print(f"{symbol.upper()} (Z={Z}) - COMPLETE SDT ANALYSIS")
        print(f"{'='*80}")
        
        # Step 1: WHERE - Spatial scales
        r_WS, n_atom = self.compute_r_WS(rho, A)
        print(f"\n[WHERE] Spatial Scales:")
        print(f"  r_WS = {r_WS*1e10:.2f} Angstrom")
        print(f"  n_atom = {n_atom:.2e} m^-3")
        
        # Step 2: WHAT - Phi fields and participation
        print(f"\n[WHAT] Phi Field Analysis:")
        Z_eff = 0
        electron_results = {}
        
        for n, l, count in config:
            result = self.compute_participation_functional(n, l, r_WS)
            status = "[PASS]" if result['participates'] else "[FAIL]"
            shell_name = f"{n}{'spdf'[l]}"
            print(f"  {shell_name}: O_i = {result['O_i']:.3f}, "
                  f"lambda = {result['lambda_nl']*1e10:.2f} Angstrom, "
                  f"count = {count} {status}")
            
            if result['participates']:
                Z_eff += count
            
            electron_results[shell_name] = {
                **result,
                'count': count,
                'n': n,
                'l': l
            }
        
        print(f"\n  Z_eff = {Z_eff}")
        
        # Step 3: VELOCITIES
        print(f"\n[VELOCITIES] From Phi Structure:")
        for shell_name, result in electron_results.items():
            v = self.compute_velocity(result['lambda_nl'])
            print(f"  {shell_name}: v = {v/1e6:.2f} Mm/s")
        
        # Step 4: DISTANCES
        print(f"\n[DISTANCES] Complete Spatial Picture:")
        print(f"  r_WS = {r_WS*1e10:.2f} Angstrom")
        for shell_name, result in electron_results.items():
            print(f"  {shell_name}: lambda = {result['lambda_nl']*1e10:.2f} Angstrom, "
                  f"lambda/r_WS = {result['lambda_nl']/r_WS:.2f}")
        
        # Step 5: WHEN - Temporal dynamics
        if Z_eff > 0:
            n_e = Z_eff * n_atom
            omega_p, E_p, T_p = self.compute_plasma_frequency(n_e)
            delta = self.compute_penetration_depth(omega_p)
            
            print(f"\n[WHEN] Temporal Dynamics:")
            print(f"  n_e = {n_e:.2e} m^-3")
            print(f"  omega_p = {omega_p:.2e} rad/s")
            print(f"  E_p = {E_p:.2f} eV")
            print(f"  T_p = {T_p*1e15:.3f} fs")
            print(f"  delta = {delta*1e9:.2f} nm")
        else:
            print(f"\n[WHEN] No participating electrons - no plasma frequency")
            omega_p, E_p, T_p, delta = 0, 0, 0, 0
            n_e = 0
        
        # Step 6: CASCADING EFFECTS
        print(f"\n[CASCADING EFFECTS] Causal Chain:")
        print(f"  Geometry (Z={Z}, rho={rho:.0f} kg/m^3)")
        print(f"    -> r_WS = {r_WS*1e10:.2f} Angstrom")
        print(f"    -> Phi fields (lambda from geometry)")
        print(f"    -> O_i values")
        print(f"    -> Z_eff = {Z_eff}")
        if Z_eff > 0:
            print(f"    -> n_e = {n_e:.2e} m^-3")
            print(f"    -> omega_p = {omega_p:.2e} rad/s")
            print(f"    -> delta = {delta*1e9:.2f} nm")
        
        return {
            'symbol': symbol,
            'Z': Z,
            'r_WS': float(r_WS),
            'n_atom': float(n_atom),
            'Z_eff': Z_eff,
            'n_e': float(n_e),
            'omega_p': float(omega_p),
            'E_p': float(E_p),
            'T_p': float(T_p),
            'delta': float(delta),
            'electrons': electron_results
        }


def main():
    """Run complete analysis for Li-Ne."""
    print("="*80)
    print("SDT PARTICIPATION ANALYSIS: LITHIUM TO NEON")
    print("="*80)
    print("\nComputing for all 8 stable atoms: Li, Be, B, C, N, O, F, Ne")
    print("Analysis: WHAT, WHERE, WHEN, VELOCITIES, DISTANCES, CASCADING EFFECTS")
    
    analyzer = SDTAnalyzer()
    all_results = {}
    
    # Analyze each element
    for symbol, data in ELEMENTS.items():
        result = analyzer.analyze_element(symbol, data)
        all_results[symbol] = result
    
    # Summary table
    print(f"\n{'='*80}")
    print("SUMMARY TABLE: Li-Ne")
    print(f"{'='*80}")
    print(f"\n{'Element':<8} {'Z':<4} {'r_WS (Å)':<12} {'Z_eff':<8} {'E_p (eV)':<12} {'delta (nm)':<12}")
    print("-" * 80)
    
    for symbol in ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne']:
        r = all_results[symbol]
        if r['Z_eff'] > 0:
            print(f"{symbol:<8} {r['Z']:<4} {r['r_WS']*1e10:<12.2f} {r['Z_eff']:<8} "
                  f"{r['E_p']:<12.2f} {r['delta']*1e9:<12.2f}")
        else:
            print(f"{symbol:<8} {r['Z']:<4} {r['r_WS']*1e10:<12.2f} {r['Z_eff']:<8} "
                  f"{'N/A':<12} {'N/A':<12}")
    
    # Participation summary
    print(f"\n{'='*80}")
    print("PARTICIPATION SUMMARY")
    print(f"{'='*80}")
    for symbol in ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne']:
        r = all_results[symbol]
        print(f"\n{symbol} (Z={r['Z']}):")
        print(f"  r_WS = {r['r_WS']*1e10:.2f} Angstrom")
        for shell_name, shell_data in r['electrons'].items():
            status = "PARTICIPATES" if shell_data['participates'] else "EXCLUDED"
            print(f"  {shell_name}: O_i = {shell_data['O_i']:.3f}, "
                  f"lambda = {shell_data['lambda_nl']*1e10:.2f} Angstrom, "
                  f"{status}")
        print(f"  Z_eff = {r['Z_eff']}")
    
    # Save results
    output_file = Path(__file__).parent / "li_to_ne_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            'method': 'Pure Phi-overlap (no E_b imports)',
            'threshold': O_THRESHOLD,
            'elements': all_results
        }, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
