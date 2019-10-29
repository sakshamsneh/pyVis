# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%
import pandas as pd

#%%
dataset=pd.read_csv('#endgameTweets.csv')

#%%
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

#%%
from googletrans import Translator
translator = Translator()

#%%
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

#%%
# from collections import Counter
# print(sentiment_analyzer_scores(dataset.iloc[0]['Cleaned Tweet Text']))
# dataset.iloc[0]['Cleaned Tweet Text']
# list=[]
# for index, row in dataset.iterrows():
#     list.append(sentiment_analyzer_scores(row['Cleaned Tweet Text']))
# dt=Counter(list)

#%%
sent1={}
for index, row in dataset.iterrows():
    sent1[row['Cleaned Tweet Text']]=sentiment_analyzer_scores(row['Cleaned Tweet Text'])

#%%
from IPython import get_ipython

#%%
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS
get_ipython().run_line_magic('matplotlib', 'inline')

#%%
stopwords = STOPWORDS
stopwords.add('Endgame')
stopwords.add('Marvel')

#%%
pos=[]
neu=[]
neg=[]
for k,v in sent1.items():
    if v==1:
        pos.append(k)
    elif v==-1:
        neg.append(k)
    elif v==0:
        neu.append(k)
all_pos = ' '.join(pos)
all_neu = ' '.join(neu)
all_neg = ' '.join(neg)

#%%
wordcloudpos = WordCloud(stopwords=stopwords, background_color="white", max_words=100, width=1600, height=800).generate(all_pos)
wordcloudneu = WordCloud(stopwords=stopwords, background_color="white", max_words=100, width=1600, height=800).generate(all_neu)
wordcloudneg = WordCloud(stopwords=stopwords, background_color="white", max_words=100, width=1600, height=800).generate(all_neg)

#%%
rcParams['figure.figsize'] = 20, 10
plt.imshow(wordcloudpos)
plt.axis("off")
plt.show()

#%%
rcParams['figure.figsize'] = 20, 10
plt.imshow(wordcloudneu)
plt.axis("off")
plt.show()

#%%
rcParams['figure.figsize'] = 20, 10
plt.imshow(wordcloudneg)
plt.axis("off")
plt.show()
