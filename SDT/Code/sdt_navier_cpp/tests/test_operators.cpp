#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include "sdt_navier/fields.hpp"
#include "sdt_navier/operators.hpp"
#include <vector>
#include <cmath>

TEST_CASE("Gradient of linear field", "[operators]") {
    std::size_t nx = 10, ny = 10, nz = 10;
    double dx = 1.0e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);

    // Linear field: f(x) = x
    std::vector<double> field(fields.size());
    for (std::size_t i = 0; i < nx; ++i) {
        for (std::size_t j = 0; j < ny; ++j) {
            for (std::size_t k = 0; k < nz; ++k) {
                std::size_t idx = fields.index(i, j, k);
                field[idx] = static_cast<double>(i) * dx;
            }
        }
    }

    auto grad = compute_gradient(field, fields, "extrapolate");

    // Check interior points
    for (std::size_t i = 1; i < nx - 1; ++i) {
        for (std::size_t j = 0; j < ny; ++j) {
            for (std::size_t k = 0; k < nz; ++k) {
                std::size_t idx = fields.index(i, j, k);
                REQUIRE(std::abs(grad[idx][0] - 1.0) < 1e-10);
                REQUIRE(std::abs(grad[idx][1]) < 1e-10);
                REQUIRE(std::abs(grad[idx][2]) < 1e-10);
            }
        }
    }
}

