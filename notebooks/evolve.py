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
recombine = rec.order
replace = sel.rank_based

params = {'generations': 1000,
          'num_children': 50,
          'num_parents': 100,
          'num_solutions': 150,
          'len_allele': 100,
          'mutation rate': 0.5,
          'data': np.random.randint(size=(100, 100), low=0, high=1000)}

population = initialize(params)
population = evaluate(params, population)

for generation in range(params['generations']):
    parents = select(population, params['num_parents'])
    children = recombine(params, parents)
    children = mutate(params, children)
    children = evaluate(params, children)
    population = replace(np.concatenate((population, children), axis=0), params['num_solutions'])

