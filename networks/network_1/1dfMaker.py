# %%
import collections
import numpy as np
import pandas as pd
import tweepy
import re
import sys
import getopt
from yaspin import yaspin

import config as cfg

# %%
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth)

# %%


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


def get_tweets(listOfTweets, keyword, numOfTweets=20, date_since='2019-1-1', lang="en"):
    # Iterate through all tweets containing the given word, api search mode
    spinner = yaspin()
    spinner.start()
    for tweet in tweepy.Cursor(api.search, q=keyword, lang=lang, since=date_since).items(numOfTweets):
        # Add tweets in this format
        dict_ = {'Screen Name': tweet.user.screen_name,
                 'User Name': tweet.user.name,
                 'Tweet Created At': str(tweet.created_at),
                 'Tweet Text': tweet.text,
                 'Cleaned Tweet Text': clean_tweets(tweet.text),
                 'User Location': str(tweet.user.location),
                 'Tweet Coordinates': str(tweet.coordinates),
                 'Retweet Count': str(tweet.retweet_count),
                 'Retweeted': str(tweet.retweeted),
                 'Phone Type': str(tweet.source),
                 'Favorite Count': str(tweet.favorite_count),
                 'Favorited': str(tweet.favorited),
                 'Replied': str(tweet.in_reply_to_status_id_str)
                 }
        listOfTweets.append(dict_)
    spinner.stop()
    return listOfTweets


# %%
# dfmaker.py -t #Endgame -c 5000 -d 2019-4-4
listOfTweets = []
tag = '#Endgame'
count = 5
date_since = '2019-4-4'
listOfTweets = get_tweets(listOfTweets, tag, count, date_since)

# %%
dataset = pd.DataFrame(listOfTweets)
dataset.to_csv('data/'+tag+'Tweets.csv')

# %%
data = dataset[['Cleaned Tweet Text', 'Retweet Count',
                'Screen Name', 'Tweet Created At']].copy()
data.columns = ['tweet', 'rtc', 'user', 'datetime']
data.to_csv('data/egManipTweets2.csv')
dataset = pd.read_csv('egManipTweets.csv')
