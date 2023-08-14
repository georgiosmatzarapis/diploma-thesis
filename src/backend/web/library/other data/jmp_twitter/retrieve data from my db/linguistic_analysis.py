import re
import datetime
import string
import csv
import json
import operator
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import urllib

from dateutil import parser
from pymongo import MongoClient
from collections import deque
from textblob import TextBlob
from wordcloud import WordCloud
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords


# current Datetime the process is running
now = datetime.datetime.now()
print('Time now:', now)

utcnow = datetime.datetime.utcnow()
print('Time now in UTC:', utcnow)

# connect to database
# using urllib.parse.quote to pass the 'a' inside the password and the URI of MongoDB connection
mongo_uri = "mongodb://iotlabRoot:" + urllib.parse.quote("wsnlab123@") + "@192.168.99.11"
connection = MongoClient(mongo_uri, 27017)
print('MongoDB connection is successful!')

# connect to database "threats"
db = connection.admin
# db.authenticate('allergy', 'dust')

# find the db
allergydb = connection.allergy

# find the right collection
allergyGlobal = allergydb.allergyGlobal

print("Database connection successful..")


def retrieve_Tweets():
    query = {
        '$or': [{'user.location': re.compile(r'\bUSA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bUS\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bUnited States\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bAK\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bAlaska\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bAL\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bAlabama\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bAR\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bArkansas\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bAS\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bAS\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bAZ\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bArizona\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bCA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bCalifornia\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bCO\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bColorado\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bCT\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bConnecticut\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bDC\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWashington, DC\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bDE\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bDelaware\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bFL\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bFlorida\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bGA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bGeorgia\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bGU\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bGU\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bHI\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bHawaii\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIowa\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bID\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIdaho\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIL\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIllinois\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIN\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bIndiana\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bKS\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bKansas\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bKY\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bKentucky\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bLA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bLouisiana\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMassachusetts\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMD\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMaryland\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bME\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMaine\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMI\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMichigan\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMN\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMinnesota\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMO\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMissouri\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMS\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMississippi\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMT\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bMontana\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNC\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNorth Carolina\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bND\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNorth Dakota\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNE\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNebraska\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNH\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNew Hampshire\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNJ\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNew Jersey\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNM\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNew Mexico\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNV\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNevada\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNY\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bNew York\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bOH\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bOhio\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bOK\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bOklahoma\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bOR\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bOregon\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bPA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bPennsylvania\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bPR\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bPR\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bRI\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bRhode Island\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bSC\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bSouth Carolina\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bSD\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bSouth Dakota\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bTN\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bTennessee\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bTX\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bTexas\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bUT\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bUtah\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bVA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bVirginia\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bVI\b', re.IGNORECASE)},
                # {'user.location': re.compile(r'\bVI\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bVT\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bVermont\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWA\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWashington\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWI\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWisconsin\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWV\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWest Virginia\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)},
                {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}

    projection = {'created_at': 1, '_id': 0, 'text': 1}
    # projection = {'created_at': 1, '_id': 0, 'text': 1, 'user.screen_name': 1}

    # running query
    cursor = []
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(50)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    return cursor


"""CATEGORICAL ANALYSIS - MOST FREQUENT TERMS"""


# function for tweet processing
def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
    """Process the text of a tweet:
        1. Lowercase
        2. Tokenize
        3. Stopword removal
        4. Digits removal
        5. Return list
    """
    textLowercase = text.lower()
    textLowercase = textLowercase
    tokens = tokenizer.tokenize(textLowercase)

    return [tok for tok in tokens if tok not in stopwords and not tok.isdigit() and not tok.startswith(('#', '@', 'http', 'https'))]


# function for splitting contracted forms of two separate tokens
def normalize_contractions(tokens):
    token_map = {
        "i'm": "i am",
        "you're": "you are",
        "it's": "it is",
        "we're": "we are",
        "we'll": "we will",
    }
    for tok in tokens:
        if tok in token_map.keys():
            for item in token_map[tok].split():
                yield item
        else:
            yield tok


def sentiment_Tweet(tweet_list):
    sent_results=[]
    for i in tweet_list:
        sent_results.append(tuple(TextBlob(i).sentiment))
    return sent_results



#https://python-graph-gallery.com/261-custom-python-wordcloud/
def wordcloud(str_t):
    # Create a list of word
    text = (str_t)

    # Create the wordcloud object
    wordcloud = WordCloud(width=480, height=480,background_color="white", margin=0).generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()

# + word tree


def freq_phrases(tweet_list, num_grams):
    phrase = {}
    for i in tweet_list: # list from db
        blob = TextBlob(i)
        temp = blob.ngrams(n=num_grams)
        for j in temp:
            phr=' '.join(map(str, j))
            if phr in phrase:
                phrase[phr] += 1
            else:
                phrase[phr] = 1
    return phrase



def find_url(string):
    # findall() has been used
    # with valid conditions for urls in string
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] '
                     '| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', string)
    return urls



def main():
    cursor=retrieve_Tweets()

    tweetTokenizer = TweetTokenizer()
    punct = list(string.punctuation)
    stopWordsUsed = ['get', 'broke']
    # stopwordList = stopwords.words('english') + punct + ['rt', 'via', '…', '...'] + stopWordsUsed
    stopwordList = punct + ['rt', 'via', '…', '...']


    domains = {}
    sent_results ={}
    tweet_list=[]
    for doc in cursor:
        tokens = ''

        # urls = find_url(str(doc['text']))
        # print(doc['text'])

        parsed_date = parser.parse(doc['created_at']).date()

        polarity = TextBlob(doc['text']).sentiment.polarity

        # print(TextBlob(doc['text']).sentiment.polarity)
        # print(TextBlob(doc['text']).sentiment.subjectivity)

        if parsed_date in sent_results:
            sent_results[parsed_date].append(polarity)
        else:
            sent_results[parsed_date]=[polarity]

        tweet_list.append(str(doc['text']))



        # x=input("next...")
        # if urls:
        #     for u in urls:
        #         if u in domains:
        #             domains[u]+=1
        #         else:
        #             domains[u] =1
        # print(urls)




        # try:
        #     tokens = process(text=doc['text'], tokenizer=tweetTokenizer, stopwords=stopwordList)
        #     # print(tokens)
        #     # x=input("next")
        # except Exception as exceptionTweet:
        #     print('Error! Not valid term:', exceptionTweet)

    # print(sent_results)

    freq_phr= freq_phrases(tweet_list, 3)
    distr = sorted(freq_phr.items(), key=operator.itemgetter(1), reverse=True)

    print(distr[0:20])

    temp_pl_sent={}
    x=[]
    y=[]
    for i in sent_results:
        temp_pl_sent[i]=np.mean(sent_results[i])
        y.append(np.mean(sent_results[i]))
        x.append(i)
    # print(x)
    # x=input("next ...")
    # print(y)




    # print(domains)



    # tweet_list = ["I love football now", "I love football ", " I admire football"]
    #
    # print(sentiment_Tweet(tweet_list))
    # print(freq_phrases(tweet_list, 3))

    # wordcloud("Python Python Python Matplotlib Matplotlib Seaborn Network Plot Violin Chart Pandas Datascience")


if __name__ == '__main__':
    main()


