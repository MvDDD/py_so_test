#ifndef STDDEF_H
#define STDDEF_H

/* Types */
typedef long ptrdiff_t;
typedef unsigned long size_t;
typedef unsigned short wchar_t; /* minimal parser-safe definition */
typedef struct max_align_t max_align_t; /* opaque, standard */

/* Macros */
#define NULL ((void*)0)
#define offsetof(type, member) ((size_t) &(((type *)0)->member))

#endif /* STDDEF_H */