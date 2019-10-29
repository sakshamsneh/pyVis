# %%
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# %%
plt.ion()
Gv = Network(notebook=False)
dataset = pd.read_csv('/data/edgelist1.csv', index_col=0)
G = nx.Graph()

# %%
u1 = dataset["u1"].tolist()
u2 = dataset["u2"].tolist()
w = dataset["w"].tolist()
for index, row in dataset.iterrows():
    G.add_edge(row['u1'], row['u2'], weight=row['w'])
# e = zip(u1, u2)
# G.add_edges_from(e)

# %%
# nx.draw(G)
Gv.from_nx(G)
Gv.show_buttons(filter_=['nodes','edges','physics'])
Gv.show("/output/mygraph.html")