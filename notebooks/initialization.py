import numpy as np


def permutation(params):
    return np.array([{'gene': np.random.permutation(params['len_gene']), 'fitness': np.array([0 for _ in range(params['n_objs'])])} for _ in range(params['pop_size'])])