add_library(Wire OBJECT Wire.cpp)

add_library(Vec3 OBJECT Vec3.cpp)

add_library(Biot-Savart STATIC Biot-Savart.cpp)
target_link_libraries(Biot-Savart Wire Vec3)