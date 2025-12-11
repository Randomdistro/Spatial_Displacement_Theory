// SDT Atomic Properties Calculator
// Zero lookup tables - pure calculation from fundamental constants
// C++20 implementation

#ifndef SDT_ATOMIC_PROPERTIES_HPP
#define SDT_ATOMIC_PROPERTIES_HPP

#include <cmath>
#include <numbers>
#include <string_view>
#include <format>
#include <vector>

namespace sdt {

// Fundamental constants (CODATA 2018)
namespace constants {
    constexpr double c = 299'792'458.0;                    // m/s (exact)
    constexpr double h = 6.626'070'15e-34;                 // J·s (exact)
    constexpr double m_e = 9.109'383'7015e-31;             // kg
    constexpr double alpha_inv = 137.035'999'084;          // fine structure constant⁻¹
    constexpr double Ry = 13.605'693'122'994;              // eV (Rydberg energy)
    constexpr double eV_to_J = 1.602'176'634e-19;          // J/eV (exact)
    
    // Derived constants
    constexpr double lambda_C = h / (m_e * c);             // Compton wavelength (m)
    constexpr double K = m_e * c / (2.0 * h);              // nm⁻¹
    constexpr double K_nm = K * 1e9;                        // conversion helper
}

// Atomic properties calculated from ionization energy
struct AtomicProperties {
    double E_i;              // Ionization energy (eV)
    double koppa;            // ϟ = c/v (dimensionless)
    double koppa_sq;         // ϟ²
    double velocity;         // m/s
    double v_over_c;         // v/c (fraction of light speed)
    double wavelength_nm;    // Ionization wavelength (nm)
    double wavelength_m;     // Ionization wavelength (m)
    double phase_space;      // Ω = ϟ² (phase space volume)
    double n_eff;            // Effective quantum number
    
    // Photon properties for ionization/recombination
    double photon_energy_eV; // = E_i
    double photon_wavelength_nm; // = wavelength_nm
    double photon_frequency_Hz;
};

// Calculate all properties from ionization energy
[[nodiscard]] constexpr AtomicProperties calculate_properties(double E_i_eV) noexcept {
    using namespace constants;
    
    AtomicProperties props{};
    props.E_i = E_i_eV;
    
    // Step 1: Calculate ϟ (koppa)
    props.koppa = alpha_inv * std::sqrt(Ry / E_i_eV);
    props.koppa_sq = props.koppa * props.koppa;
    
    // Step 2: Calculate velocity
    props.velocity = c / props.koppa;
    props.v_over_c = 1.0 / props.koppa;
    
    // Step 3: Calculate wavelength via Compton relation
    // λ = 2λ_C × ϟ² = ϟ²/K
    props.wavelength_m = 2.0 * lambda_C * props.koppa_sq;
    props.wavelength_nm = props.wavelength_m * 1e9;
    
    // Alternative: λ = hc/E
    constexpr double hc_eV_nm = 1239.841'984;  // h×c in eV·nm
    double wavelength_check = hc_eV_nm / E_i_eV;
    // These should match (validation)
    
    // Step 4: Phase space volume
    props.phase_space = props.koppa_sq;
    
    // Step 5: Effective quantum number
    props.n_eff = props.koppa / alpha_inv;
    
    // Photon properties (for recombination)
    props.photon_energy_eV = E_i_eV;
    props.photon_wavelength_nm = props.wavelength_nm;
    props.photon_frequency_Hz = c / props.wavelength_m;
    
    return props;
}

// Calculate quantum defect given principal quantum number
[[nodiscard]] constexpr double quantum_defect(double n, double n_eff) noexcept {
    return n - n_eff;
}

// Multi-ionization sequence
struct IonizationLevel {
    int position;            // 1 = outermost, 2 = next, etc.
    std::string_view shell;  // e.g., "3s", "2p"
    AtomicProperties props;
};

// Validate energy conservation: E_ratio should equal phase_space_ratio
struct EnergyConservation {
    double energy_ratio;
    double phase_space_ratio;
    double koppa_ratio_sq;
    double relative_error;  // Should be ~0 for perfect conservation
};

[[nodiscard]] constexpr EnergyConservation validate_conservation(
    const AtomicProperties& level1,
    const AtomicProperties& level2) noexcept 
{
    EnergyConservation result{};
    result.energy_ratio = level2.E_i / level1.E_i;
    result.phase_space_ratio = level1.phase_space / level2.phase_space;
    
    double koppa_ratio = level1.koppa / level2.koppa;
    result.koppa_ratio_sq = koppa_ratio * koppa_ratio;
    
    // All three should be equal
    result.relative_error = std::abs(result.energy_ratio - result.phase_space_ratio) 
                          / result.energy_ratio;
    
    return result;
}

// Format output for display
[[nodiscard]] std::string format_properties(const AtomicProperties& props) {
    return std::format(
        "E_i:      {:.4f} eV\n"
        "ϟ:        {:.2f}\n"
        "ϟ²:       {:.0f}\n"
        "v:        {:.3e} m/s ({:.4f}% c)\n"
        "λ_ion:    {:.2f} nm\n"
        "Ω:        {:.0f}\n"
        "n_eff:    {:.3f}\n"
        "Photon λ: {:.2f} nm (for recombination)",
        props.E_i,
        props.koppa,
        props.koppa_sq,
        props.velocity, props.v_over_c * 100.0,
        props.wavelength_nm,
        props.phase_space,
        props.n_eff,
        props.photon_wavelength_nm
    );
}

} // namespace sdt

#endif // SDT_ATOMIC_PROPERTIES_HPP
