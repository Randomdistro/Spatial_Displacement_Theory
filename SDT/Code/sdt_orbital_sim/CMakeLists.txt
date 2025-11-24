cmake_minimum_required(VERSION 3.20)
project(SDT_Orbital_Sim CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags for optimization and warnings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -O3 -march=native")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0 -fsanitize=address")

# Find dependencies
find_package(Eigen3 REQUIRED)
find_package(fmt REQUIRED)
find_package(VTK REQUIRED COMPONENTS 
    CommonCore
    CommonDataModel
    FiltersCore
    InteractionStyle
    RenderingCore
    RenderingOpenGL2
    ViewsCore
)

include(${VTK_USE_FILE})

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
add_library(sdt_orbital STATIC ${SOURCES} ${HEADERS})

target_link_libraries(sdt_orbital
    Eigen3::Eigen
    fmt::fmt
    ${VTK_LIBRARIES}
)

target_include_directories(sdt_orbital PUBLIC
    ${VTK_INCLUDE_DIRS}
)

# Create simulation executable
add_executable(sdt_sim
    ${CMAKE_SOURCE_DIR}/main.cpp
)

target_link_libraries(sdt_sim
    sdt_orbital
)

# Create visualization executable
add_executable(sdt_viewer
    ${CMAKE_SOURCE_DIR}/src/visualization/main_viewer.cpp
)

target_link_libraries(sdt_viewer
    sdt_orbital
)

# Installation
install(TARGETS sdt_sim DESTINATION bin)
install(TARGETS sdt_orbital DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)

