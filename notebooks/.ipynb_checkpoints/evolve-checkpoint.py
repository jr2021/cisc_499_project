import initialize as init

params = {'generations': 10,
          'num_children': 10,
          'num_parents': 10,
          'num_solutions': 20,
          'min_f': None,
          'max_f': None,
          'len_genome': None,
          'mutation rate': 0.5,
          'representation': init.permutation}

population = params['representation']()


