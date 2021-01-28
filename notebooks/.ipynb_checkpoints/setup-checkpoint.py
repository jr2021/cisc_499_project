from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import initialization as init
import pandas as pd
import json

representation = None



def create_app():

    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    server = app.server

    app.layout = html.Div([
        dcc.Markdown(children='''### Define Static Parameters'''),
        dbc.DropdownMenu(id='rep-dropdown',
                         label="Choose a representation",
                         children=[dbc.DropdownMenuItem('Permutation', id='perm-option'),
                                   dbc.DropdownMenuItem('Binary', id='bin-option'),
                                   dbc.DropdownMenuItem('Integer', id='int-option'),
                                   dbc.DropdownMenuItem('Real-Valued', id='real-option')]),
        dbc.Collapse(id='sel-collapse')
    ])   
    
    @app.callback(
         Output('sel-collapse', 'is_open'),
         Output('rep-dropdown', 'label'),
         Output('sel-collapse', 'children'),
         Input('perm-option', 'n_clicks'),
         State('sel-collapse', 'is_open'),
    )
    def open_perm_options(n, is_open):
        if n:
            representation = 'permutation'
            return True, 'Permutation', [dbc.Input(id='min-perm-val',
                                                   placeholder='Enter the minimum value for your permutation',
                                                   type='number',
                                                   min=0, 
                                                   step=1),
                                         dbc.Input(id='max-perm-val',
                                                   placeholder='Enter the maximum value for your permutation',
                                                   type='number',
                                                   min=1, 
                                                   step=1),
                                         dbc.Button('Save static parameters', id='save-perm-params')]
        else:
            return False, 'Choose a representation', []
            
    
    @app.callback(
         Output('save-perm-params', 'children'),
         Input('save-perm-params', 'n_clicks'),
         State('min-perm-val', 'value'),
         State('max-perm-val', 'value')
    )
    def save_perm_params(n, low, high):
        if n:
            with open('params.txt', 'w') as f:
                json.dump({'min': low,
                           'max': high,
                           'len': high - low}, f)
            return 'Saved'
        else:
            return 'Save static parameters'
    
    return app