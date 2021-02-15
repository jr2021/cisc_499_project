import numpy as np
from Permutation import Perm


class Config:
    pop_size, par_size, off_size, gene_size = 5, None, None, None
    prob_type, num_objs, objs, obj_names = None, None, None, None
    enc = None
    sel, eval, rep, vis = None, None, None, None
    mut_rate = None


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