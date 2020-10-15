project(PackageTest CXX)
cmake_minimum_required(VERSION 3.1.2)

set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(ortools CONFIG REQUIRED)
find_package(OpenMP)

add_executable(test_or_tools test_or_tools.cpp)
target_link_libraries(test_or_tools ortools::ortools)

if(OpenMP_CXX_FOUND)
    target_link_libraries(test_or_tools
        OpenMP::OpenMP_CXX)
endif()

# CTest is a testing tool that can be used to test your project.
enable_testing()
add_test(NAME test_or_tools
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/Release
         COMMAND test_or_tools)
