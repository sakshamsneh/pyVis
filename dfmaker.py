import collections
import numpy as np
import pandas as pd
import tweepy
import re
import sys
import getopt

import config as cfg
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


def get_tweets(listOfTweets, keyword, numOfTweets=20, date_since='2019-1-1', lang="en"):
    # Iterate through all tweets containing the given word, api search mode
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
    return listOfTweets


def main(argv):
    listOfTweets = []
    tag = ''
    count = 200
    date_since = '2019-1-1'
    opts, _ = getopt.getopt(argv, "ht:c:d:", ["tag=", "count=", "date="])
    if not opts:
        print('dfmaker.py -t <tag> -c <count> -d <date>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dfmaker.py -t <tag> -c <count> -d <date>')
            sys.exit()
        elif opt in ("-t", "--tag"):
            tag = arg
        elif opt in ("-c", "--count"):
            count = arg
        elif opt in ("-d", "--date"):
            date_since = arg
    if not tag:
        print('Input tag')
        sys.exit(2)
    listOfTweets = get_tweets(listOfTweets, tag, count, date_since)
    dataset = pd.DataFrame(listOfTweets)
    dataset.to_csv(tag+'Tweets.csv')


if __name__ == "__main__":
    main(sys.argv[1:])
