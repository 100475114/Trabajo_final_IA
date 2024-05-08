import matplotlib.pyplot as plt
import numpy as np

# Leer el texto de entrada
input_text = open('InputVarSets.txt').read()

# Parsear el texto de entrada
lines = input_text.strip().split('\n')
fuzzy_sets = {}
for line in lines:
    parts = line.split(',')
    variable, label = parts[0].split('=')
    universe_start, universe_end, rise_start, rise_end, stable_end, fall_end = map(float, parts[1:])
    x = np.linspace(universe_start, universe_end, 1000)
    y = np.piecewise(x,
                     [x < rise_start, (x >= rise_start) & (x < rise_end), (x >= rise_end) & (x < stable_end), (x >= stable_end) & (x < fall_end), x >= fall_end],
                     [0, lambda x: (x - rise_start) / (rise_end - rise_start), 1, lambda x: (fall_end - x) / (fall_end - stable_end), 0])
    if variable not in fuzzy_sets:
        fuzzy_sets[variable] = {}
    fuzzy_sets[variable][label] = (x, y)

# Trazar las funciones de pertenencia
for variable, sets in fuzzy_sets.items():
    plt.figure()
    for label, (x, y) in sets.items():
        plt.plot(x, y, label=label)
    plt.title(f'Fuzzy Membership Functions for {variable}')
    plt.xlabel('Universe')
    plt.ylabel('Membership Degree')
    plt.legend()

plt.show()

