#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include "sdt_navier/fields.hpp"
#include "sdt_navier/nuclear.hpp"
#include "sdt_navier/constants.hpp"

TEST_CASE("Deuteron initialization", "[nuclear]") {
    std::size_t nx = 50, ny = 50, nz = 50;
    double dx = 0.2e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);
    std::array<std::size_t, 3> center = {nx/2, ny/2, nz/2};
    double separation_cells = 10.0;

    DeuteronSystem deuteron(fields, center, separation_cells);

    REQUIRE(deuteron.proton().cell_type == "proton");
    REQUIRE(deuteron.neutron().cell_type == "neutron");
}

TEST_CASE("Binding energy calculation", "[nuclear]") {
    std::size_t nx = 50, ny = 50, nz = 50;
    double dx = 0.2e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);
    std::array<std::size_t, 3> center = {nx/2, ny/2, nz/2};
    double separation_cells = 10.0;

    DeuteronSystem deuteron(fields, center, separation_cells);

    double B_mev = deuteron.compute_binding_energy_mev();
    REQUIRE(B_mev > 0.0);
    REQUIRE(B_mev < 10.0);  // Should be in reasonable range
}

