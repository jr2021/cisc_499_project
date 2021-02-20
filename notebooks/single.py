import numpy as np

class Single:
    
    params = None

    def __init__(self, params):
        self.params = params
        self.params['gene_meta'] = None
        
    def get_functions(self):
        return ['rank-based']

    def rank_based(self, pop, sel_size):
        if self.params['objs'][0] == min:
            return np.array(sorted(pop, 
                                   key=lambda sol: sol['fitness'][0])[:sel_size])
        else:
            return np.array(sorted(pop, 
                                   key=lambda sol: sol['fitness'][0], 
                                   reverse=True)[:sel_size])

    def tournament(self, pop):
        pass