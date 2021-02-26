import numpy as np

class Multi:
    params = None

    def __init__(self, params):
        self.params = params
        self.params['gene_meta'] = {'dominated': None, 
                                    'dominates': None}
        
    def get_functions(self):
        return ['NSGA-II']

    def NSGA_II(self, pop, pop_size, sel_size):
        sel = []

        print(pop_size, sel_size)
        
        fronts = self.fast_nondominated_sort(pop, pop_size)

        print(fronts)
        
        j = 0
        while len(sel) + len(fronts[j]) < sel_size:
            sel += fronts[j]
            j += 1
            print(j)

        sel += np.random.choice(a=fronts[j], size=sel_size - len(sel), replace=False).tolist()

        return np.array(sel)


    def fast_nondominated_sort(self, pop, pop_size):
        fronts = [[]]
        
        for i in range(pop_size):
            pop[i]['meta']['dominates'], pop[i]['meta']['dominated'] = set(), 0   
            for j in range(pop_size):
                results = []
                for k in range(self.params['num_objs']):
                    if self.params['objs'][k] == min:
                        if pop[i]['fitness'][k] < pop[j]['fitness'][k]:
                            results.append(True)
                        elif pop[j]['fitness'][k] < pop[i]['fitness'][k]:
                            results.append(False)
                    else:
                        if pop[i]['fitness'][k] > pop[j]['fitness'][k]:
                            results.append(True)
                        elif pop[j]['fitness'][k] > pop[i]['fitness'][k]:
                            results.append(False)
                if results == [True for _ in range(self.params['num_objs'])]:
                    pop[i]['meta']['dominates'].add(j)
                elif results == [False for _ in range(self.params['num_objs'])]:
                    pop[i]['meta']['dominated'] += 1
            if pop[i]['meta']['dominated'] == 0:
                fronts[0].append(pop[i])
                
        print(fronts[0])
            
        k = 0
        while len(fronts[k]) > 0:
            fronts.append([])
            for i in range(len(fronts[k])):
                for j in fronts[k][i]['meta']['dominates']:
                    pop[j]['meta']['dominated'] -= 1
                    if pop[j]['meta']['dominated'] == 0:
                        fronts[k + 1].append(pop[j])
            k += 1
   
        return fronts