cmake_minimum_required(VERSION 4.0.0)

project(magvis)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

# add google test
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)


enable_testing()

find_package(OpenGL REQUIRED)

# set(SDL_SHARED OFF CACHE BOOL "" FORCE)
# set(SDL_STATIC ON  CACHE BOOL "" FORCE)
add_subdirectory(library/SDL3 EXCLUDE_FROM_ALL)
add_subdirectory(library/spdlog EXCLUDE_FROM_ALL)
add_subdirectory(library/glad)
add_subdirectory(src)
add_subdirectory(tests)