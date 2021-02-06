import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
from Permutation import *
from plotly import graph_objects as go
import pickle

# - these are all of the default configurations for the TSP

def TSP(pop):
    dist = np.loadtxt('dist.txt')

    for ind in pop:
        ind['fitness'][0] += dist[0][ind['gene'][0]]
        ind['fitness'][0] += np.array([dist[ind['gene'][i - 1]][ind['gene'][i]] 
                                       for i in range(1, configs.gene_size)]).sum()
        ind['fitness'][0] += dist[ind['gene'][-1]][0]

    return pop

def network(ind):
    locs = np.loadtxt('loc.txt')  
    
    fig = go.Figure(data=[go.Scatter(x=[locs[0][0]] 
                                        + [locs[0][ind['gene'][i]] for i in range(configs.gene_size)] 
                                        + [locs[0][-1]],
                                     y=[locs[1][0]] 
                                        + [locs[1][ind['gene'][i]] for i in range(configs.gene_size)] 
                                        + [locs[1][-1]],
                                     mode='lines')])
    return fig

configs = Config()
configs.pop_size, configs.par_size, configs.off_size, configs.gene_size = 64, 32, 32, 100
configs.enc = Perm(configs)
configs.eval, configs.vis = TSP, network
configs.num_objs = 1
configs.sel = Single(configs).rank_based
# configs.sel.obs = [min]
configs.pair = Pairing(configs).adjacent
configs.enc.min_value, configs.enc.max_value = 0, 99
configs.enc.rec = configs.enc.Recombination(configs, configs.enc.configs).order
configs.enc.mut = configs.enc.Mutation(configs, configs.enc.configs).swap
configs.rep = Single(configs).rank_based

# - end of default configurations

running = None
population = configs.enc.initialize()

def create_app():
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='selection',
                                        options=[{'label': 'foo', 'value': 'foo'},
                                                 {'label': 'bar', 'value': 'bar'}],
                                        value='foo',
                                        disabled=False),
                           dbc.Button(id='start', 
                                      children='Start',
                                      disabled=True), 
                           dbc.Button(id='stop', 
                                      children='Stop',
                                      disabled=False),
                           dbc.Button(id='restart', 
                                      children='Restart',
                                      disabled=False),
                           dbc.Button(id='pause', 
                                      children='Pause',
                                      disabled=False),
                           dbc.Button(id='resume', 
                                      children='Resume',
                                      disabled=False),
                           dcc.Graph(id='custom'),
                           dcc.Interval(id='interval', 
                                        disabled=True)])
        
    @app.callback(
        Output('custom', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_custom(n):
        return configs.vis(configs.sel(population, 1)[0])
    
#     @app.callback(
#         Output('start', 'disabled'),
#         Input('selection', 'value'), prevent_initial_call = True
#     )
#     def selection(n):
#         False
    
    @app.callback(
        Output('start', 'disabled'),
        Input('start', 'n_clicks'),
        Input('selection', 'value'), prevent_initial_call = True
    )
    def start(n, value):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'selection.value':
            return False
        
#     @app.callback(
#         Output('pause', 'disabled'),
#         Input('pause', 'n_clicks'), prevent_initial_call = True
#     )
#     def pause(n):
#         True
        
#     @app.callback(
#         Output('stop', 'disabled'),
#         Input('stop', 'n_clicks'), prevent_initial_call = True
#     )
#     def stop(n):
#         True
    
#     @app.callback(
#         Output('resume', 'disabled'),
#         Input('resume', 'n_clicks'), prevent_initial_call = True
#     )
#     def resume(n):
#         True
        
    def run_GA():
        global population, running
        population = configs.enc.initialize()
        population = configs.eval(population)

        while running:
            parents = configs.sel(population, configs.par_size)
            offspring = configs.pair(parents)
            offspring = configs.enc.mut(offspring)
            offspring = configs.eval(offspring)
            population = configs.rep(np.concatenate((population, offspring), axis=0), 
                                     configs.pop_size)
    
        
    return app