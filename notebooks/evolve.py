import numpy as np
import initialize as init
import evaluation as eval
import selection as sel


params = {'generations': 1,
          'num_children': 10,
          'num_parents': 10,
          'num_solutions': 20,
          'len_genome': 10,
          'mutation rate': 0.5,
          'representation': init.permutation,
          'evaluation': eval.TSP,
          'selection': sel.rank_based,
          'data': np.random.randint(size=(10, 10), low=0, high=1000)}

print(params['data'].sum())

population = params['representation'](params)
population = params['evaluation'](params, population)

for generation in range(params['generations']):
    parents = params['selection'](population, params['num_parents'])

print(population)
print(parents)


