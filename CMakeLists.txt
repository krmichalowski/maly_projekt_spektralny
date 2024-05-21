cmake_minimum_required(VERSION 3.1)
project(fft_python)

add_library(
    FFTW_python SHARED
    biblioteka.c
)

target_link_libraries(FFTW_python fftw3)

#add_executable(test main.c)

#target_link_libraries(test FFTW_python)