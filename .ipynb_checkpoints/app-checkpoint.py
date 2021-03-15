import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from plotly import graph_objects as go
import pickle
from dash.exceptions import PreventUpdate
import numpy as np
from threading import Thread
from statistics import Statistics
from single import Single
import plotly.express as px
import copy

Population, Running, Configs, Stats = None, None, None, None

def create_app(configs, stats):
    global Configs, Stats
    Configs, Stats = configs, stats

    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Markdown('''##### Run GA configuration'''),
                           dbc.Row([ 
                           dbc.Col(children=(dcc.Markdown('''###### Selection, recombination, mutation, replacement'''))),
                           dbc.Col(children=(dcc.Markdown('''###### Population parameters'''))),
                           ]),
        dbc.Row([ 
                           dbc.Col(children=(dcc.Dropdown(id='sel_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.params['prob_type'].get_functions()],
                                        placeholder='Selection'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='sel_type_error'),
                           dcc.Dropdown(id='rec_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.params['enc_type'].Cross(Configs.params).get_functions()],
                                        placeholder='Recombination'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='rec_type_error'),
                           dbc.Collapse(dbc.Input(id='n_crossover_value',
                                                  type = 'number',
                                                  placeholder='Number of Crossover Points',
                                                  min=0,
                                                  max=Configs.params['gene_size']),
                                        id='n_crossover_value_collapse'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='n_crossover_value_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('n must be in the range from 0 to gene size')),
                                        id='n_crossover_value_wrong'),
                           dbc.Collapse(dbc.Input(id='alpha',
                                                  type = 'number',
                                                  placeholder='Blending Ratio',
                                                  min=0,
                                                  max=1),
                                        id='alpha_collapse'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='alpha_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('alpha must be be in the range from 0 to 1')),
                                        id='alpha_wrong'),
                           dcc.Dropdown(id='mut_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.params['enc_type'].Mutation(Configs.params).get_functions()],
                                        placeholder='Mutation'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='mut_type_error'),
                           dbc.Collapse(dbc.Input(id='theta',
                                                  type = 'number',
                                                  placeholder='Standard Deviation',
                                                  min=0),
                                        id='theta_collapse'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='theta_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Theta must be non-negative')),
                                        id='theta_wrong'),
                           dcc.Dropdown(id='rep_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.params['prob_type'].get_functions()],
                                        placeholder='Replacement'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='rep_type_error'))),
                           
                           dbc.Col(children=(dbc.Input(id='pop_size',
                                     placeholder='Population Size',
                                     type='number',
                                     min=4, max=128,
                                     step=2),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='pop_size_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Population size must be in the range from 1 to 128')),
                                        id='pop_size_wrong'),
                           dbc.Input(id='par_size',
                                     placeholder='Num. Parents',
                                     type='number',
                                     min=2, max=64,
                                     step=2),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='par_size_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Parent size must be non-negative')),
                                                id='wrong_par_size'),
                           dbc.Input(id='off_size',
                                     placeholder='Num. Offspring',
                                     type='number',
                                     min=2, max=64,
                                     step=2),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='off_size_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Children size must be non-negative')),
                                                id='wrong_off_size'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Parent and children size must be greater than or equal to population size')),
                                        id='par_chi_error'),
                           dbc.Collapse(dcc.Dropdown(id='tourn_size',
                                        options=[{'label': '2', 
                                                  'value': 2},
                                                {'label': '4', 
                                                  'value': 4},
                                                {'label': '8', 
                                                  'value': 8},
                                                {'label': '16', 
                                                  'value': 16},
                                                {'label': '32', 
                                                  'value': 32},
                                                {'label': '64', 
                                                  'value': 64}],
                                        placeholder='Tournament Size'),
                                        id='tourn_size_collapse'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='tourn_size_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Tournament size must be in the range from 0 to the minimum of parent size and population size')),
                                        id='tourn_parent_error'),
                           dbc.Input(id='mut_rate',
                                     placeholder='Mutation Rate',
                                     type='number',
                                     min=0, max=1,
                                     step=0.01),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='mut_rate_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('Mutation rate must be in the range from 0 to 1')),
                                        id='mut_rate_wrong'))),
                            ]),
                           dbc.Button(id='save',
                                      children='Save'),
                           
                           dbc.Button(id='start',
                                      children='Start',
                                      disabled=True),
                           dbc.Button(id='stop',
                                      children='Stop',
                                      disabled=True),
                           dbc.Button(id='restart',
                                      children='Restart',
                                      disabled=True),
                           dbc.Button(id='pause',
                                      children='Pause',
                                      disabled=True),
                           dbc.Button(id='resume',
                                      children='Resume',
                                      disabled=True),
        dbc.Row([
                           dbc.Col(children=(html.Div(id='custom',
                                    children=[dcc.Graph(figure=go.Figure())]))),
                          dbc.Col(children=( dcc.Graph(id='curr_pop',
                                     figure=go.Figure()),
                           dcc.Interval(id='interval',
                                        disabled=True,
                                        interval=1500)))
        ]),
                           dcc.Graph(id='fitness',
                                     figure=go.Figure())])
    
    @app.callback(
        Output('fitness', 'figure'),
        Input('interval', 'n_intervals')
    )
    def update_fitness(n):
        fig = go.Figure()

        line_colors = px.colors.qualitative.Plotly
        colors = ['rgba(99,110,250,0.5)', 'rgba(239,85,59,0.5)', 'rgba(0,204,150,0.5)']
        for i in range(configs.params['num_objs']):
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['maxs'][i],
                                     mode=None,
                                     fill=None,
                                     opacity=0,
                                     showlegend=False))
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['maxs'][i],
                                     mode='lines',
                                     fill='tonexty',
                                     line_color=line_colors[i],
                                     legendgroup=str(i),
                                     name='Max. ' + Configs.params['obj_names'][i]))
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['avgs'][i],
                                     name='Avg. ' + Configs.params['obj_names'][i],
                                     fill='tonexty',
                                     line_color=line_colors[i],
                                     legendgroup=str(i),
                                     mode='lines'))
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['mins'][i],
                                     mode=None,
                                     name='Min. ' + Configs.params['obj_names'][i],
                                     line_color=line_colors[i],
                                     legendgroup=str(i),
                                     fill='tonexty'))

        fig.update_layout(title='Fitness Convergence',
                              xaxis_title='Generations',
                              yaxis_title='Fitness Value')

        return fig

    @app.callback(
        Output('custom', 'children'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_custom(n):
        if Configs.params['cust_vis'] == None:
            return dcc.Graph(figure=go.Figure())
        else:
            if Configs.params['num_objs'] == 1:
                best = Configs.params['prob_type'].rank_based(Population, 
                                                                 Configs.params['pop_size'], 
                                                                 1)[0]
            else:
                best = Configs.params['prob_type'].NSGA_II(copy.deepcopy(Population),
                                                              Configs.params['pop_size'],
                                                              1)[0]
            return Configs.params['cust_vis'](Configs, best)
            

    @app.callback(
        Output('curr_pop', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_curr_pop(n):
        fig = go.Figure(data=[go.Heatmap(z=[ind['gene'] for ind in Population])])
        fig.update_layout(title='Population ' + Configs.params['enc_name'] + ' Distribution',
                          xaxis_title=Configs.params['enc_name'], yaxis_title='Candidate Solution')
        return fig

    @app.callback(
        Output('save', 'disabled'),
        Input('start', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'),
        Input('stop', 'n_clicks'), prevent_initial_call=True
    )
    def enable_save(startclicks, resumeclicks, pauseclicks, stopclicks):
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            return False
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'stop.n_clicks':
            return False

    @app.callback(
        Output('start', 'disabled'),
        Input('start', 'n_clicks'),
        Input('save', 'n_clicks'),
        State('resume', 'disabled'),
        State('sel_type', 'value'),
        State('rec_type', 'value'),
        State('mut_type', 'value'),
        State('rep_type', 'value'),
        State('pop_size', 'value'),
        State('par_size', 'value'),
        State('off_size', 'value'),
        State('mut_rate', 'value'),
        State('n_crossover_value', 'value'),
        State('tourn_size', 'value'),
        State('alpha', 'value'),
        State('theta', 'value'),
        State('n_crossover_value_collapse', 'is_open'),
        State('tourn_size_collapse', 'is_open'),
        State('alpha_collapse', 'is_open'),
        State('theta_collapse', 'is_open'), prevent_initial_call=True
    )
    def enable_start(start_clicks, save_clicks, resume_dis, sel_type, rec_type, mut_type, rep_type, pop_size, par_size, off_size, mut_rate, n_crossover, tourn_size, alpha, theta, n_open, tourn_open, alpha_open, theta_open):
    
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            if None in (sel_type, rec_type, mut_type, rep_type, pop_size, par_size, off_size, mut_rate):
                raise PreventUpdate
            elif alpha is None and alpha_open == True:
                raise PreventUpdate
            elif theta is None and theta_open == True:
                raise PreventUpdate
            elif tourn_size is None and tourn_open == True:
                raise PreventUpdate
            elif n_crossover is None and n_open == True:
                raise PreventUpdate
            elif mut_rate < 0 or mut_rate > 1:
                raise PreventUpdate
            elif pop_size < 1 or pop_size > 128:
                raise PreventUpdate
            elif tourn_open == True and (tourn_size < 0 or (tourn_size > par_size) or (tourn_size > pop_size)):
                raise PreventUpdate
            elif (par_size + off_size) < pop_size:
                raise PreventUpdate
            elif par_size < 0:
                raise PreventUpdate
            elif off_size < 0:
                raise PreventUpdate
            elif n_crossover is not None and n_crossover < 0:
                raise PreventUpdate
            elif alpha is not None and (alpha < 0 or alpha > 1):
                raise PreventUpdate
            elif theta is not None and (theta < 0 or theta > (Configs.params['max_value'] - Configs.params['min_value']) / 10):
                raise PreventUpdate
            
            if sel_type == 'rank-based':
                Configs.params['sel_type'] = Configs.params['prob_type'].rank_based
            elif sel_type == 'tournament':
                Configs.params['sel_type'] = Configs.params['prob_type'].tournament
            elif sel_type == 'NSGA-II':
                Configs.params['sel_type'] = Configs.params['prob_type'].NSGA_II
                
            # add other parent selection options here
            
            if rec_type == 'order':
                Configs.params['enc_type'].params['rec_type'] = Configs.params['enc_type'].Cross(Configs.params).order
            elif rec_type == 'partially-mapped':
                Configs.params['enc_type'].params['rec_type'] = Configs.params['enc_type'].Cross(Configs.params).PMX
            elif rec_type == 'whole-arithmetic':
                Configs.params['enc_type'].params['rec_type'] = Configs.params['enc_type'].Cross(Configs.params).whole_arithmetic
            elif rec_type == 'simple-arithmetic':
                Configs.params['enc_type'].params['rec_type'] = Configs.params['enc_type'].Cross(Configs.params).simple_arithmetic
            elif rec_type == 'n-point':
                Configs.params['enc_type'].params['rec_type'] = Configs.params['enc_type'].Cross(Configs.params).n_point
            elif rec_type == 'uniform':
                Configs.params['enc_type'].params['rec_type'] = Configs.params['enc_type'].Cross(Configs.params).uniform
                
            # add other crossover options here
            
            if mut_type == 'swap':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).swap
            elif mut_type == 'scramble':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).scramble
            elif mut_type == 'uniform':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).uniform
            elif mut_type == 'non-uniform':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).non_uniform
            elif mut_type == 'random-resetting':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).random_resetting
            elif mut_type == 'creep':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).creep
            elif mut_type == 'bit-flip':
                Configs.params['enc_type'].params['mut_type'] = Configs.params['enc_type'].Mutation(Configs.params).bit_flip
             
            # add other mutation options here
            
            if rep_type == 'rank-based':
                Configs.params['rep_type'] = Configs.params['prob_type'].rank_based
            elif rep_type == 'tournament':
                Configs.params['rep_type'] = Configs.params['prob_type'].tournament
            elif rep_type == 'NSGA-II':
                Configs.params['rep_type'] = Configs.params['prob_type'].NSGA_II
                
            # add other survivor selection options here
            
            Configs.params['pop_size'] = pop_size
            Configs.params['par_size'] = par_size
            Configs.params['off_size'] = off_size
            Configs.params['mut_rate'] = mut_rate
            Configs.params['tourn_size'] = tourn_size
            Configs.params['alpha'] = alpha
            Configs.params['theta'] = theta
            Configs.params['n'] = n_crossover
            

            if resume_dis == True:
                return False
            else:
                return True

    @app.callback(
        Output('pause', 'disabled'),
        Input('start', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'), prevent_initial_call=True
    )
    def enable_pause(startclicks, resumeclicks, stopclicks):
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return False
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return False

    @app.callback(
        Output('resume', 'disabled'),
        Input('stop', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'), prevent_initial_call=True
    )
    def enable_resume(stopclicks, resumeclicks, pauseclicks):
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'stop.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            return False
        
    @app.callback(
        Output('stop', 'disabled'),
        Input('stop', 'n_clicks'),
        Input('resume', 'n_clicks'),
        Input('pause', 'n_clicks'), prevent_initial_call=True
    )
    def enable_stop(stopclicks, resumeclicks, pauseclicks):
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'stop.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            return False

    @app.callback(
        Output('interval', 'disabled'),
        Input('pause', 'n_clicks'),
        Input('start', 'n_clicks'),
        Input('resume', 'n_clicks'), prevent_initial_call=True
    )
    def enable_interval(pauseclicks, startclicks, resumeclicks):
        global Running

        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'pause.n_clicks':
            Running = False
            return True
        elif ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            Thread(target=start_GA, args=()).start()
            return False
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            Thread(target=resume_GA, args=()).start()
            return False
    
    @app.callback(
        Output('n_crossover_value_collapse', 'is_open'),
        Input('rec_type', 'value')
    )
    def enable_n_point(value):
        if value == 'n-point':
            return True
        else:
            return False
        
    @app.callback(
        Output('tourn_size_collapse', 'is_open'),
        Input('sel_type', 'value'),
        Input('rep_type', 'value')
    )
    def enable_tourn_size(sel_type, rep_type):
        if sel_type == 'tournament' or rep_type == 'tournament':
            return True
        else:
            return False
        
    @app.callback(
        Output('alpha_collapse', 'is_open'),
        Input('rec_type', 'value')
    )
    def enable_alpha(value):
        if value == 'whole-arithmetic' or value == 'simple-arithmetic':
            return True
        else:
            return False
        
    @app.callback(
        Output('theta_collapse', 'is_open'),
        Input('mut_type', 'value')
    )
    def enable_theta(value):
        if value == 'non-uniform' or value == 'creep':
            return True
        else:
            return False
    
    @app.callback(
        Output('sel_type_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('sel_type', 'value'), prevent_initial_call=True
    )
    def no_sel_type(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('rec_type_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('rec_type', 'value'), prevent_initial_call=True
    )
    def no_rec_type(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('n_crossover_value_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('n_crossover_value', 'value'),
        State('n_crossover_value_collapse', 'is_open'), prevent_initial_call=True
    )
    def no_n(n, value, is_open):
        if n is not None and is_open == True:
            if value is None:
                return True
        return False

    @app.callback(
        Output('n_crossover_value_wrong', 'is_open'),
        Input('save', 'n_clicks'),
        State('n_crossover_value', 'value'),
        State('n_crossover_value_collapse', 'is_open'), prevent_initial_call=True
    )
    def wrong_n(n, value, is_open):
        if n is not None and is_open == True:
            if value < 0 or value >= Configs.params['gene_size']:
                return True
        return False
    
    @app.callback(
        Output('mut_type_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('mut_type', 'value'), prevent_initial_call=True
    )
    def no_mut_type(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('rep_type_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('rep_type', 'value'), prevent_initial_call=True
    )
    def no_rep_type(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('pop_size_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('pop_size', 'value'), prevent_initial_call=True
    )
    def no_pop_size(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('par_size_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('par_size', 'value'), prevent_initial_call=True
    )
    def no_par_size(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('off_size_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('off_size', 'value'), prevent_initial_call=True
    )
    def no_off_size(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('mut_rate_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('mut_rate', 'value'), prevent_initial_call=True
    )
    def no_mut_rate(n, value):
        if n:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('mut_rate_wrong', 'is_open'),
        Input('save', 'n_clicks'),
        State('mut_rate', 'value'), prevent_initial_call=True
    )
    def wrong_mut_rate(n, value):
        if None not in (n, value):
            if value < 0 or value > 1:
                return True
        return False
    
    @app.callback(
        Output('pop_size_wrong', 'is_open'),
        Input('save', 'n_clicks'),
        State('pop_size', 'value'), prevent_initial_call=True
    )
    def wrong_pop_size(n, value):
        if None not in (n, value):
            if value < 1 or value > 128:
                return True
        return False
    
    @app.callback(
        Output('wrong_off_size', 'is_open'),
        Input('save', 'n_clicks'),
        State('off_size', 'value'), prevent_initial_call=True
    )
    def wrong_off_size(n, value):
        if None not in (n, value):
            if value < 0:
                return True
        return False
    
    @app.callback(
        Output('wrong_par_size', 'is_open'),
        Input('save', 'n_clicks'),
        State('par_size', 'value'), prevent_initial_call=True
    )
    def wrong_par_size(n, value):
        if None not in (n, value):
            if value < 0:
                return True
        return False
    
    @app.callback(
        Output('tourn_size_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('tourn_size', 'value'),
        State('tourn_size_collapse', 'is_open'), prevent_initial_call=True
    )
    def no_tourn_size(n, value, is_open):
        if n is not None and is_open == True:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('alpha_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('alpha', 'value'),
        State('alpha_collapse', 'is_open'), prevent_initial_call=True
    )
    def no_alpha(n, value, is_open):
        if n is not None and is_open == True:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('alpha_wrong', 'is_open'),
        Input('save', 'n_clicks'),
        State('alpha', 'value'),
        State('alpha_collapse', 'is_open'), prevent_initial_call=True
    )
    def wrong_alpha(n, value, is_open):
        if n is not None and is_open == True:
            if value < 0 or value > 1:
                return True
        return False

    @app.callback(
        Output('theta_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('theta', 'value'),
        State('theta_collapse', 'is_open'), prevent_initial_call=True
    )
    def no_theta(n, value, is_open):
        if n is not None and is_open == True:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('theta_wrong', 'is_open'),
        Input('save', 'n_clicks'),
        State('theta', 'value'),
        State('theta_collapse', 'is_open'), prevent_initial_call=True
    )
    def wrong_theta(n, value, is_open):
        if n is not None and is_open == True:
            if value < 0 or value > (Configs.params['max_value'] - Configs.params['min_value']) / 10:
                return True
        return False
    
    @app.callback(
        Output('tourn_parent_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('tourn_size', 'value'),
        State('par_size', 'value'),
        State('pop_size', 'value'), prevent_initial_call=True
    )
    def tourn_par_error(n, tourn_size, par_size, pop_size):
        if None not in (n, tourn_size, par_size, pop_size):
            if tourn_size < 0 or (tourn_size > par_size) or (tourn_size > pop_size):
                return True
        return False
        
    @app.callback(
        Output('par_chi_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('par_size', 'value'),
        State('off_size', 'value'),
        State('pop_size', 'value'), prevent_initial_call=True
    )
    def par_chi_error(n, par_size, off_size, pop_size):
        if None not in (n, par_size, off_size, pop_size):
            if (par_size + off_size) < pop_size:
                return True
        return False

    
    return app


def start_GA():
    global Population, Running

    Stats.setup()
    Population = Configs.params['enc_type'].initialize()
    Population = Configs.params['eval_type'](Configs, Population)

    Running = True
    while Running:
        parents = Configs.params['sel_type'](Population, 
                                             Configs.params['pop_size'],
                                             Configs.params['par_size'])
        offspring = Configs.params['enc_type'].mate(parents)
        offspring = Configs.params['enc_type'].params['mut_type'](offspring)
        offspring = Configs.params['eval_type'](Configs, offspring)
        Population = Configs.params['rep_type'](np.concatenate((Population, offspring), axis=0),
                                                Configs.params['pop_size'] + Configs.params['off_size'],
                                                Configs.params['pop_size'])
        Stats.update_dynamic(Population)
    
    Stats.update_static(Population)


def resume_GA():
    global Population, Running

    Running = True
    while Running:
        parents = Configs.params['sel_type'](Population, 
                                             Configs.params['pop_size'],
                                             Configs.params['par_size'])
        offspring = Configs.params['enc_type'].mate(parents)
        offspring = Configs.params['enc_type'].params['mut_type'](offspring)
        offspring = Configs.params['eval_type'](Configs, offspring)
        Population = Configs.params['rep_type'](np.concatenate((Population, offspring)),
                                                Configs.params['pop_size'] + Configs.params['off_size'], 
                                                Configs.params['pop_size'])
        Stats.update_dynamic(Population)
        
    Stats.update_static(Population)
