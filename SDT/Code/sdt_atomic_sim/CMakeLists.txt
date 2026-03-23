cmake_minimum_required(VERSION 3.20)
project(sdt_atomic_sim LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
if(MSVC)
    add_compile_options(/W4 /O2)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -O3)
endif()

# =============================================================================
# SDT Atomic Simulator — Pressure-Node Vortex Model
# Self-contained: no external dependencies (no Eigen, no fmt, no VTK)
# =============================================================================

# Main executable — self-contained, all SDT code in main.cpp
add_executable(sdt_atomic_sim main.cpp)

# Installation
install(TARGETS sdt_atomic_sim DESTINATION bin)
