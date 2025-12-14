#!/usr/bin/env python3
"""
Run SDT Galactic Rotation Experiment
Quick test and demonstration script
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from galactic_rotation_sim import (
        SDTRotationCurve,
        SPARCAnalyzer,
        visualize_rotation_curve,
        R_FLAT_R_D_PREDICTED
    )
except ImportError:
    # If running as module
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from galactic_rotation_sim import (
        SDTRotationCurve,
        SPARCAnalyzer,
        visualize_rotation_curve,
        R_FLAT_R_D_PREDICTED
    )
import numpy as np
import matplotlib.pyplot as plt

def test_individual_galaxy(galaxy_name: str = 'NGC3198'):
    """Test rotation curve for a single galaxy"""
    print(f"\n{'='*70}")
    print(f"Testing Galaxy: {galaxy_name}")
    print(f"{'='*70}\n")
    
    # Load SPARC data
    data_file = Path(__file__).parent.parent.parent / 'data' / 'galaxy_rotation_sparc.csv'
    
    if not data_file.exists():
        print(f"Warning: SPARC data file not found at {data_file}")
        print("Using default parameters...")
        R_d = 2.8  # Typical for Sc galaxies
    else:
        analyzer = SPARCAnalyzer(str(data_file))
        gal_data = analyzer.get_galaxy_data(galaxy_name)
        
        if len(gal_data) == 0:
            print(f"Galaxy '{galaxy_name}' not found, using defaults")
            R_d = 2.8
        else:
            R_d = analyzer.get_disk_scale_length(galaxy_name)
            if R_d is None:
                R_d = 2.8
    
    # Calculate rotation curve
    calculator = SDTRotationCurve(R_d)
    curve = calculator.calculate_curve(r_max_kpc=30.0)
    
    print(f"R_d: {R_d:.2f} kpc")
    print(f"R_flat (predicted): {curve['R_flat_kpc']:.2f} kpc")
    print(f"R_flat/R_d: {curve['R_flat_kpc']/R_d:.2f} (predicted: {R_FLAT_R_D_PREDICTED:.2f})")
    
    # Visualize
    output_dir = Path(__file__).parent / 'results'
    output_dir.mkdir(exist_ok=True)
    visualize_rotation_curve(curve, str(output_dir / f'{galaxy_name}_rotation_curve.png'))
    
    return curve


def test_multiple_galaxies():
    """Test multiple galaxies and show correlation"""
    print(f"\n{'='*70}")
    print(f"Testing Multiple Galaxies - R_flat/R_d Correlation")
    print(f"{'='*70}\n")
    
    data_file = Path(__file__).parent.parent.parent / 'data' / 'galaxy_rotation_sparc.csv'
    
    if not data_file.exists():
        print(f"Error: SPARC data file not found at {data_file}")
        return
    
    analyzer = SPARCAnalyzer(str(data_file))
    results = analyzer.test_rflat_rd_correlation()
    
    if 'error' in results:
        print(f"Error: {results['error']}")
        return
    
    # Create correlation plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    R_d_values = [r['R_d_kpc'] for r in results['results']]
    R_flat_values = [r['R_flat_kpc'] for r in results['results']]
    
    ax.scatter(R_d_values, R_flat_values, alpha=0.6, s=50)
    
    # Predicted line: R_flat = 2.5 * R_d
    R_d_line = np.linspace(min(R_d_values), max(R_d_values), 100)
    R_flat_line = R_FLAT_R_D_PREDICTED * R_d_line
    ax.plot(R_d_line, R_flat_line, 'r--', linewidth=2, 
            label=f'SDT Prediction: R_flat = {R_FLAT_R_D_PREDICTED} R_d')
    
    ax.set_xlabel('R_d (kpc)', fontsize=12)
    ax.set_ylabel('R_flat (kpc)', fontsize=12)
    ax.set_title('SDT R_flat/R_d Correlation Test', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add statistics text
    stats_text = (f"Average ratio: {results['average_ratio']:.2f} ± {results['std_ratio']:.2f}\n"
                  f"Predicted: {R_FLAT_R_D_PREDICTED:.2f}\n"
                  f"Deviation: {results['deviation_pct']:.1f}%\n"
                  f"N galaxies: {results['n_galaxies']}")
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    output_dir = Path(__file__).parent / 'results'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'rflat_rd_correlation.png', dpi=300, bbox_inches='tight')
    print(f"\nCorrelation plot saved to {output_dir / 'rflat_rd_correlation.png'}")
    plt.close()
    
    return results


def demonstrate_occlusion_saturation():
    """Demonstrate occlusion saturation mechanism"""
    print(f"\n{'='*70}")
    print(f"Demonstrating Disk Eclipse Saturation Mechanism")
    print(f"{'='*70}\n")
    
    R_d = 3.0  # kpc
    calculator = SDTRotationCurve(R_d)
    
    r_kpc = np.linspace(0.5, 30, 100)
    E_values = [calculator.occlusion_calc.occlusion_function_kpc(r) for r in r_kpc]
    v_values = [calculator.rotation_velocity_kpc(r) for r in r_kpc]
    
    # Create figure
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    # Occlusion function
    ax1 = axes[0]
    ax1.plot(r_kpc, E_values, 'r-', linewidth=2, label='E(r)')
    ax1.axvline(R_d, color='g', linestyle='--', alpha=0.5, label=f'R_d = {R_d} kpc')
    ax1.axvline(R_d * R_FLAT_R_D_PREDICTED, color='b', linestyle='--', alpha=0.5,
                label=f'R_flat = {R_d * R_FLAT_R_D_PREDICTED:.1f} kpc')
    ax1.axhline(max(E_values), color='orange', linestyle=':', alpha=0.5,
                label=f'E_∞ ≈ {max(E_values):.3f}')
    ax1.set_xlabel('Radius (kpc)')
    ax1.set_ylabel('Occlusion E(r)')
    ax1.set_title('Disk Eclipse Saturation: E(r) → E_∞')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Rotation velocity
    ax2 = axes[1]
    ax2.plot(r_kpc, v_values, 'b-', linewidth=2, label='v(r)')
    ax2.axvline(R_d, color='g', linestyle='--', alpha=0.5, label=f'R_d = {R_d} kpc')
    ax2.axvline(R_d * R_FLAT_R_D_PREDICTED, color='r', linestyle='--', alpha=0.5,
                label=f'R_flat = {R_d * R_FLAT_R_D_PREDICTED:.1f} kpc')
    ax2.set_xlabel('Radius (kpc)')
    ax2.set_ylabel('Rotation Velocity (km/s)')
    ax2.set_title('Flat Rotation Curve from Saturated Occlusion')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_dir = Path(__file__).parent / 'results'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'occlusion_saturation_demo.png', dpi=300, bbox_inches='tight')
    print(f"Demonstration plot saved to {output_dir / 'occlusion_saturation_demo.png'}")
    plt.close()
    
    print(f"\nKey Points:")
    print(f"- E(r) grows rapidly for r < R_d")
    print(f"- E(r) saturates to E_∞ ≈ {max(E_values):.3f} for r >> R_d")
    print(f"- When E(r) ≈ constant, acceleration ∝ 1/r → v(r) ≈ constant")
    print(f"- This produces flat rotation curves WITHOUT dark matter!")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run SDT Galactic Rotation Experiment')
    parser.add_argument('--galaxy', type=str, default='NGC3198',
                       help='Galaxy name to test')
    parser.add_argument('--test-correlation', action='store_true',
                       help='Test R_flat/R_d correlation')
    parser.add_argument('--demo', action='store_true',
                       help='Demonstrate occlusion saturation')
    parser.add_argument('--all', action='store_true',
                       help='Run all tests')
    
    args = parser.parse_args()
    
    if args.all:
        test_individual_galaxy('NGC3198')
        test_multiple_galaxies()
        demonstrate_occlusion_saturation()
    elif args.test_correlation:
        test_multiple_galaxies()
    elif args.demo:
        demonstrate_occlusion_saturation()
    else:
        test_individual_galaxy(args.galaxy)
    
    print("\n✅ Experiment complete!")

