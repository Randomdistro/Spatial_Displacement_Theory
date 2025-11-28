cmake_minimum_required(VERSION 3.20)
project(SDT_Solar_System CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -O3 -march=native")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0")

# Find dependencies
find_package(Eigen3 REQUIRED)
find_package(fmt REQUIRED)

# Optional: OpenMP for parallelization
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

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
add_library(sdt_solar_system STATIC ${SOURCES} ${HEADERS})

target_link_libraries(sdt_solar_system
    Eigen3::Eigen
    fmt::fmt
)

if(OpenMP_CXX_FOUND)
    target_link_libraries(sdt_solar_system OpenMP::OpenMP_CXX)
endif()

# Main simulator executable
add_executable(solar_system_sim
    tools/solar_system_sim.cpp
)
target_link_libraries(solar_system_sim sdt_solar_system)

# Trajectory viewer executable
add_executable(trajectory_viewer
    tools/trajectory_viewer.cpp
)
target_link_libraries(trajectory_viewer sdt_solar_system)

# Analysis tool executable
add_executable(analysis_tool
    tools/analysis_tool.cpp
)
target_link_libraries(analysis_tool sdt_solar_system)

# Tests
enable_testing()
add_subdirectory(tests)


