#pragma once

#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/core/constants.hpp"
#include <vector>
#include <string>
#include <map>

namespace sdt::physics::atomic {
#include <vector>
#include <string>
#include <map>

namespace sdt::physics::atomic {

    // Spectral series type
    enum class SpectralSeries {
        LYMAN,      // n → 1 (UV)
        BALMER,     // n → 2 (Visible)
        PASCHEN,    // n → 3 (IR)
        BRACKETT,   // n → 4 (IR)
        PFUND       // n → 5 (IR)
    };
    
    // Spectral line
    struct SpectralLine {
        int n_initial;
        int n_final;
        double wavelength = 0.0;  // m
        double frequency = 0.0;   // Hz
        double energy = 0.0;      // eV
        double intensity = 0.0;   // relative
        SpectralSeries series = SpectralSeries::LYMAN;
        std::string name;  // e.g., "Lyman α"
        
        // Calculate from SDT Rydberg formula
        void calculate_from_rydberg(int Z = 1, double reduced_mass_factor = 1.0) {
            using namespace constants;
            const double R_inf = reduced_mass_factor * 10973731.568160;  // m⁻¹
            const double wavenumber = R_inf * Z * Z * (1.0/(n_final*n_final) - 1.0/(n_initial*n_initial));
            wavelength = 1.0 / wavenumber;
            frequency = c / wavelength;
            energy = constants::h * frequency / 1.602176634e-19;  // Convert to eV
            
            // Assign series name
            if (n_final == 1) {
                series = SpectralSeries::LYMAN;
                if (n_initial == 2) name = "Lyman α";
                else if (n_initial == 3) name = "Lyman β";
                else name = "Lyman " + std::to_string(n_initial - n_final);
            } else if (n_final == 2) {
                series = SpectralSeries::BALMER;
                if (n_initial == 3) name = "Hα (Balmer α)";
                else if (n_initial == 4) name = "Hβ (Balmer β)";
                else if (n_initial == 5) name = "Hγ (Balmer γ)";
                else name = "Balmer " + std::to_string(n_initial - n_final);
            } else if (n_final == 3) {
                series = SpectralSeries::PASCHEN;
                name = "Paschen " + std::to_string(n_initial - n_final);
            } else if (n_final == 4) {
                series = SpectralSeries::BRACKETT;
                name = "Brackett " + std::to_string(n_initial - n_final);
            } else {
                series = SpectralSeries::PFUND;
                name = "Pfund " + std::to_string(n_initial - n_final);
            }
        }
    };
    
    // Spectral spectrum (collection of lines)
    class AtomicSpectrum {
    public:
        int Z = 1;  // Nuclear charge
        std::vector<SpectralLine> lines;
        
        // Generate hydrogen spectrum
        void generate_hydrogen_spectrum(int max_n = 10);
        
        // Generate spectrum for ionized atom (Z)
        void generate_ionized_spectrum(int Z, int max_n = 10);
        
        // Get lines in wavelength range
        std::vector<SpectralLine> get_lines_in_range(double lambda_min, double lambda_max) const;
        
        // Get lines in series
        std::vector<SpectralLine> get_lines_in_series(SpectralSeries series) const;
        
        // Calculate line intensities (relative)
        void calculate_intensities();
        
        // Match experimental spectrum (NIST data)
        void match_experimental(const std::vector<SpectralLine>& experimental);
    };
    
    // Fine structure splitting
    struct FineStructureComponent {
        int n;
        int l;
        int j;  // Total angular momentum j = l ± 1/2
        double energy = 0.0;  // eV
        double splitting = 0.0;  // eV (relative to center)
        
        // Calculate from SDT fine structure formula
        // From Phase 3: ΔE_fs = α² E_n (Z⁴/n⁴) × f(l, j)
        void calculate_fine_structure(int Z, int n_val, int l_val, int j_val) {
            n = n_val;
            l = l_val;
            j = j_val;
            
            using namespace constants;
            const double E_n = -0.5 * 9.1093837015e-31 * c * c * alpha * alpha * Z * Z / (n * n);
            const double E_n_eV = E_n / 1.602176634e-19;
            
            // Fine structure correction: ΔE_fs = E_n α² Z⁴/n⁴ × [j(j+1) - l(l+1) - 3/4] / [2l(l+1)]
            const double j_term = j * (j + 1) - l * (l + 1) - 0.75;
            const double denominator = 2.0 * l * (l + 1);
            const double correction_factor = (l > 0) ? (alpha * alpha * Z * Z * Z * Z / (n * n * n * n) * j_term / denominator) : 0.0;
            
            splitting = E_n_eV * correction_factor;
            energy = E_n_eV + splitting;
        }
    };
    
    // Fine structure of a level
    struct FineStructureLevel {
        int n;
        int l;
        std::vector<FineStructureComponent> components;  // j = l ± 1/2
        
        // Calculate fine structure splitting
        void calculate(int Z) {
            if (l == 0) {
                // S-state: no fine structure
                FineStructureComponent comp;
                comp.n = n;
                comp.l = l;
                comp.j = 1;  // j = 1/2, stored as 1
                comp.energy = -13.6 * Z * Z / (n * n);
                comp.splitting = 0.0;
                components.push_back(comp);
            } else {
                // j = l - 1/2
                FineStructureComponent comp1;
                comp1.calculate_fine_structure(Z, n, l, l);  // j = l
                components.push_back(comp1);
                
                // j = l + 1/2
                FineStructureComponent comp2;
                comp2.calculate_fine_structure(Z, n, l, l + 1);  // j = l + 1
                components.push_back(comp2);
            }
        }
    };
    
    // Hyperfine splitting
    struct HyperfineSplitting {
        int n;
        int F;  // Total angular momentum F = I + J
        double energy = 0.0;  // eV
        double frequency = 0.0;  // Hz (for transitions)
        
        // Calculate from SDT hyperfine formula
        // From Phase 5/8: ΔE_hf = (8/3) β_geom g_I g_e (m_e/m_p) α⁴ m_e c² / n³
        void calculate_hydrogen_1s() {
            using namespace constants;
            const double beta_geom = 0.951;
            const double g_I = 5.5856946893;  // Proton g-factor
            const double g_e = 2.00231930436;
            const double m_e_over_m_p = 5.44617021487e-4;
            const double m_e_c2_eV = 510998.9502;  // eV
            
            const double prefactor = (8.0/3.0) * beta_geom * g_I * g_e * m_e_over_m_p;
            const double energy_joule = prefactor * alpha * alpha * alpha * alpha * m_e_c2_eV * 1.602176634e-19 / (n * n * n);
            energy = energy_joule / 1.602176634e-19;  // eV
            frequency = energy * 1.602176634e-19 / h;
        }
    };
    
    // Complete spectral analysis for an atom
    class SpectralAnalyzer {
    public:
        // Analyze hydrogen spectrum
        AtomicSpectrum analyze_hydrogen(int max_n = 10);
        
        // Calculate fine structure for level
        FineStructureLevel calculate_fine_structure(int Z, int n, int l);
        
        // Calculate hyperfine splitting
        HyperfineSplitting calculate_hyperfine(int n, int l, int nuclear_spin = 1);
        
        // Compare with experimental data
        double compare_with_experimental(
            const std::vector<SpectralLine>& calculated,
            const std::vector<SpectralLine>& experimental
        );
    };

} // namespace sdt::physics::atomic

