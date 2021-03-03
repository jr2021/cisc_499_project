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
    app.layout = html.Div([dcc.Dropdown(id='sel_type',
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
                           dbc.Input(id='n_crossover_value',
                                    type = 'number',
                                    placeholder='Number of Crossover Points',
                                    disabled=True,
                                    min=0,
                                    max=Configs.params['gene_size']),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='n_crossover_value_error'),
                           dbc.Input(id='alpha',
                                    type = 'number',
                                    placeholder='Blending Ratio',
                                    disabled=True,
                                    min=0,
                                    max=1),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='alpha_error'),
                           dcc.Dropdown(id='mut_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.params['enc_type'].Mutation(Configs.params).get_functions()],
                                        placeholder='Mutation'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='mut_type_error'),
                           dbc.Input(id='theta',
                                    type = 'number',
                                    placeholder='Standard Deviation',
                                    disabled=True,
                                    min=0),
                            dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='theta_error'),
                           dcc.Dropdown(id='rep_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.params['prob_type'].get_functions()],
                                        placeholder='Replacement'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='rep_type_error'),
                           dbc.Input(id='pop_size',
                                     placeholder='Population Size',
                                     type='number',
                                     min=4, max=128,
                                     step=2),
                           dbc.Input(id='tourn_size',
                                    type = 'number',
                                    placeholder='Tournament Size',
                                    disabled=True),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='tourn_size_error'),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='pop_size_error'),
                           dbc.Input(id='par_size',
                                     placeholder='Num. Parents',
                                     type='number',
                                     min=2, max=64,
                                     step=2),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='par_size_error'),
                           dbc.Input(id='off_size',
                                     placeholder='Num. Offspring',
                                     type='number',
                                     min=2, max=64,
                                     step=2),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='off_size_error'),
                           dbc.Input(id='mut_rate',
                                     placeholder='Mutation Rate',
                                     type='number',
                                     min=0, max=1,
                                     step=0.01),
                           dbc.Collapse(dbc.Card(dbc.CardBody('This is a required field')),
                                        id='mut_rate_error'),
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
                           html.Div(id='custom',
                                    children=[dcc.Graph(figure=go.Figure())]),
                           dcc.Graph(id='curr_pop',
                                     figure=go.Figure()),
                           dcc.Interval(id='interval',
                                        disabled=True,
                                        interval=1000), 
                           dcc.Graph(id='fitness',
                                     figure=go.Figure())])

    @app.callback(
        Output('fitness', 'figure'),
        Input('interval', 'n_intervals')
    )
    def update_fitness(n):
        fig = go.Figure()

        colors = px.colors.qualitative.Plotly
        for i in range(configs.params['num_objs']):
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['maxs'][i],
                                     mode=None,
                                     fill=None,
                                     line=dict(color=colors[i]),
                                     showlegend=False,
                                     legendgroup=str(i),
                                     name='Max. ' + Configs.params['obj_names'][i]))
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['avgs'][i],
                                     name=Configs.params['obj_names'][i],
                                     fill='tonexty',
                                     line=dict(color=colors[i]),
                                     legendgroup=str(i),
                                     mode='lines'))
            fig.add_trace(go.Scatter(y=Stats.adhoc['fitness']['mins'][i],
                                     mode=None,
                                     showlegend=False,
                                     name='Min. ' + Configs.params['obj_names'][i],
                                     line=dict(color=colors[i]),
                                     legendgroup=str(i),
                                     fill='tonexty'))

        fig.update_layout(title='Fitness Convergence',
                              xaxis_title='Generations',
                              yaxis_title='Fitness')

        return fig

    @app.callback(
        Output('custom', 'children'),
        Input('interval', 'n_intervals'), prevent_initial_call = True
    )
    def update_custom(n):
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
        fig.update_layout(title='Population Genotype Distribution',
                          xaxis_title='Genotype', yaxis_title='Individual')
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
        State('n_crossover_value', 'disabled'),
        State('tourn_size', 'disabled'),
        State('alpha', 'disabled'),
        State('theta', 'disabled'), prevent_initial_call=True
    )
    def enable_start(start_clicks, save_clicks, resume_dis, sel_type, rec_type, mut_type, rep_type, pop_size, par_size, off_size, mut_rate, n_crossover, tourn_size, alpha, theta, n_disabled, tourn_disabled, alpha_disabled, theta_disabled):
    
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            if None in (sel_type, rec_type, mut_type, rep_type, pop_size, par_size, off_size, mut_rate):
                raise PreventUpdate
            elif alpha is None and alpha_disabled == False:
                raise PreventUpdate
            elif theta is None and theta_disabled == False:
                raise PreventUpdate
            elif tourn_size is None and tourn_disabled == False:
                raise PreventUpdate
            elif n_crossover is None and n_disabled == False:
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
        Output('n_crossover_value', 'disabled'),
        Input('rec_type', 'value')
    )
    def enable_n_point(value):
        if value == 'n-point':
            return False
        else:
            return True
        
    @app.callback(
        Output('tourn_size', 'disabled'),
        Input('sel_type', 'value'),
        Input('rep_type', 'value')
    )
    def enable_tourn_size(sel_type, rep_type):
        if sel_type == 'tournament' or rep_type == 'tournament':
            return False
        else:
            return True
        
    @app.callback(
        Output('alpha', 'disabled'),
        Input('rec_type', 'value')
    )
    def enable_alpha(value):
        if value == 'whole-arithmetic' or value == 'simple-arithmetic':
            return False
        else:
            return True
        
    @app.callback(
        Output('theta', 'disabled'),
        Input('mut_type', 'value')
    )
    def enable_theta(value):
        if value == 'non-uniform' or value == 'creep':
            return False
        else:
            return True
    
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
        State('n_crossover_value', 'disabled'), prevent_initial_call=True
    )
    def no_n(n, value, disabled):
        if n is not None and disabled == False:
            if value is None:
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
        Output('tourn_size_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('tourn_size', 'value'),
        State('tourn_size', 'disabled'), prevent_initial_call=True
    )
    def no_tourn_size(n, value, disabled):
        if n is not None and disabled == False:
            if value is None:
                return True
        return False
    
    @app.callback(
        Output('alpha_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('alpha', 'value'),
        State('alpha', 'disabled'), prevent_initial_call=True
    )
    def no_alpha(n, value, disabled):
        if n is not None and disabled == False:
            if value is None:
                return True
        return False

    @app.callback(
        Output('theta_error', 'is_open'),
        Input('save', 'n_clicks'),
        State('theta', 'value'),
        State('theta', 'disabled'), prevent_initial_call=True
    )
    def no_theta(n, value, disabled):
        if n is not None and disabled == False:
            if value is None:
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
