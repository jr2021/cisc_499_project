import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import no_update
from jupyter_dash import JupyterDash
from configuration import Config
from single import Single
from multi import Multi
from permutation import Perm
from integer import Integer
from binary import Binary
from real import Real
import pickle
from evaluate import *
from visualize import *
global_min, global_max = 0, 100
def create_app(configs):
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Markdown('''### Choose a predefined problem'''), 
                           dcc.Dropdown(id='pre_probs', 
                                        options=[{'label': 'Traveling salesperson', 
                                                  'value': 'trav'},
                                                 {'label': 'Knapsack', 
                                                  'value': 'knap'},
                                                 {'label': 'Eight-Queens', 
                                                  'value': 'queens'},
                                                 {'label': 'Sudoku', 
                                                  'value': 'sudoku'}]),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='pre_prob_error'),
                           dbc.Button(id='save_pre', 
                                      children='Save predefined problem'),
                           dcc.Markdown('''### Create a custom problem'''),
                           dcc.Dropdown(id='prob_type',
                                        options=[{'label': 'single-objective', 
                                                  'value': 'sing-obj'},
                                                 {'label': 'multi-objective', 
                                                  'value': 'multi-obj'}],
                                        placeholder='Objectiveness'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='prob_type_error'),
                           dbc.Input(id='num_objs',
                                     placeholder='Number of objectives',
                                     type='number', 
                                     min=1, max=3),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='num_objs_error'),
                           dbc.Input(id='obj_1_name',
                                     placeholder='Objective 1 name',
                                     type='text'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='obj_1_name_error'),
                           dcc.Dropdown(id='obj_1_goal',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 1 goal'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='obj_1_goal_error'),
                           dbc.Input(id='obj_2_name',
                                     placeholder='Objective 2 name',
                                     type='text'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='obj_2_name_error'),
                           dcc.Dropdown(id='obj_2_goal',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 2 goal'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='obj_2_goal_error'),
                           dbc.Input(id='obj_3_name',
                                     placeholder='Objective 3 name',
                                     type='text'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='obj_3_name_error'),
                           dcc.Dropdown(id='obj_3_goal',
                                        options=[{'label': 'minimize', 
                                                  'value': 'min'},
                                                 {'label': 'maximize', 
                                                  'value': 'max'}],
                                        placeholder='Objective 3 goal'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='obj_3_goal_error'),
                           dcc.Dropdown(id='enc_type',
                                        options=[{'label': 'Permutation', 
                                                  'value': 'perm'},
                                                {'label': 'Binary', 
                                                  'value': 'binary'},
                                                {'label': 'Integer', 
                                                  'value': 'int'},
                                                {'label': 'Real-Valued', 
                                                  'value': 'real'}],
                                        placeholder='Representation'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='enc_type_error'),
                           dbc.Input(id='gene_size',
                                     placeholder='Gene Size',
                                     type='number', 
                                     min=0, max=100),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='gene_size_error'),
                           dbc.Input(id='min_val',
                                     placeholder='Minimum Value',
                                     type='number', 
                                     min=0, max=100),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='min_val_error'),
                           dbc.Input(id='max_val',
                                     placeholder='Maximum Value',
                                     type='number', 
                                     min=0, max=100),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                       id='max_val_error'),
                           dbc.Button(id='save_cust', 
                                      children='Save custom problem')])   
    
    
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
         Output('gene_size', 'disabled'),
         Input('enc_type', 'value'), prevent_initial_call=True
    )
    def gene_size_enable(enc_type):
        if enc_type == 'perm':
            return True
        else:
            return False
        
    @app.callback(
         Output('min_val', 'disabled'),
         Output('max_val', 'disabled'),
         Output('min_val', 'value'),
         Output('max_val', 'value'),
         Input('enc_type', 'value'), prevent_initial_call=True
    )
    def min_max_disable(enc_type):
        if enc_type == 'binary':
            return True, True, 0, 1
        else:
            return False, False, 0, 0
        
    @app.callback(
        Output('min_val', 'max'),
        Input('max_val', 'value'), prevent_initial_call = True
    )
    def min_max_constraint(max_val):
        if max_val:
            return max_val - 1
        else:
            no_update
    
    @app.callback(
        Output('max_val', 'min'),
        Input('min_val', 'value'), prevent_initial_call = True
    )
    def max_min_constraint(min_val):
        if min_val:
            return min_val + 1
        else:
            no_update
        
        
    @app.callback(
         Output('gene_size', 'value'),
         Input('min_val', 'value'),
         Input('max_val', 'value'),
         State('enc_type', 'value'),prevent_initial_call=True
    )
    def gene_size_selection(min_val, max_val, enc_type):
        if enc_type != 'perm':
            no_update
        else:
            if min_val == None or max_val == None:
                return 0
            if min_val >= max_val:
                return 0
            else:
                return max_val - min_val
    
    @app.callback(
         Output('save_pre', 'children'),
         Input('save_pre', 'n_clicks'),
         State('pre_probs', 'value'), prevent_initial_call=True
    )
    def save_pre(n, pre_prob):
        if None in (n, pre_prob):
            raise PreventUpdate
        
        if pre_prob == 'trav':
            configs.params['prob_type'] = Single(configs.params)
            configs.params['num_objs'] = 1
            configs.params['objs'] = [min]
            configs.params['obj_names'] = ['Distance']
            configs.params['enc_type'] = Perm(configs.params)
            configs.params['gene_size'] = 64
            configs.params['enc_type'].params['min_value'] = 0
            configs.params['enc_type'].params['max_value'] = 63
            configs.params['eval_type'] = TSP
            configs.params['cust_vis'] = network
        elif pre_prob == 'knap':
            configs.params['prob_type'] = Multi(configs.params)
            configs.params['num_objs'] = 2
            configs.params['objs'] = [max, min]
            configs.params['obj_names'] = ['Value', 'Weight']
            configs.params['enc_type'] = Binary(configs.params)
            configs.params['gene_size'] = 64
            configs.params['enc_type'].params['min_value'] = 0
            configs.params['enc_type'].params['max_value'] = 1
            configs.params['eval_type'] = knapsack
            configs.params['cust_vis'] = selection
            configs.params['n'] = 8
        elif pre_prob == 'queens':
            configs.params['prob_type'] = Single(configs.params)
            configs.params['num_objs'] = 1
            configs.params['objs'] = [min]
            configs.params['obj_names'] = ['Threats']
            configs.params['enc_type'] = Perm(configs.params)
            configs.params['gene_size'] = 64
            configs.params['enc_type'].params['min_value'] = 0
            configs.params['enc_type'].params['max_value'] = 63
            configs.params['eval_type'] = eight_queens
            configs.params['cust_vis'] = chess_board
        elif pre_prob == 'sudoku':
            configs.params['prob_type'] = Single(configs.params)
            configs.params['num_objs'] = 1
            configs.params['objs'] = [min]
            configs.params['obj_names'] = ['Conflicts']
            configs.params['enc_type'] = Perm(configs.params)
            configs.params['gene_size'] = 100
            configs.params['enc_type'].params['min_value'] = 0
            configs.params['enc_type'].params['max_value'] = 99
            configs.params['eval_type'] = sudoku
            configs.params['cust_vis'] = sudoku_board
        
        return 'Saved'
    
    @app.callback(
         Output('save_cust', 'children'),
         Input('save_cust', 'n_clicks'),
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
        if None in (n, prob_type, num_objs, obj_1_name, obj_2_name, obj_3_name, obj_1_goal, obj_2_goal, obj_3_goal, enc_type, gene_size, min_value, max_value):
            raise PreventUpdate
            
        if prob_type == 'sing-obj':
            configs.params['prob_type'] = Single(configs.params)
        else:
            configs.params['prob_type'] = Multi(configs.params)
        configs.params['num_objs'] = num_objs
        configs.params['objs'], configs.params['obj_names'] = [], []
        
        dirs, names = [obj_1_goal, obj_2_goal, obj_3_goal], [obj_1_name, obj_2_name, obj_3_name]
        for i in range(configs.params['num_objs']):
            if dirs[i] == 'min':
                configs.params['objs'].append(min)
            else:
                configs.params['objs'].append(max)
            configs.params['obj_names'].append(names[i])
        
        if enc_type == 'perm':
            configs.params['enc_type'] = Perm(configs.params)
        elif enc_type == 'binary':
            configs.params['enc_type'] = Binary(configs.params)
        elif enc_type == 'int':
            configs.params['enc_type'] = Integer(configs.params)
        elif enc_type == 'real':
            configs.params['enc_type'] = Real(configs.params)
        configs.params['gene_size'] = gene_size
        configs.params['enc_type'].params['min_value'] = min_value
        configs.params['enc_type'].params['max_value'] = max_value
        
        return 'Saved'
        
    
    @app.callback(
        Output('prob_type_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('prob_type', 'value'), prevent_initial_call=True
    )
    def no_prob_type(n, value):
        if n:
            if value is None:
                return True
        no_update
            
    
    @app.callback(
        Output('num_objs_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('num_objs', 'value'), prevent_initial_call=True
    )
    def no_num_objs(n, value):
        if n:
            if value is None:
                return True
        no_update
    
    @app.callback(
        Output('obj_1_name_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('obj_1_name', 'value'), prevent_initial_call=True
    )
    def no_obj_1_name(n, value):
        if n:
            if value is None:
                return True
        no_update
        
    @app.callback(
        Output('obj_2_name_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('obj_2_name', 'value'),
        State('num_objs', 'value'), prevent_initial_call=True
    )
    def no_obj_2_name(n, value, num_objs):
        if n is not None or num_objs < 2:
            if value is None:
                return True
        no_update
    
    @app.callback(
        Output('obj_3_name_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('obj_3_name', 'value'),
        State('num_objs', 'value'), prevent_initial_call=True
    )
    def no_obj_3_name(n, value, num_objs):
        if n is not None or num_objs < 3:
            if value is None:
                return True
        no_update
    
    @app.callback(
        Output('obj_1_goal_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('obj_1_goal', 'value'), prevent_initial_call=True
    )
    def no_obj_1_goal(n, value):
        if n:
            if value is None:
                return True
        no_update
        
    @app.callback(
        Output('obj_2_goal_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('obj_2_goal', 'value'),
        State('num_objs', 'value'), prevent_initial_call=True
    )
    def no_obj_2_goal(n, value, num_objs):
        if n is not None or num_objs < 2:
            if value is None:
                return True
        no_update
    
    @app.callback(
        Output('obj_3_goal_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('obj_3_goal', 'value'),
        State('num_objs', 'value'), prevent_initial_call=True
    )
    def no_obj_3_goal(n, value, num_objs):
        if n is not None or num_objs < 3:
            if value is None:
                return True
        no_update
    
    @app.callback(
        Output('enc_type_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('enc_type', 'value'), prevent_initial_call=True
    )
    def no_enc_type(n, value):
        if n:
            if value is None:
                return True
        no_update
        
    @app.callback(
        Output('gene_size_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('gene_size', 'value'), prevent_initial_call=True
    )
    def no_gene_size(n, value):
        if n:
            if value is None:
                return True
        no_update
        
    @app.callback(
        Output('min_val_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('min_val', 'value'), prevent_initial_call=True
    )
    def no_min_val(n, value):
        if n:
            if value is None:
                return True
        no_update

    @app.callback(
        Output('max_val_error', 'is_open'),
        Input('save_cust', 'n_clicks'),
        State('max_val', 'value'), prevent_initial_call=True
    )
    def no_max_val(n, value):
        if n:
            if value is None:
                return True
        no_update
    
    @app.callback(
        Output('pre_prob_error', 'is_open'),
        Input('save_pre', 'n_clicks'),
        State('pre_probs', 'value'), prevent_initial_call=True
    )
    def no_max_val(n, value):
        if n:
            if value is None:
                return True
        no_update
    
    
    return app