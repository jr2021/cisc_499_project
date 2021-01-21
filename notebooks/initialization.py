import numpy as np


def permutation(params):
    return np.array([{'allele': np.random.permutation(params['len_allele']), 'fitness': None} for _ in range(params['num_solutions'])])