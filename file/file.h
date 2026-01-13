#include <stdio.h>
#include <stdint.h>

#undef COMPILE
#ifdef COMPILE
#define export __attribute__((__visibility__("default")))
#else
#define export
#endif

typedef struct File {
	FILE *f;
	int _error;
} File;


export int File__error(File *f);
export void File_create(File *f, char *path, char *mode);
export void File_destroy(File *f);
export size_t File_read(File *f, void *buffer, size_t length);
export size_t File_write(File *f, void *buffer, size_t length);
export FILE *File_gethandle(File *f);