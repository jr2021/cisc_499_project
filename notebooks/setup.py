from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

static_params = {'representation_type': None,
                 'min': None,
                 'max': None,
                 'length': None
                }

all_options = {'permutation': {'min': None, 
                               'max': None,
                              }
              }


def create_app():

    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    server = app.server

    app.layout = html.Div([
        dbc.DropdownMenu(id='representation_dropdown',
                         label="Choose a representation", 
                         children=[dbc.DropdownMenuItem('Permutation')]),
        html.Hr(),
        dbc.Input(id='minimum_value', type='number', min=0, step=1, placeholder='Minimum Value'),
        html.Hr(),
        dbc.Input(id='maximum_value', type='number', min=0, step=1, placeholder='Minimum Value')
        
        
    ])    
    
    
    @app.callback(
        Output('representation_dropdown', 'children'),
        Input('representation_dropdown', 'children')
    )
    def update_graph(children):
        return children
    
    return app