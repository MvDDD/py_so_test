import nn
from libso import *
import math
import random

# --- network configuration ---
# Example: 3 inputs -> two hidden layers of 10 neurons -> 2 outputs
shape = cast_buffer(createbuffer(sizeof(i32) * 4), i32)
copybuffer([3, 100, 100, 2], shape)
basenet = nn.NN(5, shape)

# --- training data ---
# Multiple inputs and outputs
INPUTS = [
    [0.1, 0.2, 0.3],
    [0.5, 0.4, 0.6],
    [0.9, 0.8, 0.7],
    [0.3, 0.7, 0.2],
    [0.6, 0.1, 0.9],
]
OUTPUTS = [
    [0.5, 0.7],
    [0.2, 0.1],
    [0.9, 0.8],
    [0.4, 0.6],
    [0.3, 0.2],
]

# Buffers for NN input/output
BUFF_IN = cast_buffer(createbuffer(sizeof(f32) * len(INPUTS[0])), f32)
BUFF_OUT = cast_buffer(createbuffer(sizeof(f32) * len(OUTPUTS[0])), f32)

# --- helper functions ---
def buffer_to_list(buffer):
    return [buffer[i] for i in range(len(buffer))]

def compute_loss(net):
    """Compute total normalized loss for multiple outputs."""
    total = 0.0
    for IN, TRG in zip(INPUTS, OUTPUTS):
        copybuffer(IN, BUFF_IN)
        net.run(BUFF_IN, BUFF_OUT)
        out = buffer_to_list(BUFF_OUT)
        # Normalized absolute difference for each output
        total += sum(abs(o - t)/(abs(t) + 0.01) for o, t in zip(out, TRG))
    return total

def clone_and_mutate(net, rate, n_clones=50):
    """Clone a network multiple times and mutate each clone."""
    clones = []
    for _ in range(n_clones):
        item = nn.NN.Struct_LP()
        item.contents = nn.NN.Struct()
        net.clone(item)
        newnet = nn.NN.init_from(item.contents)
        # Add per-node random mutation for diversity
        mutation_strength = f32(rate)
        newnet.mutate(mutation_strength)
        clones.append(newnet)
    return clones

# --- evolutionary loop ---
mutation_rate = 0.5  # initial mutation
generation = 0

try:
    while True:
        # Generate mutated population
        population = clone_and_mutate(basenet, mutation_rate, n_clones=50)
        population.append(basenet)  # include current best

        # Evaluate each network
        results = [(net, compute_loss(net)) for net in population]

        # Sort by fitness (lower loss = better)
        results.sort(key=lambda x: x[1])
        best_net, best_loss = results[0]

        # Update basenet
        basenet = best_net

        # Compute average loss
        avg_loss = sum(r[1] for r in results) / len(results)

        # Adaptive mutation: higher loss -> bigger mutation
        mutation_rate = min(10, max(0.01, math.atan(avg_loss)))

        generation += 1

        print(f"Gen {generation:03d} | Best: {best_loss:.4f} | Avg: {avg_loss:.4f} | Mutation: {mutation_rate:.4f}")

except KeyboardInterrupt:
    print("Training stopped by user.")
    final_loss = compute_loss(basenet)
    print("Final loss:", final_loss)
