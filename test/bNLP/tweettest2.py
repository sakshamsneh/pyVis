# %%
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re
import tweepy
from statistics import mean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import config as cfg

# %%
hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
analyser = SentimentIntensityAnalyzer()
userval = {}
dataset = pd.read_csv('data/csv/egManipTweets2.csv')

# %%
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# %%


def extractHashtag(input_txt):
    r = re.findall(hashtag_re, input_txt)
    hashlist = [i for i in r]
    return hashlist


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def clean_tweets(lst):
    lst = np.vectorize(remove_pattern)(lst, r"RT @[\w]*:")
    lst = np.vectorize(remove_pattern)(lst, r"@[\w]*")
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst


def sentiment_analyzer_scores(txt):
    score = analyser.polarity_scores(str(txt))
    lb = score['compound']
    return lb

# %%


def getDataset(headsize, itemsize):
    userlist = dataset['user'].head(headsize).tolist()

    res = []
    [res.append(x) for x in userlist if x not in res]

    data = []
    for x in res:
        val = []
        h = []
        r = 0
        f = 0
        try:
            for tweet in tweepy.Cursor(api.user_timeline, id=x).items(itemsize):
                h.extend(extractHashtag(tweet.text))
                t = clean_tweets(tweet.text)
                k = sentiment_analyzer_scores(t)
                val.append(k)
                r = r + tweet.retweet_count
                f = f + tweet.favorite_count
            userval[str(x)] = mean(val)
            hl = []
            [hl.append(x) for x in h if x not in hl]
            data.append([str(x), mean(val), hl, r, f])
        except tweepy.TweepError:  # Caused by inexistance of user x
            pass

    return pd.DataFrame(data, columns=['user', 'sent', 'hashtags', 'rt', 'fav'])


# %%
df = getDataset(500, 20)
df.head(5)

# %%
df.to_csv('data/csv/hashTweets.csv')
