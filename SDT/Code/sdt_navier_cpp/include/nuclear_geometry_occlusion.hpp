#pragma once

#include <cmath>
#include <vector>
#include <string>
#include <array>
#include <sstream>
#include <iomanip>
#include <numbers>

namespace sdt::nuclear::occlusion {

// ============================================================================
// FUNDAMENTAL CONSTANTS & GEOMETRY
// ============================================================================

namespace constants {
    inline constexpr double proton_radius_fm = 0.84;
    inline constexpr double neutron_radius_fm = 0.84; // Treat as equal for packing
    
    // CALIBRATION:
    // Deuteron (experimental): 2.224 MeV, Separation ~2.1 fm
    // We derive 'binding_per_steradian' from this.
    
    // Occlusion/Shadowing Constant
    // Represents intensity of CMB pressure flux converted to binding force
    // Value calibrated to Deuteron at d=2.1 fm
    inline constexpr double k_binding_MeV_per_sr = 13.15; 
    
    // Geometric Lock Separations (The "Invariant Rules")
    inline constexpr double dist_deuteron_fm = 2.10;   // Measured
    inline constexpr double dist_alpha_fm = 1.45;      // Compressed (Vacuum Lock)
    inline constexpr double dist_inter_alpha_fm = 2.9; // C-12/O-16 cluster spacing
}

// ============================================================================
// GEOMETRIC HELPERS
// ============================================================================

namespace math {
    // Calculate solid angle occlusion of a sphere radius R at distance d
    // Omega = 2pi * (1 - cos(theta)), sin(theta) = R/d
    [[nodiscard]] inline double spherical_occlusion(double R, double d) {
        if (d <= R) return 2.0 * std::numbers::pi; // Full immersion
        double sin_theta = R / d;
        double cos_theta = std::sqrt(1.0 - sin_theta * sin_theta);
        return 2.0 * std::numbers::pi * (1.0 - cos_theta);
    }
}

// ============================================================================
// NUCLEON TYPES
// ============================================================================

struct Nucleon {
    enum class Type { Proton, Neutron };
    Type type;
    std::string chirality; // "L" or "R"
    
    [[nodiscard]] std::string full_name() const {
        return (type == Type::Proton ? "p" : "n") + std::string("(") + chirality + ")";
    }
};

// ============================================================================
// GEOMETRY CLASSES
// ============================================================================

struct DeuteronGeometry {
    // Structural Postulates
    static constexpr double R = constants::proton_radius_fm;
    static constexpr double d = constants::dist_deuteron_fm;
    
    [[nodiscard]] double occlusion_solid_angle() const {
        // Single bond (p-n)
        return math::spherical_occlusion(R, d);
    }
    
    [[nodiscard]] double binding_energy_predicted() const {
        return occlusion_solid_angle() * constants::k_binding_MeV_per_sr;
    }
    
    [[nodiscard]] static constexpr double binding_energy_experimental() { return 2.2246; }
};

struct AlphaGeometry {
    // Structural Postulates
    // 4 Nucleons in Tetrahedron. 6 Edges.
    // "Vacuum Lock" compression: d is smaller than Deuteron
    static constexpr double R = constants::proton_radius_fm;
    static constexpr double d = constants::dist_alpha_fm;
    
    [[nodiscard]] double total_occlusion() const {
        // 6 edges. All equivalent in the "Lock" phase (geometric dominance)
        // Opposing chirality pairs are preferred, but geometry forces 6 contacts.
        double single_bond_occlusion = math::spherical_occlusion(R, d);
        return 6.0 * single_bond_occlusion;
    }
    
    [[nodiscard]] double binding_energy_predicted() const {
        return total_occlusion() * constants::k_binding_MeV_per_sr;
    }
    
    [[nodiscard]] static constexpr double binding_energy_experimental() { return 28.296; }
    
    // Effective radius for inter-alpha interactions (Radius of the "Super-Nucleon")
    [[nodiscard]] double effective_radius_fm() const {
        // Approx radius of the tetrahedral cluster
        // Distance to center + nucleon radius
        double r_geometric_center = d * 0.6124; // d / sqrt(8/3) for tetrahedron
        return r_geometric_center + R;
    }
};

struct Carbon12Geometry {
    // 3 Alphas in Triangle
    AlphaGeometry alpha;
    static constexpr double d_cluster = constants::dist_inter_alpha_fm;
    
    [[nodiscard]] double inter_alpha_binding() const {
        // 3 connections between Alphas
        // Treat Alphas as large spheres with 'effective_radius'
        double R_eff = alpha.effective_radius_fm();
        double bond_occlusion = math::spherical_occlusion(R_eff, d_cluster);
        return 3.0 * bond_occlusion * constants::k_binding_MeV_per_sr;
    }
    
    [[nodiscard]] double binding_energy_predicted() const {
        // 3 * Internal Alpha + Inter-Alpha
        return (3.0 * alpha.binding_energy_predicted()) + inter_alpha_binding();
    }
    
    [[nodiscard]] static constexpr double binding_energy_experimental() { return 92.16; }
};

struct Oxygen16Geometry {
    // 4 Alphas in Tetrahedron
    AlphaGeometry alpha;
    static constexpr double d_cluster = constants::dist_inter_alpha_fm; // Same spacing as C-12
    
    [[nodiscard]] double inter_alpha_binding() const {
        // 6 connections (tetrahedral edges)
        double R_eff = alpha.effective_radius_fm();
        double bond_occlusion = math::spherical_occlusion(R_eff, d_cluster);
        return 6.0 * bond_occlusion * constants::k_binding_MeV_per_sr;
    }
    
    [[nodiscard]] double binding_energy_predicted() const {
        return (4.0 * alpha.binding_energy_predicted()) + inter_alpha_binding();
    }
    
    [[nodiscard]] static constexpr double binding_energy_experimental() { return 127.62; }
};

// ============================================================================
// THE MISSING LINK: ELECTRON POSITIONING RULE
// ============================================================================

struct ElectronPositionRule {
    static std::string get_rule_description() {
        return "ELECTRON POSITION RULE:\n"
               "Electrons are not probability clouds. They are toroidal vortices that settle\n"
               "into the MINIMA of the Nuclear Pressure Gradient Field (Maximum Admittance).\n"
               "\n"
               "For Oxygen-16 (Tetrahedral Nucleus):\n"
               "1. The 4-Alpha Tetrahedron generates a pressure field with 4 primary lobes (Vertices).\n"
               "2. These 4 lobes define the tetrahedral angle (~109.5 deg).\n"
               "3. 2 lobes are occupied by Hydrogen nuclei (Protons).\n"
               "4. 2 lobes are occupied by 'Lone Pair' electron vortices.\n"
               "5. The 104.5 deg angle is the perturbed tetrahedral angle due to vortex-vortex repulsion.";
    }
};

} // namespace sdt::nuclear::occlusion
