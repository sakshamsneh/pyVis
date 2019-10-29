# %%
import pandas as pd
import numpy as np
import networkx as nx
import re
import matplotlib.pyplot as plt
from pyvis.network import Network

# %%
G = Network(notebook=False)
G_fb = nx.read_edgelist("data/facebook_combined.txt",
                        create_using=nx.Graph(), nodetype=int)
print(nx.info(G_fb))

# %%
# nx.draw(G_fb)

# %%
pos = nx.spring_layout(G_fb)
betCent = nx.betweenness_centrality(G_fb, normalized=True, endpoints=True)
node_color = [20000.0 * G_fb.degree(v) for v in G_fb]
node_size = [v * 10000 for v in betCent.values()]
plt.figure(figsize=(20, 20))
nx.draw_networkx(G_fb, pos=pos, with_labels=False,
                 node_color=node_color,
                 node_size=node_size)
plt.axis('off')
# plt.show()

# %%
G.from_nx(G_fb)
G.show_buttons(filter_=['physics'])
# G.enable_physics(True)
G.show("mygraph.html")