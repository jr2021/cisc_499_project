import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
from Configuration import *
from Permutation import *
from plotly import graph_objects as go
import pickle
from threading import Thread
from Statistics import Statistics

Population, Running, Configs, Stats = None, None, None, None

def create_app(configs):
    global Configs
    Configs = configs

    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.layout = html.Div([dcc.Dropdown(id='sel_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.prob_type.get_functions()],
                                        placeholder='Selection'),
                           dcc.Dropdown(id='rec_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.enc.Recombination(Configs,
                                                                                      configs.enc.configs).get_functions()],
                                        placeholder='Recombination'),
                           dcc.Dropdown(id='mut_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.enc.Mutation(Configs,
                                                                                 Configs.enc.configs).get_functions()],
                                        placeholder='Mutation'),
                           dcc.Dropdown(id='rep_type',
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in Configs.prob_type.get_functions()],
                                        placeholder='Replacement'),
                           dbc.Input(id='pop_size',
                                     placeholder='Population Size',
                                     type='number',
                                     min=4, max=128,
                                     step=2),
                           dbc.Input(id='par_size',
                                     placeholder='Num. Parents',
                                     type='number',
                                     min=2, max=64,
                                     step=2),
                           dbc.Input(id='off_size',
                                     placeholder='Num. Offspring',
                                     type='number',
                                     min=2, max=64,
                                     step=2),
                           dbc.Input(id='mut_rate',
                                     placeholder='Mutation Rate',
                                     type='number',
                                     min=0, max=1,
                                     step=0.1),
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
                           dcc.Graph(id='custom',
                                     figure=go.Figure()),
                           dcc.Graph(id='heatmap',
                                     figure=go.Figure()),
                           dcc.Interval(id='interval',
                                        disabled=True,
                                        interval=500)] + [dcc.Graph(id='fitness_' + str(i),
                                                                    figure=go.Figure()) for i in
                                                          range(1, Configs.num_objs + 1)])

    @app.callback(
        Output('fitness_1', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call=True
    )
    def update_fitness_1(n):
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=Stats.gen_level['fitness']['mins'][0],
                                 mode='lines',
                                 name='Min.'))
        fig.add_trace(go.Scatter(y=Stats.gen_level['fitness']['avgs'][0],
                                 mode='lines',
                                 name='Avg.'))
        fig.add_trace(go.Scatter(y=Stats.gen_level['fitness']['maxs'][0],
                                 mode='lines',
                                 name='Max.'))
        fig.update_layout(title='Fitness Objective 1 Convergence',
                          xaxis_title='Generations',
                          yaxis_title=Configs.obj_names[0])
        return fig

    @app.callback(
        Output('custom', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call=True
    )
    def update_custom(n):
        return Configs.vis(Configs.sel(Population, 1)[0])

    @app.callback(
        Output('heatmap', 'figure'),
        Input('interval', 'n_intervals'), prevent_initial_call=True
    )
    def update_heatmap(n):
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
        State('mut_rate', 'value'), prevent_initial_call=True
    )
    def enable_start(start_clicks, save_clicks, resume_dis, sel_type, rec_type, mut_type, rep_type, pop_size,
                     par_size, off_size, mut_rate):
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'start.n_clicks':
            return True
        elif ctx.triggered[0]['prop_id'] == 'save.n_clicks':
            if sel_type == 'rank-based':
                Configs.sel = Configs.prob_type.rank_based
            if rec_type == 'order':
                Configs.enc.rec = Configs.enc.Recombination(Configs, Configs.enc.configs).order
            if mut_type == 'swap':
                Configs.enc.mut = Configs.enc.Mutation(Configs, Configs.enc.configs).swap
            if rep_type == 'rank-based':
                Configs.rep = Configs.prob_type.rank_based
            Configs.pop_size = pop_size
            Configs.par_size = par_size
            Configs.off_size = off_size
            Configs.mut_rate = mut_rate

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
            Running = True
            Thread(target=start_GA, args=()).start()
            return False
        elif ctx.triggered[0]['prop_id'] == 'resume.n_clicks':
            Running = True
            Thread(target=resume_GA, args=()).start()
            return False

    return app


def start_GA():
    global Population, Stats

    Stats = Statistics(Configs)
    Population = Configs.enc.initialize()
    Population = Configs.eval(Population)

    while Running:
        parents = Configs.sel(Population, Configs.par_size)
        offspring = Configs.enc.rec(parents)
        offspring = Configs.enc.mut(offspring)
        offspring = Configs.eval(offspring)
        Population = Configs.rep(np.concatenate((Population, offspring), axis=0),
                                 Configs.pop_size)
        Stats.update_dynamic(Population)


def resume_GA():
    global Population

    while Running:
        parents = Configs.sel(Population, Configs.par_size)
        offspring = Configs.enc.rec(parents)
        offspring = Configs.enc.mut(offspring)
        offspring = Configs.eval(offspring)
        Population = Configs.rep(np.concatenate((Population, offspring), axis=0),
                                 Configs.pop_size)
        Stats.update_dynamic(Population)
