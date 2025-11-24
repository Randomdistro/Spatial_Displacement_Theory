#pragma once

/**
 * @file lattice.hpp
 * @brief Dodecahedral lattice structure
 */

#include <array>
#include <vector>
#include <cstddef>

namespace sdt_navier {

/**
 * @brief 12-axis dodecahedral lattice
 * 
 * Each cell has 12 neighbors corresponding to the 12 faces of a dodecahedron.
 * Directions are defined by icosahedral vertices for uniform angular distribution.
 */
class DodecahedralLattice {
public:
    static constexpr std::size_t NUM_NEIGHBORS = 12;

    /**
     * @brief Construct lattice
     * @param nx, ny, nz Grid dimensions
     * @param dx, dy, dz Grid spacing
     */
    DodecahedralLattice(
        std::size_t nx, std::size_t ny, std::size_t nz,
        double dx, double dy, double dz
    );

    /**
     * @brief Get neighbor direction vectors (normalized)
     */
    const std::array<std::array<double, 3>, NUM_NEIGHBORS>& directions() const {
        return directions_;
    }

    /**
     * @brief Get neighbor indices for cell (i, j, k)
     * @return Vector of (i', j', k') tuples for valid neighbors
     */
    std::vector<std::array<std::size_t, 3>> get_neighbor_indices(
        std::size_t i, std::size_t j, std::size_t k
    ) const;

    std::size_t nx() const { return nx_; }
    std::size_t ny() const { return ny_; }
    std::size_t nz() const { return nz_; }

private:
    std::size_t nx_, ny_, nz_;
    double dx_, dy_, dz_;
    std::array<std::array<double, 3>, NUM_NEIGHBORS> directions_;
    std::array<std::array<int, 3>, NUM_NEIGHBORS> neighbor_offsets_;
};

}  // namespace sdt_navier

