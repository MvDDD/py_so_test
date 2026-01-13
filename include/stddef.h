#ifndef STDDEF_H
#define STDDEF_H

/* Types */
#define ptrdiff_t intptr_t
#define wchar_t unsigned short
typedef struct max_align_t {} max_align_t;

/* Macros */
#define NULL ((void*)0)
#define offsetof(type, member) ((size_t) &(((type *)0)->member))

#endif /* STDDEF_H */