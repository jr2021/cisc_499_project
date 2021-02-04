import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
import pickle


configs = Config()

def create_app():
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='dropdown',
                                       options=options,
                                       value=[configs.rep.identity, 'single_obj', 'rank_based', 'order', 'swap', 'tournament'],
                                       clearable=True,
                                       multi=True
                                      ),
                          dbc.Button('Save dynamic parameters', id='save_dynam')])
    
    
    
    
    return app