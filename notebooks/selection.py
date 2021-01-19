import numpy as np


def rank_based(population, sel_size):
    return np.array(sorted(population, key=lambda sol: sol['fitness'])[:sel_size])