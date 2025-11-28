cmake_minimum_required(VERSION 3.20)

enable_testing()

# Unit tests
add_executable(test_basic
    unit_tests/test_basic.cpp
)

target_link_libraries(test_basic
    sdt_solar_system
)

add_test(NAME BasicTests COMMAND test_basic)


