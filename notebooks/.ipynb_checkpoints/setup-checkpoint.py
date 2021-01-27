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
         Output('sel-collapse', 'children'),
         Output('rep-dropdown', 'label'),
         Input('perm-option', 'n_clicks'),
         State('sel-collapse', 'is_open'),
    )
    def open_perm_options(n, is_open):
        if n:
            representation = 'permutation'
            return True, [html.Br(),
                          dbc.Input(id='min-val',
                                    placeholder='Enter the minimum value for your permutation',
                                    type='number',
                                    value=0,
                                    min=0, 
                                    step=1), 
                          html.Br(),
                          dbc.Input(id='max-val',
                                    placeholder='Enter the maximum value for your permutation',
                                    type='number', 
                                    value=1,
                                    min=1, 
                                    step=1),
                          html.Br(),
                          dbc.Button('Create sample population', id='create-perms'),
                          html.Br(),
                          dbc.Collapse(id='perms-collapse')], 'Permutation',
        else:
            return False, [], 'Choose a representation'
            
        
    @app.callback(
        Output('perms-collapse', 'is_open'),
        Output('perms-collapse', 'children'),
        Input('create-perms', 'n_clicks'),
        State('min-val', 'value'),
        State('max-val', 'value'),
        State('perms-collapse', 'is_open')
    )
    def show_perms(n, low, high, is_open):
        if n:
            df = pd.DataFrame(init.sample_perm(low, high))
            return True, [html.Br(), dbc.Table.from_dataframe(df), html.Br(), dbc.Button('Save static parameters', id='save-params')]
        else:
            return False, []
            
    
    @app.callback(
         Output('save-params', 'children'),
         Input('save-params', 'n_clicks'),
         State('min-val', 'value'),
         State('max-val', 'value')
    )
    def save_params(n, low, high):
        if n:
            with open('params.txt', 'w') as f:
                json.dump({'min': low,
                           'max': high,
                           'len': high - low}, f)
            return 'Saved'
        else:
            return 'Save static parameters'
    
    return app