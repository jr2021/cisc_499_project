import numpy

def permutation(params):
    return np.array([{'genome' : np.random.permutation(params['len_genome']), 'fitness': None}])