pybind11_add_module(sdt_navier_cpp bindings.cpp)
target_link_libraries(sdt_navier_cpp PRIVATE sdt_navier pybind11::module)

