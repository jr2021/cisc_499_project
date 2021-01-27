from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import initialization as init
import pandas as pd


static_params = {'permutation' : {'min': None,
                                  'max': None},
                 'binary': {},
                 'integer': {},
                 'real': {}
                }

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
        [Output('sel-collapse', 'is_open'),
         Output('sel-collapse', 'children'),
         Output('rep-dropdown', 'label')],
        [Input('perm-option', 'n_clicks')],
        [State('sel-collapse', 'is_open')],
    )
    def open_perm_sel(n, is_open):
        if n:
            representation = 'permutation'
            return True, [html.Br(),
                          dbc.Input(id='min-val',
                                    placeholder='Enter the minimum value for your permutation',
                                    type='number', 
                                    min=0, 
                                    step=1), 
                          html.Br(),
                          dbc.Input(id='max-val',
                                    placeholder='Enter the maximum value for your permutation',
                                    type='number', 
                                    min=1, 
                                    step=1),
                          html.Br(),
                          dbc.Button('Create sample population', id='create-perms'),
                          html.Br(),
                          dbc.Collapse(id='perms-collapse')], 'Permutation',
        else:
            return False, [], 'Choose a representation'
            
        
    @app.callback(
        [Output('perms-collapse', 'is_open'),
         Output('perms-collapse', 'children')],
        [Input('create-perms', 'n_clicks'),
         Input('min-val', 'value'),
         Input('max-val', 'value')],
        [State('perms-collapse', 'is_open')],
    )
    def open_perms(n, low, high, is_open):
        if n:
            df = pd.DataFrame(init.sample_perm(low, high))
            return True, [html.Br(), dbc.Table.from_dataframe(df)]
        else:
            return False, [] 
            
    
    return app