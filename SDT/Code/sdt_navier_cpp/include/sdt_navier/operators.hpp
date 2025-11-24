#pragma once

/**
 * @file operators.hpp
 * @brief Discrete differential operators
 */

#include "sdt_navier/fields.hpp"
#include <vector>
#include <string>

namespace sdt_navier {

/**
 * @brief Compute gradient of scalar field
 * @param field Scalar field (size = nx*ny*nz)
 * @param fields Field system (for grid parameters)
 * @param boundary Boundary condition: "zero", "periodic", or "extrapolate"
 * @return Gradient field (size = nx*ny*nz, 3 components per point)
 */
std::vector<std::array<double, 3>> compute_gradient(
    const std::vector<double>& field,
    const FieldSystem& fields,
    const std::string& boundary = "zero"
);

/**
 * @brief Compute divergence of vector field
 * @param v Vector field (size = nx*ny*nz, 3 components per point)
 * @param fields Field system
 * @param boundary Boundary condition
 * @return Divergence field (size = nx*ny*nz)
 */
std::vector<double> compute_divergence(
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& boundary = "zero"
);

/**
 * @brief Compute velocity gradient tensor
 * @param v Velocity field
 * @param fields Field system
 * @param boundary Boundary condition
 * @return Gradient tensor (size = nx*ny*nz, 3x3 tensor per point)
 */
std::vector<std::array<std::array<double, 3>, 3>> compute_velocity_gradient(
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& boundary = "zero"
);

/**
 * @brief Compute advection term (v·∇)field
 * @param field Scalar field to advect
 * @param v Velocity field
 * @param fields Field system
 * @param method "upwind" or "central"
 * @return Advection field (size = nx*ny*nz)
 */
std::vector<double> compute_advection(
    const std::vector<double>& field,
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& method = "upwind"
);

}  // namespace sdt_navier

