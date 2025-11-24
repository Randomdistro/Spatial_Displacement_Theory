#pragma once

#include "sdt/core/types.hpp"
#include "sdt/core/constants.hpp"
#include <vector>
#include <complex>
#include <string>
#include <map>
#include <cmath>
#include <numbers>

namespace sdt::physics::atomic {
#include <Eigen/Dense>
#include <vector>
#include <complex>
#include <string>
#include <map>
#include <cmath>

namespace sdt::physics::atomic {

    // Quantum numbers
    struct QuantumNumbers {
        int n = 1;  // Principal quantum number
        int l = 0;  // Angular momentum quantum number (0=s, 1=p, 2=d, 3=f)
        int m = 0;  // Magnetic quantum number (-l to +l)
        double s = 0.5;  // Spin (±1/2)
        
        bool operator<(const QuantumNumbers& other) const {
            if (n != other.n) return n < other.n;
            if (l != other.l) return l < other.l;
            if (m != other.m) return m < other.m;
            return s < other.s;
        }
    };
    
    // Orbital state
    struct OrbitalState {
        QuantumNumbers qn;
        double energy = 0.0;  // eV
        double radius = 0.0;  // m (expected value)
        double kappa = 0.0;   // SDT velocity factor Ϟ
        
        // Calculate radius from SDT
        // From Phase 2: r_n = a_0 n² / Z
        void calculate_radius(int Z) {
            radius = constants::a_0 * qn.n * qn.n / Z;
        }
        
        // Calculate energy from SDT
        // From Phase 2: E_n = -½ μ c² α² Z² / n²
        void calculate_energy(int Z, double reduced_mass_factor = 1.0) {
            const double mu = reduced_mass_factor * 9.1093837015e-31;  // kg
            energy = -0.5 * mu * constants::c * constants::c * 
                     constants::alpha * constants::alpha * Z * Z / (qn.n * qn.n);
            // Convert from J to eV
            energy /= 1.602176634e-19;
        }
        
        // Calculate kappa from SDT orbital mechanics
        // From Phase 2: Ϟ_n = n / (Z α)
        void calculate_kappa(int Z) {
            kappa = static_cast<double>(qn.n) / (Z * constants::ALPHA);
        }
    };
    
    // Electron orbital wave function (SDT helical standing wave representation)
    class ElectronOrbital {
    public:
        OrbitalState state;
        int Z = 1;  // Nuclear charge
        
        // Calculate probability density |ψ(r,θ,φ)|² at position
        double probability_density(const Vec3d& position) const;
        
        // Calculate wave function value ψ(r,θ,φ) (complex)
        std::complex<double> wave_function(const Vec3d& position) const;
        
        // Generate 3D probability density grid
        // Returns grid of probability values on a 3D grid
        std::vector<std::vector<std::vector<double>>> generate_probability_grid(
            const Vec3d& center,
            double extent,
            int resolution = 100
        ) const;
        
        // Calculate expected radius (Bohr radius scaling)
        double expected_radius() const {
            return state.radius;
        }
        
        // Calculate orbital angular momentum
        double angular_momentum() const {
            return std::sqrt(state.qn.l * (state.qn.l + 1)) * constants::H_BAR;
        }
        
        // Calculate radial probability distribution (probability vs radius)
        std::vector<std::pair<double, double>> radial_probability_distribution(
            int num_points = 1000
        ) const;
        
    private:
        // Radial wave function R_nl(r)
        double radial_wave_function(double r) const;
        
        // Spherical harmonic Y_lm(θ, φ)
        std::complex<double> spherical_harmonic(double theta, double phi) const;
        
        // Normalization constant for orbital
        double normalization_constant() const;
    };
    
    // Atomic system (single atom with electrons)
    class AtomicSystem {
    public:
        int Z = 1;  // Nuclear charge
        std::vector<OrbitalState> occupied_orbitals;
        
        // Calculate total energy
        double total_energy() const;
        
        // Add electron to orbital
        void add_electron(const QuantumNumbers& qn);
        
        // Calculate ionization energy
        double ionization_energy(int electron_index = -1) const;
        
        // Calculate electron density at position
        double electron_density(const Vec3d& position) const;
        
        // Generate electron density grid
        std::vector<std::vector<std::vector<double>>> generate_electron_density_grid(
            const Vec3d& center,
            double extent,
            int resolution = 100
        ) const;
    };
    
    // Hydrogen atom (single electron)
    class HydrogenAtom {
    public:
        OrbitalState ground_state;
        
        HydrogenAtom() {
            ground_state.qn = {1, 0, 0, 0.5};
            ground_state.calculate_radius(1);
            ground_state.calculate_energy(1);
            ground_state.calculate_kappa(1);
        }
        
        // Get state for quantum numbers
        OrbitalState get_state(int n, int l = 0, int m = 0) const {
            OrbitalState state;
            state.qn = {n, l, m, 0.5};
            state.calculate_radius(1);
            state.calculate_energy(1);
            state.calculate_kappa(1);
            return state;
        }
        
        // Calculate transition energy between states
        double transition_energy(int n1, int n2) const {
            const auto state1 = get_state(n1);
            const auto state2 = get_state(n2);
            return std::abs(state2.energy - state1.energy);
        }
        
        // Calculate wavelength for transition
        double transition_wavelength(int n1, int n2) const {
            const double E_eV = transition_energy(n1, n2);
            // λ = hc / E
            return (1240.0 / E_eV) * 1e-9;  // Convert to meters
        }
    };
    
    // Spectral transition
    struct SpectralTransition {
        QuantumNumbers initial_state;
        QuantumNumbers final_state;
        double energy = 0.0;  // eV
        double wavelength = 0.0;  // m
        double frequency = 0.0;  // Hz
        double oscillator_strength = 0.0;
        double transition_probability = 0.0;  // s⁻¹ (Einstein A coefficient)
        
        // Calculate from SDT
        void calculate_from_states(const OrbitalState& initial, const OrbitalState& final) {
            energy = std::abs(final.energy - initial.energy);
            frequency = energy * 1.602176634e-19 / constants::hbar / (2.0 * constants::pi);
            wavelength = constants::c / frequency;
        }
    };
    
    // Calculate all allowed transitions for an atom
    std::vector<SpectralTransition> calculate_transitions(
        const AtomicSystem& atom,
        int max_n = 10
    );
    
    // Selection rules for electric dipole transitions
    bool is_allowed_transition(const QuantumNumbers& initial, const QuantumNumbers& final);
    
    // Calculate oscillator strength for transition
    double oscillator_strength(const OrbitalState& initial, const OrbitalState& final);
    
    // Calculate Einstein A coefficient (spontaneous emission rate)
    double einstein_a_coefficient(const SpectralTransition& transition);

} // namespace sdt::physics::atomic

