#pragma once

/**
 * @file solver.hpp
 * @brief SDT-Navier time-stepping solver
 */

#include "sdt_navier/fields.hpp"
#include "sdt_navier/equations.hpp"
#include "sdt_navier/operators.hpp"
#include <functional>
#include <string>

namespace sdt_navier {

/**
 * @brief SDT-Navier solver with time-stepping and incompressibility enforcement
 */
class SDTNavierSolver {
public:
    /**
     * @brief Construct solver
     * @param fields Field system
     * @param equations SDT-Navier equations
     * @param dt Timestep (if 0, use adaptive)
     * @param cfl CFL number for adaptive timestep
     * @param method Time-stepping method: "euler" or "rk4"
     * @param enforce_incompressibility Whether to enforce ∇·v = 0
     */
    SDTNavierSolver(
        FieldSystem& fields,
        const SDTNavierEquations& equations,
        double dt = 0.0,
        double cfl = 0.5,
        const std::string& method = "rk4",
        bool enforce_incompressibility = true
    );

    /**
     * @brief Perform one time step
     */
    void step();

    /**
     * @brief Run until t_end
     * @param t_end End time
     * @param callback Optional callback function called after each step
     */
    void run_until(
        double t_end,
        std::function<void(SDTNavierSolver&)> callback = nullptr
    );

    /**
     * @brief Get maximum divergence error
     */
    double get_divergence_error() const;

    FieldSystem& fields() { return fields_; }
    const FieldSystem& fields() const { return fields_; }
    double dt() const { return dt_; }
    double t() const { return t_; }

private:
    void step_euler();
    void step_rk4();
    void project_pressure();
    double estimate_timestep() const;

    FieldSystem& fields_;
    const SDTNavierEquations& equations_;
    double dt_;
    double cfl_;
    std::string method_;
    bool enforce_incompressibility_;
    double t_;
};

}  // namespace sdt_navier

