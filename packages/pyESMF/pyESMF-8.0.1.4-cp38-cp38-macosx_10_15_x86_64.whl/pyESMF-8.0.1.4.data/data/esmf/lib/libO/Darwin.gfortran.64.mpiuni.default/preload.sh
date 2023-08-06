#!/bin/sh
# Script to preload ESMF dynamic trace library
env LD_PRELOAD="$LD_PRELOAD /Users/runner/.conan/data/esmf/8.0.1/CHM/stable/package/ccfcfe63664926af39fa1a9f97d2f0dcf252dbf6/lib/libO/Darwin.gfortran.64.mpiuni.default/libesmftrace_preload.dylib" $*
