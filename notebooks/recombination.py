import numpy as np


def pairwise(params, parents, crossover):
    offspring = np.empty(shape=params['n_off'], dtype=dict)

    for i in range(0, params['n_off'] - 1, 2):
        offspring[i], offspring[i + 1] = crossover(params, parents[i], parents[i + 1]), crossover(params, parents[i + 1], parents[i])

    return offspring


def order(params, mother, father):
    x, y = np.random.randint(0, params['len_gene']), np.random.randint(0, params['len_gene'])
    off = {'gene': -np.ones(shape=params['len_gene'], dtype=np.int), 'fitness': np.array([0 for _ in range(params['n_objs'])]), 'meta': np.array([0 for _ in range(params['len_meta'])])}

    off['gene'][min(x, y):max(x, y)] = mother['gene'][min(x, y):max(x, y)]

    j, k = max(x, y) - params['len_gene'], max(x, y) - params['len_gene']
    while j < min(x, y):
        if father['gene'][k] not in off['gene']:
            off['gene'][j] = father['gene'][k]
            j += 1
        k += 1

    return off