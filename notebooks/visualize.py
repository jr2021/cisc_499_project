import numpy as np
from plotly import graph_objects as go

def network(self, ind):
    locs = np.loadtxt('loc.txt')  
    
    fig = go.Figure(data=[go.Scatter(x=[locs[0][0]] + [locs[0][ind['gene'][i]] for i in range(self.params['gene_size'])] + [locs[0][0]],
                                     y=[locs[1][0]] + [locs[1][ind['gene'][i]] for i in range(self.params['gene_size'])] + [locs[1][0]],
                                     mode='lines+markers')])
    fig.update_layout(xaxis_title='Latitude', yaxis_title='Longitude')
    return fig

def empty(self, ind):
    return go.Figure()