add_library(Wire OBJECT Wire.cpp)

add_library(Vec3 OBJECT Vec3.cpp)

add_library(Biot-Savart STATIC Biot-Savart.cpp)
target_link_libraries(Biot-Savart Wire Vec3)

add_executable(MagVizGUI main.cpp)
target_link_libraries(MagVizGUI PRIVATE SDL3::SDL3 spdlog::spdlog OpenGL::GL glad)
#target_include_directories(MagVizGUI PRIVATE ${PROJECT_SOURCE_DIR}/library/glad/include)