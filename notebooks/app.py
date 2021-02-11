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
from threading import Thread

Population, Running, Configs = None, None, None

def create_app(configs):
    global Configs
    Configs = configs
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='sel_type',
                                        options=[{'label' : opt, 'value': opt} 
                                                 for opt in Configs.prob_type.get_functions()],
                                        placeholder='Selection',
                                        disabled=False),
                           dcc.Dropdown(id='pair_type',
                                        options=[{'label' : opt, 'value': opt}
                                                 for opt in Pairing(Configs).get_functions()],
                                        placeholder='Pairing',
                                        disabled=True),
                           dcc.Dropdown(id='rec_type',
                                        options=[{'label' : opt, 'value': opt}
                                                 for opt in Configs.enc.Recombination(Configs,                                                                 configs.enc.configs).get_functions()],
                                        placeholder='Recombination',
                                        disabled=True),
                           dcc.Dropdown(id='mut_type',
                                        options=[{'label' : opt, 'value': opt}
                                                 for opt in Configs.enc.Mutation(Configs,         
                                                        Configs.enc.configs).get_functions()],
                                        placeholder='Mutation',
                                        disabled=True),
                            dcc.Dropdown(id='rep_type',
                                         options=[{'label' : opt, 'value': opt} 
                                                  for opt in Configs.prob_type.get_functions()],
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
                           dcc.Graph(id='custom',
                                     figure=go.Figure()),
                           dcc.Graph(id='heatmap',
                                     figure=go.Figure()),
                           dcc.Interval(id='interval', 
                                        disabled=True,
                                        interval=500)])
        
    @app.callback(
        Output('custom', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_custom(n):
        return Configs.vis(Configs.sel(Population, 1)[0])    
    
    @app.callback(
        Output('heatmap', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_heatmap(n):
        return go.Figure(data=[go.Heatmap(z=[ind['gene'] for ind in Population])])   
    
    @app.callback(
        Output('pair_type', 'disabled'),
        Input('sel_type', 'value'), prevent_initial_call = True
    )
    def enable_pair(value): 
        if value == 'rank-based':
            Configs.sel = Configs.prob_type.rank_based
        return False
        
    @app.callback(
        Output('rec_type', 'disabled'),
        Input('pair_type', 'value'), prevent_initial_call = True
    )
    def enable_rec(value):
        if value == 'adjacent':
            Configs.pair = Pairing(configs).adjacent
        return False
        
    @app.callback(
        Output('mut_type', 'disabled'),
        Input('rec_type', 'value'), prevent_initial_call = True
    )
    def enable_mut(value):
        if value == 'order':
            Configs.enc.rec = Configs.enc.Recombination(Configs, Configs.enc.configs).order
            
        return False
        
    @app.callback(
        Output('rep_type', 'disabled'),
        Input('mut_type', 'value'), prevent_initial_call = True
    )
    def enable_rep(value):
        if value == 'swap':
            Configs.enc.mut = Configs.enc.Mutation(Configs, Configs.enc.configs).swap
        
        return False
    
    @app.callback(
        Output('pop_size', 'disabled'),
        Input('rep_type', 'value'), prevent_initial_call = True
    )
    def enable_pop_size(value):
        if value == 'rank-based':
            Configs.rep = Configs.prob_type.rank_based
        
        return False
    
    @app.callback(
        Output('par_size', 'disabled'),
        Input('pop_size', 'value'), prevent_initial_call = True
    )
    def enable_par_size(value):
        Configs.pop_size = value
        
        return False
    
    @app.callback(
        Output('off_size', 'disabled'),
        Input('par_size', 'value'), prevent_initial_call = True
    )
    def enable_off_size(value):
        Configs.par_size = value
        
        return False
    
    @app.callback(
        Output('mut_rate', 'disabled'),
        Input('off_size', 'value'), prevent_initial_call = True
    )
    def enable_mut_rate(value):
        Configs.off_size = value
        
        return False
    
    @app.callback(
        Output('sel_type', 'disabled'),
        Input('mut_rate', 'value'), prevent_initial_call = True
    )
    def mut_rate(value):
        Configs.mut_rate = value
        
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
    def enable_save(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11):
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
        
    @app.callback(
        Output('interval', 'disabled'),
        Input('pause', 'n_clicks'),
        Input('start', 'n_clicks'),
        Input('resume', 'n_clicks'), prevent_initial_call = True
    )
    def enable_interval(pauseclicks, startclicks, resumeclicks): 
        global Running
        
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            Running = [False]
            return True
        elif ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            Running = [True]
            Thread(target=start_GA, args=()).start()
            return False    
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            Running = [True]
            Thread(target=resume_GA, args=()).start()
            return False

    return app


def start_GA():
    global Population
    
    Population = Configs.enc.initialize()
    Population = Configs.eval(Population)

    while Running[0]:
        parents = Configs.sel(Population, Configs.par_size)
        offspring = Configs.pair(parents)
        offspring = Configs.enc.mut(offspring)
        offspring = Configs.eval(offspring)
        Population = Configs.rep(np.concatenate((Population, offspring), axis=0), 
                                 Configs.pop_size) 
        print(Population)
        
def resume_GA():
    global Population
    
    while Running[0]:
        parents = Configs.sel(Population, Configs.par_size)
        offspring = Configs.pair(parents)
        offspring = Configs.enc.mut(offspring)
        offspring = Configs.eval(offspring)
        Population = Configs.rep(np.concatenate((Population, offspring), axis=0), 
                                 Configs.pop_size) 
    
        print(Population)