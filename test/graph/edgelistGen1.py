# Create edges from hashtags matches
# %%
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools

# %%
dataset = pd.read_csv('data/csv/hashTweets.csv', index_col=0,
                      converters={"hashtags": lambda x: x.strip("[]").replace("'", "").split(", ")})
dataset = dataset.sample(n=100, replace=True)

# %%
k = dataset.shape[0]
stoptag = ['endgame', 'marvel', 'avengers',
           'exclusive', 'giveaway', 'fun', 'funko', 'pop', 'Gi', 'E', 'G', '1', '2', '3', '', 'c', 'ff', 't', 'th', 'rt', 'repost', 'pl', 'po', 'p', 'mcu', 'maga', 'm', 'in', 'infinitywar', 'give', 'givea', 'giveawa']
commontags = set()


def list_contains(List1, List2):
    set1 = set([x.lower() for x in List1])
    set2 = set([x.lower() for x in List2])
    s = set2.intersection(set1).difference(set(stoptag))
    # commontags.update(s)
    return len(s)


# %%
edgelist = []
for index, row in dataset.iterrows():
    w = row['hashtags']
    u = row['user']
    for index2, row2 in dataset.tail(k-(index+1)).iterrows():
        w2 = row2['hashtags']
        u2 = row2['user']
        check = list_contains(w, w2)
        if(check != 0):
            edgelist.append([u, u2, check])
len(edgelist)

# %%
with open("data/edgelist.txt", "w") as output:
    for i in edgelist:
        for j in i:
            output.write('%s ' % j)
        output.write('\n')

# %%
data = pd.DataFrame(edgelist, columns=['u1', 'u2', 'w'])
data.to_csv('data/csv/edgelist1.csv')
