import numpy as np


def perm(params):
    return np.array([{'gene': np.random.permutation(params['len_gene']), 'fitness': np.array([0 for _ in range(params['n_objs'])])} for _ in range(params['pop_size'])])


def sample_perm(min, max):
    return [np.random.permutation(np.arange(start=min, stop=max+1)) for _ in range(5)]
        