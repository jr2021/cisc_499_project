import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
import pickle

def TSP(pop):
    dist = np.loadtxt('dist.txt')

    for ind in pop:
        ind['fitness'][0] += dist[0][ind['gene'][0]]
        ind['fitness'][0] += np.array([dist[ind['gene'][i - 1]][ind['gene'][i]] for i in range(1, configs.gene_size)]).sum()
        ind['fitness'][0] += dist[ind['gene'][-1]][0]

    return pop

# FIXME - default configurations
configs = Config()
configs.pop_size, configs.par_size, configs.off_size, configs.gene_size = 32, 16, 16, 99
configs.enc = Permutation(configs)
configs.eval = TSP
configs.num_objs = 1
configs.sel = Single(configs).rank_based
configs.pair = Pairing(configs).adjacent
configs.enc.min_value, configs.enc.max_value = 1, 99
configs.enc.rec = configs.enc.Recombination(configs, configs.enc.configs).order
configs.enc.mut = configs.enc.Mutation(configs, configs.enc.configs).swap
configs.rep = Single(configs).rank_based

def create_app():
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div(dbc.Button(id='start', children='Start'))
        
    @app.callback(
        Output('start', 'children'),
        Input('start', 'n_clicks'), prevent_initial_call = True
    )
    def run(n):
        if n:
            population = configs.enc.initialize()
            population = configs.eval(population)

            for i in range(0, 100):
                parents = configs.sel(population, configs.par_size)
                offspring = configs.pair(parents)
                offspring = configs.enc.mut(offspring)
                offspring = configs.eval(offspring)
                population = configs.rep(np.concatenate((population, offspring), axis=0), configs.pop_size)

            return 'Finished'
        
    return app