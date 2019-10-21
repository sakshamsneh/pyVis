import config as cfg
from googletrans import Translator
import pandas as pd
import tweepy
import numpy as np
import re
import sys

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

translator = Translator()

auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth)


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


def sentiment_analyzer_scores(text, engl=True):
    if engl:
        trans = text
    else:
        trans = translator.translate(text).text
    score = analyser.polarity_scores(trans)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1


def getDataset():
    dataset = pd.read_csv('egManipTweets.csv')
    userlist = dataset['user'].tolist()

    res = []
    [res.append(x) for x in userlist if x not in res]
    for x in res:
        tweetlist = {}
        for tweet in tweepy.Cursor(api.user_timeline, id=x).items(50):
            t = clean_tweets(tweet.text)
            tweetlist[t] = sentiment_analyzer_scores(t)
        # tweet.retweet_count
        # tweet.favorite_count
        # listOfTweets.append(dict_)
