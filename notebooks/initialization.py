import numpy as np


def permutation(params):
    return np.array([{'genome': np.random.permutation(params['len_genome']), 'fitness': None} for _ in range(params['num_solutions'])])