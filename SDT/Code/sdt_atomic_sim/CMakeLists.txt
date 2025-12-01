cmake_minimum_required(VERSION 3.20)


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
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
    CommonColor
)

include(${VTK_USE_FILE})

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/../shared/include)
include_directories(${CMAKE_SOURCE_DIR}/../sdt_orbital_sim/include)
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
add_library(sdt_atomic STATIC ${SOURCES} ${HEADERS})

target_link_libraries(sdt_atomic
    Eigen3::Eigen
    fmt::fmt
    ${VTK_LIBRARIES}
)

target_include_directories(sdt_atomic PUBLIC
    ${VTK_INCLUDE_DIRS}
)

# Create main executable
add_executable(sdt_atomic_sim
    ${CMAKE_SOURCE_DIR}/main.cpp
)

target_link_libraries(sdt_atomic_sim
    sdt_atomic
)

# Create visualization executable
add_executable(sdt_atomic_viewer
    ${CMAKE_SOURCE_DIR}/tools/atomic_viewer.cpp
)

target_link_libraries(sdt_atomic_viewer
    sdt_atomic
)

# Installation
install(TARGETS sdt_atomic_sim sdt_atomic_viewer DESTINATION bin)
install(TARGETS sdt_atomic DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)

