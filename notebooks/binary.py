import numpy as np

class Binary:
    configs = None
    rec, mut = None, None

    def __init__(self, configs):
        self.configs = configs

    def initialize(self):
        return np.array([{'gene': np.random.randint(low=0, high=2, size=self.configs.gene),
                          'fitness': np.array([0 for _ in range(self.configs.num_objs)])} 
                                                 for _ in range(self.configs.pop_size)])

    class Cross:
        configs, bin_configs = None, None

        def __init__(self, configs, bin_configs):
            self.configs, self.bin_configs = configs, bin_configs
            
        def get_functions(self):
            return ['n-point']
        
        def pair(self, pars):
            offs = np.empty(shape=self.configs.off_size, dtype=dict)
            
            np.random.shuffle(pars)

            for i in range(0, self.configs.off_size - 1, 2):
                offs[i] = self.configs.rec(pars[i], pars[i + 1])
                offs[i + 1] = self.configs.rec(pars[i + 1], pars[i])
                
            return offs

        def n_point(self, mother, father):
            pass

    class Mutation:
        configs, bin_configs = None, None

        def __init__(self, configs, bin_configs):
            self.configs, self.bin_configs = configs, bin_configs
            
        def get_functions(self):
            return ['bit-flip']

        def flip(self, offs):
            pass