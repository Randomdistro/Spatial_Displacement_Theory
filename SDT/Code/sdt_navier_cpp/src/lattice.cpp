#include "sdt_navier/lattice.hpp"
#include <cmath>
#include <algorithm>

namespace sdt_navier {

// Icosahedral vertex directions (normalized)
static constexpr std::array<std::array<double, 3>, 12> ICOSAHEDRAL_DIRECTIONS = {{
    {0.0, 0.525731, 0.850651},
    {0.0, -0.525731, 0.850651},
    {0.0, 0.525731, -0.850651},
    {0.0, -0.525731, -0.850651},
    {0.850651, 0.0, 0.525731},
    {-0.850651, 0.0, 0.525731},
    {0.850651, 0.0, -0.525731},
    {-0.850651, 0.0, -0.525731},
    {0.525731, 0.850651, 0.0},
    {-0.525731, 0.850651, 0.0},
    {0.525731, -0.850651, 0.0},
    {-0.525731, -0.850651, 0.0}
}};

DodecahedralLattice::DodecahedralLattice(
    std::size_t nx, std::size_t ny, std::size_t nz,
    double dx, double dy, double dz
) : nx_(nx), ny_(ny), nz_(nz), dx_(dx), dy_(dy), dz_(dz)
{
    // Copy and normalize directions
    for (std::size_t i = 0; i < NUM_NEIGHBORS; ++i) {
        double norm = std::sqrt(
            ICOSAHEDRAL_DIRECTIONS[i][0] * ICOSAHEDRAL_DIRECTIONS[i][0] +
            ICOSAHEDRAL_DIRECTIONS[i][1] * ICOSAHEDRAL_DIRECTIONS[i][1] +
            ICOSAHEDRAL_DIRECTIONS[i][2] * ICOSAHEDRAL_DIRECTIONS[i][2]
        );
        directions_[i][0] = ICOSAHEDRAL_DIRECTIONS[i][0] / norm;
        directions_[i][1] = ICOSAHEDRAL_DIRECTIONS[i][1] / norm;
        directions_[i][2] = ICOSAHEDRAL_DIRECTIONS[i][2] / norm;

        // Convert to grid offsets (rounded to nearest integer)
        neighbor_offsets_[i][0] = static_cast<int>(std::round(directions_[i][0] * dx / dx));
        neighbor_offsets_[i][1] = static_cast<int>(std::round(directions_[i][1] * dy / dy));
        neighbor_offsets_[i][2] = static_cast<int>(std::round(directions_[i][2] * dz / dz));
    }
}

std::vector<std::array<std::size_t, 3>> DodecahedralLattice::get_neighbor_indices(
    std::size_t i, std::size_t j, std::size_t k
) const {
    std::vector<std::array<std::size_t, 3>> neighbors;

    for (const auto& offset : neighbor_offsets_) {
        std::size_t ni = i + offset[0];
        std::size_t nj = j + offset[1];
        std::size_t nk = k + offset[2];

        // Check bounds
        if (ni < nx_ && nj < ny_ && nk < nz_) {
            neighbors.push_back({ni, nj, nk});
        }
    }

    return neighbors;
}

}  // namespace sdt_navier

