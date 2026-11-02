#pragma once

typedef struct {
    unsigned long long lo;
    unsigned long long hi;
} __uint128_t;

#ifdef __cplusplus
    static_assert(sizeof(__uint128_t) == 16);
#endif
