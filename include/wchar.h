#ifndef WCHAR_H
#define WCHAR_H

#include <stddef.h>

typedef struct FILE {} FILE;
/* Types */
#define wint_t long
#define wctype_t long
typedef struct { int __count; } mbstate_t;

#define WEOF ((wint_t)(-1))

#endif /* WCHAR_H */