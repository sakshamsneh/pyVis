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
analyser = SentimentIntensityAnalyzer()
translator = Translator()
userval = {}
dataset = pd.read_csv('csv/egManipTweets.csv')

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


def sentiment_analyzer_scores(txt, engl=True):
    if engl:
        trans = txt
    else:
        trans = translator.translate(txt).text
    score = analyser.polarity_scores(str(trans))
    lb = score['compound']
    return lb
    # if lb >= 0.05:
    #     return 1
    # elif (lb > -0.05) and (lb < 0.05):
    #     return 0
    # else:
    #     return -1

# %%


def getDataset(headsize, itemsize):
    userlist = dataset['user'].head(headsize).tolist()

    res = []
    [res.append(x) for x in userlist if x not in res]

    for x in res:
        tweetlist = {}
        val = []
        try:
            for tweet in tweepy.Cursor(api.user_timeline, id=x).items(itemsize):
                t = clean_tweets(tweet.text)
                k = sentiment_analyzer_scores(t)
                val.append(k)
                tweetlist[str(t)] = k
                # tweetlist.update({ t : k })
                # tweetlist.append(sentiment_analyzer_scores(t))
            userval[str(x)] = mean(val)
            print('.')
        except tweepy.TweepError:  # Caused by inexistance of user x
            pass
        # tweet.retweet_count
        # tweet.favorite_count
        # listOfTweets.append(dict_)


# %%
# print(dataset.shape[0])
getDataset(dataset.shape[0], 20)

# %%
itemMaxValue = max(userval.items(), key=lambda x: x[1])
listOfKeys = list()
for key, value in userval.items():
    if value == itemMaxValue[1]:
        listOfKeys.append(key)

print('Maximum Sentiment Value : ', itemMaxValue[1])
print('Users with maximum Value : ', listOfKeys)

# %%
itemMinValue = min(userval.items(), key=lambda x: x[1])
listOfKeys = list()
for key, value in userval.items():
    if value == itemMinValue[1]:
        listOfKeys.append(key)

print('Minimum Sentiment Value : ', itemMinValue[1])
print('Users with minimum Value : ', listOfKeys)

# %%
s=pd.DataFrame(list(userval.items()), columns=['user', 'sent'])
s.to_csv('csv/egUserSent.csv')