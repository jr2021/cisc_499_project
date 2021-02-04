import numpy as np


class Config:
    pop_size, par_size, off_size, gene_size = None, None, None, None
    prob_type, num_objs = None, None
    enc = None
    pair, sel, eval, rep = None, None, None, None


class Pairing:
    configs = None

    def __init__(self, configs):
        self.configs = configs

    def adjacent(self, pars):
        offs = np.empty(shape=self.configs.off_size, dtype=dict)

        for i in range(0, self.configs.off_size - 1, 2):
            offs[i], offs[i + 1] = self.configs.enc.rec(pars[i], pars[i + 1]), self.configs.enc.rec(pars[i + 1], pars[i])

        return offs


class Single:
    configs = None

    def __init__(self, configs):
        self.configs = configs

    def rank_based(self, pop, sel_size):
        return np.array(sorted(pop, key=lambda sol: sol['fitness'])[:sel_size])

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
    min_value, max_value = None, None
    rec, mut = None, None

    def __init__(self, configs):
        self.configs = configs

    def initialize(self):
        return np.array([{'gene': np.random.permutation(np.arange(start=self.min_value, stop=self.max_value + 1)),
                          'fitness': np.array([0 for _ in range(self.configs.num_objs)])} for _ in
                         range(self.configs.pop_size)])

    class Recombination:
        configs, perm_configs = None, None

        def __init__(self, configs, perm_configs):
            self.configs, self.perm_configs = configs, perm_configs

        def order(self, mother, father):
            x, y = np.random.randint(0, self.configs.gene_size), np.random.randint(0, self.configs.gene_size)
            off = {'gene': -np.ones(shape=self.configs.gene_size, dtype=np.int),
                   'fitness': np.array([0 for _ in range(self.configs.num_objs)])}

            off['gene'][min(x, y):max(x, y)] = mother['gene'][min(x, y):max(x, y)]

            j, k = max(x, y) - self.configs.gene_size, max(x, y) - self.configs.gene_size
            while j < min(x, y):
                if father['gene'][k] not in off['gene']:
                    off['gene'][j] = father['gene'][k]
                    j += 1
                k += 1

            return off

        def cycle(self, mother, father):
            pass

    class Mutation:
        configs, perm_configs = None, None

        def __init__(self, configs, perm_configs):
            self.configs, self.perm_configs = configs, perm_configs

        def swap(self, offs):
            for off in offs:
                i, j = np.random.randint(low=0, high=self.configs.gene_size), np.random.randint(low=0,
                                                                                                high=self.configs.gene_size)
                off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

            return offs

        def scramble(self, offs):
            pass
