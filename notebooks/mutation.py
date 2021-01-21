import numpy as np


def swap(params, children):
    for child in children:
        i, j = np.random.randint(low=0, high=params['len_allele']), np.random.randint(low=0, high=params['len_allele'])
        child['allele'][i], child['allele'][j] = child['allele'][j], child['allele'][i]

    return children