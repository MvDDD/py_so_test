#ifndef STDLIB_H
#define STDLIB_H

#include <stddef.h>
#include <wchar.h>

/* Macros */
#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define RAND_MAX 32767
#define MB_CUR_MAX 1  /* for simplicity, can vary in real implementation */

typedef struct { int quot; int rem; } div_t;
typedef struct { long int quot; long int rem; } ldiv_t;
typedef struct { long long int quot; long long int rem; } lldiv_t;

#endif /* STDLIB_H */
