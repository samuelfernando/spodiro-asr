# Copyright: (C) 2010 RobotCub Consortium
# Author: Paul Fitzpatrick
# CopyPolicy: Released under the terms of the LGPLv2.1 or later, see LGPL.TXT
# YARP needs CMake 2.8.9 or greater
cmake_minimum_required(VERSION 2.8.9)
# find YARP
find_package(YARP REQUIRED)
find_package (Threads)
# add YARP include directories
include_directories(${YARP_INCLUDE_DIRS})
# set up our program
add_executable(input input.cpp)
add_executable(act_input act_input.cpp)
add_executable(yarp_close yarp_close.cpp)
add_executable(easel easel.cpp)
add_executable(com_slave com_slave.cpp)
add_executable(com_master com_master.cpp)
add_executable(asr_master asr_master.cpp)
add_executable(new_asr_master new_asr_master.cpp)
add_executable(static_master static_master.cpp)
add_executable(asr_slave asr_slave.cpp)
add_executable(fork fork.cpp)

# link with YARP libraries
target_link_libraries(input ${YARP_LIBRARIES})
target_link_libraries(act_input ${YARP_LIBRARIES})
target_link_libraries(yarp_close ${YARP_LIBRARIES})
target_link_libraries(easel ${YARP_LIBRARIES})
target_link_libraries(asr_master ${YARP_LIBRARIES})
target_link_libraries (asr_master ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries (asr_slave ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(yarp_close ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(new_asr_master ${YARP_LIBRARIES})
target_link_libraries (new_asr_master ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(static_master ${YARP_LIBRARIES})
target_link_libraries (static_master ${CMAKE_THREAD_LIBS_INIT})
