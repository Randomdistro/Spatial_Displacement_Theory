#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "sdt_navier/fields.hpp"
#include "sdt_navier/equations.hpp"
#include "sdt_navier/solver.hpp"
#include "sdt_navier/nuclear.hpp"
#include "sdt_navier/analysis.hpp"
#include "sdt_navier/constants.hpp"

namespace py = pybind11;
using namespace sdt_navier;

PYBIND11_MODULE(sdt_navier_cpp, m) {
    m.doc() = "SDT-Navier C++ bindings";

    // Constants
    py::module_ constants = m.def_submodule("constants", "Physical constants");
    constants.attr("C") = constants::C;
    constants.attr("NUCLEAR_MAGNETON") = constants::NUCLEAR_MAGNETON;
    constants.attr("B_DEUTERON") = sdt::B_DEUTERON;
    constants.attr("MU_D") = sdt::MU_D;

    // FieldSystem
    py::class_<FieldSystem>(m, "FieldSystem")
        .def(py::init<std::size_t, std::size_t, std::size_t, double, double, double, double>(),
             py::arg("nx"), py::arg("ny"), py::arg("nz"),
             py::arg("dx"), py::arg("dy"), py::arg("dz"),
             py::arg("P_infinity") = sdt::P_INFINITY_NUCLEAR)
        .def("nx", &FieldSystem::nx)
        .def("ny", &FieldSystem::ny)
        .def("nz", &FieldSystem::nz)
        .def("size", &FieldSystem::size)
        .def("dx", &FieldSystem::dx)
        .def("dy", &FieldSystem::dy)
        .def("dz", &FieldSystem::dz)
        .def("t", &FieldSystem::t)
        .def("set_t", &FieldSystem::set_t)
        .def("dt", &FieldSystem::dt)
        .def("set_dt", &FieldSystem::set_dt);

    // SDTNavierEquations
    py::class_<SDTNavierEquations>(m, "SDTNavierEquations")
        .def(py::init<>());

    // SDTNavierSolver
    py::class_<SDTNavierSolver>(m, "SDTNavierSolver")
        .def(py::init<FieldSystem&, const SDTNavierEquations&, double, double, std::string, bool>(),
             py::arg("fields"), py::arg("equations"),
             py::arg("dt") = 0.0, py::arg("cfl") = 0.5,
             py::arg("method") = "rk4", py::arg("enforce_incompressibility") = true)
        .def("step", &SDTNavierSolver::step)
        .def("run_until", &SDTNavierSolver::run_until)
        .def("get_divergence_error", &SDTNavierSolver::get_divergence_error)
        .def("fields", &SDTNavierSolver::fields, py::return_value_policy::reference)
        .def("t", &SDTNavierSolver::t)
        .def("dt", &SDTNavierSolver::dt);

    // DeuteronSystem
    py::class_<DeuteronSystem>(m, "DeuteronSystem")
        .def(py::init<FieldSystem&, const std::array<std::size_t, 3>&, double>(),
             py::arg("fields"), py::arg("center"), py::arg("separation_cells"))
        .def("compute_binding_energy", &DeuteronSystem::compute_binding_energy)
        .def("compute_binding_energy_mev", &DeuteronSystem::compute_binding_energy_mev);

    // Analysis functions
    m.def("compute_nuclear_magnetic_moment", &compute_nuclear_magnetic_moment,
          "Compute nuclear magnetic moment");
    m.def("compare_magnetic_moment", &compare_magnetic_moment,
          "Compare computed vs experimental magnetic moment");
}

