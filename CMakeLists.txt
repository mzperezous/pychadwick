cmake_minimum_required(VERSION 3.15...3.30)
project(libchadwick C)
set(CMAKE_VERBOSE_MAKEFILE on)

add_definitions(-DVERSION=\"0.7.0\")

file(GLOB CWLIB_SOURCES "src/pychadwicklib/cwlib/*.c")
include_directories(src/pychadwicklib)

set(CWEVENT_SOURCES src/pychadwicklib/cwtools/cwevent.c src/pychadwicklib/cwtools/cwtools.c ${CWLIB_SOURCES})
add_library(cwevent SHARED ${CWEVENT_SOURCES})

# DESTINATION must match the package-relative path cwlib.py loads via ctypes:
# pychadwick/lib/cwevent/libcwevent.{dylib,so,dll}
install(TARGETS cwevent
        LIBRARY DESTINATION pychadwick/lib/cwevent
        RUNTIME DESTINATION pychadwick/lib/cwevent)
