cmake_minimum_required(VERSION 3.20)
project(SDT_Chemistry_Simulator CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Compiler flags for optimization and warnings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -O3 -march=native")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0 -fsanitize=address")

# Find dependencies
find_package(Eigen3 REQUIRED)
find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)
find_package(nlohmann_json REQUIRED)

# OpenMP for parallelization
find_package(OpenMP REQUIRED)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${EIGEN3_INCLUDE_DIR})

# Source files
file(GLOB_RECURSE SOURCES
    "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

# Header files
file(GLOB_RECURSE HEADERS
    "${CMAKE_SOURCE_DIR}/include/*.hpp"
)

# Create library
add_library(sdt_chemistry STATIC ${SOURCES} ${HEADERS})

target_link_libraries(sdt_chemistry
    Eigen3::Eigen
    fmt::fmt
    spdlog::spdlog
    nlohmann_json::nlohmann_json
    OpenMP::OpenMP_CXX
)

# Create compound designer executable
add_executable(compound_designer
    ${CMAKE_SOURCE_DIR}/tools/compound_designer.cpp
)

target_link_libraries(compound_designer
    sdt_chemistry
)

# Create batch processor executable
add_executable(batch_processor
    ${CMAKE_SOURCE_DIR}/tools/batch_processor.cpp
)

target_link_libraries(batch_processor
    sdt_chemistry
)

# Create molecule viewer executable
add_executable(molecule_viewer
    ${CMAKE_SOURCE_DIR}/tools/molecule_viewer.cpp
)

target_link_libraries(molecule_viewer
    sdt_chemistry
)

# Tests
enable_testing()
add_executable(test_basic
    ${CMAKE_SOURCE_DIR}/tests/unit_tests/test_basic.cpp
)
target_link_libraries(test_basic
    sdt_chemistry
)
add_test(NAME BasicTests COMMAND test_basic)

# Installation
install(TARGETS compound_designer batch_processor molecule_viewer test_basic DESTINATION bin)
install(TARGETS sdt_chemistry DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)

