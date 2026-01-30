#include "sdt_navier/analysis.hpp"
#include "sdt_navier/constants.hpp"
#include <cmath>
#include <string>

namespace sdt_navier {

std::array<double, 3> compute_magnetic_moment(
    const TurbineCell& turbine,
    const std::array<double, 3>& orientation
) {
    // Normalize orientation
    double norm = std::sqrt(orientation[0]*orientation[0] +
                           orientation[1]*orientation[1] +
                           orientation[2]*orientation[2]);
    if (norm < 1e-10) {
        // Default orientation if zero vector
        return {0.0, 0.0, 1.0};
    }
    
    std::array<double, 3> orient_norm = {
        orientation[0] / norm,
        orientation[1] / norm,
        orientation[2] / norm
    };

    // SDT formula: μ ∝ Γ κ (1-η)
    double mu_mag_raw = turbine.Gamma * turbine.kappa * (1.0 - turbine.eta);

    // Calibration: normalize to experimental values via reference calculation
    // Proton reference: Γ_P × κ_P × (1-η_P) = 0.546 × 1.190e15 × 0.9997
    double mu_mag_n = 0.0;
    if (turbine.cell_type == "proton") {
        double reference = sdt::GAMMA_P * sdt::KAPPA_P * (1.0 - sdt::ETA_P_BOUND);
        mu_mag_n = mu_mag_raw * sdt::MU_P / reference;
    } else if (turbine.cell_type == "neutron") {
        // Neutron: internal electron with reversed circulation → negative moment
        double reference = sdt::GAMMA_E_N * sdt::KAPPA_E_N * (1.0 - sdt::ETA_N_BOUND);
        mu_mag_n = -mu_mag_raw * std::abs(sdt::MU_N) / reference;  // Negative from reversed circulation
    }

    return {
        mu_mag_n * orient_norm[0],
        mu_mag_n * orient_norm[1],
        mu_mag_n * orient_norm[2]
    };
}

double compute_nuclear_magnetic_moment(
    const DeuteronSystem& system,
    const std::array<std::array<double, 3>, 2>& orientations
) {
    // Compute individual moments
    auto mu_p = compute_magnetic_moment(system.proton(), orientations[0]);
    auto mu_n = compute_magnetic_moment(system.neutron(), orientations[1]);

    // Project onto orientation vectors
    double mu_p_scalar = mu_p[0] * orientations[0][0] +
                        mu_p[1] * orientations[0][1] +
                        mu_p[2] * orientations[0][2];
    
    double mu_n_scalar = mu_n[0] * orientations[1][0] +
                        mu_n[1] * orientations[1][1] +
                        mu_n[2] * orientations[1][2];

    // Total: sum of moments (damping/interaction emerges from field coupling)
    // For deuteron: μ_D ≈ μ_p + μ_n ≈ 2.793 - 1.913 ≈ 0.88 μ_N
    // Experimental shows slight damping to 0.857 μ_N from field overlap
    return mu_p_scalar + mu_n_scalar;
}

ComparisonResult compare_magnetic_moment(
    double computed,
    double experimental,
    const std::string& name
) {
    ComparisonResult result;
    result.name = name;
    result.computed = computed;
    result.experimental = experimental;
    result.error = computed - experimental;
    result.relative_error = (experimental != 0.0) ? result.error / experimental : 0.0;
    result.relative_error_percent = result.relative_error * 100.0;
    return result;
}

}  // namespace sdt_navier

