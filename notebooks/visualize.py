import numpy as np
import pandas as pd
from plotly import graph_objects as go
from plotly import figure_factory as ff
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import base64

# raw_board = 'board.png' # replace with your own image
# encoded_board = base64.b64encode(open(raw_board, 'rb').read())
# decoded_board = 'data:image/png;base64,{}'.format(encoded_board.decode())

# raw_queen = 'queen.png' # replace with your own image
# encoded_queen = base64.b64encode(open(raw_queen, 'rb').read())
# decoded_queen = 'data:image/png;base64,{}'.format(encoded_queen.decode())

# chess_board_fig = go.Figure()


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
    fig.update_layout(title='Current Best Item Selection', xaxis_title='Value of Item', yaxis_title='Weight of Item')
    
    return dcc.Graph(figure=fig)


def chess_board(self, ind):
    fig = go.Figure()

    z = np.zeros(shape=(self.params['gene_size'], self.params['gene_size']))
    for i in range(self.params['gene_size']):
        z[i][ind['gene'][i]] = 1
    
    fig.add_trace(go.Heatmap(z=z))
    fig.update_layout(title='Current Best Placement', xaxis_title='Column', yaxis_title='Row')

    return dcc.Graph(figure=fig)

# def chess_board(self, ind):
#     fig = go.Figure()

#     fig.update_yaxes(range=(0, self.params['gene_size']), visible=False)
#     fig.update_xaxes(range=(0, self.params['gene_size']), visible=False)
#     fig.update_layout()
#     fig.add_layout_image(
#             dict(
#                 source=decoded_board,
#                 xref="x",
#                 yref="y",
#                 x=0,
#                 y=self.params['gene_size'],
#                 sizex=self.params['gene_size'],
#                 sizey=self.params['gene_size'],
#                 sizing="stretch",
#                 opacity=1,
#                 layer="below")
#     )

#     for i in range(self.params['gene_size']):
#         fig.add_layout_image(
#             dict(
#                 source=decoded_queen,
#                 xref="x",
#                 yref="y",
#                 x=i + 0.25,
#                 y=ind['gene'][i],
#                 sizex=1,
#                 sizey=1,
#                 opacity=0.75,
#                 layer="below")
#         )

#     return dcc.Graph(figure=fig)



def sudoku_board(self, ind): 
    fig = ff.create_annotated_heatmap(np.array(ind['gene'] % 10).reshape(10, 10), annotation_text=np.array(ind['gene'] % 10).reshape(10, 10))
    
    fig.update_layout(title='Current Best Solution', xaxis_title='Column', yaxis_title='Row')
    
    return dcc.Graph(figure=fig)