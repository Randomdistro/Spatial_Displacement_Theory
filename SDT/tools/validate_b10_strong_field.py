"""
B10: Strong Field Tests Validation

Validates Mercury precession and gravitational lensing from Phase_15.
"""

import numpy as np
from pathlib import Path
import json

# Physical constants
C = 2.99792458e8  # m/s
BETA_SUN = 1.32712e20  # m^3/s^2

class StrongFieldValidator:
    """Validates SDT strong field predictions."""
    
    def validate_mercury_precession(self) -> dict:
        """Validate Mercury perihelion precession."""
        print("\n" + "="*60)
        print("VALIDATING MERCURY PERIHELION PRECESSION")
        print("="*60)
        
        # Mercury orbital parameters
        a = 5.791e10  # Semi-major axis (m)
        e = 0.2056  # Eccentricity
        period_days = 87.97  # Orbital period (days)
        orbits_per_century = 415
        
        # SDT formula from Phase_15, Eq. 5.13
        # Delta_phi = 6pi*beta / (c^2 * a * (1-e^2))
        delta_phi_per_orbit = (6 * np.pi * BETA_SUN) / (C**2 * a * (1 - e**2))
        
        # Convert to arcseconds per century
        arcsec_per_rad = 206265
        delta_phi_per_century = delta_phi_per_orbit * orbits_per_century * arcsec_per_rad
        
        # Experimental value
        exp_value = 42.98  # arcsec/century
        exp_uncertainty = 0.04
        
        error = abs(delta_phi_per_century - exp_value)
        error_pct = abs(error / exp_value) * 100
        
        result = {
            'test': 'Mercury Precession',
            'predicted (arcsec/century)': delta_phi_per_century,
            'experimental (arcsec/century)': exp_value,
            'uncertainty': exp_uncertainty,
            'error (arcsec/century)': error,
            'error (%)': error_pct,
            'status': 'PASS' if error_pct < 1.0 else 'FAIL'
        }
        
        print(f"SDT Prediction: {delta_phi_per_century:.2f} arcsec/century")
        print(f"Experimental:   {exp_value:.2f} +/- {exp_uncertainty:.2f} arcsec/century")
        print(f"Error:           {error:.2f} arcsec/century ({error_pct:.2f}%)")
        
        return result
    
    def validate_gravitational_lensing(self) -> dict:
        """Validate gravitational light deflection."""
        print("\n" + "="*60)
        print("VALIDATING GRAVITATIONAL LENSING")
        print("="*60)
        
        # Solar limb parameters
        b = 6.96e8  # Solar radius (m), impact parameter
        
        # SDT formula from Phase_15, Eq. 5.9
        # delta_theta = 4*beta / (c^2 * b)
        delta_theta_rad = (4 * BETA_SUN) / (C**2 * b)
        
        # Convert to arcseconds
        arcsec_per_rad = 206265
        delta_theta_arcsec = delta_theta_rad * arcsec_per_rad
        
        # Experimental value
        exp_value = 1.7517  # arcseconds
        exp_uncertainty = 0.0005
        
        error = abs(delta_theta_arcsec - exp_value)
        error_pct = abs(error / exp_value) * 100
        
        result = {
            'test': 'Solar Light Deflection',
            'predicted (arcsec)': delta_theta_arcsec,
            'experimental (arcsec)': exp_value,
            'uncertainty': exp_uncertainty,
            'error (arcsec)': error,
            'error (%)': error_pct,
            'status': 'PASS' if error_pct < 1.0 else 'FAIL'
        }
        
        print(f"SDT Prediction: {delta_theta_arcsec:.4f} arcsec")
        print(f"Experimental:   {exp_value:.4f} +/- {exp_uncertainty:.4f} arcsec")
        print(f"Error:           {error:.4f} arcsec ({error_pct:.2f}%)")
        
        return result
    
    def generate_report(self, output_file: str):
        """Generate validation report."""
        print("\n" + "="*60)
        print("GENERATING VALIDATION REPORT")
        print("="*60)
        
        precession = self.validate_mercury_precession()
        lensing = self.validate_gravitational_lensing()
        
        summary = {
            'benchmark': 'B10',
            'name': 'Strong Field Tests',
            'phase_document': 'Phase_15_Gravitation_from_Spation_Pressure_Gradients',
            'validation_date': str(Path().cwd()),
            'mercury_precession': precession,
            'gravitational_lensing': lensing,
            'overall_status': 'CERTIFIED' if (
                precession['status'] == 'PASS' and lensing['status'] == 'PASS'
            ) else 'FAILED'
        }
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nReport saved to: {output_file}")
        print(f"\nOverall Status: {summary['overall_status']}")
        
        return summary

def main():
    validator = StrongFieldValidator()
    report_file = Path(__file__).parent.parent / "benchmarks" / "B10_validation_report.json"
    report_file.parent.mkdir(exist_ok=True)
    summary = validator.generate_report(str(report_file))
    
    print("\n" + "="*60)
    if summary['overall_status'] == 'CERTIFIED':
        print("BENCHMARK B10: CERTIFIED")
    else:
        print("BENCHMARK B10: FAILED")
    print("="*60)

if __name__ == '__main__':
    main()

