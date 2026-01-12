#ifndef WCHAR_H
#define WCHAR_H

#include <stddef.h>

typedef struct FILE FILE;
/* Types */
typedef long wint_t;
typedef long wctype_t;
typedef struct { int __count; } mbstate_t;

/* Macros */
#define WEOF ((wint_t)(-1))

/* Functions */
wint_t btowc(int c);
int wctob(wint_t wc);

size_t mbrlen(const char *restrict s, size_t n, mbstate_t *restrict ps);
size_t mbrtowc(wchar_t *restrict pwc, const char *restrict s, size_t n, mbstate_t *restrict ps);
size_t wcrtomb(char *restrict s, wchar_t wc, mbstate_t *restrict ps);

size_t mbsrtowcs(wchar_t *restrict dst, const char **restrict src, size_t len, mbstate_t *restrict ps);
size_t wcsrtombs(char *restrict dst, const wchar_t **restrict src, size_t len, mbstate_t *restrict ps);

wint_t fgetwc(FILE *stream);
wint_t getwc(FILE *stream);
wint_t getwchar(void);

wint_t fputwc(wchar_t wc, FILE *stream);
wint_t putwc(wchar_t wc, FILE *stream);
wint_t putwchar(wchar_t wc);

wchar_t *fgetws(wchar_t *restrict s, int n, FILE *restrict stream);
int fputws(const wchar_t *restrict s, FILE *restrict stream);

wint_t ungetwc(wint_t wc, FILE *stream);

#endif /* WCHAR_H */