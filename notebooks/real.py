import numpy as np
import random

class Real:
    configs = None
    min_value, max_value = None, None
    rec, mut = None, None

    def __init__(self, configs):
        self.configs = configs

    def initialize(self):
        pass

    class Cross:
        configs, real_configs = None, None

        def __init__(self, configs, real_configs):
            self.configs, self.real_configs = configs, real_configs
            
        def get_functions(self):
            return ['whole']
        
        def pair(self, pars):
            offs = np.empty(shape=self.configs.off_size, dtype=dict)
            
            np.random.shuffle(pars)

            for i in range(0, self.configs.off_size - 1, 2):
                offs[i] = self.configs.rec(pars[i], pars[i + 1])
                offs[i + 1] = self.configs.rec(pars[i + 1], pars[i])
                
            return offs

        def whole(self, mother, father):
            pass

    class Mutation:
        configs, real_configs = None, None

        def __init__(self, configs, real_configs):
            self.configs, self.real_configs = configs, real_configs
            
        def get_functions(self):
            return ['uniform']

        def uniform(self, offs):
            for off in offs:
                for i in range(self.configs.gene_size):
                    if np.random.uniform(low=0, high=1) < self.configs.mut_rate:
                        off['gene'][i] = np.random.uniform(low=self.configs.min_value,
                                                           high=self.configs.max_value)
            return offs
