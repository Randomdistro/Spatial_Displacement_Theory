cmake_minimum_required(VERSION 3.20)
project(SDTNavier VERSION 0.1.0 LANGUAGES CXX)

# C++20 standard required
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler-specific options
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        add_compile_options(-O3 -march=native)
    endif()
endif()

# Find dependencies
find_package(Eigen3 REQUIRED)
find_package(HDF5 REQUIRED COMPONENTS CXX)
find_package(pybind11 QUIET)
find_package(OpenMP QUIET)

# Optional dependencies
option(BUILD_PYTHON_BINDINGS "Build Python bindings" ON)
option(BUILD_TESTS "Build tests" ON)
option(BUILD_TOOLS "Build executable tools" ON)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${EIGEN3_INCLUDE_DIR}
    ${HDF5_INCLUDE_DIRS}
)

# Source files
set(SDT_NAVIER_SOURCES
    src/fields.cpp
    src/lattice.cpp
    src/operators.cpp
    src/equations.cpp
    src/solver.cpp
    src/nuclear.cpp
    src/analysis.cpp
    src/io.cpp
)

# Header files
set(SDT_NAVIER_HEADERS
    include/sdt_navier/fields.hpp
    include/sdt_navier/lattice.hpp
    include/sdt_navier/operators.hpp
    include/sdt_navier/equations.hpp
    include/sdt_navier/solver.hpp
    include/sdt_navier/nuclear.hpp
    include/sdt_navier/analysis.hpp
    include/sdt_navier/constants.hpp
    include/sdt_navier/io.hpp
    include/state_28d.hpp
)

# Create library
add_library(sdt_navier STATIC
    ${SDT_NAVIER_SOURCES}
    ${SDT_NAVIER_HEADERS}
)

target_link_libraries(sdt_navier
    PUBLIC
        Eigen3::Eigen
        ${HDF5_LIBRARIES}
)

if(OpenMP_CXX_FOUND)
    target_link_libraries(sdt_navier PUBLIC OpenMP::OpenMP_CXX)
    target_compile_options(sdt_navier PUBLIC ${OpenMP_CXX_FLAGS})
endif()

# Install library
install(TARGETS sdt_navier
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(FILES ${SDT_NAVIER_HEADERS}
    DESTINATION include/sdt_navier
)

# Build tools
if(BUILD_TOOLS)
    add_subdirectory(tools)
endif()

# Build tests
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Python bindings
if(BUILD_PYTHON_BINDINGS AND pybind11_FOUND)
    add_subdirectory(python)
endif()

