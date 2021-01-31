import json
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import Config, Permutation

import pickle

def create_app():

    config = Config()
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dbc.DropdownMenu(id='rep-dropdown',
                                            label="Choose a representation",
                                            children=[dbc.DropdownMenuItem('Permutation', id='perm-option'),
                                                      dbc.DropdownMenuItem('Binary', id='bin-option'),
                                                      dbc.DropdownMenuItem('Integer', id='int-option'),
                                                      dbc.DropdownMenuItem('Real-Valued', id='real-option')]),
                           dbc.Collapse(id='sel-collapse')
    ])   
    
    @app.callback(
         Output('sel-collapse', 'is_open'),
         Output('sel-collapse', 'children'),
         Input('perm-option', 'n_clicks'),
    )
    def open_perm_options(n):
        if n:
            config.rep = Permutation(config)
            
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
        else:
            return False, []
            
    
    @app.callback(
         Output('save-perm-params', 'children'),
         Input('save-perm-params', 'n_clicks'),
         State('min-perm-val', 'value'),
         State('max-perm-val', 'value')
    )
    def save_perm_params(n, low, high):
        if n:
            config.rep.min_value, config.rep.max_value = low, high
            with open('configs.pkl', 'wb') as f:
                pickle.dump(config, f)
            
            return 'Saved'
        else:
            return 'Save static parameters'
    
    return app