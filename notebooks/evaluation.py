import numpy as np


def TSP(params, population):
    for sol in population:
        sol['fitness'] = np.array([params['data'][sol['genome'][i - 1]][sol['genome'][i]] for i in range(1, params['len_genome'])]).sum()
    return population