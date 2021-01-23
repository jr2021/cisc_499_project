import numpy as np


def custom(params, population):
    data = np.loadtxt('data.txt')

    for ind in population:
        ind['fitness'][0] += data[0][ind['gene'][0]]
        ind['fitness'][0] += np.array([data[ind['gene'][i - 1]][ind['gene'][i]] for i in range(1, params['len_gene'])]).sum()
        data[ind['gene'][-1]][0]

    return population