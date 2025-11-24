#pragma once

/**
 * @file io.hpp
 * @brief I/O utilities for field snapshots and results
 */

#include "sdt_navier/fields.hpp"
#include "sdt_navier/analysis.hpp"
#include <string>
#include <vector>

namespace sdt_navier {

/**
 * @brief Save field snapshot to CSV
 */
void save_fields_csv(
    const FieldSystem& fields,
    const std::string& filename
);

/**
 * @brief Save time series data to CSV
 */
void save_timeseries_csv(
    const std::vector<double>& times,
    const std::vector<double>& values,
    const std::string& filename,
    const std::string& header = "time,value"
);

/**
 * @brief Save results to JSON
 */
void save_results_json(
    const std::string& filename,
    double binding_energy_mev,
    double magnetic_moment,
    double experimental_binding_energy = sdt::B_DEUTERON,
    double experimental_magnetic_moment = sdt::MU_D
);

}  // namespace sdt_navier

