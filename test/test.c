#include "test.h"
#include <stddef.h>

int add(int a, int b){
	return a + b;
}

void add_array(int *a, int *b, int *c, int count){
	for (int i = 0; i < count; i++){
		c[i] = a[i] + b[i];
	}
}

void init_str_arr(str *s, int num){
	for (int i = 0; i < num; i++){
		(s + i)->len=0;
		(s + i)->data=NULL;
	}
}