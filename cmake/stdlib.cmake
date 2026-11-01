set(LIBSTD_PATH "${CMAKE_CURRENT_SOURCE_DIR}/lib/std")

set(STDLIB_INCLUDES
    "${LIBSTD_PATH}/llvm-project/build/include/c++/v1"
    "${LIBSTD_PATH}/llvm-project/libunwind/include"
    "${LIBSTD_PATH}/musl/include"
    "${LIBSTD_PATH}/musl/obj/include"
    "${LIBSTD_PATH}/musl/arch/generic"
    "${LIBSTD_PATH}/musl/arch/arm"
)

foreach(INCLUDE_DIR ${STDLIB_INCLUDES})
    if(NOT EXISTS "${INCLUDE_DIR}")
        message(FATAL_ERROR "Missing standard library include: ${INCLUDE_DIR}")
    endif()
endforeach()

set(STDLIB_LIBS
    "${LIBSTD_PATH}/libc++.a"
    "${LIBSTD_PATH}/libc++abi.a"
    "${LIBSTD_PATH}/libunwind.a"
    "${LIBSTD_PATH}/libc.a"
    "${LIBSTD_PATH}/libm.a"
    "${LIBSTD_PATH}/libclang_rt.builtins-arm.a"
)
