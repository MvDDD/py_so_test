#ifdef COMPILE

	#include <stdint.h>
	#include <stdlib.h>
	#include <stdio.h>
	#include <time.h>
	#include <math.h>
	#define export __attribute__((visibility("default")))
#else
	#define export
	#include <stdint.h>

#endif


#define NN_MALLOC_ERROR 1


typedef struct Layer {
	int size;
	float *weights;
} Layer;

typedef struct Path {
	int source;
	int target;
	float weight;
} Path;

typedef struct PathLayer {
	int numpaths;
	Path *paths;
} PathLayer;

typedef struct Net {
	int numlayers;
	Layer *layers;
	PathLayer *pathlayers;
} Net;

typedef struct NN {
	Net net;
	int _error;
} NN;

export void NN_create(NN *n, int numlayers, int *layersizes);
export void NN_destroy(NN *n);
export void NN_run(NN *n, float *input, float *output);
export void NN_clone(NN *old, NN *new);
export void NN_mutate(NN *n, float rate);
export int NN__error(NN *n);