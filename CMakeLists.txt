cmake_minimum_required(VERSION 3.5)
project(subsdk0 C CXX ASM)

set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_ASM_COMPILER clang)

set(ARCH_FLAGS "--target=armv7l-none-eabihf -mcpu=cortex-a57 -mfpu=crypto-neon-fp-armv8 -mfloat-abi=hard -fPIC")
set(CMAKE_C_FLAGS "${ARCH_FLAGS} -nostdlib")
set(CMAKE_CXX_FLAGS "${ARCH_FLAGS} -nostdlib -fno-rtti -fno-exceptions -fpermissive -fno-sized-deallocation")
set(CMAKE_ASM_FLAGS "${ARCH_FLAGS}")

file(GLOB_RECURSE SOURCES source/*.*)

include_directories(include ${CMAKE_CURRENT_BINARY_DIR})

add_executable(subsdk0.elf ${SOURCES})

set_target_properties(subsdk0.elf PROPERTIES
    LINK_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/linker.ld;${CMAKE_CURRENT_SOURCE_DIR}/main.ld;${CMAKE_CURRENT_SOURCE_DIR}/sdk.ld"
)

set(CMAKE_C_LINK_EXECUTABLE "arm-none-eabi-ld -pie -z noexecstack -T ${CMAKE_CURRENT_SOURCE_DIR}/linker.ld -T ${CMAKE_CURRENT_SOURCE_DIR}/main.ld -T ${CMAKE_CURRENT_SOURCE_DIR}/sdk.ld <OBJECTS> -o <TARGET>")
set(CMAKE_CXX_LINK_EXECUTABLE ${CMAKE_C_LINK_EXECUTABLE})

find_program(OBJDUMP NAMES llvm-objdump REQUIRED)

add_custom_command(
    OUTPUT subsdk0.sym
    DEPENDS subsdk0.elf
    COMMAND ${OBJDUMP} -t subsdk0.elf > subsdk0.sym
)

add_custom_target(syms ALL DEPENDS subsdk0.sym)
