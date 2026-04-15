cmake_minimum_required(VERSION 3.13)
project(RobotRTCClient VERSION 1.0.0 LANGUAGES CXX)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置编译选项
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")

# 包含目录
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# 源文件
set(SOURCES
    src/RobotRTCClient.cpp
    src/main.cpp
)

# 创建可执行文件
add_executable(robot_rtc_client ${SOURCES})

# 链接库（实际应链接火山引擎RTC SDK）
# target_link_libraries(robot_rtc_client ${RTC_SDK_LIBRARIES})

# 安装
install(TARGETS robot_rtc_client DESTINATION bin)

# 打印配置信息
message(STATUS "==========================================")
message(STATUS "Robot RTC Client Configuration")
message(STATUS "==========================================")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "==========================================")
