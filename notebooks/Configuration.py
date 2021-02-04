import numpy as np


class Config:

    
    pop_size = 32
    par_size = 16
    off_size = 16
    gene_size = 99
    fit_eval = None
    prob_type, representation, pairing = None, None, None
    num_objs = 1
    pair, select, replace = None, None, None
    
    #FIXME
    def __init__(self):
        self.representation, self.prob_type, self.pairing = Permutation(self), Single(self), Pairing(self)
        self.pair, self.select, self.eval, self.replace = self.pairing.adjacent, self.prob_type.rank_based, self.TSP, self.prob_type.rank_based
    
    def TSP(pop):
        dist = np.loadtxt('dist.txt')

        for ind in pop:
            ind['fitness'][0] += dist[0][ind['gene'][0]]
            ind['fitness'][0] += np.array([dist[ind['gene'][i - 1]][ind['gene'][i]] for i in range(1, configs.gene_size)]).sum()
            ind['fitness'][0] += dist[ind['gene'][-1]][0]

        return pop

    
class Pairing:
    
    configs = None
    
    def __init__(self, configs):
        self.configs = configs

    def adjacent(self, pars):
        offs = np.empty(shape=self.off_size, dtype=dict)

        for i in range(0, self.off_size - 1, 2):
            offs[i], offs[i + 1] = self.rep.sel(pars[i], pars[i + 1]), self.rep.sel(pars[i + 1], pars[i])

        return offs

class Single:

    configs = None

    def __init__(self, configs):
        self.configs = configs

    def rank_based(self, pop):
        return np.array(sorted(pop, key=lambda sol: sol['fitness'])[:self.configs.par_size])
    
    def tournament(self, pop):
        pass
    

class Multi:
    
    configs = None

    def __init__(self, configs):
        self.configs = configs

    def NSGA_II(self, pop):
        pass
    
        
class Permutation:

    configs = None
    min_value, max_value = 1, 99
    recombination, mutation = None, None
    recombine, mutate = None, None
    identity = 'perm'

    # FIXME
    def __init__(self, configs):
        self.configs = configs
        self.recombination, self.mutation = self.Recombination(configs, self), self.Mutation(configs, self)
        self.recombine, self.mutate = self.recombination.order, self.mutation.swap

    def initialize(self):
        return np.array([{'gene': np.random.permutation(np.arange(start=self.min_value, stop=self.max_value + 1)), 
                          'fitness': np.array([0 for _ in range(self.configs.num_objs)])} for _ in range(self.configs.pop_size)])

    class Recombination:
        
        configs, perm_configs = None, None

        def __init__(self, configs, perm_configs):
            self.configs, self.perm_configs = configs, perm_configs

        def order(self, mother, father):
            x, y = np.random.randint(0, self.configs.gene_size), np.random.randint(0, self.configs.gene_size)
            off = {'gene': -np.ones(shape=self.configs.gene_size, dtype=np.int), 
                   'fitness': np.array([0 for _ in range(self.configs.num_objs)])}

            off['gene'][min(x, y):max(x, y)] = mother['gene'][min(x, y):max(x, y)]

            j, k = max(x, y) - self.config.gene_size, max(x, y) - self.configs.gene_size
            while j < min(x, y):
                if father['gene'][k] not in off['gene']:
                    off['gene'][j] = father['gene'][k]
                    j += 1
                k += 1

            return off
        
        def cycle(self, mother, father):
            pass

    class Mutation:

        config = None
        perm_config = None

        def __init__(self, configs, perm_configs):
            self.configs, self.perm_configs = configs, perm_configs


        def swap(self, offs):

            for off in offs:
                i, j = np.random.randint(low=0, high=self.configs.gene_size), np.random.randint(low=0, high=self.configs.gene_size)
                off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

            return offs
        
        def scramble(self, offs):
            pass

