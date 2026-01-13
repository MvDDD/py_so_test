#ifndef _DIRENT_H
#define _DIRENT_H

#include <bits/types.h>

/* Adjusted typedefs for portability */
#ifdef __USE_XOPEN
# ifndef __ino_t_defined
#  ifndef __USE_FILE_OFFSET64
typedef __ino_t ino_t;
#  else
typedef __ino64_t ino_t;
#  endif
#  define __ino_t_defined
# endif
# if defined __USE_LARGEFILE64 && !defined __ino64_t_defined
typedef __ino64_t ino64_t;
#  define __ino64_t_defined
# endif
#endif

/* Structs only */
typedef struct __dirstream DIR;

#endif /* _DIRENT_H */
