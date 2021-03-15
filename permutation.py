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
        
        for i in range(0, self.params['off_size'] - 1, 2):
            j = np.random.randint(low=0, high=self.params['par_size'])
            k = np.random.randint(low=0, high=self.params['par_size'])
            offs[i] = self.params['rec_type'](pars[j], pars[k])
            offs[i + 1] = self.params['rec_type'](pars[k], pars[j])

        return offs
    
    class Cross:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['order', 'partially-mapped']

        def order(self, mother, father):
            x = np.random.randint(low=0, high=self.params['gene_size'])
            y = np.random.randint(low=x, high=self.params['gene_size'])
            off = {'gene': -np.ones(shape=self.params['gene_size'], dtype=int),
                   'fitness': np.array([0 for _ in range(self.params['num_objs'])])}

            off['gene'][x:y] = mother['gene'][x:y]

            j, k = y - self.params['gene_size'], y - self.params['gene_size']
            while j < x:
                if father['gene'][k] not in off['gene']:
                    off['gene'][j] = father['gene'][k]
                    j += 1
                k += 1

            return off

        def PMX(self, mother, father):
            x = np.random.randint(low=0, high=self.params['gene_size'])
            y = np.random.randint(low=x, high=self.params['gene_size'])
            
            off = {'gene': -np.ones(shape=self.params['gene_size'], dtype=int),
                   'fitness': np.array([0 for _ in range(self.params['num_objs'])])}

            off['gene'][x:y] = mother['gene'][x:y]

            for i in range(x, y):
                if father['gene'][i] not in off['gene']:
                    k = i
                    while off['gene'][k] != -1:
                        j = off['gene'][k]
                        k = np.where(father['gene'] == j)
                    off['gene'][k] = father['gene'][i]

            for i in range(self.params['gene_size']):
                if off['gene'][i] == -1:
                    off['gene'][i] = father['gene'][i]

            return off

    class Mutation:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['swap', 'scramble']

        def swap(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        j = np.random.randint(low=0, high=self.params['gene_size'])
                        off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

            return offs
        
        def scramble(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        j = np.random.randint(low=0, high=self.params['gene_size'])
                        k = np.random.randint(low=j, high=self.params['gene_size']) 
                        np.random.shuffle(off['gene'][j:k])

            return offs