class Multi:
    configs = None

    def __init__(self, configs):
        self.configs = configs
        
    def get_functions(self):
        return ['nsga_ii']

    def NSGA_II(self, pop):
        pass