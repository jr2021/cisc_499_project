import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
from Permutation import *
import pickle


def create_app(configs):
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='prob_type',
                                        options=[{'label': 'single-objective', 
                                                  'value': 'sing-obj'},
                                                 {'label': 'multi-objective', 
                                                  'value': 'multi-obj'}],
                                        placeholder='Objectiveness',
                                        disabled=False),
                           dcc.Dropdown(id='obj_one',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 1',
                                        disabled=True),
                           dcc.Dropdown(id='enc_type',
                                        options=[{'label': 'permutation', 
                                                  'value': 'perm'}],
                                        placeholder='Representation',
                                        disabled=True),
                           dcc.Input(id='gene_size',
                                     placeholder='Gene Size',
                                     type='number', 
                                     min=0, max=100,
                                     disabled=True),
                           dcc.Input(id='min_val',
                                     placeholder='Minimum Value',
                                     type='number', 
                                     min=0, max=100,
                                     disabled=True),
                           dcc.Input(id='max_val',
                                     placeholder='Maximum Value',
                                     type='number', 
                                     min=0, max=100,
                                     disabled=True),
                           dbc.Button(id='save', 
                                      children='Save',
                                      disabled=True)])   
    
    @app.callback(
         Output('obj_one', 'disabled'),
         Input('prob_type', 'value'), prevent_initial_call=True
    )
    def prob_type(value):
        if value == 'sing-obj':
            configs.prob_type = Single(configs)
        
        return False
    
    @app.callback(
         Output('enc_type', 'disabled'),
         Input('obj_one', 'value'), prevent_initial_call=True
    )
    def obj_one(value):
        if value == 'min':
            configs.objs = [min]
        else:
            configs.objs = [max]
        
        return False
    
    @app.callback(
         Output('gene_size', 'disabled'),
         Input('enc_type', 'value'), prevent_initial_call=True
    )
    def enc_type(value):
        if value == 'perm':
            configs.enc = Perm(configs)
        
        return False

    @app.callback(
         Output('min_val', 'disabled'),
         Input('gene_size', 'value'), prevent_initial_call=True
    )
    def gene_size(value):
        configs.gene_size = value
        
        return False
    
    
    @app.callback(
         Output('max_val', 'disabled'),
         Input('min_val', 'value'), prevent_initial_call=True
    )
    def min_val(value):
        configs.enc.min_value = value
        
        return False
    
    @app.callback(
         Output('prob_type', 'disabled'),
         Input('max_val', 'value'), prevent_initial_call=True
    )
    def max_val(value):
        configs.enc.max_value = value
        
        return False
        
    @app.callback(
        Output('save', 'disabled'),
        Input('save', 'n_clicks'),
        Input('prob_type', 'value'),
        Input('obj_one', 'value'),
        Input('enc_type', 'value'),
        Input('min_val', 'value'),
        Input('max_val', 'value'), prevent_initial_call = True
    )
    def enable_save(saveclicks, probvalue, encvalue, obj1value, minvalue, maxvalue):
        with open('configs.pkl', 'wb') as f:
            pickle.dump(configs, f)
        
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] in ['prob_type.value', 
                                             'obj_one.value', 
                                             'enc_type.value', 
                                             'min_val.value', 
                                             'max_val.value', 
                                             'gene_size.value']:
            return False
    
    return app