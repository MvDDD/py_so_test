#ifndef NN_H
#define NN_H

#ifdef COMPILE
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#endif // COMPILE

// ---------------------- Struct ----------------------
typedef struct NN {
    int32_t depth;
    int32_t *layer_sizes;
    float **weights;
    float **biases;
    int32_t _error;
} NN;

// ---------------------- Function prototypes ----------------------
int32_t NN__error(NN *nn);

void NN_create(NN *nn, int32_t depth, const int32_t *layer_sizes);
void NN_destroy(NN *nn);

void NN_forward(NN *nn, const float *input, float *output);

void NN_train_sample(NN *nn, const float *input, const float *target, float learning_rate);
void NN_train_batch(NN *nn, const float *inputs, const float *targets, int32_t batch_size, float learning_rate);

void NN_save(NN *nn, const char *filename);
void NN_load(NN *nn, const char *filename);
#endif // NN2_H
