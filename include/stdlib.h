#ifndef STDLIB_H
#define STDLIB_H

#include <stddef.h>
#include <wchar.h>

/* Macros */
#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define RAND_MAX 32767
#define MB_CUR_MAX 1  /* for simplicity, can vary in real implementation */

/* Types */
typedef struct { int quot; int rem; } div_t;
typedef struct { long int quot; long int rem; } ldiv_t;
typedef struct { long long int quot; long long int rem; } lldiv_t;

/* Memory management */
void *malloc(size_t size);
void *calloc(size_t nmemb, size_t size);
void *realloc(void *ptr, size_t size);
void free(void *ptr);

/* Process control */
void abort(void);
void exit(int status);
int atexit(void (*func)(void));
void *getenv(const char *name);
int system(const char *command);

/* Conversion */
int atoi(const char *nptr);
long int atol(const char *nptr);
long long int atoll(const char *nptr);
double atof(const char *nptr);

long int strtol(const char *restrict nptr, char **restrict endptr, int base);
unsigned long int strtoul(const char *restrict nptr, char **restrict endptr, int base);
long long int strtoll(const char *restrict nptr, char **restrict endptr, int base);
unsigned long long int strtoull(const char *restrict nptr, char **restrict endptr, int base);
float strtof(const char *restrict nptr, char **restrict endptr);
double strtod(const char *restrict nptr, char **restrict endptr);
long double strtold(const char *restrict nptr, char **restrict endptr);

/* Random numbers */
int rand(void);
void srand(unsigned int seed);

/* Searching and sorting */
void *bsearch(const void *key, const void *base, size_t nmemb, size_t size,
              int (*compar)(const void *, const void *));
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));

/* Absolute value */
int abs(int j);
long int labs(long int j);
long long int llabs(long long int j);

div_t div(int numer, int denom);
ldiv_t ldiv(long int numer, long int denom);
lldiv_t lldiv(long long int numer, long long int denom);

/* Multibyte / wide conversion */
size_t mblen(const char *s, size_t n);
size_t mbstowcs(wchar_t *restrict pwcs, const char *restrict s, size_t n);
size_t wctomb(char *s, wchar_t wc);
size_t wcstombs(char *restrict s, const wchar_t *restrict pwcs, size_t n);

/* Temporary files */
char *tmpnam(char *s);

#endif /* STDLIB_H */
