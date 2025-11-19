"""
B01: Atomic Structure Validation

Validates SDT atomic structure predictions from Phase_27A against NIST data.
Tolerance: <0.8% for all hydrogen spectral lines.
"""

import numpy as np
from pathlib import Path
import json

# Physical constants (CODATA 2018)
H = 6.62607015e-34  # Planck constant (J·s)
C = 2.99792458e8  # Speed of light (m/s)
E_CHARGE = 1.602176634e-19  # Elementary charge (C)
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity (F/m)
M_E = 9.1093837015e-31  # Electron mass (kg)
M_P = 1.67262192369e-27  # Proton mass (kg)
ALPHA = 7.2973525693e-3  # Fine structure constant

# Derived constants
K_E = 1 / (4 * np.pi * EPSILON_0)  # Coulomb constant
A_0 = 5.29177210903e-11  # Bohr radius (m)
RYDBERG_EV = 13.605693122994  # Rydberg energy (eV)
HC_EV_NM = 1239.841984  # hc in eV·nm

# Reduced mass correction for hydrogen
MU_H = M_E * M_P / (M_E + M_P)  # Reduced mass
REDUCED_MASS_FACTOR = MU_H / M_E  # ≈ 0.9994556

class AtomicStructureValidator:
    """Validates SDT atomic structure predictions."""
    
    def __init__(self):
        self.results = []
        self.errors = []
        
    def calculate_orbital_radius(self, n: int, Z: int = 1) -> float:
        """
        Calculate orbital radius from Phase_27A.
        
        Formula: r_n = n²a₀/Z
        """
        return n**2 * A_0 / Z
    
    def calculate_energy_level(self, n: int, Z: int = 1, use_reduced_mass: bool = True) -> float:
        """
        Calculate energy level from Phase_27A.
        
        Formula: E_n = -13.6 Z²/n² eV
        With reduced mass correction: E_n = -13.6 Z²/n² × (μ/m_e) eV
        """
        energy = -RYDBERG_EV * Z**2 / n**2
        if use_reduced_mass and Z == 1:  # Hydrogen only
            energy *= REDUCED_MASS_FACTOR
        return energy
    
    def calculate_transition_energy(self, n_i: int, n_f: int, Z: int = 1) -> float:
        """
        Calculate transition energy from Phase_27A.
        
        Formula: ΔE = E_nf - E_ni = -13.6 Z²(1/n_f² - 1/n_i²) eV
        For emission: n_i > n_f, so ΔE should be positive
        """
        E_i = self.calculate_energy_level(n_i, Z)
        E_f = self.calculate_energy_level(n_f, Z)
        # For emission (higher to lower), energy is positive
        return abs(E_f - E_i)
    
    def calculate_wavelength(self, delta_E_eV: float) -> float:
        """
        Calculate wavelength from transition energy.
        
        Formula: λ = hc/ΔE
        """
        if delta_E_eV <= 0:
            return np.nan
        return HC_EV_NM / delta_E_eV
    
    def validate_energy_levels(self) -> dict:
        """Validate energy levels against known values."""
        print("\n" + "="*60)
        print("VALIDATING ENERGY LEVELS")
        print("="*60)
        
        known_levels = {
            1: -13.59843449,  # eV, CODATA 2018
            2: -3.399699,     # eV
            3: -1.510934,     # eV
            4: -0.850302,     # eV
        }
        
        results = []
        for n, E_exp in known_levels.items():
            E_sdt = self.calculate_energy_level(n)
            error_eV = abs(E_sdt - E_exp)
            error_pct = abs(error_eV / E_exp) * 100
            
            results.append({
                'n': n,
                'E_SDT (eV)': E_sdt,
                'E_exp (eV)': E_exp,
                'Error (eV)': error_eV,
                'Error (%)': error_pct
            })
            
            status = "PASS" if error_pct < 0.8 else "FAIL"
            print(f"{status} n={n}: E_SDT={E_sdt:.6f} eV, E_exp={E_exp:.6f} eV, Error={error_pct:.4f}%")
        
        return results
    
    def validate_spectral_lines(self) -> dict:
        """Validate spectral line wavelengths against NIST data."""
        print("\n" + "="*60)
        print("VALIDATING SPECTRAL LINES")
        print("="*60)
        
        # Known hydrogen spectral lines (NIST values)
        spectral_lines = [
            # Lyman series (n->1)
            {'name': 'Lyman a', 'n_i': 2, 'n_f': 1, 'lambda_exp': 121.567, 'series': 'Lyman'},
            {'name': 'Lyman b', 'n_i': 3, 'n_f': 1, 'lambda_exp': 102.572, 'series': 'Lyman'},
            {'name': 'Lyman g', 'n_i': 4, 'n_f': 1, 'lambda_exp': 97.254, 'series': 'Lyman'},
            {'name': 'Lyman d', 'n_i': 5, 'n_f': 1, 'lambda_exp': 94.974, 'series': 'Lyman'},
            
            # Balmer series (n->2)
            {'name': 'Balmer a (Ha)', 'n_i': 3, 'n_f': 2, 'lambda_exp': 656.279, 'series': 'Balmer'},
            {'name': 'Balmer b (Hb)', 'n_i': 4, 'n_f': 2, 'lambda_exp': 486.133, 'series': 'Balmer'},
            {'name': 'Balmer g (Hg)', 'n_i': 5, 'n_f': 2, 'lambda_exp': 434.047, 'series': 'Balmer'},
            {'name': 'Balmer d (Hd)', 'n_i': 6, 'n_f': 2, 'lambda_exp': 410.174, 'series': 'Balmer'},
            
            # Paschen series (n->3)
            {'name': 'Paschen a', 'n_i': 4, 'n_f': 3, 'lambda_exp': 1875.1, 'series': 'Paschen'},
            {'name': 'Paschen b', 'n_i': 5, 'n_f': 3, 'lambda_exp': 1281.8, 'series': 'Paschen'},
            {'name': 'Paschen g', 'n_i': 6, 'n_f': 3, 'lambda_exp': 1093.8, 'series': 'Paschen'},
            
            # Brackett series (n->4)
            {'name': 'Brackett a', 'n_i': 5, 'n_f': 4, 'lambda_exp': 4051.2, 'series': 'Brackett'},
            {'name': 'Brackett b', 'n_i': 6, 'n_f': 4, 'lambda_exp': 2625.1, 'series': 'Brackett'},
        ]
        
        results = []
        max_error = 0.0
        failed_lines = []
        
        for line in spectral_lines:
            # Calculate transition energy
            delta_E = self.calculate_transition_energy(line['n_i'], line['n_f'])
            
            # Calculate wavelength
            lambda_sdt = self.calculate_wavelength(delta_E)
            lambda_exp = line['lambda_exp']
            
            # Calculate error
            error_nm = abs(lambda_sdt - lambda_exp)
            error_pct = abs(error_nm / lambda_exp) * 100
            
            results.append({
                'Transition': line['name'],
                'n_i → n_f': f"{line['n_i']}→{line['n_f']}",
                'Series': line['series'],
                'λ_SDT (nm)': lambda_sdt,
                'λ_exp (nm)': lambda_exp,
                'Error (nm)': error_nm,
                'Error (%)': error_pct,
                'Status': 'PASS' if error_pct < 0.8 else 'FAIL'
            })
            
            max_error = max(max_error, error_pct)
            if error_pct >= 0.8:
                failed_lines.append(line['name'])
            
            status = "PASS" if error_pct < 0.8 else "FAIL"
            print(f"{status} {line['name']:20s} {line['n_i']}->{line['n_f']}: "
                  f"lambda_SDT={lambda_sdt:.3f} nm, lambda_exp={lambda_exp:.3f} nm, "
                  f"Error={error_pct:.4f}%")
        
        print(f"\nMaximum error: {max_error:.4f}%")
        if failed_lines:
            print(f"FAILED lines: {', '.join(failed_lines)}")
        else:
            print("All lines pass <0.8% tolerance!")
        
        return {
            'results': results,
            'max_error': max_error,
            'failed_lines': failed_lines,
            'total_lines': len(spectral_lines),
            'passed_lines': len(spectral_lines) - len(failed_lines)
        }
    
    def calculate_chi_squared(self, spectral_results: dict) -> float:
        """Calculate χ² for spectral line validation."""
        chi_sq = 0.0
        for result in spectral_results['results']:
            error_nm = result['Error (nm)']
            lambda_exp = result['λ_exp (nm)']
            # Use relative error squared
            chi_sq += (error_nm / lambda_exp)**2
        return chi_sq
    
    def generate_report(self, output_file: str):
        """Generate validation report."""
        print("\n" + "="*60)
        print("GENERATING VALIDATION REPORT")
        print("="*60)
        
        # Validate energy levels
        energy_results = self.validate_energy_levels()
        
        # Validate spectral lines
        spectral_results = self.validate_spectral_lines()
        
        # Calculate χ²
        chi_sq = self.calculate_chi_squared(spectral_results)
        
        # Create summary
        summary = {
            'benchmark': 'B01',
            'name': 'Atomic Structure',
            'phase_document': 'Phase_27A_Foundation_and_Single_Electron_Systems',
            'tolerance': '<0.8%',
            'validation_date': str(Path().cwd()),
            'energy_levels': {
                'tested': len(energy_results),
                'max_error_pct': max(r['Error (%)'] for r in energy_results),
                'all_pass': all(r['Error (%)'] < 0.8 for r in energy_results)
            },
            'spectral_lines': {
                'total': spectral_results['total_lines'],
                'passed': spectral_results['passed_lines'],
                'failed': len(spectral_results['failed_lines']),
                'max_error_pct': spectral_results['max_error'],
                'chi_squared': chi_sq,
                'all_pass': len(spectral_results['failed_lines']) == 0
            },
            'overall_status': 'CERTIFIED' if (
                all(r['Error (%)'] < 0.8 for r in energy_results) and
                len(spectral_results['failed_lines']) == 0
            ) else 'FAILED',
            'details': {
                'energy_levels': energy_results,
                'spectral_lines': spectral_results['results']
            }
        }
        
        # Save report
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nReport saved to: {output_file}")
        print(f"\nOverall Status: {summary['overall_status']}")
        print(f"Energy levels: {summary['energy_levels']['tested']} tested, "
              f"max error: {summary['energy_levels']['max_error_pct']:.4f}%")
        print(f"Spectral lines: {summary['spectral_lines']['passed']}/{summary['spectral_lines']['total']} passed, "
              f"max error: {summary['spectral_lines']['max_error_pct']:.4f}%, "
              f"chi-squared = {chi_sq:.4f}")
        
        return summary

def main():
    """Main execution."""
    validator = AtomicStructureValidator()
    
    # Generate report
    report_file = Path(__file__).parent.parent / "benchmarks" / "B01_validation_report.json"
    report_file.parent.mkdir(exist_ok=True)
    
    summary = validator.generate_report(str(report_file))
    
    # Print final status
    print("\n" + "="*60)
    if summary['overall_status'] == 'CERTIFIED':
        print("BENCHMARK B01: CERTIFIED")
        print("All atomic structure predictions validated within <0.8% tolerance")
    else:
        print("BENCHMARK B01: FAILED")
        print("Some predictions exceed 0.8% tolerance")
    print("="*60)

if __name__ == '__main__':
    main()

