// stdio.h
#pragma once

typedef struct FILE FILE;
typedef long fpos_t;
typedef size_t size_t;
// File I/O

FILE *fopen(const char *restrict filename, const char *restrict mode);
FILE *freopen(const char *restrict filename, const char *restrict mode, FILE *restrict stream);
int fclose(FILE *stream);
int fflush(FILE *stream);

// Formatted I/O
int fprintf(FILE *restrict stream, const char *restrict format, ...);
int fscanf(FILE *restrict stream, const char *restrict format, ...);
int printf(const char *restrict format, ...);
int scanf(const char *restrict format, ...);
int snprintf(char *restrict s, size_t n, const char *restrict format, ...);
int sprintf(char *restrict s, const char *restrict format, ...);
int sscanf(const char *restrict s, const char *restrict format, ...);
int vfprintf(FILE *restrict stream, const char *restrict format, va_list arg);
int vprintf(const char *restrict format, va_list arg);
int vsnprintf(char *restrict s, size_t n, const char *restrict format, va_list arg);
int vsprintf(char *restrict s, const char *restrict format, va_list arg);
int vfscanf(FILE *restrict stream, const char *restrict format, va_list arg);
int vscanf(const char *restrict format, va_list arg);

// Character I/O
int fgetc(FILE *stream);
char *fgets(char *restrict s, int n, FILE *restrict stream);
int fputc(int c, FILE *stream);
int fputs(const char *restrict s, FILE *restrict stream);
int getc(FILE *stream);
int getchar(void);
char *gets(char *s); // deprecated
int putc(int c, FILE *stream);
int putchar(int c);
int puts(const char *s);
int ungetc(int c, FILE *stream);

// Block I/O
size_t fread(void *restrict ptr, size_t size, size_t nmemb, FILE *restrict stream);
size_t fwrite(const void *restrict ptr, size_t size, size_t nmemb, FILE *restrict stream);

// File positioning
int fgetpos(FILE *restrict stream, fpos_t *restrict pos);
int fseek(FILE *stream, long offset, int whence);
int fsetpos(FILE *stream, const fpos_t *pos);
long ftell(FILE *stream);
void rewind(FILE *stream);

// Error handling
int feof(FILE *stream);
int ferror(FILE *stream);
void clearerr(FILE *stream);

// Temporary files
FILE *tmpfile(void);
char *tmpnam(char *s);

// File operations
int remove(const char *filename);
int rename(const char *old_filename, const char *new_filename);

// Standard streams
extern FILE *stdin;
extern FILE *stdout;
extern FILE *stderr;
