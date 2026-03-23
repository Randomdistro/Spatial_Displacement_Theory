#include "sdt/physics/spectral_transitions.hpp"
#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/core/constants.hpp"
#include <algorithm>
#include <cmath>

namespace sdt::physics::atomic {

    void AtomicSpectrum::generate_hydrogen_spectrum(int max_n) {
        lines.clear();
        
        // Generate all transitions
        for (int n_final = 1; n_final < max_n; ++n_final) {
            for (int n_initial = n_final + 1; n_initial <= max_n; ++n_initial) {
                SpectralLine line;
            line.n_initial = n_initial;
            line.n_final = n_final;
            line.calculate_from_rydberg(Z, 1.0);  // Hydrogen: reduced mass factor = 1.0
            lines.push_back(line);
            }
        }
        
        calculate_intensities();
    }
    
    void AtomicSpectrum::generate_ionized_spectrum(int Z_val, int max_n) {
        Z = Z_val;
        lines.clear();
        
        // For ions, use reduced mass correction
        const double reduced_mass_factor = 1.0 - (9.1093837015e-31 / (1.67262192369e-27 * Z));
        
        for (int n_final = 1; n_final < max_n; ++n_final) {
            for (int n_initial = n_final + 1; n_initial <= max_n; ++n_initial) {
                SpectralLine line;
                line.n_initial = n_initial;
                line.n_final = n_final;
                line.calculate_from_rydberg(Z, reduced_mass_factor);
                lines.push_back(line);
            }
        }
        
        calculate_intensities();
    }
    
    std::vector<SpectralLine> AtomicSpectrum::get_lines_in_range(
        double lambda_min,
        double lambda_max
    ) const {
        std::vector<SpectralLine> filtered;
        for (const auto& line : lines) {
            // Wavelengths are in meters, so compare directly
            if (line.wavelength >= lambda_min && line.wavelength <= lambda_max) {
                filtered.push_back(line);
            }
        }
        return filtered;
    }
    
    std::vector<SpectralLine> AtomicSpectrum::get_lines_in_series(SpectralSeries series) const {
        std::vector<SpectralLine> filtered;
        for (const auto& line : lines) {
            if (line.series == series) {
                filtered.push_back(line);
            }
        }
        return filtered;
    }
    
    void AtomicSpectrum::calculate_intensities() {
        // Simplified intensity calculation
        // Intensity ∝ oscillator strength × population × transition probability
        
        for (auto& line : lines) {
            // Approximate: intensity ∝ 1/λ⁴ × 1/n_initial³
            const double lambda_factor = 1.0 / (line.wavelength * line.wavelength * 
                                               line.wavelength * line.wavelength);
            const double n_factor = 1.0 / (line.n_initial * line.n_initial * line.n_initial);
            
            line.intensity = lambda_factor * n_factor;
        }
        
        // Normalize to max intensity = 1.0
        double max_intensity = 0.0;
        for (const auto& line : lines) {
            max_intensity = std::max(max_intensity, line.intensity);
        }
        
        if (max_intensity > 0.0) {
            for (auto& line : lines) {
                line.intensity /= max_intensity;
            }
        }
    }
    
    std::vector<SpectralTransition> calculate_transitions(
        const AtomicSystem& atom,
        int max_n
    ) {
        std::vector<SpectralTransition> transitions;
        
        // Generate all possible transitions
        HydrogenAtom h_atom;
        
        for (int n1 = 1; n1 <= max_n; ++n1) {
            for (int n2 = 1; n2 <= max_n; ++n2) {
                if (n1 == n2) continue;
                
                const auto state1 = h_atom.get_state(n1);
                const auto state2 = h_atom.get_state(n2);
                
                QuantumNumbers qn1 = state1.qn;
                QuantumNumbers qn2 = state2.qn;
                
                // Check selection rules
                if (is_allowed_transition(qn1, qn2)) {
                    SpectralTransition trans;
                    trans.initial_state = (n1 > n2) ? qn1 : qn2;
                    trans.final_state = (n1 > n2) ? qn2 : qn1;
                    trans.calculate_from_states(
                        (n1 > n2) ? state1 : state2,
                        (n1 > n2) ? state2 : state1
                    );
                    trans.oscillator_strength = oscillator_strength(
                        (n1 > n2) ? state1 : state2,
                        (n1 > n2) ? state2 : state1
                    );
                    trans.transition_probability = einstein_a_coefficient(trans);
                    
                    transitions.push_back(trans);
                }
            }
        }
        
        return transitions;
    }
    
    AtomicSpectrum SpectralAnalyzer::analyze_hydrogen(int max_n) {
        AtomicSpectrum spectrum;
        spectrum.Z = 1;
        spectrum.generate_hydrogen_spectrum(max_n);
        return spectrum;
    }
    
    FineStructureLevel SpectralAnalyzer::calculate_fine_structure(int Z, int n, int l) {
        FineStructureLevel level;
        level.n = n;
        level.l = l;
        level.calculate(Z);
        return level;
    }
    
    HyperfineSplitting SpectralAnalyzer::calculate_hyperfine(int n, int l, int nuclear_spin) {
        HyperfineSplitting hf;
        hf.n = n;
        
        if (n == 1 && l == 0 && nuclear_spin == 1) {
            // Hydrogen 1S hyperfine
            hf.calculate_hydrogen_1s();
            // F = 0 or F = 1
            hf.F = 1;  // Higher energy state
        }
        
        return hf;
    }
    
    double SpectralAnalyzer::compare_with_experimental(
        const std::vector<SpectralLine>& calculated,
        const std::vector<SpectralLine>& experimental
    ) {
        double total_error = 0.0;
        int matches = 0;
        
        for (const auto& calc_line : calculated) {
            double min_diff = 1e9;
            
            for (const auto& exp_line : experimental) {
                const double diff = std::abs(calc_line.wavelength - exp_line.wavelength);
                if (diff < min_diff) {
                    min_diff = diff;
                }
            }
            
            if (min_diff < 1e-9) {  // Within 1 nm tolerance
                total_error += (min_diff / calc_line.wavelength) * 100.0;  // Percentage error
                matches++;
            }
        }
        
        return (matches > 0) ? (total_error / matches) : 1e9;
    }

} // namespace sdt::physics::atomic

