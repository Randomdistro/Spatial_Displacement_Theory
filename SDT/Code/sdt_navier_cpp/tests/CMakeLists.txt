find_package(Catch2 QUIET)

if(Catch2_FOUND)
    add_executable(test_fields test_fields.cpp)
    target_link_libraries(test_fields PRIVATE sdt_navier Catch2::Catch2)
    add_test(NAME test_fields COMMAND test_fields)

    add_executable(test_operators test_operators.cpp)
    target_link_libraries(test_operators PRIVATE sdt_navier Catch2::Catch2)
    add_test(NAME test_operators COMMAND test_operators)

    add_executable(test_solver test_solver.cpp)
    target_link_libraries(test_solver PRIVATE sdt_navier Catch2::Catch2)
    add_test(NAME test_solver COMMAND test_solver)

    add_executable(test_nuclear test_nuclear.cpp)
    target_link_libraries(test_nuclear PRIVATE sdt_navier Catch2::Catch2)
    add_test(NAME test_nuclear COMMAND test_nuclear)
else()
    message(WARNING "Catch2 not found, tests will not be built")
endif()

