import numpy as np

class Perm:
    configs = None
    min_value, max_value = None, None
    rec, mut = None, None

    def __init__(self, configs):
        self.configs = configs

    def initialize(self):
        return np.array([{'gene': np.random.permutation(np.arange(start=self.min_value, 
                                                                  stop=self.max_value + 1)),
                          'fitness': np.array([0 for _ in range(self.configs.num_objs)])} 
                                                 for _ in range(self.configs.pop_size)])

    class Recombination:
        configs, perm_configs = None, None

        def __init__(self, configs, perm_configs):
            self.configs, self.perm_configs = configs, perm_configs
            
        def get_functions(self):
            return [self.order, self.cycle]

        def order(self, mother, father):
            x = np.random.randint(0, self.configs.gene_size)
            y = np.random.randint(0, self.configs.gene_size)
            off = {'gene': -np.ones(shape=self.configs.gene_size, dtype=np.int),
                   'fitness': np.array([0 for _ in range(self.configs.num_objs)])}

            off['gene'][min(x, y):max(x, y)] = mother['gene'][min(x, y):max(x, y)]

            j, k = max(x, y) - self.configs.gene_size, max(x, y) - self.configs.gene_size
            while j < min(x, y):
                if father['gene'][k] not in off['gene']:
                    off['gene'][j] = father['gene'][k]
                    j += 1
                k += 1

            return off

        def cycle(self, mother, father):
            pass

    class Mutation:
        configs, perm_configs = None, None

        def __init__(self, configs, perm_configs):
            self.configs, self.perm_configs = configs, perm_configs
            
        def get_functions(self):
            return [self.swap, self.scramble]

        def swap(self, offs):
            for off in offs:
                i = np.random.randint(low=0, high=self.configs.gene_size)
                j = np.random.randint(low=0, high=self.configs.gene_size)
                off['gene'][i], off['gene'][j] = off['gene'][j], off['gene'][i]

            return offs

        def scramble(self, offs):
            pass
