import numpy as np


def TSP(params, population):
    for sol in population:
        sol['fitness'] = np.array([params['data'][sol['allele'][i - 1]][sol['allele'][i]] for i in range(1, params['len_allele'])]).sum()
    return population