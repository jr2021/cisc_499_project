import numpy as np

class Real:
    params = None

    def __init__(self, params):
        self.params = params
        self.params['min_value'], self.params['max_value'] = None, None
        self.params['rec_type'], self.params['mut_type'] = None, None
        self.params['alpha'], self.params['theta'] = 0.75, 5

    def initialize(self):
        return np.array([{'gene': np.random.uniform(low=self.params['min_value'],
                                                    high=self.params['max_value'],
                                                    size=self.params['gene_size']),
                          'fitness': np.array([0 for _ in range(self.params['num_objs'])])} 
                                                 for _ in range(self.params['pop_size'])])

    def mate(self, pars):
        offs = np.empty(shape=self.params['off_size'], dtype=dict)
        
        for i in range(0, self.params['off_size'] - 1, 2):
            j = np.random.randint(low=0, high=self.params['par_size'])
            k = np.random.randint(low=0, high=self.params['par_size'])
            offs[i] = self.params['rec_type'](pars[j], pars[k], self.params['alpha'])
            offs[i + 1] = self.params['rec_type'](pars[k], pars[j], 1 - self.params['alpha'])

        return offs
    
    class Cross:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['whole-arithmetic', 'simple-arithmetic']

        def whole_arithmetic(self, mother, father, alpha):
            return {'gene': (alpha * mother['gene'] + (1 - alpha) * father['gene']) / 2,
                    'fitness': np.array([0 for _ in range(self.params['num_objs'])])}
        
        def simple_arithmetic(self, mother, father, alpha):
            off =  {'gene': np.empty(shape=(self.params['gene_size']), dtype=float),
                    'fitness': np.array([0 for _ in range(self.params['num_objs'])])}
            k = np.random.randint(low=0, high=self.params['gene_size'])
            
            off['gene'][0:k] = mother['gene'][0:k]
            off['gene'][k:] = (alpha * mother['gene'][k:] + (1 - alpha) * father['gene'][k:]) / 2
            
            return off
            

    class Mutation:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['uniform', 'non-uniform']

        def uniform(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        off['gene'][i] = np.random.uniform(low=self.params['min_value'],
                                                           high=self.params['max_value'])

            return offs
        
        def non_uniform(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        value = np.random.normal(loc=0, scale=self.params['theta'])
                        if value > 0:
                            off['gene'][i] = min(off['gene'][i] + value, self.params['max_value'])
                        else:
                            off['gene'][i] = max(off['gene'][i] + value, self.params['min_value'])
            
            return offs