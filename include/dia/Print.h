#pragma once

#include <Types.h>

#include <cstring>
#include <nn/diag.h>

namespace nn::diag {
    struct LogMetaData {
        u32 line = 0;
        const char* file = nullptr;
        const char* function = nullptr;
        const char* _c = "";
        u32 _10 = 1;
        u32 _14 = 0;
        void* _18 = nullptr;
        void* _1c = nullptr;
        void* _20 = nullptr;
    };
}

namespace dia {
    template <typename... Args>
    void printf(
        const char* file,
        u32 line,
        const char* function,
        const char* fmt,
        Args... args
    ) {
        const char* filename = file;

        for (const char* p = file; *p != 0; p++) {
            if (*p == '/' || *p == '\\') {
                filename = p + 1;
            }
        }

        nn::diag::LogMetaData meta {
            .line = line,
            .file = filename,
            .function = function
        };

        nn::diag::detail::LogImpl(meta, fmt, args...);
    }
}

#define DIA_LOG(fmt, ...) dia::printf(__FILE__, __LINE__, __PRETTY_FUNCTION__, fmt, ##__VA_ARGS__)
