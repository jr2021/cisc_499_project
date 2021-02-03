import json
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
import pickle


def create_app():

    configs = Config()
    configs.prob_type = Single(configs)
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dbc.DropdownMenu(id='rep-dropdown',
                                            label="Choose a representation",
                                            children=[dbc.DropdownMenuItem('Permutation', id='perm-option'),
                                                      dbc.DropdownMenuItem('Binary', id='bin-option'),
                                                      dbc.DropdownMenuItem('Integer', id='int-option'),
                                                      dbc.DropdownMenuItem('Real-Valued', id='real-option')]),
                           dbc.Collapse(id='stat-collapse')
    ])   
    
    @app.callback(
         Output('stat-collapse', 'is_open'),
         Output('stat-collapse', 'children'),
         Input('perm-option', 'n_clicks'), prevent_initial_call=True, suppress_callback_exceptions=True
    )
    def open_perm_options(n):
        if n:
            configs.rep = Permutation(configs)
            
            
            return True, [dbc.Input(id='min-perm-val',
                                                   type='number',
                                                   value=0,
                                                   min=0, 
                                                   step=1),
                                         dbc.Input(id='max-perm-val',
                                                   type='number',
                                                   value=1,
                                                   min=1,
                                                   step=1),
                                         dbc.Button('Save static parameters', id='save-perm-params')]
            
    
    @app.callback(
         Output('save-perm-params', 'children'),
         Input('save-perm-params', 'n_clicks'),
         State('min-perm-val', 'value'),
         State('max-perm-val', 'value'), prevent_initial_call=True, suppress_callback_exceptions=True
    )
    def save_perm_params(n, low, high):
        if n:
            configs.rep.min_value, configs.rep.max_value, configs.gene_size = low, high, high - low + 1
            with open('configs.pkl', 'wb') as f:
                pickle.dump(configs, f)
            
            return 'Saved'
    
    return app