#pragma once

#include <numbers>
#include <cmath>

namespace sdt::chemistry::constants {

    // CODATA 2018 Fundamental Constants
    inline constexpr double c = 299792458.0;  // Speed of light (m/s), exact
    inline constexpr double hbar = 1.054571817e-34;  // Reduced Planck constant (J·s)
    inline constexpr double alpha = 7.2973525693e-3;  // Fine structure constant
    inline constexpr double e_charge = 1.602176634e-19;  // Elementary charge (C)
    
    // CMB Pressure (from recombination) - Atomic/Molecular scale
    inline constexpr double P_CMB = 2.036e-2;  // Pa (CMB radiation pressure at z=1089.9)
    
    // Nuclear-scale pressure (from Phase 19)
    inline constexpr double P_infinity_nuclear = 1.65e31;  // Pa (effective pressure at nuclear scale for toroidal geometry)
    
    // Spation Lattice Properties
    inline constexpr double r_Planck = 1.616255e-35;  // Planck radius (m)
    inline constexpr double K_bulk = 4.6e113;  // Bulk modulus (Pa)
    inline constexpr double rho_s = 5.2e96;  // Spation density (kg/m³)
    
    // Particle Radii
    inline constexpr double R_proton = 8.40e-16;  // m (proton charge radius)
    inline constexpr double R_neutron = 8.70e-16;  // m (neutron radius)
    inline constexpr double R_electron_classical = 2.818e-15;  // m (classical electron radius)
    inline constexpr double R_electron_effective = 1.0e-21;  // m (effective occlusion radius from Phase 1)
    
    // Bohr radius
    inline constexpr double a_0 = 5.29177210903e-11;  // m (Bohr radius)
    
    // Mathematical Constants
    inline constexpr double pi = std::numbers::pi_v<double>;
    inline constexpr double two_pi = 2.0 * pi;
    inline constexpr double four_pi = 4.0 * pi;
    
    // Unit Conversions
    inline constexpr double eV_to_J = 1.602176634e-19;  // J/eV
    inline constexpr double J_to_eV = 1.0 / eV_to_J;  // eV/J
    inline constexpr double Angstrom_to_m = 1.0e-10;  // m/Å
    inline constexpr double m_to_Angstrom = 1.0e10;  // Å/m
    inline constexpr double pm_to_m = 1.0e-12;  // m/pm
    inline constexpr double m_to_pm = 1.0e12;  // pm/m
    
    // Avogadro's number (for molar quantities)
    inline constexpr double N_A = 6.02214076e23;  // mol⁻¹
    
    // Boltzmann constant
    inline constexpr double k_B = 1.380649e-23;  // J/K
    
    // Proton turbine parameters (Phase 19)
    inline constexpr double Gamma_proton = 0.546;  // Circulation factor
    inline constexpr double kappa_proton = 1.190e15;  // m⁻¹ (curvature)
    inline constexpr double traction_proton = 0.9997;  // (1-eta) for bound proton
    inline constexpr double A_eff_proton = 5.013e-30;  // m² (corrected capture area)
    
    // Electron turbine parameters (Phase 19)
    inline constexpr double Gamma_electron = 0.548;  // Circulation factor
    inline constexpr double kappa_electron = 3.549e14;  // m⁻¹ (curvature)
    inline constexpr double traction_electron_free = 7.297e-3;  // (1-eta) for free electron
    inline constexpr double A_eff_electron = 3.718e-29;  // m² (corrected capture area)
    
} // namespace sdt::chemistry::constants

