#ifdef COMPILE
#define export __attribute__((__visibility__("default")))
#else
#define export
#endif

typedef struct str {
	int len;
	char *data;
} str;

export int add(int a, int b);
export void add_array(int *a, int *b, int *c, int count);
export void init_str_arr(str *s, int num);