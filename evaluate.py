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

def eight_queens(self, pop):
    for ind in pop:
        for i in range(self.params['gene_size']):
            for j in range(i + 1, self.params['gene_size']):
                if abs(ind['gene'][i] - ind['gene'][j]) == abs(i - j):
                    ind['fitness'][0] += 1
                    
    return pop
        

def sudoku(self, pop):
    for ind in pop:
        for i in range(self.params['gene_size']):
            for j in range(i - i % 10, i + (10 - i % 10)): 
                if i == j:
                    continue
                elif ind['gene'][i] % 10 == ind['gene'][j] % 10:
                    ind['fitness'][0] += 1
            for k in range(i, self.params['gene_size'], 10): 
                if i == k:
                    continue
                elif ind['gene'][i] % 10 == ind['gene'][k] % 10:
                    ind['fitness'][0] += 1            
                    
    return pop
    
    