#pragma once

/**
 * @file analysis.hpp
 * @brief Analysis tools for binding energy and magnetic moments
 */

#include "sdt_navier/fields.hpp"
#include "sdt_navier/nuclear.hpp"
#include <array>

namespace sdt_navier {

/**
 * @brief Compute magnetic moment for a turbine cell
 * @param turbine Turbine cell
 * @param orientation Orientation vector (unit vector)
 * @return Magnetic moment vector (in units of μ_N)
 */
std::array<double, 3> compute_magnetic_moment(
    const TurbineCell& turbine,
    const std::array<double, 3>& orientation = {1.0, 0.0, 0.0}
);

/**
 * @brief Compute total magnetic moment for deuteron
 * @param system Deuteron system
 * @param orientations Orientation vectors for each turbine
 * @return Total magnetic moment (in units of μ_N)
 */
double compute_nuclear_magnetic_moment(
    const DeuteronSystem& system,
    const std::array<std::array<double, 3>, 2>& orientations = {{{1.0, 0.0, 0.0}, {1.0, 0.0, 0.0}}}
);

/**
 * @brief Compare computed vs experimental value
 */
struct ComparisonResult {
    std::string name;
    double computed;
    double experimental;
    double error;
    double relative_error;
    double relative_error_percent;
};

ComparisonResult compare_magnetic_moment(
    double computed,
    double experimental,
    const std::string& name = "nucleus"
);

}  // namespace sdt_navier

