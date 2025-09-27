include(GoogleTest)

include_directories(../src)


# Wire --------------------------------------------------------
add_executable(
    Wire_test
    Wire_test.cpp
)
target_link_libraries(
    Wire_test
    Wire
    GTest::gtest_main
)
gtest_discover_tests(Wire_test)

# Vec3 --------------------------------------------------------
add_executable(
    Vec3_test
    Vec3_test.cpp
)
target_link_libraries(
    Vec3_test
    GTest::gtest_main
)
gtest_discover_tests(Vec3_test)

# Biot-Savart -------------------------------------------------
add_executable(
    Biot-Savart_test
    Biot-Savart_test.cpp
)
target_link_libraries(
    Biot-Savart_test
    Biot-Savart
    GTest::gtest_main
)
gtest_discover_tests(Biot-Savart_test)