import numpy as np


class Config:

    rep = None
    pop_size = None
    par_size = None
    off_size = None
    gene_size = None
    fit_eval = None

    class Recombination:

        def pairwise(self, pars):
            offs = np.empty(shape=self.off_size, dtype=dict)

            for i in range(0, self.off_size - 1, 2):
                offs[i], offs[i + 1] = self.rep.sel(pars[i], pars[i + 1]), self.rep.sel(pars[i + 1], pars[i])

            return offs
        
class Permutation:

    config = None
    min_value, max_value = None, None
    select, mutate, cross, replace = None, None, None, None


    def __init__(self, config):
        self.config = config

    def initialize(self):
        return np.array([{'gene': np.random.permutation(self.length), 'fitness': np.array([0 for _ in range(self.config.num_objs)])} for _ in range(self.config.pop_size)])

    class Selection:

        config = None
        perm_config = None

        def __init__(self, config, perm_config):
            self.config, self.perm_config = config, perm_config

        def rank_based(self, pop):
            return np.array(sorted(pop, key=lambda sol: sol['fitness'])[:self.config.par_size])


    class Crossover:

        config = None
        perm_config = None

        def __init__(self, config, perm_config):
            self.config, self.perm_config = config, perm_config

        def order(self, mother, father):
            x, y = np.random.randint(0, self.config.gene_size), np.random.randint(0, self.config.gene_size)
            off = {'gene': -np.ones(shape=self.config.gene_size, dtype=np.int), 'fitness': np.array([0 for _ in range(self.config.num_objs)])}

            off['gene'][min(x, y):max(x, y)] = mother['gene'][min(x, y):max(x, y)]

            j, k = max(x, y) - self.config.gene_size, max(x, y) - self.config.gene_length
            while j < min(x, y):
                if father['gene'][k] not in off['gene']:
                    off['gene'][j] = father['gene'][k]
                    j += 1
                k += 1

            return off

    class Mutation:

        config = None
        perm_config = None

        def __init__(self, config, perm_config):
            self.config, self.perm_config = config, perm_config


        def swap(self, offs):

            for off in offs:
                i, j = np.random.randint(low=0, high=self.config.gene_size), np.random.randint(low=0, high=self.config.gene_size)
                off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

            return offs

    class Replacement:

        config = None
        perm_config = None

        def __init__(self, config, perm_config):
            self.config, self.perm_config = config, perm_config

        def rank_based(self, pop):
            return np.array(sorted(pop, key=lambda sol: sol['fitness'])[:self.config.pop_size])

