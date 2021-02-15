import numpy as np
import pickle
import json


class Statistics:
    
    def __init__(self, configs):
        self.configs = configs
        self.gen_level = {'fitness': {'mins': [[], [], []],
                                    'avgs': [[], [], []],
                                    'maxs': [[], [], []]}}

    def update_dynamic(self, population):
        self.set_mins(population)
        self.set_avgs(population)
        self.set_maxs(population)

    def set_mins(self, population):
        for i in range(self.configs.num_objs):
            self.gen_level['fitness']['mins'][i].append(np.array([ind['fitness'][i] for ind in population]).min())
            
    def set_maxs(self, population):
        for i in range(self.configs.num_objs):
            self.gen_level['fitness']['maxs'][i].append(np.array([ind['fitness'][i] for ind in population]).max())
        
    def set_avgs(self, population):
        for i in range(self.configs.num_objs):
            self.gen_level['fitness']['avgs'][i].append(np.array([ind['fitness'][i] for ind in population]).mean())
        


