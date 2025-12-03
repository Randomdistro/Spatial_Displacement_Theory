// L × k² = ε Mc² Validation Tool
// Demonstrates luminosity-based baryonic mass determination without dark matter
// Based on: J. Tyndall (2025) "Galactic Structure via z-Scaling and Luminosity"

#include "galactic_rotation.hpp"
#include <iostream>
#include <iomanip>

using namespace sdt;

int main() {
    std::cout << "\n";
    std::cout << "╔══════════════════════════════════════════════════════════════════════╗\n";
    std::cout << "║   SDT Luminosity-Mass Relation: L × k² = ε Mc²                       ║\n";
    std::cout << "║   No Dark Matter Required - Pure Geometric Scaling                   ║\n";
    std::cout << "║   Reference: Tyndall (2025)                                          ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════════════════╝\n\n";
    
    auto galaxies = GalacticRotationCalculator::get_standard_test_galaxies();
    
    // Table header
    std::cout << "Validation of the Universal Invariant: z × k² = 1\n";
    std::cout << std::string(80, '=') << "\n\n";
    
    std::cout << std::setw(20) << "Galaxy"
              << std::setw(12) << "v_rot (km/s)"
              << std::setw(10) << "k"
              << std::setw(12) << "z"
              << std::setw(12) << "z × k²\n";
    std::cout << std::string(66, '-') << "\n";
    
    for (const auto& gal : galaxies) {
        const double k = gal.k_parameter();
        const double z = gal.z_compactness();
        const double zk2 = gal.zk2_product();
        
        std::cout << std::setw(20) << gal.name
                  << std::fixed << std::setprecision(1)
                  << std::setw(12) << gal.v_flat_kms
                  << std::setw(10) << static_cast<int>(k)
                  << std::scientific << std::setprecision(2)
                  << std::setw(12) << z
                  << std::fixed << std::setprecision(4)
                  << std::setw(12) << zk2 << "\n";
    }
    
    std::cout << std::string(66, '-') << "\n";
    std::cout << "Expected: z × k² = 1.0000 (geometric identity)\n\n";
    
    // L × k² = ε Mc² validation
    std::cout << "\nValidation of L × k² = ε Mc² Relationship\n";
    std::cout << std::string(80, '=') << "\n\n";
    
    std::cout << std::setw(20) << "Galaxy"
              << std::setw(12) << "L (10⁹ L☉)"
              << std::setw(10) << "k"
              << std::setw(15) << "Lk²/(Mc²)"
              << std::setw(15) << "M_predicted/M_obs\n";
    std::cout << std::string(72, '-') << "\n";
    
    double sum_ratio = 0.0;
    double sum_diagnostic = 0.0;
    
    for (const auto& gal : galaxies) {
        const double k = gal.k_parameter();
        const double diagnostic = GalacticRotationCalculator::calculate_lk2_diagnostic(gal);
        const double mass_ratio = GalacticRotationCalculator::validate_luminosity_mass_relation(gal);
        
        sum_diagnostic += diagnostic;
        sum_ratio += mass_ratio;
        
        std::cout << std::setw(20) << gal.name
                  << std::fixed << std::setprecision(1)
                  << std::setw(12) << (gal.luminosity_solar / 1e9)
                  << std::setw(10) << static_cast<int>(k)
                  << std::scientific << std::setprecision(2)
                  << std::setw(15) << diagnostic
                  << std::fixed << std::setprecision(3)
                  << std::setw(15) << mass_ratio << "\n";
    }
    
    const double mean_diagnostic = sum_diagnostic / galaxies.size();
    const double mean_ratio = sum_ratio / galaxies.size();
    
    std::cout << std::string(72, '-') << "\n";
    std::cout << "Mean Lk²/(Mc²): " << std::scientific << std::setprecision(2) 
              << mean_diagnostic << "\n";
    std::cout << "Expected ε:     " << 1e-15 << " (nuclear burning efficiency)\n";
    std::cout << "Mean M_pred/M_obs: " << std::fixed << std::setprecision(3) 
              << mean_ratio << "\n\n";
    
    // Mass determination example
    std::cout << "\nBaryonic Mass Determination from Observables Only\n";
    std::cout << std::string(80, '=') << "\n\n";
    std::cout << "Given ONLY luminosity L and rotation velocity v_rot:\n";
    std::cout << "  1. Calculate k = c/v_rot\n";
    std::cout << "  2. Calculate M = (L × k²) / (ε × c²)\n\n";
    
    std::cout << "Example: Milky Way\n";
    std::cout << std::string(40, '-') << "\n";
    
    const auto& mw = galaxies[0];
    const double k_mw = mw.k_parameter();
    const double M_predicted = GalacticRotationCalculator::calculate_mass_from_luminosity(
        mw.luminosity_solar, k_mw
    );
    
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "  Luminosity:         " << std::scientific << mw.luminosity_solar << " L☉\n";
    std::cout << "  Rotation velocity:  " << std::fixed << mw.v_flat_kms << " km/s\n";
    std::cout << "  Calculated k:       " << static_cast<int>(k_mw) << "\n";
    std::cout << "  Predicted mass:     " << std::scientific << std::setprecision(2) 
              << M_predicted << " M☉\n";
    std::cout << "  Observed mass:      " << mw.M_disk_solar << " M☉\n";
    std::cout << "  Agreement:          " << std::fixed << std::setprecision(1)
              << (M_predicted / mw.M_disk_solar * 100.0) << "%\n\n";
    
    // Key insight
    std::cout << "\n" << std::string(80, '=') << "\n";
    std::cout << "Key Insight:\n";
    std::cout << std::string(80, '=') << "\n\n";
    std::cout << "The relationship L × k² = ε Mc² allows direct determination of\n";
    std::cout << "baryonic mass from luminosity and rotation velocity alone.\n\n";
    std::cout << "NO DARK MATTER REQUIRED:\n";
    std::cout << "  • Flat rotation curves emerge from disk geometry\n";
    std::cout << "  • The z × k² = 1 invariant extends from atomic to galactic scales\n";
    std::cout << "  • All galactic dynamics follow from geometric scaling laws\n\n";
    std::cout << "Reference: Tyndall, J. (2025). \"Extrapolation of Spatial Displacement\n";
    std::cout << "           Theory to Galactic Structure: Determining Size and Rotation\n";
    std::cout << "           Curves via z-Scaling and Luminosity\"\n\n";
    
    return 0;
}
