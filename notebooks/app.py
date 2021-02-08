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
    app.layout = html.Div([dcc.Dropdown(id='prob_type',
                                        options=[{'label': 'single-obj', 
                                                  'value': 'sing-obj'},],
                                        placeholder='Objectiveness',
                                        disabled=False),
                           dcc.Dropdown(id='sel_type',
                                        options=[],
                                        placeholder='Selection',
                                        disabled=True),
                           dcc.Dropdown(id='pair_type',
                                        options=[{'label' : opt, 'value': opt}
                                                 for opt in Pairing(configs).get_functions()],
                                        placeholder='Pairing',
                                        disabled=True),
                           dcc.Dropdown(id='rec_type',
                                        options=[{'label' : opt, 'value': opt}
                                                 for opt in configs.enc.Recombination(configs,                                                                   configs.enc.configs).get_functions()],
                                        placeholder='Recombination',
                                        disabled=True),
                           dcc.Dropdown(id='mut_type',
                                        options=[{'label' : opt, 'value': opt}
                                                 for opt in configs.enc.Mutation(configs,         
                                                        configs.enc.configs).get_functions()],
                                        placeholder='Mutation',
                                        disabled=True),
                            dcc.Dropdown(id='rep_type',
                                         options=[],
                                         placeholder='Replacement',
                                         disabled=True),
                           dbc.Button(id='save', 
                                      children='Save',
                                      disabled=True), 
                           dbc.Button(id='start', 
                                      children='Start',
                                      disabled=True), 
                           dbc.Button(id='stop', 
                                      children='Stop',
                                      disabled=True),
                           dbc.Button(id='restart', 
                                      children='Restart',
                                      disabled=True),
                           dbc.Button(id='pause', 
                                      children='Pause',
                                      disabled=True),
                           dbc.Button(id='resume', 
                                      children='Resume',
                                      disabled=True),
                           dcc.Graph(id='custom'),
                           dcc.Interval(id='interval', 
                                        disabled=True)])
        
    @app.callback(
        Output('custom', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_custom(n):
        return configs.vis(configs.sel(population, 1)[0])

    
    @app.callback(
        Output('sel_type', 'options'),
        Output('rep_type', 'options'),
        Input('prob_type', 'value'), prevent_initial_call = True
    )
    def update_sel_options(value):
        if value == 'sing-obj':
            configs.prob_type = Single(configs)
        else:
            configs.prob_type = Multi(configs)
            
        options = [{'label' : opt, 'value': opt} for opt in configs.prob_type.get_functions()]
        return options, options

    @app.callback(
        Output('sel_type', 'disabled'),
        Input('prob_type', 'value'), prevent_initial_call = True
    )
    def enable_sel_type(value):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'prob_type.value':
            return False
        
    @app.callback(
        Output('pair_type', 'disabled'),
        Input('sel_type', 'value'), prevent_initial_call = True
    )
    def enable_pair_type(value):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'sel_type.value':
            return False
        
    @app.callback(
        Output('rec_type', 'disabled'),
        Input('pair_type', 'value'), prevent_initial_call = True
    )
    def enable_rec_type(value):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'pair_type.value':
            return False
        
    @app.callback(
        Output('mut_type', 'disabled'),
        Input('rec_type', 'value'), prevent_initial_call = True
    )
    def enable_mut_type(value):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'rec_type.value':
            return False
        
    @app.callback(
        Output('rep_type', 'disabled'),
        Input('mut_type', 'value'), prevent_initial_call = True
    )
    def enable_mut_type(value):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'mut_type.value':
            return False
    
    @app.callback(
        Output('save', 'disabled'),
        Input('save', 'n_clicks'),
        Input('prob_type', 'value'),
        Input('sel_type', 'value'),
        Input('pair_type', 'value'),
        Input('rec_type', 'value'),
        Input('mut_type', 'value'),
        Input('rep_type', 'value'), prevent_initial_call = True
    )
    def enable_save(saveclicks, probvalue, selvalue, pairvalue, recvalue, mutvalue, repvalue):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] in ['prob_type', 'sel_type.value', 'pair_type.value', 'rec_type.value', 'mut_type.value']:
            return False
    
    @app.callback(
        Output('start', 'disabled'),
        Input('start', 'n_clicks'),
        Input('save', 'n_clicks'), prevent_initial_call = True
    )
    def enable_start(startclicks, saveclicks):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            return False
        
    @app.callback(
        Output('pause', 'disabled'),
        Input('start', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'), prevent_initial_call = True
    )
    def enable_pause(startclicks, resumeclicks, stopclicks):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return False
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return False
        
    @app.callback(
        Output('resume', 'disabled'),
        Input('stop', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'), prevent_initial_call = True
    )
    def enable_resume(stopclicks, resumeclicks, pauseclicks):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'stop.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            return False
    
    @app.callback(
        Output('stop', 'disabled'),
        Input('stop', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'), prevent_initial_call = True
    )
    def enable_stop(stopclicks, resumeclicks, pauseclicks):
        ctx = dash.callback_context
        
        if ctx.triggered[0]['prop_id'] == 'stop.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
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