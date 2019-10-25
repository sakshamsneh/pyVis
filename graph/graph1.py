# %%
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
import networkx as nx
import re
import matplotlib.pyplot as plt
from pyvis.network import Network
import colorsys

# %%
plt.ion()
Gv = Network(notebook=False)
dataset = pd.read_csv('data/csv/egUserSent.csv', index_col=0)
norm = mpl.colors.Normalize(vmin=-20, vmax=10)
cmap = cm.hot
m = cm.ScalarMappable(norm=norm, cmap=cmap)

# %%
G = nx.Graph()
color_map = []
dataset = dataset.sort_values(by=['sent'])
for index, row in dataset.iterrows():
    w = row['sent']
    if(w <= -0.05):
        c='red'
    elif(w > -0.05 and w < 0.05):
        c='blue'
    else:
        c='green'
    color_map.append(c)
    Gv.add_node(row['user'], color=c)

# %%
# pos=nx.circular_layout(G)
# pos2=nx.spring_layout(G, k=1,iterations=1)
# pos3=nx.random_layout(G)
# nx.draw_networkx_nodes(G, pos3, node_color=color_map, node_size=20)
# plt.figure(figsize=(20,10))
# plt.show()

# %%
# Gv.from_nx(G)
Gv.show_buttons(filter_=['physics'])
# G.enable_physics(True)
Gv.show("html/mygraph.html")