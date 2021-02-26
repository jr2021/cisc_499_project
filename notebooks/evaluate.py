import numpy as np

def TSP(self, pop):
    dist = np.loadtxt('dist.txt')

    for ind in pop:
        ind['fitness'][0] = dist[0][ind['gene'][0]] + np.array([dist[ind['gene'][i - 1]][ind['gene'][i]] for i in range(1, self.params['gene_size'])]).sum() + dist[ind['gene'][-1]][0]

    return pop
                                                                
def knapsack(self, pop):
    value = np.loadtxt('value.txt')
    weight = np.loadtxt('weight.txt')
    
    for ind in pop:
        for i in range(self.params['gene_size']):
            if ind['gene'][i] == 1:
                ind['fitness'][0] += value[i]
                ind['fitness'][1] += weight[i]
            
    return pop