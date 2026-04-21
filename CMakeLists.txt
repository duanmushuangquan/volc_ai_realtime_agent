cmake_minimum_required(VERSION 3.20)
project(volc_ai_realtime_agent VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Add source directory
include_directories(src/cpp/include)

# Main executable
add_executable(hello_world 
    src/cpp/main.cpp
    src/cpp/src/hello.cpp
)

# Unit tests (placeholder)
enable_testing()
add_test(NAME hello_world COMMAND hello_world)

# Print configuration
message(STATUS "=== Build Configuration ===")
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "===========================")
