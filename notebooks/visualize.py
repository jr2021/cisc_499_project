import numpy as np
import pandas as pd
from plotly import graph_objects as go
from plotly import figure_factory as ff
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import base64

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
                             name='Selected item'))
    fig.add_trace(go.Scatter(x=value[np.where(ind['gene'] == 0)], 
                         y=weight[np.where(ind['gene'] == 0)],
                         mode='markers',
                         name='Not selected item'))
    fig.update_layout(title='Current Non-Dominated Item Selection', 
                      xaxis_title='Value of item', 
                      yaxis_title='Weight of item')
    
    return dcc.Graph(figure=fig)


def chess_board(self, ind):
    fig = go.Figure()

    z = np.indices((self.params['gene_size'], self.params['gene_size'])).sum(axis=0) % 2
    
    for i in range(self.params['gene_size']):
        z[i][ind['gene'][i]] = 2
    
    fig.add_trace(go.Heatmap(z=z, x=[], y=[], showscale=False, colorscale=[[0, '#d18b47'], [0.5, '#ffce9e'], [1, 'black']]))
    fig.update_layout(title='Current Best Placement')
    

    return dcc.Graph(figure=fig)


def sudoku_board(self, ind): 
    fig = ff.create_annotated_heatmap(np.array(ind['gene'] % 10).reshape(10, 10), annotation_text=np.array(ind['gene'] % 10).reshape(10, 10))
    
    fig.update_layout(title='Current Best Solution')
    
    return dcc.Graph(figure=fig)