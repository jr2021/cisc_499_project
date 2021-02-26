import numpy as np

class Single:
    
    params = None

    def __init__(self, params):
        self.params = params
        self.params['gene_meta'] = {}
        self.params['tourn_size'] = 4 # must be less than par_size and pop_size

        
    def get_functions(self):
        return ['rank-based', 'tournament']

    def rank_based(self, pop, pop_size, sel_size):
        if self.params['objs'][0] == min:
            return np.array(sorted(pop, 
                                   key=lambda sol: sol['fitness'][0])[:sel_size])
        else:
            return np.array(sorted(pop, 
                                   key=lambda sol: sol['fitness'][0], 
                                   reverse=True)[:sel_size])

    def tournament(self, pop, pop_size, sel_size):
        winners = []
        for i in range(sel_size):
            indices = np.random.choice(a=pop_size, size=self.params['tourn_size'], replace=False)
            index = self.play(pop, indices)
            winners.append(pop[index])
        return np.array(winners)


    def play(self, pop, indices):
        if len(indices) == 1:
            return indices[0]
        else:
            left = self.play(pop, indices[int(len(indices) / 2):])
            right = self.play(pop, indices[:int(len(indices) / 2)])
            if self.params['objs'][0] == min:
                if pop[left]['fitness'][0] < pop[right]['fitness'][0]:
                    return left
                else:
                    return right
            else:
                if pop[left]['fitness'][0] > pop[right]['fitness'][0]:
                    return left
                else:
                    return right