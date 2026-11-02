cmake_minimum_required(VERSION 3.5)
project(subsdk0 C CXX ASM)

set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_ASM_COMPILER clang)

include(cmake/stdlib.cmake)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(ARCH_FLAGS "--target=armv7l-none-eabihf -mcpu=cortex-a57 -mfpu=crypto-neon-fp-armv8 -mfloat-abi=hard -fPIC")
set(CMAKE_C_FLAGS "${ARCH_FLAGS} -nostdlib")
set(CMAKE_CXX_FLAGS "${ARCH_FLAGS} -std=c++17 -nostdlib -fno-rtti -fno-exceptions -fpermissive -fno-sized-deallocation -D_LIBCPP_HAS_NO_THREADS")
set(CMAKE_ASM_FLAGS "${ARCH_FLAGS}")

file(GLOB_RECURSE SOURCES src/*.*)

include_directories(include ${CMAKE_CURRENT_BINARY_DIR})

file(GLOB LIB_SUBDIRS lib/*)
foreach(SUBDIR ${LIB_SUBDIRS})
    if(IS_DIRECTORY "${SUBDIR}")
        if(EXISTS "${SUBDIR}/include")
            include_directories("${SUBDIR}/include")
        else()
            include_directories("${SUBDIR}")
        endif()
    endif()
endforeach()

add_executable(subsdk0.elf ${SOURCES})

target_include_directories(subsdk0.elf SYSTEM PRIVATE
    "$<$<COMPILE_LANGUAGE:C>:${STDLIB_INCLUDES}>"
    "$<$<COMPILE_LANGUAGE:CXX>:${STDLIB_INCLUDES}>"
)

set_target_properties(subsdk0.elf PROPERTIES
    LINK_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/linker/linker.ld;${CMAKE_CURRENT_SOURCE_DIR}/linker/main.ld;${CMAKE_CURRENT_SOURCE_DIR}/linker/sdk.ld"
)

set(CMAKE_C_LINK_EXECUTABLE "arm-none-eabi-ld -pie -z noexecstack -T ${CMAKE_CURRENT_SOURCE_DIR}/linker/linker.ld -T ${CMAKE_CURRENT_SOURCE_DIR}/linker/main.ld -T ${CMAKE_CURRENT_SOURCE_DIR}/linker/sdk.ld <OBJECTS> -o <TARGET>")
set(CMAKE_CXX_LINK_EXECUTABLE ${CMAKE_C_LINK_EXECUTABLE})

find_program(OBJDUMP NAMES llvm-objdump REQUIRED)

add_custom_command(
    OUTPUT subsdk0.sym
    DEPENDS subsdk0.elf
    COMMAND ${OBJDUMP} -t subsdk0.elf > subsdk0.sym
)

add_custom_target(syms ALL DEPENDS subsdk0.sym)
