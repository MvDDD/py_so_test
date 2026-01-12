#define COMPILE
#include "nn2.h"
int32_t NN__error(NN *nn) {
	return nn->_error;
}
static inline float activate_hidden(float x) {
	if (fabsf(x) < 1e-7f) return 0.0f;
	return cbrt(x*x*(x + 1)/2.0f);
}

static inline float activate_hidden_derivative(float x) {
	float g = x*x*(x+1)/2.0f;
	if (fabsf(g) < 1e-7f) return 1.0f;
	float deriv = (1.0f/3.0f) * powf(fabsf(g), -2.0f/3.0f) * (3*x*x + 2*x)/2.0f;
	if (isnan(deriv) || deriv > 10.0f) deriv = 10.0f;
	if (deriv < -10.0f) deriv = -10.0f;
	return deriv;
}
static inline float activate_output(float x) {
	return x;
}

static inline float activate_output_derivative(float y) {
	return 1.0f;
}
void NN_create(NN *nn, int32_t depth, const int32_t *layer_sizes) {
	nn->_error = 0;
	nn->depth = depth;

	nn->layer_sizes = (int32_t*)malloc(sizeof(int32_t) * depth);
	if (!nn->layer_sizes) { nn->_error = __LINE__; return; }
	memcpy(nn->layer_sizes, layer_sizes, sizeof(int32_t) * depth);

	nn->weights = (float**)malloc(sizeof(float*) * (depth - 1));
	nn->biases  = (float**)malloc(sizeof(float*) * (depth - 1));
	if (!nn->weights || !nn->biases) {
		nn->_error = __LINE__;
		free(nn->layer_sizes);
		free(nn->weights);
		free(nn->biases);
		nn->layer_sizes = NULL;
		nn->weights = NULL;
		nn->biases = NULL;
		return;
	}

	srand((unsigned int)time(NULL));

	for (int32_t l = 0; l < depth - 1; l++) {
		int32_t in = nn->layer_sizes[l];
		int32_t out = nn->layer_sizes[l+1];

		nn->weights[l] = (float*)malloc(sizeof(float) * in * out);
		nn->biases[l]  = (float*)malloc(sizeof(float) * out);

		if (!nn->weights[l] || !nn->biases[l]) {
			nn->_error = __LINE__;
			for (int32_t k = 0; k <= l; k++) {
				free(nn->weights[k]);
				free(nn->biases[k]);
			}
			free(nn->weights);
			free(nn->biases);
			free(nn->layer_sizes);
			nn->weights = NULL;
			nn->biases = NULL;
			nn->layer_sizes = NULL;
			return;
		}
		for (int32_t i = 0; i < in*out; i++)
			nn->weights[l][i] = ((float)rand() / RAND_MAX - 0.5f);
		for (int32_t j = 0; j < out; j++)
			nn->biases[l][j] = 0.0f;
	}
}

void NN_destroy(NN *nn) {
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
void NN_forward(NN *nn, const float *input, float *output) {
	if (!nn || !input || !output) { nn->_error = __LINE__; return; }

	int32_t max_size = 0;
	for (int32_t l = 0; l < nn->depth; l++)
		if (nn->layer_sizes[l] > max_size) max_size = nn->layer_sizes[l];

	float *buf1 = malloc(sizeof(float) * max_size);
	float *buf2 = malloc(sizeof(float) * max_size);
	if (!buf1 || !buf2) { nn->_error = __LINE__; free(buf1); free(buf2); return; }

	memcpy(buf1, input, sizeof(float) * nn->layer_sizes[0]);
	float *layer_in = buf1;
	float *layer_out = buf2;

	for (int32_t l = 0; l < nn->depth - 1; l++) {
		for (int32_t j = 0; j < nn->layer_sizes[l+1]; j++) {
			float sum = nn->biases[l][j];
			for (int32_t i = 0; i < nn->layer_sizes[l]; i++)
				sum += layer_in[i] * nn->weights[l][i * nn->layer_sizes[l+1] + j];

			layer_out[j] = (l == nn->depth-2) ? sum : activate_hidden(sum);
		}

		if (l < nn->depth-2) {
			float *tmp = layer_in;
			layer_in = layer_out;
			layer_out = tmp;
		}
	}

	memcpy(output, layer_out, sizeof(float) * nn->layer_sizes[nn->depth-1]);
	free(buf1);
	free(buf2);
}
static float **NN_forward_intermediate(NN *nn, const float *input) {
	float **activations = (float**)malloc(sizeof(float*) * nn->depth);
	if (!activations) { nn->_error = __LINE__; return NULL; }

	for (int32_t l = 0; l < nn->depth; l++) {
		activations[l] = (float*)malloc(sizeof(float) * nn->layer_sizes[l]);
		if (!activations[l]) {
			nn->_error = __LINE__;
			for (int32_t k = 0; k < l; k++) free(activations[k]);
				free(activations);
			return NULL;
		}
	}

	memcpy(activations[0], input, sizeof(float) * nn->layer_sizes[0]);

	for (int32_t l = 0; l < nn->depth - 1; l++) {
		for (int32_t j = 0; j < nn->layer_sizes[l+1]; j++) {
			float sum = nn->biases[l][j];
			for (int32_t i = 0; i < nn->layer_sizes[l]; i++)
				sum += activations[l][i] * nn->weights[l][i * nn->layer_sizes[l+1] + j];

			if (l == nn->depth - 2)
				activations[l+1][j] = activate_output(sum);
			else
				activations[l+1][j] = activate_hidden(sum);
		}
	}

	return activations;
}
void NN_train_sample(NN *nn, const float *input, const float *target, float learning_rate) {
	nn->_error = 0;

	float **activations = NN_forward_intermediate(nn, input);
	if (!activations) return;

	float *delta = (float*)malloc(sizeof(float) * nn->layer_sizes[nn->depth-1]);
	if (!delta) { nn->_error = __LINE__; goto cleanup; }
	for (int32_t j = 0; j < nn->layer_sizes[nn->depth-1]; j++)
		delta[j] = (activations[nn->depth-1][j] - target[j]) * activate_output_derivative(activations[nn->depth-1][j]);
	for (int32_t l = nn->depth - 2; l >= 0; l--) {
		float *prev_delta = (float*)malloc(sizeof(float) * nn->layer_sizes[l]);
		if (!prev_delta) { nn->_error = __LINE__; free(delta); goto cleanup; }

		for (int32_t i = 0; i < nn->layer_sizes[l]; i++) {
			float sum = 0;
			for (int32_t j = 0; j < nn->layer_sizes[l+1]; j++)
				sum += nn->weights[l][i * nn->layer_sizes[l+1] + j] * delta[j];

			prev_delta[i] = activate_hidden_derivative(activations[l][i]) * sum;
		}
		for (int32_t j = 0; j < nn->layer_sizes[l+1]; j++) {
			for (int32_t i = 0; i < nn->layer_sizes[l]; i++)
				nn->weights[l][i * nn->layer_sizes[l+1] + j] -= learning_rate * delta[j] * activations[l][i];
			nn->biases[l][j] -= learning_rate * delta[j];
		}

		free(delta);
		delta = prev_delta;
	}

	free(delta);

	cleanup:
	for (int32_t l = 0; l < nn->depth; l++) free(activations[l]);
		free(activations);
}
void NN_train_batch(NN *nn, const float *inputs, const float *targets, int32_t batch_size, float learning_rate) {
	for (int32_t b = 0; b < batch_size; b++) {
		NN_train_sample(nn,
			inputs + b * nn->layer_sizes[0],
			targets + b * nn->layer_sizes[nn->depth-1],
			learning_rate
			);
		if (NN__error(nn)) return;
	}
}


void NN_save(NN *nn, const char *filename) {
	if (!nn || !filename) {
		nn->_error = __LINE__;
		return;
	}
	puts(filename);
	puts("\n");
	FILE *f = fopen(filename, "wb");
	if (!f) {
		nn->_error = __LINE__;
		return;
	}
	fwrite(&nn->depth, sizeof(int32_t), 1, f);
	fwrite(nn->layer_sizes, sizeof(int32_t), nn->depth, f);
	for (int32_t l = 0; l < nn->depth - 1; l++) {
		int32_t in = nn->layer_sizes[l];
		int32_t out = nn->layer_sizes[l+1];
		fwrite(nn->weights[l], sizeof(float), in*out, f);
		fwrite(nn->biases[l], sizeof(float), out, f);
	}

	fclose(f);
	return;
}
void NN_load(NN *nn, const char *filename) {
	if (!nn || !filename) {
		nn->_error = __LINE__;
		return;
	}
	FILE *f = fopen(filename, "rb");
	if (!f) {
		nn->_error = __LINE__;
		return;
	}
	int32_t file_depth;
	fread(&file_depth, sizeof(int32_t), 1, f);

	if (file_depth != nn->depth) {
		fclose(f);
		nn->_error = __LINE__;
		return;
	}
	int32_t *file_layers = (int32_t*)malloc(sizeof(int32_t) * file_depth);
	fread(file_layers, sizeof(int32_t), file_depth, f);
	for (int32_t i = 0; i < file_depth; i++) {
		if (file_layers[i] != nn->layer_sizes[i]) {
			free(file_layers);
			fclose(f);
			nn->_error = __LINE__;
			return;
		}
		free(file_layers);
		for (int32_t l = 0; l < nn->depth - 1; l++) {
			int32_t in = nn->layer_sizes[l];
			int32_t out = nn->layer_sizes[l+1];
			fread(nn->weights[l], sizeof(float), in*out, f);
			fread(nn->biases[l], sizeof(float), out, f);
		}

		fclose(f);
		return;
	}
}
