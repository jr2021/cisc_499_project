import numpy as np
import pandas as pd
from plotly import graph_objects as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import base64

raw_board = 'board.png' # replace with your own image
encoded_board = base64.b64encode(open(raw_board, 'rb').read())

raw_queen = 'queen.png' # replace with your own image
encoded_queen = base64.b64encode(open(raw_queen, 'rb').read())


def network(self, ind):
    locs = np.loadtxt('loc.txt')  
    
    fig = go.Figure(data=[go.Scatter(x=[locs[0][0]] + [locs[0][ind['gene'][i]] for i in range(self.params['gene_size'])] + [locs[0][0]],
                                     y=[locs[1][0]] + [locs[1][ind['gene'][i]] for i in range(self.params['gene_size'])] + [locs[1][0]],
                                     mode='lines+markers')])
    fig.update_layout(xaxis_title='Latitude', yaxis_title='Longitude')
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
    fig.update_layout(title='Selected objects', xaxis_title='Value', yaxis_title='Weight')
    
    return dcc.Graph(figure=fig)

def chess_board(self, ind):
    fig = go.Figure()

    fig.update_yaxes(range=(0, 8), visible=False)
    fig.update_xaxes(range=(0, 8), visible=False)
    fig.update_layout()
    fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_board.decode()),
                xref="x",
                yref="y",
                x=0,
                y=8,
                sizex=8,
                sizey=8,
                sizing="stretch",
                opacity=1,
                layer="below")
    )

    for i in range(self.params['gene_size']):
        fig.add_layout_image(
            dict(
                source='data:image/png;base64,{}'.format(encoded_queen.decode()),
                xref="x",
                yref="y",
                x=i + 0.25,
                y=ind['gene'][i],
                sizex=1,
                sizey=1,
                opacity=0.75,
                layer="below")
        )

    return dcc.Graph(figure=fig)

def sudoku_board(self, ind):
    return dcc.Graph(figure=go.Figure())