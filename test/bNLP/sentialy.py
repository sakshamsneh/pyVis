# %%
import pandas as pd

# %%
dataset = pd.read_csv('data/csv/#EndgameTweetsBig.csv')
dataset.head(3)

# %%
data = dataset[['Cleaned Tweet Text', 'Retweet Count',
                'Screen Name', 'Tweet Created At']].copy()

# %%
data.columns = ['tweet', 'rtc', 'user', 'datetime']

# %%
data.to_csv('data/csv/egManipTweets2.csv')

# %%
dataset = pd.read_csv('egManipTweets.csv')
userlist = dataset['user'].tolist()

# %%
res = []
[res.append(x) for x in userlist if x not in res]