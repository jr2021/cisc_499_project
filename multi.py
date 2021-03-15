import numpy as np

class Multi:
    params = None

    def __init__(self, params):
        self.params = params
        
    def get_functions(self):
        return ['NSGA-II']

    def NSGA_II(self, pop, pop_size, sel_size):
        sel = []
        
        fronts = self.fast_nondominated_sort(pop, pop_size)
        
        j = 0
        while len(sel) + len(fronts[j]) < sel_size:
            for ind in fronts[j]:
                sel.append(ind)
            j += 1

        np.random.shuffle(fronts[j])
        
        k = 0
        while len(sel) < sel_size:
            sel.append(fronts[j][k])
            k += 1

        return sel


    def fast_nondominated_sort(self, pop, pop_size):
        fronts = [[] for _ in range(pop_size)]
        
        for i in range(pop_size):
            pop[i]['dominates'], pop[i]['dominated'] = set(), 0
            for j in range(pop_size):
                results = []
                for k in range(self.params['num_objs']):
                    if self.params['objs'][k] == min:
                        if pop[i]['fitness'][k] < pop[j]['fitness'][k]:
                            results.append(True)
                        elif pop[j]['fitness'][k] < pop[i]['fitness'][k]:
                            results.append(False)
                        else:
                            results.append(None)
                    elif self.params['objs'][k] == max:
                        if pop[i]['fitness'][k] > pop[j]['fitness'][k]:
                            results.append(True)
                        elif pop[j]['fitness'][k] > pop[i]['fitness'][k]:
                            results.append(False)
                        else:
                            results.append(None)
                if results == [True for _ in range(self.params['num_objs'])]:
                    pop[i]['dominates'].add(j)
                elif results == [False for _ in range(self.params['num_objs'])]:
                    pop[i]['dominated'] += 1
            if pop[i]['dominated'] == 0:
                fronts[0].append(pop[i])
        
        k = 0
        while len(fronts[k]) > 0:
            for i in range(len(fronts[k])):
                for j in fronts[k][i]['dominates']: 
                    pop[j]['dominated'] -= 1
                    if pop[j]['dominated'] == 0:
                        fronts[k + 1].append(pop[j])
            k += 1
   
        return fronts