#include "file.h"

int File__error(File *f){return f->_error;}

void File_create(File *f, char *path, char *mode){
	f->_error = 0;
	f->f = fopen(path, mode);
	if (!f->f) f->_error = 1;
}

void File_destroy(File *f){
	fclose(f->f);
}

size_t File_read(File *f, void *buffer, size_t length){
	return fread(buffer, 1, length, f->f);
}

size_t File_write(File *f, void *buffer, size_t length){
	return fwrite(buffer, 1, length, f->f);
}

FILE *File_gethandle(File *f){
	return f->f;
}