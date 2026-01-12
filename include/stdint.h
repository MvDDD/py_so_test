#ifndef STDINT_H
#define STDINT_H

/* Exact-width integer types */


/* Least types */


/* Fast types */


/* Integer types capable of holding object pointers */

/* Greatest-width integer types */
'-Dint8_t=signed char',
'-Dint16_t=short',
'-Dint32_t=int',
'-Dint64_t=long long',
'-Duint8_t=unsigned char',
'-Duint16_t=unsigned short',
'-Duint32_t=unsigned int',
'-Duint64_t=unsigned long long',
'-Dint_least8_t=int8_t',
'-Dint_least16_t=int16_t',
'-Dint_least32_t=int32_t',
'-Dint_least64_t=int64_t',
'-Duint_least8_t=uint8_t',
'-Duint_least16_t=uint16_t',
'-Duint_least32_t=uint32_t',
'-Duint_least64_t=uint64_t',
'-Dint_fast8_t=int8_t',
'-Dint_fast16_t=int16_t',
'-Dint_fast32_t=int32_t',
'-Dint_fast64_t=int64_t',
'-Duint_fast8_t=uint8_t',
'-Duint_fast16_t=uint16_t',
'-Duint_fast32_t=uint32_t',
'-Duint_fast64_t=uint64_t',
'-Dintptr_t=long',
'-Duintptr_t=unsigned long',
'-Dintmax_t=long long',
'-Duintmax_t=unsigned long long',

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