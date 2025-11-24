#pragma once

#include <Eigen/Dense>
#include <complex>
#include <vector>
#include <string>

namespace sdt {

    // Vector types
    using Vec3d = Eigen::Vector3d;
    using Vec3f = Eigen::Vector3f;
    using Mat3d = Eigen::Matrix3d;
    
    // Scalar types
    using scalar_t = double;
    using index_t = std::size_t;
    
    // Compatibility: Vector3D (array-based)
    using Vector3D = std::array<double, 3>;

} // namespace sdt

