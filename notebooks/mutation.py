import numpy as np


def swap(params, offspring):
    for off in offspring:
        i, j = np.random.randint(low=0, high=params['len_gene']), np.random.randint(low=0, high=params['len_gene'])
        off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

    return offspring