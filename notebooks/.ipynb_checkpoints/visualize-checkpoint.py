import numpy as np
import pandas as pd
from plotly import graph_objects as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc


def network(self, ind):
    locs = np.loadtxt('loc.txt')  
    
    fig = go.Figure(data=[go.Scatter(x=[locs[0][0]] + [locs[0][ind['gene'][i]] for i in range(self.params['gene_size'])] + [locs[0][0]],
                                     y=[locs[1][0]] + [locs[1][ind['gene'][i]] for i in range(self.params['gene_size'])] + [locs[1][0]],
                                     mode='lines+markers')])
    fig.update_layout(title='Current Best Route', xaxis_title='Latitude', yaxis_title='Longitude')
    return dcc.Graph(figure=fig)


def selection(self, ind):
    value = np.loadtxt('value.txt')
    weight = np.loadtxt('weight.txt')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=value[np.where(ind['gene'] == 1)], 
                             y=weight[np.where(ind['gene'] == 1)],
                             mode='markers',
                             name='Selected'))
    fig.add_trace(go.Scatter(x=value[np.where(ind['gene'] == 0)], 
                         y=weight[np.where(ind['gene'] == 0)],
                         mode='markers',
                         name='Not selected'))
    fig.update_layout(title='Current Best Selection', xaxis_title='Value', yaxis_title='Weight')
    
    return dcc.Graph(figure=fig)


def chess_board(self, ind):
    fig = go.Figure()

    z = np.zeros(shape=(self.params['gene_size'], self.params['gene_size']))
    for i in range(self.params['gene_size']):
        z[i][ind['gene'][i]] = 1
    
    fig.add_trace(go.Heatmap(z=z))
    fig.update_layout(title='Current Best Arrangement')

    return dcc.Graph(figure=fig)


def sudoku_board(self, ind):
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(z=np.array(ind['gene'] % 10).reshape(10, 10)))
    fig.update_layout(title='Current Best Solution')
    
    return dcc.Graph(figure=fig)