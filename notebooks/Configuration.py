import numpy as np
from Permutation import Perm


class Config:
    pop_size, par_size, off_size, gene_size = 5, None, None, None
    prob_type, num_objs, objs = None, 1, None
    enc = None
    pair, sel, eval, rep, vis = None, None, None, None, None
    mut_rate = None


class Pairing:
    configs = None

    def __init__(self, configs):
        self.configs = configs
        
    def get_functions(self):
        return ['adjacent']

    def adjacent(self, pars):
        offs = np.empty(shape=self.configs.off_size, dtype=dict)

        for i in range(0, self.configs.off_size - 1, 2):
            offs[i], offs[i + 1] = self.configs.enc.rec(pars[i], pars[i + 1]), self.configs.enc.rec(pars[i + 1], pars[i])

        return offs
    
    def random(self, pars):
        pass


class Single:
    configs = None

    def __init__(self, configs):
        self.configs = configs
        
    def get_functions(self):
        return ['rank-based']

    def rank_based(self, pop, sel_size):
        if self.configs.objs[0] == min:
            return np.array(sorted(pop, key=lambda sol: sol['fitness'][0])[:sel_size])
        else:
            return np.array(sorted(pop, key=lambda sol: sol['fitness'][0], reverse=True)[:sel_size])

    def tournament(self, pop):
        pass


class Multi:
    configs = None

    def __init__(self, configs):
        self.configs = configs
        
    def get_functions(self):
        return ['nsga_ii']

    def NSGA_II(self, pop):
        pass