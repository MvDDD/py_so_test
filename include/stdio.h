// stdio.h
#pragma once

typedef struct FILE FILE;
typedef long fpos_t;
typedef size_t size_t;
// File I/O

FILE *fopen(char *filename, char *mode);
FILE *freopen(char *filename, char *mode, FILE *stream);
int fclose(FILE *stream);
int fflush(FILE *stream);

// Formatted I/O
int fprintf(FILE *stream, char *format, ...);
int fscanf(FILE *stream, char *format, ...);
int printf(char *format, ...);
int scanf(char *format, ...);
int snprintf(char *s, size_t n, char *format, ...);
int sprintf(char *s, char *format, ...);
int sscanf(char *s, char *format, ...);
int vfprintf(FILE *stream, char *format, va_list arg);
int vprintf(char *format, va_list arg);
int vsnprintf(char *s, size_t n, char *format, va_list arg);
int vsprintf(char *s, char *format, va_list arg);
int vfscanf(FILE *stream, char *format, va_list arg);
int vscanf(char *format, va_list arg);

// Character I/O
int fgetc(FILE *stream);
char *fgets(char *s, int n, FILE *stream);
int fputc(int c, FILE *stream);
int fputs(char *s, FILE *stream);
int getc(FILE *stream);
int getchar(void);
char *gets(char *s); // deprecated
int putc(int c, FILE *stream);
int putchar(int c);
int puts(char *s);
int ungetc(int c, FILE *stream);

// Block I/O
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
size_t fwrite(void *ptr, size_t size, size_t nmemb, FILE *stream);

// File positioning
int fgetpos(FILE *stream, fpos_t *pos);
int fseek(FILE *stream, long offset, int whence);
int fsetpos(FILE *stream, fpos_t *pos);
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
int remove(char *filename);
int rename(char *old_filename, char *new_filename);

// Standard streams
extern FILE *stdin;
extern FILE *stdout;
extern FILE *stderr;
