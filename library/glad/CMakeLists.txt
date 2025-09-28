add_library(glad OBJECT src/gl.c)
target_include_directories(glad PUBLIC ${PROJECT_SOURCE_DIR}/library/glad/include/)