import numpy as np
import pickle
import json


class Statistics:
    
    params = None
    
    def __init__(self, params):
        self.params = params
        self.gen_level = {'fitness': {'mins': [[], [], []],
                                      'avgs': [[], [], []],
                                      'maxs': [[], [], []]}}

    def clear(self):
        self.adhoc = {'fitness': {'mins': [[], [], []],
                                  'avgs': [[], [], []],
                                  'maxs': [[], [], []]}}
        self.posthoc = {'population': {'all': []}}
        
    def update_dynamic(self, population):
        self.set_fitt_mins(population)
        self.set_fitt_avgs(population)
        self.set_fitt_maxs(population)
        
    def update_static(self, population):
        self.set_pop(population)

    def set_fitt_mins(self, population):
        for i in range(self.params['num_objs']):
            self.adhoc['fitness']['mins'][i].append(np.array([ind['fitness'][i] for ind in population]).min())
            
    def set_fitt_maxs(self, population):
        for i in range(self.params['num_objs']):
            self.adhoc['fitness']['maxs'][i].append(np.array([ind['fitness'][i] for ind in population]).max())
        
    def set_fitt_avgs(self, population):
        for i in range(self.params['num_objs']):
            self.adhoc['fitness']['avgs'][i].append(np.array([ind['fitness'][i] for ind in population]).mean())
            
    def set_pop(self, population):
        self.posthoc['population']['all'] = [ind['gene'] for ind in population]
            
        


