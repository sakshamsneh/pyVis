# %%
import config as cfg
from googletrans import Translator
import pandas as pd
import tweepy
import numpy as np
import re
from statistics import mean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# %%
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth)

# %%
trends1 = api.trends_place(23424848)
# trends1 is a list with only one element in it, which is a
# dict which we'll put in data.
data = trends1[0]
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
# put all the names together with a ' ' separating them
trendsName = ' '.join(names)

# %%
print(trendsName)