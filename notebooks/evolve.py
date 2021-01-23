import numpy as np
import initialization as init
import evaluation as eval
import selection as sel
import recombination as rec
import mutation as mut


initialize = init.permutation
evaluate = eval.custom
select = sel.rank_based
mutate = mut.swap
reproduce = rec.pairwise
crossover = rec.order
replace = sel.rank_based

params = {'gens': 100,
          'n_off': 50,
          'n_pars': 100,
          'n_objs': 1,
          'len_meta': 0,
          'pop_size': 150,
          'len_gene': 100,
          'mut_rate': 0.5}

population = initialize(params)
population = evaluate(params, population)

for gen in range(params['gens']):
    parents = select(population, params['n_pars'])
    offspring = reproduce(params, parents, crossover)
    offspring = mutate(params, offspring)
    offspring = evaluate(params, offspring)
    population = replace(np.concatenate((population, offspring), axis=0), params['pop_size'])

    print(gen)
