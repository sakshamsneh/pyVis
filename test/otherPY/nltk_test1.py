import nltk

from urllib.request import Request, urlopen
req = Request('https://en.wikipedia.org/wiki/Python_(programming_language)', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html,'html.parser')
text = soup.get_text(strip = True)
# print(text)

import re

tokens = [t for t in text.split()]
# tokens = re.split(r'\W+', text)
# print(tokens)

from nltk.corpus import stopwords
sr= stopwords.words('english')
clean_tokens = tokens[:]
for token in tokens:
    if token in sr:
        clean_tokens.remove(token)
    
freq = nltk.FreqDist(clean_tokens)
# for key,val in freq.items():
#     print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)