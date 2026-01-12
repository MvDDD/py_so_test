#define COMPILE
#include "nn.h"

static inline uint64_t get_cpu_cycles() {
    unsigned int hi, lo;
    __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}
static inline float nn_rand(NN *n) {
    return rand() / (float)RAND_MAX; // [0,1)
}

void NN_create(NN *n, int numlayers, int *layersizes){
	srand(get_cpu_cycles());
	n->_error = 0;
	n->net.numlayers = numlayers;
	n->net.layers = malloc(sizeof(Layer) * numlayers);
	if (n->net.layers == NULL) {
		n->_error = NN_MALLOC_ERROR;
		return;
	}
	for (int i = 0; i < numlayers; i++){
		n->net.layers[i].size = layersizes[i];
		n->net.layers[i].weights = malloc(sizeof(float) * layersizes[i]);
		if (n->net.layers[i].weights == NULL) {
			n->_error = NN_MALLOC_ERROR;
			for (int q = i-1; q>=0; q--){
				free(n->net.layers[q].weights);
				n->net.layers[q].weights = NULL;
			}
			return;
		}
		for (int j = 0; j < layersizes[i]; j++) 
			n->net.layers[i].weights[j] = (nn_rand(n) - 0.5f) * 0.1f;
	}
	n->net.pathlayers = malloc(sizeof(PathLayer) * (numlayers-1));
	if (n->net.pathlayers == NULL){
		n->_error = NN_MALLOC_ERROR;
		for (int i = 0; i < numlayers; i++){
			free(n->net.layers[i].weights);
			n->net.layers[i].weights = NULL;
		}
		free(n->net.layers);
		n->net.layers = NULL;
		return;
	}
	for (int i = 0; i < numlayers-1; i++){
		n->net.pathlayers[i].numpaths = layersizes[i] * layersizes[i+1];
		n->net.pathlayers[i].paths = malloc(sizeof(Path) * n->net.pathlayers[i].numpaths);
		if (n->net.pathlayers[i].paths == NULL){
			n->_error = NN_MALLOC_ERROR;
			for (int i = 0; i < numlayers; i++){
				free(n->net.layers[i].weights);
				n->net.layers[i].weights = NULL;
			}
			free(n->net.layers);
			n->net.layers = NULL;
			
			for(int q = i-1; q >= 0; q--){
				free(n->net.pathlayers[q].paths);
				n->net.pathlayers[q].paths = NULL;
			}

			free(n->net.pathlayers);
			n->net.pathlayers = NULL;
			return;
		}
		int pathidx = 0;
		for (int j = 0; j < layersizes[i]; j++){
			for (int k = 0; k < layersizes[i+1]; k++){
				n->net.pathlayers[i].paths[pathidx].source = j;
				n->net.pathlayers[i].paths[pathidx].target = k;
				n->net.pathlayers[i].paths[pathidx].weight = (nn_rand(n) - 0.5f) * 0.1f;
				pathidx++;
			}
		}
	}
}

void NN_destroy(NN *n){
	for (int i = 0; i < n->net.numlayers; i++){
		free(n->net.layers[i].weights);
	}
	free(n->net.layers);

	for (int i = 0; i < n->net.numlayers-1; i++){
		free(n->net.pathlayers[i].paths);
	}
	free(n->net.pathlayers);
}

void NN_run(NN *n, float *input, float *output) {
    int numlayers = n->net.numlayers;

    // --- Allocate temporary activation buffers ---
    float **activations = malloc(sizeof(float*) * numlayers);
    for (int l = 0; l < numlayers; l++)
        activations[l] = calloc(n->net.layers[l].size, sizeof(float));

    // --- Copy input to first layer ---
    for (int i = 0; i < n->net.layers[0].size; i++)
        activations[0][i] = input[i];

    // --- Forward propagation ---
    for (int l = 0; l < numlayers - 1; l++) {
        PathLayer *pl = &n->net.pathlayers[l];
        Path *paths = pl->paths; // use the real network paths

        for (int j = 0; j < pl->numpaths; j++) {
            Path *p = &paths[j];
            activations[l + 1][p->target] += atanf(activations[l][p->source] * p->weight);
        }
    }

    // --- Collect output from last layer ---
    Layer *last = &n->net.layers[numlayers - 1];
    for (int i = 0; i < last->size; i++)
        output[i] = activations[numlayers - 1][i];

    // --- Free temporary buffers ---
    for (int l = 0; l < numlayers; l++)
        free(activations[l]);
    free(activations);
}


void NN_clone(NN *old, NN *new) {
    new->_error = 0;
    new->net.numlayers = old->net.numlayers;

    // --- Allocate layers ---
    new->net.layers = malloc(sizeof(Layer) * old->net.numlayers);
    if (!new->net.layers) {
        new->_error = NN_MALLOC_ERROR;
        return;
    }

    for (int i = 0; i < old->net.numlayers; i++) {
        int sz = old->net.layers[i].size;
        new->net.layers[i].size = sz;

        new->net.layers[i].weights = malloc(sizeof(float) * sz);
        if (!new->net.layers[i].weights) {
            new->_error = NN_MALLOC_ERROR;
            // cleanup previous allocations
            for (int j = 0; j < i; j++)
                free(new->net.layers[j].weights);
            free(new->net.layers);
            new->net.layers = NULL;
            return;
        }

        // Copy weights
        for (int j = 0; j < sz; j++)
            new->net.layers[i].weights[j] = old->net.layers[i].weights[j];
    }

    // --- Allocate pathlayers ---
    new->net.pathlayers = malloc(sizeof(PathLayer) * (old->net.numlayers - 1));
    if (!new->net.pathlayers) {
        new->_error = NN_MALLOC_ERROR;
        // cleanup layers
        for (int i = 0; i < old->net.numlayers; i++)
            free(new->net.layers[i].weights);
        free(new->net.layers);
        new->net.layers = NULL;
        return;
    }

    // --- Copy pathlayers ---
    for (int i = 0; i < old->net.numlayers - 1; i++) {
        int np = old->net.pathlayers[i].numpaths;
        new->net.pathlayers[i].numpaths = np;

        new->net.pathlayers[i].paths = malloc(sizeof(Path) * np);
        if (!new->net.pathlayers[i].paths) {
            new->_error = NN_MALLOC_ERROR;
            // cleanup previous path allocations
            for (int q = 0; q < i; q++)
                free(new->net.pathlayers[q].paths);
            free(new->net.pathlayers);
            new->net.pathlayers = NULL;
            for (int l = 0; l < old->net.numlayers; l++)
                free(new->net.layers[l].weights);
            free(new->net.layers);
            new->net.layers = NULL;
            return;
        }

        // Copy paths
        for (int j = 0; j < np; j++) {
            new->net.pathlayers[i].paths[j] = old->net.pathlayers[i].paths[j];
        }
    }
}




void NN_mutate(NN *n, float rate) {
    // Mutate layer weights
    for (int l = 0; l < n->net.numlayers; l++) {
        Layer *layer = &n->net.layers[l];
        for (int i = 0; i < layer->size; i++) {
            float delta = (nn_rand(n) - 0.5f) * 2.0f * rate; // [-rate, +rate]
            layer->weights[i] += delta;
        }
    }

    // Mutate path weights
    for (int l = 0; l < n->net.numlayers - 1; l++) {
        PathLayer *pl = &n->net.pathlayers[l];
        for (int p = 0; p < pl->numpaths; p++) {
            float delta = (nn_rand(n) - 0.5f) * 2.0f * rate; // [-rate, +rate]
            pl->paths[p].weight += delta;
        }
    }
}


int NN__error(NN *n){
	return n->_error;
}