cmake_minimum_required(VERSION 3.20)
project(Vulkan_Solar_System VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4 /O2")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /Zi /Od")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -O3")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0")
endif()

# Find Vulkan
find_package(Vulkan REQUIRED)
if(NOT Vulkan_FOUND)
    message(FATAL_ERROR "Vulkan SDK not found. Please install Vulkan SDK 1.3+")
endif()

# Find GLFW
find_package(glfw3 REQUIRED)
if(NOT glfw3_FOUND)
    message(FATAL_ERROR "GLFW not found. Please install GLFW 3.3+")
endif()

# GLM (header-only, assume it's in a subdirectory or system path)
find_path(GLM_INCLUDE_DIR glm/glm.hpp
    PATHS
        ${CMAKE_SOURCE_DIR}/third_party/glm
        ${CMAKE_SOURCE_DIR}/../third_party/glm
        /usr/include
        /usr/local/include
        C:/VulkanSDK/*/Include/glm
)

if(NOT GLM_INCLUDE_DIR)
    message(WARNING "GLM not found in standard locations. Assuming it's available via system paths.")
    set(GLM_INCLUDE_DIR "")
endif()

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/src)
if(GLM_INCLUDE_DIR)
    include_directories(${GLM_INCLUDE_DIR})
endif()

# Source files
file(GLOB_RECURSE SOURCES
    "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

# Header files (for IDE support)
file(GLOB_RECURSE HEADERS
    "${CMAKE_SOURCE_DIR}/include/*.hpp"
    "${CMAKE_SOURCE_DIR}/src/*.hpp"
)

# Create executable
add_executable(vulkan_solar_system ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(vulkan_solar_system
    Vulkan::Vulkan
    glfw
)

# Include Vulkan headers
target_include_directories(vulkan_solar_system PRIVATE
    ${Vulkan_INCLUDE_DIRS}
)

# Copy shaders to build directory
file(GLOB SHADER_FILES "${CMAKE_SOURCE_DIR}/shaders/*")
foreach(SHADER ${SHADER_FILES})
    get_filename_component(SHADER_NAME ${SHADER} NAME)
    configure_file(${SHADER} ${CMAKE_BINARY_DIR}/shaders/${SHADER_NAME} COPYONLY)
endforeach()

# Set output directory
set_target_properties(vulkan_solar_system PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

