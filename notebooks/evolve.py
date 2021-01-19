import numpy as np
import initialization as init
import evaluation as eval
import selection as sel
import recombination as rec
import mutation as mut


initialize = init.permutation
evaluate = eval.TSP
select = sel.rank_based
mutate = mut.swap
replace = sel.rank_based()

params = {'generations': 1,
          'num_children': 10,
          'num_parents': 10,
          'num_solutions': 20,
          'len_genome': 10,
          'mutation rate': 0.5,
          'data': np.random.randint(size=(10, 10), low=0, high=1000)}

population = initialize(params)
population = evaluate(params, population)

for generation in range(params['generations']):
    parents = select(population, params['num_parents'])
    children = mutate(params, parents)
    children = mutate(params, children)
    children = evaluate(params, children)
    population = replace(np.concatenate(population, children), params['num_solutions'])



