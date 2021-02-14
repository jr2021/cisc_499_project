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

global_min, global_max = 0, 100

def create_app(configs):
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='prob_type',
                                        options=[{'label': 'single-objective', 
                                                  'value': 'sing-obj'},
                                                 {'label': 'multi-objective', 
                                                  'value': 'multi-obj'}],
                                        placeholder='Objectiveness'),
                           dcc.Input(id='num_objs',
                                     placeholder='Number of objectives',
                                     type='number', 
                                     min=1, max=3),
                           dcc.Input(id='obj_1_name',
                                     placeholder='Objective 1 name',
                                     type='text'),
                           dcc.Dropdown(id='obj_1_goal',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 1 goal'),
                           dcc.Input(id='obj_2_name',
                                     placeholder='Objective 2 name',
                                     type='text'),
                           dcc.Dropdown(id='obj_2_goal',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 2 goal'),
                           dcc.Input(id='obj_3_name',
                                     placeholder='Objective 3 name',
                                     type='text'),
                           dcc.Dropdown(id='obj_3_goal',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 3 goal'),
                           dcc.Dropdown(id='enc_type',
                                        options=[{'label': 'permutation', 
                                                  'value': 'perm'}],
                                        placeholder='Permutation'),
                           dcc.Input(id='gene_size',
                                     placeholder='Gene Size',
                                     type='number', 
                                     min=0, max=100),
                           dcc.Input(id='min_val',
                                     placeholder='Minimum Value',
                                     type='number', 
                                     min=0, max=100),
                           dcc.Input(id='max_val',
                                     placeholder='Maximum Value',
                                     type='number', 
                                     min=0, max=100),
                           dbc.Button(id='save', 
                                      children='Save static parameters')])   
    
    
    @app.callback(
         Output('obj_1_name', 'disabled'),
         Output('obj_2_name', 'disabled'),
         Output('obj_3_name', 'disabled'),
         Output('obj_1_goal', 'disabled'),
         Output('obj_2_goal', 'disabled'),
         Output('obj_3_goal', 'disabled'),
         Input('num_objs', 'value')
    )
    def objs_enable(num_objs):
        if num_objs:
            if num_objs == 1:
                return False, True, True, False, True, True
            elif num_objs == 2:
                return False, False, True, False, False, True
            else:
                return False, False, False, False, False, False
        else:
            return True, True, True, True, True, True
            
    
    @app.callback(
         Output('min_val', 'disabled'),
         Output('max_val', 'disabled'),
         Input('enc_type', 'value'), prevent_initial_call=True
    )
    def min_max_enable(enc_type):
        if enc_type == 'perm':
            return True, True
        else:
            return False, False
        
    @app.callback(
         Output('min_val', 'value'),
         Output('max_val', 'value'),
         Input('gene_size', 'value'),
         State('enc_type', 'value'),
         State('min_val', 'value'), 
         State('max_val', 'value'), prevent_initial_call=True
    )
    def min_max_value(gene_size, enc_type, min_val, max_val):
        if gene_size:
            if enc_type == 'perm':
                return 0, gene_size - 1
        return min_val, max_val      
    
    @app.callback(
         Output('save', 'disabled'),
         Input('save', 'n_clicks'),
         State('prob_type', 'value'),
         State('num_objs', 'value'),
         State('obj_1_name', 'value'),
         State('obj_2_name', 'value'),
         State('obj_3_name', 'value'),
         State('obj_1_goal', 'value'),
         State('obj_2_goal', 'value'),
         State('obj_3_goal', 'value'),
         State('enc_type', 'value'),
         State('gene_size', 'value'), 
         State('min_val', 'value'), 
         State('max_val', 'value'), prevent_initial_call=True
    )
    def save(n, prob_type, num_objs, obj_1_name, obj_2_name, obj_3_name, obj_1_goal, obj_2_goal, obj_3_goal, enc_type, gene_size, min_value, max_value):
        if prob_type == 'sing-obj':
            configs.prob_type = Single(configs)
        else:
            configs.prob_type = Multi(configs)
        configs.num_objs = num_objs
        configs.objs, configs.obj_names = [], []
        
        dirs, names = [obj_1_goal, obj_2_goal, obj_3_goal], [obj_1_name, obj_2_name, obj_3_name]
        for i in range(configs.num_objs):
            if dirs[i] == 'min':
                configs.objs.append(min)
            else:
                configs.objs.append(max)
            configs.obj_names.append(names[i])
        
        if enc_type == 'perm':
            configs.enc = Perm(configs)
        configs.gene_size = gene_size
        configs.enc.min_value = min_value
        configs.enc.max_value = max_value
    
    return app