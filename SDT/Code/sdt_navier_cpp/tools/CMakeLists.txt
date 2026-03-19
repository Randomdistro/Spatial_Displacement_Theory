# SDT Calculator Tools - CMake Build Configuration

cmake_minimum_required(VERSION 3.20)

# World-class C++20 calculator tools
add_executable(stellar_calculator stellar_calculator.cpp)
add_executable(atomic_calculator atomic_calculator.cpp)
add_executable(galactic_rotation galactic_rotation.cpp)
add_executable(validate_lk2_relation validate_lk2_relation.cpp)
add_executable(benchmarks_b25_b50 benchmarks_b25_b50.cpp)
add_executable(benchmarks_b51_b60 benchmarks_b51_b60.cpp)
add_executable(benchmarks_b61_b70 benchmarks_b61_b70.cpp)
add_executable(benchmarks_b71_b80 benchmarks_b71_b80.cpp)
add_executable(benchmarks_b81_b100 benchmarks_b81_b100.cpp)
add_executable(zk2_systematic_40 zk2_systematic_40.cpp)
add_executable(isoelectronic_convergence isoelectronic_convergence.cpp)

# Set C++20 with std::format support
target_compile_features(stellar_calculator PRIVATE cxx_std_20)
target_compile_features(atomic_calculator PRIVATE cxx_std_20)
target_compile_features(galactic_rotation PRIVATE cxx_std_20)
target_compile_features(validate_lk2_relation PRIVATE cxx_std_20)
target_compile_features(benchmarks_b25_b50 PRIVATE cxx_std_20)
target_compile_features(benchmarks_b51_b60 PRIVATE cxx_std_20)
target_compile_features(benchmarks_b61_b70 PRIVATE cxx_std_20)
target_compile_features(benchmarks_b71_b80 PRIVATE cxx_std_20)
target_compile_features(benchmarks_b81_b100 PRIVATE cxx_std_20)
target_compile_features(zk2_systematic_40 PRIVATE cxx_std_20)
target_compile_features(isoelectronic_convergence PRIVATE cxx_std_20)

# Include header directories
target_include_directories(stellar_calculator PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(atomic_calculator PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(galactic_rotation PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(validate_lk2_relation PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(benchmarks_b25_b50 PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(benchmarks_b51_b60 PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(benchmarks_b61_b70 PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(benchmarks_b71_b80 PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(benchmarks_b81_b100 PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(zk2_systematic_40 PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(isoelectronic_convergence PRIVATE ${CMAKE_SOURCE_DIR}/include)

# Link core library (needed for FieldSystem + compute_p_infinity)
target_link_libraries(benchmarks_b25_b50 PRIVATE sdt_navier)

# Compiler-specific options — optimise only in Release/RelWithDebInfo
set(SDT_TOOL_TARGETS stellar_calculator atomic_calculator galactic_rotation validate_lk2_relation benchmarks_b25_b50 benchmarks_b51_b60 benchmarks_b61_b70 benchmarks_b71_b80 benchmarks_b81_b100 zk2_systematic_40 isoelectronic_convergence)

foreach(tgt IN LISTS SDT_TOOL_TARGETS)
    if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
        target_compile_options(${tgt} PRIVATE
            /W4
            $<$<CONFIG:Release,RelWithDebInfo>:/O2>
        )
    elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(${tgt} PRIVATE
            -Wall -Wextra
            $<$<CONFIG:Release,RelWithDebInfo>:-O3 -march=native>
        )
    endif()
endforeach()

# Install executables
install(TARGETS stellar_calculator atomic_calculator galactic_rotation validate_lk2_relation benchmarks_b25_b50 benchmarks_b51_b60 benchmarks_b61_b70 benchmarks_b71_b80 benchmarks_b81_b100 zk2_systematic_40 isoelectronic_convergence
    RUNTIME DESTINATION bin
)

# Create convenience launcher scripts
if(WIN32)
    file(WRITE "${CMAKE_BINARY_DIR}/run_stellar_calc.bat"
        "@echo off\n\"${CMAKE_BINARY_DIR}/tools/stellar_calculator.exe\" %*\n")
    file(WRITE "${CMAKE_BINARY_DIR}/run_atomic_calc.bat"
        "@echo off\n\"${CMAKE_BINARY_DIR}/tools/atomic_calculator.exe\" %*\n")
    file(WRITE "${CMAKE_BINARY_DIR}/run_galactic_rot.bat"
        "@echo off\n\"${CMAKE_BINARY_DIR}/tools/galactic_rotation.exe\" %*\n")
else()
    file(WRITE "${CMAKE_BINARY_DIR}/run_stellar_calc.sh"
        "#!/bin/bash\n\"${CMAKE_BINARY_DIR}/tools/stellar_calculator\" \"$@\"\n")
    file(WRITE "${CMAKE_BINARY_DIR}/run_atomic_calc.sh"
        "#!/bin/bash\n\"${CMAKE_BINARY_DIR}/tools/atomic_calculator\" \"$@\"\n")
    file(WRITE "${CMAKE_BINARY_DIR}/run_galactic_rot.sh"
        "#!/bin/bash\n\"${CMAKE_BINARY_DIR}/tools/galactic_rotation\" \"$@\"\n")
    file(CHMOD "${CMAKE_BINARY_DIR}/run_stellar_calc.sh" PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
    file(CHMOD "${CMAKE_BINARY_DIR}/run_atomic_calc.sh" PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
    file(CHMOD "${CMAKE_BINARY_DIR}/run_galactic_rot.sh" PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
endif()
