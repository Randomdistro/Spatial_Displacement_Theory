#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include "sdt_navier/fields.hpp"
#include "sdt_navier/constants.hpp"

TEST_CASE("Field system initialization", "[fields]") {
    std::size_t nx = 10, ny = 10, nz = 10;
    double dx = 1.0e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);

    REQUIRE(fields.nx() == nx);
    REQUIRE(fields.ny() == ny);
    REQUIRE(fields.nz() == nz);
    REQUIRE(fields.size() == nx * ny * nz);
    REQUIRE(fields.dx() == dx);
}

TEST_CASE("Field validation", "[fields]") {
    std::size_t nx = 5, ny = 5, nz = 5;
    double dx = 1.0e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);

    auto eta = fields.eta();
    for (std::size_t i = 0; i < fields.size(); ++i) {
        REQUIRE(eta[i] >= 0.0);
        REQUIRE(eta[i] <= 1.0);
    }
}

