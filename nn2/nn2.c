#define COMPILE
#include "nn2.h"

// ---------------------- Error checking ----------------------
int32_t NN__error(NN *nn) {
    return nn->_error;
}

// ---------------------- Lifecycle ----------------------
void NN_create(NN *nn, int32_t depth, const int32_t *layer_sizes) {
    nn->_error = 0;

    nn->depth = depth;
    nn->layer_sizes = (int32_t*)malloc(sizeof(int32_t) * depth);
    if (!nn->layer_sizes) { nn->_error = 1; return; }
    memcpy(nn->layer_sizes, layer_sizes, sizeof(int32_t) * depth);

    nn->weights = (float**)malloc(sizeof(float*) * (depth - 1));
    nn->biases  = (float**)malloc(sizeof(float*) * (depth - 1));
    if (!nn->weights || !nn->biases) {
        nn->_error = 1;
        free(nn->layer_sizes);
        free(nn->weights);
        free(nn->biases);
            nn->layer_sizes = NULL;
    nn->weights = NULL;
    nn->biases = NULL;
        return;
    }

    for (int32_t l = 0; l < depth - 1; l++) {
        nn->weights[l] = (float*)malloc(sizeof(float) * nn->layer_sizes[l] * nn->layer_sizes[l+1]);
        nn->biases[l]  = (float*)malloc(sizeof(float) * nn->layer_sizes[l+1]);
        if (!nn->weights[l] || !nn->biases[l]) {
            nn->_error = 1;
            for (int32_t k = 0; k <= l; k++) {
                free(nn->weights[k]);
                free(nn->biases[k]);
            }
            free(nn->weights);
            free(nn->biases);
            free(nn->layer_sizes);
            nn->layer_sizes = NULL;
            nn->weights = NULL;
            nn->biases = NULL;
            return;
        }
        memset(nn->weights[l], 0, sizeof(float) * nn->layer_sizes[l] * nn->layer_sizes[l+1]);
        memset(nn->biases[l], 0, sizeof(float) * nn->layer_sizes[l+1]);
    }
}

void NN_destroy(NN *nn) {
    if (!nn) return;
    for (int32_t l = 0; l < nn->depth - 1; l++) {
        free(nn->weights[l]);
        free(nn->biases[l]);
    }
    free(nn->weights);
    free(nn->biases);
    free(nn->layer_sizes);

    nn->weights = NULL;
    nn->biases = NULL;
    nn->layer_sizes = NULL;
    nn->_error = 0;
}

// ---------------------- Forward pass ----------------------
void NN_forward(NN *nn, const float *input, float *output) {
    if (!nn || !input || !output) {
        nn->_error = 2;
        return;
    }

    float *layer_in = (float*)malloc(sizeof(float) * nn->layer_sizes[0]);
    if (!layer_in) { nn->_error = 1; return; }
    memcpy(layer_in, input, sizeof(float) * nn->layer_sizes[0]);

    for (int32_t l = 0; l < nn->depth - 1; l++) {
        float *layer_out = (float*)malloc(sizeof(float) * nn->layer_sizes[l+1]);
        if (!layer_out) { nn->_error = 1; free(layer_in); return; }

        for (int32_t j = 0; j < nn->layer_sizes[l+1]; j++) {
            float sum = nn->biases[l][j];
            for (int32_t i = 0; i < nn->layer_sizes[l]; i++) {
                sum += layer_in[i] * nn->weights[l][i * nn->layer_sizes[l+1] + j];
            }
            layer_out[j] = sum > 0 ? sum : 0; // ReLU
        }

        free(layer_in);
        layer_in = layer_out;
    }

    memcpy(output, layer_in, sizeof(float) * nn->layer_sizes[nn->depth-1]);
    free(layer_in);
}
