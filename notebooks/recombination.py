import numpy as np


def order(params, parents):
    children = np.empty(shape=params['num_children'], dtype=dict)

    for i in range(0, params['num_parents'] - 1, 2):
        x, y = np.random.randint(0, params['len_allele']), np.random.randint(0, params['len_allele'])
        child = {'allele': -np.ones(shape=params['len_allele'], dtype=np.int), 'fitness': None}

        child['allele'][min(x, y):max(x, y)] = parents[i]['allele'][min(x, y):max(x, y)]

        j, k = max(x, y) - params['len_allele'], max(x, y) - params['len_allele']
        while j < min(x, y):
            if parents[i + 1]['allele'][k] not in child['allele']:
                child['allele'][j] = parents[i + 1]['allele'][k]
                j += 1
            k += 1

        children[i // 2] = child

    return children