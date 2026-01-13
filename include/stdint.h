#ifndef STDINT_H
#define STDINT_H


typedef signed char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef long long int64_t;
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef unsigned long long uint64_t;
typedef long intptr_t;
typedef unsigned long uintptr_t;

#define int_least8_t int8_t;
#define int_least16_t int16_t;
#define int_least32_t int32_t;
#define int_least64_t int64_t;
#define uint_least8_t uint8_t;
#define uint_least16_t uint16_t;
#define uint_least32_t uint32_t;
#define uint_least64_t uint64_t;

#define int_fast8_t int8_t;
#define int_fast16_t int16_t;
#define int_fast32_t int32_t;
#define int_fast64_t int64_t;
#define uint_fast8_t uint8_t;
#define uint_fast16_t uint16_t;
#define uint_fast32_t uint32_t;
#define uint_fast64_t uint64_t;

#define intmax_t long long
#define uintmax_t unsigned long long

/* Limits macros */
#define INT8_MIN   (-128)
#define INT8_MAX   127
#define INT16_MIN  (-32768)
#define INT16_MAX  32767
#define INT32_MIN  (-2147483648)
#define INT32_MAX  2147483647
#define INT64_MIN  (-9223372036854775807LL - 1)
#define INT64_MAX  9223372036854775807LL

#define UINT8_MAX   255
#define UINT16_MAX  65535
#define UINT32_MAX  4294967295U
#define UINT64_MAX  18446744073709551615ULL

#endif /* STDINT_H */