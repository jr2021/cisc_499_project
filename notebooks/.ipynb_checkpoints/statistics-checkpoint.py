import numpy as np
import pickle
import json


class Statistics:

    def __init__(self, params):
        self.data = {'meta': params,
                     'evolution': {'all': {'f': [],
                                           'n': [],
                                           'k': []}},
                     'generational': {'gens': [],
                                      'avg': {'f': [],
                                              'n': [],
                                              'k': []},
                                      'min': {'f': [],
                                              'n': [],
                                              'k': []},
                                      'max': {'f': [],
                                              'n': [],
                                              'k': []},
                                      'all': {'f': [],
                                              'n': [],
                                              'k': [],
                                              'sol_sums': []}},
                     'final': {'pop': {},
                               'sols': [],
                               'sol_sums': None,
                               'f': [],
                               'n': [],
                               'k': []}}

    def update_dynamic(self, population, generation):
        self.set_generations(generation)
        self.set_all(population)

    def update_static(self, population):
        self.data['final']['pop'] = population
        self.data['final']['sol_sums'] = np.zeros(self.data['meta']['features'], dtype=int)

        for i in range(len(population)):
            self.data['final']['sol_sums'] = np.add(self.data['final']['sol_sums'], population[i]['data'])
            self.data['final']['sols'].append(population[i]['data'])
            self.data['final']['f'].append(population[i]['meta']['error'])
            self.data['final']['k'].append(population[i]['meta']['k_value'])
            self.data['final']['n'].append(population[i]['meta']['size'])

        self.set_minimums()
        self.set_averages()
        self.set_maximums()

    def set_generations(self, generation):
        self.data['generational']['gens'].append(generation)

    def set_minimums(self):
        for gen in range(self.data['meta']['generations']):
            self.data['generational']['min']['f'].append(min(self.data['generational']['all']['f'][gen]))
            self.data['generational']['min']['n'].append(min(self.data['generational']['all']['n'][gen]))
            self.data['generational']['min']['k'].append(min(self.data['generational']['all']['k'][gen]))

    def set_maximums(self):
        for gen in range(self.data['meta']['generations']):
            self.data['generational']['max']['f'].append(max(self.data['generational']['all']['f'][gen]))
            self.data['generational']['max']['n'].append(max(self.data['generational']['all']['n'][gen]))
            self.data['generational']['max']['k'].append(max(self.data['generational']['all']['k'][gen]))

    def set_averages(self):
        for gen in range(self.data['meta']['generations']):
            self.data['generational']['avg']['f'].append(np.array(self.data['generational']['all']['f'][gen]).mean())
            self.data['generational']['avg']['n'].append(np.array(self.data['generational']['all']['n'][gen]).mean())
            self.data['generational']['avg']['k'].append(np.array(self.data['generational']['all']['k'][gen]).mean())

    def set_all(self, population):
        f, k, n = [], [], []
        gen_sum = np.zeros(self.data['meta']['features'], dtype=int)

        for i in range(len(population)):
            f.append(population[i]['meta']['error'])
            k.append(population[i]['meta']['k_value'])
            n.append(population[i]['meta']['size'])
            gen_sum = np.add(gen_sum, population[i]['data'])
            self.data['evolution']['all']['f'].append(population[i]['meta']['error'])
            self.data['evolution']['all']['n'].append(population[i]['meta']['size'])
            self.data['evolution']['all']['k'].append(population[i]['meta']['k_value'])

        self.data['generational']['all']['f'].append(f)
        self.data['generational']['all']['n'].append(n)
        self.data['generational']['all']['k'].append(k)
        self.data['generational']['all']['sol_sums'].append(gen_sum)

