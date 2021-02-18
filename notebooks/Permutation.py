import numpy as np

class Perm:
    params = None

    def __init__(self, params):
        self.params = params
        self.params['min_value'], self.params['max_value'] = None, None
        self.params['rec_type'], self.params['mut_type'] = None, None

    def initialize(self):
        return np.array([{'gene': np.random.permutation(np.arange(start=self.params['min_value'], 
                                stop=self.params['max_value'] + 1)),
                          'fitness': np.array([0 for _ in range(self.params['num_objs'])])} 
                                                 for _ in range(self.params['pop_size'])])

    def mate(self, pars):
        offs = np.empty(shape=self.params['off_size'], dtype=dict)

        np.random.shuffle(pars)

        for i in range(0, self.params['off_size'] - 1, 2):
            offs[i] = self.params['rec_type'](pars[i], pars[i + 1])
            offs[i + 1] = self.params['rec_type'](pars[i + 1], pars[i])

        return offs
    
    class Cross:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['order']

        def order(self, mother, father):
            x = np.random.randint(0, self.params['gene_size'])
            y = np.random.randint(0, self.params['gene_size'])
            off = {'gene': -np.ones(shape=self.params['gene_size'], dtype=np.int),
                   'fitness': np.array([0 for _ in range(self.params['num_objs'])])}

            off['gene'][min(x, y):max(x, y)] = mother['gene'][min(x, y):max(x, y)]

            j, k = max(x, y) - self.params['gene_size'], max(x, y) - self.params['gene_size']
            while j < min(x, y):
                if father['gene'][k] not in off['gene']:
                    off['gene'][j] = father['gene'][k]
                    j += 1
                k += 1

            return off

        def cycle(self, mother, father):
            pass

    class Mutation:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['swap']

        def swap(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        j = np.random.randint(low=0, high=self.params['gene_size'])
                        off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

            return offs