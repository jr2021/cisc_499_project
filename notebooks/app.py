import json
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
import pickle

with open('configs.pkl', 'rb') as f:
    configs = pickle.load(f)

def create_app():
    
    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dbc.DropdownMenu(id='objs_dropdown',
                                            label='Problem type',
                                            children=[dbc.DropdownMenuItem('single_objective', 
                                                                           id='sing_option'),
                                                      dbc.DropdownMenuItem('multi_objective', 
                                                                           id='multi_option')]),
                           dbc.Collapse(id='sel_collapse')])
    
    @app.callback(
        Output('sel_collapse', 'is_open'),
        Output('objs_dropdown', 'label'),
        Output('sel_collapse', 'children'),
        Input('sing_option', 'n_clicks'), prevent_initial_call=True
    )
    def sing_obj_sel(n):
        if n:
            configs.prob_type = Single(configs)
            
            funcs = [f for f in dir(configs.prob_type) 
                     if callable(getattr(configs.prob_type, f)) and f[0] not in ['_']]
            
            children = [dbc.DropdownMenuItem(f, id=f) for f in funcs]
            sel_dropdown = [dbc.DropdownMenu(id='sel_dropdown',
                                      label='Parent selection',
                                      children=children),
                           dbc.Collapse(id='rec_dropdown')]
            
            return True, 'single_objective', sel_dropdown
        
    
    @app.callback(
        Output('sel_dropdown', 'label'),
        Input('rank_based', 'n_clicks'), prevent_initial_call=True
    )
    def rank_based(n):
        if n:
            configs.select = configs.prob_type.rank_based
            
            return 'rank_based'
    
    return app