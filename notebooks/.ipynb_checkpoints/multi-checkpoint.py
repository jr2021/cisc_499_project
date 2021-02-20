class Multi:
    params = None

    def __init__(self, params):
        self.params = params
        params['gene_meta'] = {'dominated': None, 
                               'dominates': None}
        
    def get_functions(self):
        return ['nsga_ii']

    def NSGA_II(self, pop, sel_size):
        sel = []

        fronts = self.fast_nondominated_sort(pop)

        j = 0
        while sel.size + fronts[j].size < sel_size:
            sel += fronts[j]
            j += 1

        sel += np.random.choice(a=fronts[j], size=sel_size - sel.size)

        return sel


    def fast_nondominated_sort(self, pop):
        fronts = [[]]

        for i in range(len(pop)):
            pop[i]['meta']['dominates'], pop[i]['meta']['dominated'] = set(), 0
            for j in range(len(pop)):
                results = []
                for k in range(self.params['objs']):
                    if self.params['objs'][k] == min:
                        if pop[i]['fitness'][k] < pop[j]['fitness'][k]:
                            results.append(True)
                        else:
                            results.append(False)
                    else:
                        if pop[i]['fitness'][k] > pop[j]['fitness'][k]:
                            results.append(True)
                        else:
                            results.append(False)
                if all(results):
                    pop[i]['meta']['dominates'].add(j)
                else:
                    pop[i]['meta']['dominated'] += 1
            if pop[i]['meta']['dominated'] == 0:
                fronts[0].append(population[i])

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