#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>
#include "sdt_navier/fields.hpp"
#include "sdt_navier/equations.hpp"
#include "sdt_navier/solver.hpp"

TEST_CASE("Solver initialization", "[solver]") {
    std::size_t nx = 10, ny = 10, nz = 10;
    double dx = 1.0e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);
    SDTNavierEquations equations;
    SDTNavierSolver solver(fields, equations, 1.0e-24);

    REQUIRE(solver.dt() == 1.0e-24);
    REQUIRE(solver.t() == 0.0);
}

TEST_CASE("Single time step", "[solver]") {
    std::size_t nx = 10, ny = 10, nz = 10;
    double dx = 1.0e-15;

    FieldSystem fields(nx, ny, nz, dx, dx, dx);
    SDTNavierEquations equations;
    SDTNavierSolver solver(fields, equations, 1.0e-24);

    double t0 = solver.t();
    solver.step();

    REQUIRE(solver.t() > t0);
}

