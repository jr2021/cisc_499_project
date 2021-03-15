
import numpy as np

class Integer:
    params = None

    def __init__(self, params):
        self.params = params
        self.params['min_value'], self.params['max_value'] = None, None
        self.params['rec_type'], self.params['mut_type'] = None, None
        self.params['n'] = None
        self.params['theta'] = None

    def initialize(self):
        return np.array([{'gene': np.random.randint(low=self.params['min_value'], 
                                                    high=self.params['max_value'], 
                                                    size=self.params['gene_size']),
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
            return ['n-point', 'uniform']

        def n_point(self, mother, father):
            off = {'gene': np.empty(shape=self.params['gene_size']),
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
        
        def uniform(self, mother, father):
            off = {'gene': np.empty(shape=self.params['gene_size']),
                   'fitness': np.array([0 for _ in range(self.params['num_objs'])])}
            
            for i in range(self.params['gene_size']):
                if np.random.uniform() < 0.5:
                    off['gene'][i] = mother['gene'][i]
                else:
                    off['gene'][i] = father['gene'][i]
                    
            return off

    class Mutation:
        params = None

        def __init__(self, params):
            self.params = params
            
        def get_functions(self):
            return ['random-resetting', 'creep']

        def random_resetting(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        off['gene'][i] = np.random.uniform(low=self.params['min_value'],
                                                           high=self.params['max_value'])
                        
            return offs
        
        def creep(self, offs):
            for off in offs:
                for i in range(self.params['gene_size']):
                    if np.random.uniform(low=0, high=1) < self.params['mut_rate']:
                        value = np.round(np.random.normal(loc=0, scale=self.params['theta']))
                        if value > 0:
                            off['gene'][i] = min(off['gene'][i] + value, self.params['max_value'])
                        else:
                            off['gene'][i] = max(off['gene'][i] + value, self.params['max_value'])
            
            return offs