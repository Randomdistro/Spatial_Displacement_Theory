/**
 * @file test_navier_core.cpp
 * @brief Standalone tests for sdt_navier_cpp core modules.
 *        No external dependencies (replaces Catch2 tests).
 *
 * Tests: fields, nuclear, operators, solver
 */

#include "sdt_navier/fields.hpp"
#include "sdt_navier/nuclear.hpp"
#include "sdt_navier/equations.hpp"
#include "sdt_navier/operators.hpp"
#include "sdt_navier/solver.hpp"
#include "sdt_navier/constants.hpp"

#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <cassert>
#include <functional>

using namespace sdt_navier;

// ============================================================
// Minimal test harness
// ============================================================

static int total_tests = 0;
static int passed_tests = 0;
static int failed_tests = 0;

static void run_test(const char* name, std::function<bool()> test_fn) {
    total_tests++;
    try {
        if (test_fn()) {
            passed_tests++;
            std::cout << "  [PASS] " << name << "\n";
        } else {
            failed_tests++;
            std::cout << "  [FAIL] " << name << "\n";
        }
    } catch (const std::exception& e) {
        failed_tests++;
        std::cout << "  [FAIL] " << name << " EXCEPTION: " << e.what() << "\n";
    } catch (...) {
        failed_tests++;
        std::cout << "  [FAIL] " << name << " UNKNOWN EXCEPTION\n";
    }
}

// ============================================================
// FIELDS TESTS
// ============================================================

static void test_fields() {
    std::cout << "\n=== Fields ===\n";

    run_test("Field system initialization", []() {
        std::size_t nx = 10, ny = 10, nz = 10;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        if (fields.nx() != nx) return false;
        if (fields.ny() != ny) return false;
        if (fields.nz() != nz) return false;
        if (fields.size() != nx * ny * nz) return false;
        if (fields.dx() != dx) return false;
        return true;
    });

    run_test("Field eta bounds [0,1]", []() {
        std::size_t nx = 5, ny = 5, nz = 5;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        auto eta = fields.eta();
        for (Eigen::Index i = 0; i < static_cast<Eigen::Index>(fields.size()); ++i) {
            if (eta[i] < 0.0 || eta[i] > 1.0) return false;
        }
        return true;
    });

    run_test("Field pressure non-negative", []() {
        std::size_t nx = 5, ny = 5, nz = 5;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        auto P = fields.P();
        for (Eigen::Index i = 0; i < static_cast<Eigen::Index>(fields.size()); ++i) {
            if (P[i] < 0.0) return false;
        }
        return true;
    });

    run_test("Field Gamma non-negative", []() {
        std::size_t nx = 5, ny = 5, nz = 5;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        auto G = fields.Gamma();
        for (Eigen::Index i = 0; i < static_cast<Eigen::Index>(fields.size()); ++i) {
            if (G[i] < 0.0) return false;
        }
        return true;
    });

    run_test("Index round-trip", []() {
        std::size_t nx = 10, ny = 8, nz = 6;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        for (std::size_t i = 0; i < nx; ++i) {
            for (std::size_t j = 0; j < ny; ++j) {
                for (std::size_t k = 0; k < nz; ++k) {
                    auto idx = fields.index(i, j, k);
                    auto c = fields.coords(idx);
                    if (c[0] != i || c[1] != j || c[2] != k) return false;
                }
            }
        }
        return true;
    });
}

// ============================================================
// NUCLEAR TESTS
// ============================================================

static void test_nuclear() {
    std::cout << "\n=== Nuclear ===\n";

    run_test("Deuteron initialization", []() {
        std::size_t nx = 50, ny = 50, nz = 50;
        double dx = 0.2e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);
        std::array<std::size_t, 3> center = {nx/2, ny/2, nz/2};
        double separation_cells = 10.0;

        DeuteronSystem deuteron(fields, center, separation_cells);

        if (deuteron.proton().cell_type != "proton") return false;
        if (deuteron.neutron().cell_type != "neutron") return false;
        return true;
    });

    run_test("Deuteron binding energy in range [0, 10] MeV", []() {
        std::size_t nx = 50, ny = 50, nz = 50;
        double dx = 0.2e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);
        std::array<std::size_t, 3> center = {nx/2, ny/2, nz/2};
        double separation_cells = 10.0;

        DeuteronSystem deuteron(fields, center, separation_cells);

        double B_mev = deuteron.compute_binding_energy_mev();
        std::cout << "    Binding energy = " << B_mev << " MeV\n";
        if (B_mev <= 0.0) return false;
        if (B_mev >= 10.0) return false;
        return true;
    });
}

// ============================================================
// OPERATORS TESTS
// ============================================================

static void test_operators() {
    std::cout << "\n=== Operators ===\n";

    run_test("Gradient of linear field", []() {
        std::size_t nx = 10, ny = 10, nz = 10;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        // Linear field: f(x) = x * dx
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

        // Interior: df/dx ≈ 1, df/dy = df/dz = 0
        for (std::size_t i = 1; i < nx - 1; ++i) {
            for (std::size_t j = 0; j < ny; ++j) {
                for (std::size_t k = 0; k < nz; ++k) {
                    std::size_t idx = fields.index(i, j, k);
                    if (std::abs(grad[idx][0] - 1.0) > 1e-10) return false;
                    if (std::abs(grad[idx][1]) > 1e-10) return false;
                    if (std::abs(grad[idx][2]) > 1e-10) return false;
                }
            }
        }
        return true;
    });

    run_test("Divergence of constant field is zero", []() {
        std::size_t nx = 10, ny = 10, nz = 10;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);

        std::vector<FieldSystem::Vector3d> v_field(fields.size(), FieldSystem::Vector3d(1.0, 0.0, 0.0));
        auto div = compute_divergence(v_field, fields, "extrapolate");

        for (std::size_t i = 1; i < nx - 1; ++i) {
            for (std::size_t j = 1; j < ny - 1; ++j) {
                for (std::size_t k = 1; k < nz - 1; ++k) {
                    std::size_t idx = fields.index(i, j, k);
                    if (std::abs(div[idx]) > 1e-10) return false;
                }
            }
        }
        return true;
    });
}

// ============================================================
// SOLVER TESTS
// ============================================================

static void test_solver() {
    std::cout << "\n=== Solver ===\n";

    run_test("Solver initialization", []() {
        std::size_t nx = 10, ny = 10, nz = 10;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24);

        if (solver.dt() != 1.0e-24) return false;
        if (solver.t() != 0.0) return false;
        return true;
    });

    run_test("Single time step advances time", []() {
        std::size_t nx = 10, ny = 10, nz = 10;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24);

        double t0 = solver.t();
        solver.step();

        if (solver.t() <= t0) return false;
        return true;
    });

    run_test("Ten steps maintain numerical stability", []() {
        std::size_t nx = 10, ny = 10, nz = 10;
        double dx = 1.0e-15;
        FieldSystem fields(nx, ny, nz, dx, dx, dx);
        SDTNavierEquations equations;
        SDTNavierSolver solver(fields, equations, 1.0e-24);

        for (int i = 0; i < 10; ++i) {
            solver.step();
        }

        // Check eta stays finite
        auto eta = fields.eta();
        for (Eigen::Index i = 0; i < static_cast<Eigen::Index>(fields.size()); ++i) {
            if (std::isnan(eta[i]) || std::isinf(eta[i])) return false;
        }
        return true;
    });
}

// ============================================================
// MAIN
// ============================================================

int main() {
    std::cout << "======================================================================\n";
    std::cout << "SDT Navier Core Tests (standalone, no Catch2)\n";
    std::cout << "======================================================================\n";

    test_fields();
    test_nuclear();
    test_operators();
    test_solver();

    std::cout << "\n======================================================================\n";
    std::cout << "Total: " << total_tests << "  Passed: " << passed_tests
              << "  Failed: " << failed_tests << "\n";
    std::cout << "======================================================================\n";

    if (failed_tests == 0) {
        std::cout << "ALL TESTS PASSED\n\n";
    } else {
        std::cout << failed_tests << " TEST(S) FAILED\n\n";
    }

    return failed_tests > 0 ? 1 : 0;
}
