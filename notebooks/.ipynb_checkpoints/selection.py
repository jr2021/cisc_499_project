import numpy as np


def rank_based(params, population, sel_size):
    np.array(sorted(population, key=lambda sol: ['fitness'])[:sel_size])