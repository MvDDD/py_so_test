#ifndef NN2_H
#define NN2_H

#include <stdint.h>

typedef struct NN {
    int32_t depth;          // number of layers
    int32_t *layer_sizes;   // array of layer sizes

    float **weights;        // weights[l] is array of floats for layer l->l+1
    float **biases;         // biases[l] is array of floats for layer l+1

    int32_t _error;
} NN;

int32_t NN__error(NN *nn);

void NN_create(NN *nn, int32_t depth, const int32_t *layer_sizes);
void NN_destroy(NN *nn);
void NN_forward(NN *nn, const float *input, float *output);

#ifdef COMPILE
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#endif

#endif // NN2_H
