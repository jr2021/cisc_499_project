
import numpy as np

class Binary:
    params = None

    def __init__(self, params):
        self.params = params
        self.params['min_value'], self.params['max_value'] = None, None
        self.params['rec_type'], self.params['mut_type'] = None, None
        self.params['n'] = None

    def initialize(self):
        return np.array([{'gene': np.random.randint(low=0, high=2, size=self.configs.gene),
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
            return ['n-point']

        def n_point(self, mother, father):
            off = {'gene': np.empty(size=self.params['gene_size']),
                   'fitness': np.array([0 for _ in range(self.params['num_objs'])])}
            
            points = np.sort(np.random.choice(a=self.params['gene_size'], 
                                              size=self.params['n'], 
                                              replace=False))
            
            off['gene'][0:points[0]] = mother['gene'][0:points[0]]
            
            parent = father
            for i in range(len(points) - 1):
                off['gene'] = parent['gene'][points[i]:points[i + 1]]
                if parent == mother:
                    parent = father
                else:
                    parent = mother
     
            off['gene'][points[-1]:] = parent['gene'][points[-1]:]
                    
            return off

    class Mutation:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['bit-flip']

        def bit_flip(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        off['gene'][i] = np.random.uniform(low=0, high=2)

            return offs