#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/core/constants.hpp"
#include <complex>
#include <cmath>
#include <numbers>

namespace sdt::physics::atomic {

    using namespace std::complex_literals;
    
    double ElectronOrbital::probability_density(const Vec3d& position) const {
        const std::complex<double> psi = wave_function(position);
        return std::norm(psi);
    }
    
    std::complex<double> ElectronOrbital::wave_function(const Vec3d& position) const {
        const double r = position.norm();
        const double theta = std::acos(position.z() / r);
        const double phi = std::atan2(position.y(), position.x());
        
        const double R = radial_wave_function(r);
        const std::complex<double> Y = spherical_harmonic(theta, phi);
        const double N = normalization_constant();
        
        return N * R * Y;
    }
    
    double ElectronOrbital::radial_wave_function(double r) const {
        const double a_0 = constants::a_0;
        const double Z_eff = static_cast<double>(Z);
        const double rho = 2.0 * Z_eff * r / (state.qn.n * a_0);
        
        // Simplified radial function (full implementation would use Laguerre polynomials)
        // For n=1: R_10 = 2 (Z/a_0)^(3/2) exp(-ρ/2)
        if (state.qn.n == 1 && state.qn.l == 0) {
            const double prefactor = 2.0 * std::pow(Z_eff / a_0, 1.5);
            return prefactor * std::exp(-rho / 2.0);
        }
        
        // For n=2, l=0: R_20 = (1/√2) (Z/a_0)^(3/2) (1 - ρ/2) exp(-ρ/2)
        if (state.qn.n == 2 && state.qn.l == 0) {
            const double prefactor = (1.0 / std::sqrt(2.0)) * std::pow(Z_eff / a_0, 1.5);
            return prefactor * (1.0 - rho / 2.0) * std::exp(-rho / 2.0);
        }
        
        // For n=2, l=1: R_21 = (1/√24) (Z/a_0)^(3/2) ρ exp(-ρ/2)
        if (state.qn.n == 2 && state.qn.l == 1) {
            const double prefactor = (1.0 / std::sqrt(24.0)) * std::pow(Z_eff / a_0, 1.5);
            return prefactor * rho * std::exp(-rho / 2.0);
        }
        
        // General form (simplified - full would use associated Laguerre polynomials)
        const double prefactor = std::sqrt(std::pow(2.0 * Z_eff / (state.qn.n * a_0), 3) / 
                                          (2.0 * state.qn.n * std::tgamma(state.qn.n + state.qn.l + 1)));
        return prefactor * std::pow(rho, state.qn.l) * std::exp(-rho / 2.0);
    }
    
    std::complex<double> ElectronOrbital::spherical_harmonic(double theta, double phi) const {
        const int l = state.qn.l;
        const int m = state.qn.m;
        
        // Simplified spherical harmonics (full would use associated Legendre polynomials)
        if (l == 0 && m == 0) {
            // Y_00 = 1/√(4π)
            return 1.0 / std::sqrt(4.0 * std::numbers::pi);
        }
        
        if (l == 1) {
            if (m == 0) {
                // Y_10 = √(3/4π) cos(θ)
                return std::sqrt(3.0 / (4.0 * std::numbers::pi)) * std::cos(theta);
            } else if (m == 1) {
                // Y_11 = -√(3/8π) sin(θ) exp(iφ)
                return -std::sqrt(3.0 / (8.0 * std::numbers::pi)) * std::sin(theta) * 
                       std::exp(1.0i * phi);
            } else if (m == -1) {
                // Y_1-1 = √(3/8π) sin(θ) exp(-iφ)
                return std::sqrt(3.0 / (8.0 * std::numbers::pi)) * std::sin(theta) * 
                       std::exp(-1.0i * phi);
            }
        }
        
        // General form (simplified)
        return std::sqrt((2.0 * l + 1.0) / (4.0 * std::numbers::pi)) * 
               std::exp(static_cast<double>(m) * 1.0i * phi);
    }
    
    double ElectronOrbital::normalization_constant() const {
        // Normalization from quantum mechanics
        const double a_0 = constants::a_0;
        const double Z_eff = static_cast<double>(Z);
        
        const double factor = std::pow(2.0 * Z_eff / (state.qn.n * a_0), 3);
        const double normalization = std::sqrt(factor / (2.0 * state.qn.n));
        
        return normalization;
    }
    
    std::vector<std::vector<std::vector<double>>> ElectronOrbital::generate_probability_grid(
        const Vec3d& center,
        double extent,
        int resolution
    ) const {
        std::vector<std::vector<std::vector<double>>> grid(
            resolution,
            std::vector<std::vector<double>>(
                resolution,
                std::vector<double>(resolution, 0.0)
            )
        );
        
        const double step = 2.0 * extent / resolution;
        const double start = -extent;
        
        for (int i = 0; i < resolution; ++i) {
            for (int j = 0; j < resolution; ++j) {
                for (int k = 0; k < resolution; ++k) {
                    const double x = center.x() + start + i * step;
                    const double y = center.y() + start + j * step;
                    const double z = center.z() + start + k * step;
                    const Vec3d pos(x, y, z);
                    
                    grid[i][j][k] = probability_density(pos);
                }
            }
        }
        
        return grid;
    }
    
    std::vector<std::pair<double, double>> ElectronOrbital::radial_probability_distribution(
        int num_points
    ) const {
        std::vector<std::pair<double, double>> distribution;
        distribution.reserve(num_points);
        
        const double max_r = 5.0 * state.radius;  // Extend to 5× expected radius
        const double dr = max_r / num_points;
        
        for (int i = 0; i < num_points; ++i) {
            const double r = i * dr;
            const double R = radial_wave_function(r);
            const double prob = r * r * R * R;  // Radial probability density
            
            distribution.push_back({r, prob});
        }
        
        return distribution;
    }
    
    double AtomicSystem::total_energy() const {
        double total = 0.0;
        for (const auto& orbital : occupied_orbitals) {
            total += orbital.energy;
        }
        // Add electron-electron interaction terms (simplified)
        // Full calculation would include screening and exchange
        return total;
    }
    
    void AtomicSystem::add_electron(const QuantumNumbers& qn) {
        OrbitalState state;
        state.qn = qn;
        state.calculate_radius(Z);
        state.calculate_energy(Z);
        state.calculate_kappa(Z);
        occupied_orbitals.push_back(state);
    }
    
    double AtomicSystem::electron_density(const Vec3d& position) const {
        double density = 0.0;
        for (const auto& orbital_state : occupied_orbitals) {
            ElectronOrbital orbital;
            orbital.state = orbital_state;
            orbital.Z = Z;
            density += orbital.probability_density(position);
        }
        return density;
    }
    
    std::vector<std::vector<std::vector<double>>> AtomicSystem::generate_electron_density_grid(
        const Vec3d& center,
        double extent,
        int resolution
    ) const {
        std::vector<std::vector<std::vector<double>>> grid(
            resolution,
            std::vector<std::vector<double>>(
                resolution,
                std::vector<double>(resolution, 0.0)
            )
        );
        
        const double step = 2.0 * extent / resolution;
        const double start = -extent;
        
        for (int i = 0; i < resolution; ++i) {
            for (int j = 0; j < resolution; ++j) {
                for (int k = 0; k < resolution; ++k) {
                    const double x = center.x() + start + i * step;
                    const double y = center.y() + start + j * step;
                    const double z = center.z() + start + k * step;
                    const Vec3d pos(x, y, z);
                    
                    grid[i][j][k] = electron_density(pos);
                }
            }
        }
        
        return grid;
    }
    
    bool is_allowed_transition(const QuantumNumbers& initial, const QuantumNumbers& final) {
        // Electric dipole selection rules:
        // Δl = ±1
        // Δm = 0, ±1
        // Δn = any
        // Δs = 0
        
        const int delta_l = final.l - initial.l;
        const int delta_m = final.m - initial.m;
        
        if (std::abs(delta_l) != 1) {
            return false;
        }
        
        if (std::abs(delta_m) > 1) {
            return false;
        }
        
        return true;
    }
    
    double oscillator_strength(const OrbitalState& initial, const OrbitalState& final) {
        // Oscillator strength calculation (simplified)
        // Full calculation requires transition dipole moment
        
        if (!is_allowed_transition(initial.qn, final.qn)) {
            return 0.0;
        }
        
        // Approximate: f ∝ |<final|r|initial>|²
        const double energy_diff = std::abs(final.energy - initial.energy);
        const double prefactor = (2.0 / 3.0) * (initial.qn.n * initial.qn.n) / 
                                (final.qn.n * final.qn.n);
        
        return prefactor * std::exp(-energy_diff / 13.6);  // Simplified
    }
    
    double einstein_a_coefficient(const SpectralTransition& transition) {
        // Einstein A coefficient: A = (64π⁴ e² ν³) / (3h m_e c³) × |<i|r|f>|²
        const double nu = transition.frequency;
        const double f = transition.oscillator_strength;
        
        const double e = 1.602176634e-19;  // C
        const double m_e = 9.1093837015e-31;  // kg
        const double h_val = constants::h;
        
        const double prefactor = 64.0 * std::pow(constants::pi, 4) * e * e * 
                                std::pow(nu, 3) / (3.0 * h_val * m_e * constants::c * constants::c * constants::c);
        
        return prefactor * f;
    }

} // namespace sdt::physics::atomic

