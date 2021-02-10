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

def create_app(configs):
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='sel_type',
                                        options=[{'label' : opt, 'value': opt} 
                                                 for opt in configs.prob_type.get_functions()],
                                        placeholder='Selection',
                                        disabled=False),
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
                                         options=[{'label' : opt, 'value': opt} 
                                                  for opt in configs.prob_type.get_functions()],
                                         placeholder='Replacement',
                                         disabled=True),
                           dcc.Input(id='pop_size', 
                                     placeholder='Population Size',
                                     type='number', 
                                     min=4, max=128, 
                                     step=2, 
                                     disabled=True),
                           dcc.Input(id='par_size', 
                                     placeholder='Num. Parents',
                                     type='number', 
                                     min=2, max=64, 
                                     step=2, 
                                     disabled=True),
                           dcc.Input(id='off_size', 
                                     placeholder='Num. Offspring',
                                     type='number', 
                                     min=2, max=64, 
                                     step=2, 
                                     disabled=True),
                           dcc.Input(id='mut_rate',
                                     placeholder='Mutation Rate',
                                     type='number', 
                                     min=0, max=1, 
                                     step=0.1, 
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
        Output('pair_type', 'disabled'),
        Input('sel_type', 'value'), prevent_initial_call = True
    )
    def sel_sel(value): 
        if value == 'rank_based':
            configs.sel = configs.prob_type.rank_based
        return False
        
    @app.callback(
        Output('rec_type', 'disabled'),
        Input('pair_type', 'value'), prevent_initial_call = True
    )
    def pair_sel(value):
        if value == 'adjacent':
            configs.pair = Pairing(configs).adjacent
        return False
        
    @app.callback(
        Output('mut_type', 'disabled'),
        Input('rec_type', 'value'), prevent_initial_call = True
    )
    def rec_sel(value):
        if value == 'order':
            configs.enc.rec = configs.enc.Recombination(configs, configs.enc.configs).order
            
        return False
        
    @app.callback(
        Output('rep_type', 'disabled'),
        Input('mut_type', 'value'), prevent_initial_call = True
    )
    def mut_sel(value):
        if value == 'swap':
            configs.enc.mut = configs.enc.Mutation(configs, configs.enc.configs).swap
        
        return False
    
    @app.callback(
        Output('pop_size', 'disabled'),
        Input('rep_type', 'value'), prevent_initial_call = True
    )
    def rep_sel(value):
        if value == 'rank_based':
            configs.rep = configs.prob_type.rank_based
        
        return False
    
    @app.callback(
        Output('par_size', 'disabled'),
        Input('pop_size', 'value'), prevent_initial_call = True
    )
    def pop_size(value):
        configs.pop_size = value
        
        return False
    
    @app.callback(
        Output('off_size', 'disabled'),
        Input('par_size', 'value'), prevent_initial_call = True
    )
    def par_size(value):
        configs.par_size = value
        
        return False
    
    @app.callback(
        Output('mut_rate', 'disabled'),
        Input('off_size', 'value'), prevent_initial_call = True
    )
    def off_size(value):
        configs.off_size = value
        
        return False
    
    @app.callback(
        Output('sel_type', 'disabled'),
        Input('mut_rate', 'value'), prevent_initial_call = True
    )
    def mut_rate(value):
        configs.mut_rate = value
        
        return False
    
    
    @app.callback(
        Output('save', 'disabled'),
        Input('save', 'n_clicks'),
        Input('stop', 'n_clicks'),
        Input('sel_type', 'value'),
        Input('pair_type', 'value'),
        Input('rec_type', 'value'),
        Input('mut_type', 'value'),
        Input('rep_type', 'value'),
        Input('pop_size', 'value'),
        Input('par_size', 'value'),
        Input('off_size', 'value'),
        Input('mut_rate', 'value'), prevent_initial_call = True
    )
    def enable_save(saveclicks, stopclicks, selvalue, pairvalue, recvalue, mutratevalue, repvalue, popvalue, parvalue, offvalue, mutvalue):
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'stop.n_clicks':
            return False
        elif ctx.triggered[0]['prop_id'] in ['prob_type.value', 
                                             'sel_type.value', 
                                             'pair_type.value', 
                                             'rec_type.value', 
                                             'mut_type.value', 
                                             'rep_type.value', 
                                             'pop_size.value', 
                                             'par_size.value', 
                                             'off_size.value', 
                                             'mut_rate.value']:
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