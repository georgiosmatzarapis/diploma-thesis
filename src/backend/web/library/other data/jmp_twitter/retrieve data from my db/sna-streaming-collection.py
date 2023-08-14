from pymongo import MongoClient
import pandas as pd
from collections import Counter
import urllib

# NLP libraries
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
import csv
import json
# from datetime import datetime
import datetime
from collections import deque
import re


"""TIME SERIES DESCRIPTIVE ANALYSIS SECTION"""

"""TIME SERIES DESCRIPTIVE ANALYSIS - BUG BOUNTY HASHTAGS"""
# Function for Data Analysis and CSV file creation
def findHashtagsTimeSeriesAllergy():

    print("Finding tweets with #allergy hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"allergy ",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    # query = {'entities.hashtags.text': {'$regex': 'allergy', '$options': 'i'}}
    # query for USA localized queries
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



    # projection = {'created_at': 1, '_id': 0, 'user.location': 1}
    projection = {'created_at': 1, '_id': 0}

    # running query
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(2)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    # Listing dates coming from tweets for storing later the corresponding query in a CSV file
    datesQuery = []
    counter = 0
    for doc in cursor:
        # print(doc['created_at'])
        # print(doc['user']['location'])
        datesQuery.append(doc['created_at'])
        counter += 1

    print('Number of returned results:', counter)
    print()
    print()

    """
        TIME SERIES ANALYSIS PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating Time Series:')
    # a list of "1" to count the hashtags
    ones = [1] * len(datesQuery)
    # the index of the series
    idx = pd.DatetimeIndex(datesQuery)
    # print('idx:')
    # print(idx)
    # the actual series (at series of 1s for the moment)
    timeSeries01 = pd.Series(ones, index=idx)
    print(timeSeries01.head())
    print("Counting tweets per day - executing descriptive analysis - Re-sampling / Bucketing..")
    # Resampling / bucketing
    per_day = timeSeries01.resample('1D').sum().fillna(0)
    print('Time Series created:')
    print(per_day.head())
    print('Creating data frame..')
    s = pd.DataFrame(per_day)
    print('Data frame:')
    print(s.head())

    print('Writing CSV file..')
    s.to_csv('/home/allergy/containers/website/files/perdayTimeSeriesAllergy.csv')
    print('Writing Allergy Time Series Descriptive Analysis CSV file completed!')


# function for converting CSV to JSON
def csvToJsonTimeSeriesAllergy():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/home/allergy/containers/website/files/perdayTimeSeriesAllergy.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            row[0] = row[0] + ' 14:00:00.000'
            datetimeObject = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            millisec = datetimeObject.timestamp() * 1000
            row[0] = millisec
            row[1] = int(float(row[1]))
            # print(row)
            jsonTimeSeries.append(row)
    # removing the head (first object) with not useful data - Data cleaning
    del jsonTimeSeries[0]

    # print('New file --> Time Series:')
    # print(jsonTimeSeries)
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/perdayTimeSeriesAllergy.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Dust JSON file completed!')
    print()
    print('Next:')


def findHashtagsTimeSeriesDust():

    print("Finding tweets with #dust hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"allergy ",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    # query = {'entities.hashtags.text': {'$regex': 'allergy', '$options': 'i'}}
    # query for USA localized queries
    query = {'$and': [{'text': re.compile('dust', re.IGNORECASE)},
        {'$or': [{'user.location': re.compile(r'\bUSA\b', re.IGNORECASE)},
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
    {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)}, {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}



    # projection = {'created_at': 1, '_id': 0, 'user.location': 1}
    projection = {'created_at': 1, '_id': 0}

    # running query
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(2)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    # Listing dates coming from tweets for storing later the corresponding query in a CSV file
    datesQuery = []
    counter = 0
    for doc in cursor:
        # print(doc['created_at'])
        # print(doc['user']['location'])
        datesQuery.append(doc['created_at'])
        counter += 1

    print('Number of returned results:', counter)
    print()
    print()

    """
        TIME SERIES ANALYSIS PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating Time Series:')
    # a list of "1" to count the hashtags
    ones = [1] * len(datesQuery)
    # the index of the series
    idx = pd.DatetimeIndex(datesQuery)
    # print('idx:')
    # print(idx)
    # the actual series (at series of 1s for the moment)
    timeSeries01 = pd.Series(ones, index=idx)
    print(timeSeries01.head())
    print("Counting tweets per day - executing descriptive analysis - Re-sampling / Bucketing..")
    # Resampling / bucketing
    per_day = timeSeries01.resample('1D').sum().fillna(0)
    print('Time Series created:')
    print(per_day.head())
    print('Creating data frame..')
    s = pd.DataFrame(per_day)
    print('Data frame:')
    print(s.head())

    print('Writing CSV file..')
    s.to_csv('/home/allergy/containers/website/files/perdayTimeSeriesDust.csv')
    print('Writing Dust Time Series Descriptive Analysis CSV file completed!')

# function for converting CSV to JSON
def csvToJsonTimeSeriesDust():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/home/allergy/containers/website/files/perdayTimeSeriesDust.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            row[0] = row[0] + ' 14:00:00.000'
            datetimeObject = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            millisec = datetimeObject.timestamp() * 1000
            row[0] = millisec
            row[1] = int(float(row[1]))
            # print(row)
            jsonTimeSeries.append(row)
    # removing the head (first object) with not useful data - Data cleaning
    del jsonTimeSeries[0]

    # print('New file --> Time Series:')
    # print(jsonTimeSeries)
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/perdayTimeSeriesDust.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Dust JSON file completed!')
    print()
    print('Next:')



def findHashtagsTimeSeriesHumidity():

    print("Finding tweets with #humidity hashtag from Database.")
    print('Querying database and retrieving the data.')

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$regex:"allergy ",$options:"$i"}}, {'created_at': 1, '_id':0})

    # creating query + projection for MongoDB
    # query = {'entities.hashtags.text': {'$regex': 'allergy', '$options': 'i'}}
    # query for USA localized queries
    query = {'$and': [{'text': re.compile('humidity', re.IGNORECASE)},
        {'$or': [{'user.location': re.compile(r'\bUSA\b', re.IGNORECASE)},
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
    {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)}, {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}



    # projection = {'created_at': 1, '_id': 0, 'user.location': 1}
    projection = {'created_at': 1, '_id': 0}

    # running query
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(2)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    # Listing dates coming from tweets for storing later the corresponding query in a CSV file
    datesQuery = []
    counter = 0
    for doc in cursor:
        # print(doc['created_at'])
        # print(doc['user']['location'])
        datesQuery.append(doc['created_at'])
        counter += 1

    print('Number of returned results:', counter)
    print()
    print()

    """
        TIME SERIES ANALYSIS PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating Time Series:')
    # a list of "1" to count the hashtags
    ones = [1] * len(datesQuery)
    # the index of the series
    idx = pd.DatetimeIndex(datesQuery)
    # print('idx:')
    # print(idx)
    # the actual series (at series of 1s for the moment)
    timeSeries01 = pd.Series(ones, index=idx)
    print(timeSeries01.head())
    print("Counting tweets per day - executing descriptive analysis - Re-sampling / Bucketing..")
    # Resampling / bucketing
    per_day = timeSeries01.resample('1D').sum().fillna(0)
    print('Time Series created:')
    print(per_day.head())
    print('Creating data frame..')
    s = pd.DataFrame(per_day)
    print('Data frame:')
    print(s.head())

    print('Writing CSV file..')
    s.to_csv('/home/allergy/containers/website/files/perdayTimeSeriesHumidity.csv')
    print('Writing Humidity Time Series Descriptive Analysis CSV file completed!')

# function for converting CSV to JSON
def csvToJsonTimeSeriesHumidity():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonTimeSeries = []
    with open('/home/allergy/containers/website/files/perdayTimeSeriesHumidity.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            row[0] = row[0] + ' 14:00:00.000'
            datetimeObject = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            millisec = datetimeObject.timestamp() * 1000
            row[0] = millisec
            row[1] = int(float(row[1]))
            # print(row)
            jsonTimeSeries.append(row)
    # removing the head (first object) with not useful data - Data cleaning
    del jsonTimeSeries[0]

    # print('New file --> Time Series:')
    # print(jsonTimeSeries)
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/perdayTimeSeriesHumidity.json', 'w') as file:
        json.dump(jsonTimeSeries, file, indent=4)
    print('Writing Time Series Humidity JSON file completed!')
    print()
    print('Next:')




"""CATEGORICAL ANALYSIS SECTION"""

"""CATEGORICAL ANALYSIS - MOST FREQUENT HASHTAGS"""
# Function for Categorical Analysis and CSV file creation
def findMostFrequentHashtags():

    print("Finding tweets with included hashtags from the Database, over the last 7 days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    sevenDaysAgo = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.hashtags.text': {$exists : true}}, {'entities.hashtags.text': 1, '_id': 0}).limit(5)

    # creating query + projection for MongoDB
    # query = {'$and': [{'entities.hashtags.text': {'$exists': 'true'}}, {'mongoDate': {'$gte': sevenDaysAgo}}]}

    # query for USA localized queries
    query = {
        '$and': [{'mongoDate': {'$gte': sevenDaysAgo}}, {'entities.hashtags.text': {'$exists': 'true'}}, {'user.lang': 'en'}, {
                '$or': [{'user.location': re.compile(r'\bUSA\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bUS\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bUnited States\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAK\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAlaska\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAL\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAlabama\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAR\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bArkansas\b', re.IGNORECASE)},
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
    {'user.location': re.compile(r'\bVT\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bVermont\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWA\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWashington\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWI\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWisconsin\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWV\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWest Virginia\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}

    projection = {'entities.hashtags.text': 1, '_id': 0}

    # running query
    cursor = []
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(20)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    print("Finding used hashtags frequency..")
    # Listing countered hashtags coming from tweets for storing later the corresponding query in a CSV file
    countAllHashtags = Counter()
    hashtagsList = []
    for doc in cursor:
        hashtagsKey = doc['entities']['hashtags']
        for item in hashtagsKey:
            itemNew = str(item['text'])
            # print(item['text'])
            # print(itemNew)
            hashtagsList.append(('#' + itemNew.lower()))
            # countAllHashtags.update(item['text'])

    # print(hashtagsList)
    countAllHashtags.update(hashtagsList)

    print('Most 10 frequently used hashtags:')
    print(countAllHashtags.most_common(10))

    """
    CATEGORICAL ANALYSIS (BAR-PLOT) PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating data frame:')
    hash_freq = countAllHashtags.most_common(10)
    hash = pd.DataFrame(hash_freq)
    hash.set_index(0, inplace=True)
    print('Data frame:')
    print(hash.head())
    print('Writing CSV file..')
    hash.to_csv('/home/allergy/containers/website/files/hashtagsAllergy.csv')
    print('Writing Hashtags Categorical Analysis to CSV file completed!')

# function for converting CSV to JSON
def csvToJsonHashtags():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsHashtags = []
    with open('/home/allergy/containers/website/files/hashtagsAllergy.csv') as csvfileHash:
        readCSVHash = csv.reader(csvfileHash, delimiter=',')
        next(readCSVHash)
        for row in readCSVHash:
            row[1] = int(row[1])
            jsonBarPlotsHashtags.append(row)

    # print('New file --> Hashtags Bar-Plots:')
    # print(jsonBarPlotsHashtags)
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/hashtagsAllergy.json', 'w') as file:
        json.dump(jsonBarPlotsHashtags, file, indent=4)
    print('Writing Hashtags Bar-Plots JSON file completed!')
    print()
    print('Next:')



"""CATEGORICAL ANALYSIS - MOST FREQUENT MENTIONS"""
# Function for Categorical Analysis and CSV file creation
def findMostFrequentMentions():

    print("Finding tweets with included mentions from the Database, over the last 7 days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    sevenDaysAgo = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # Mongo Shell query
    # db.twitterQuery2.find({'entities.user_mentions.screen_name': {$exists : true}}, {'entities.user_mentions.screen_name': 1, '_id': 0}).limit(5)

    # creating query + projection for MongoDB
    # query = {'$and': [{'entities.user_mentions.screen_name': {'$exists': 'true'}}, {'mongoDate': {'$gte': sevenDaysAgo}}]}
    # query for USA localized queries
    query = {
        '$and': [{'mongoDate': {'$gte': sevenDaysAgo}}, {'entities.user_mentions.screen_name': {'$exists': 'true'}}, {'user.lang': 'en'}, {
                '$or': [{'user.location': re.compile(r'\bUSA\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bUS\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bUnited States\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAK\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAlaska\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAL\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAlabama\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAR\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bArkansas\b', re.IGNORECASE)},
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
    {'user.location': re.compile(r'\bVT\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bVermont\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWA\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWashington\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWI\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWisconsin\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWV\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWest Virginia\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}

    projection = {'entities.user_mentions.screen_name': 1, '_id': 0}

    # running query
    cursor = []
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(20)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    print("Finding used mentions frequency..")
    # Listing countered mentions coming from tweets for storing later the corresponding query in a CSV file
    countAllMentions = Counter()
    mentionsList = []
    for doc in cursor:
        screenNameKey = doc['entities']['user_mentions']
        for item in screenNameKey:
            # print(item['screen_name'])
            mentionsList.append(item['screen_name'])
            # countAllMentions.update(item['screen_name'])

    # print(mentionsList)
    countAllMentions.update(mentionsList)

    print('Most 10 frequently used mentions:')
    print(countAllMentions.most_common(10))

    """
        CATEGORICAL ANALYSIS (BAR-PLOT) PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating data frame:')
    mentions_freq = countAllMentions.most_common(10)
    mentions = pd.DataFrame(mentions_freq)
    mentions.set_index(0, inplace=True)
    print('Data frame:')
    print(mentions.head())
    print('Writing CSV file..')
    mentions.to_csv('/home/allergy/containers/website/files/mentionsAllergy.csv')
    print('Writing Mentions Categorical Analysis to CSV file completed!')

# function for converting CSV to JSON
def csvToJsonMentions():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsMentions = []
    with open('/home/allergy/containers/website/files/mentionsAllergy.csv') as csvfileMentions:
        readCSVMentions = csv.reader(csvfileMentions, delimiter=',')
        next(readCSVMentions)
        for row in readCSVMentions:
            row[1] = int(row[1])
            jsonBarPlotsMentions.append(row)

    # print('New file --> Mentions Bar-Plots:')
    # print(jsonBarPlotsMentions)
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/mentionsAllergy.json', 'w') as file:
        json.dump(jsonBarPlotsMentions, file, indent=4)
    print('Writing Mentions Bar-Plots JSON file completed!')
    print()
    print('Next:')



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


# Function for Categorical Analysis and CSV file creation
def findMostFrequentTerms():

    print("Finding tweets with included terms from the Database, over the last 7 days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    sevenDaysAgo = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # creating query + projection for MongoDB
    # query = {'$and': [{'text': {'$exists': 'true'}}, {'mongoDate': {'$gte': sevenDaysAgo}}]}
    # query for USA localized queries
    query = {
        '$and': [{'mongoDate': {'$gte': sevenDaysAgo}}, {'text': {'$exists': 'true'}}, {'user.lang': 'en'}, {
                '$or': [{'user.location': re.compile(r'\bUSA\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bUS\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bUnited States\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAK\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAlaska\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAL\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAlabama\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bAR\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bArkansas\b', re.IGNORECASE)},
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
    {'user.location': re.compile(r'\bVT\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bVermont\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWA\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWashington\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWI\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWisconsin\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWV\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWest Virginia\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)},
    {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}

    projection = {'text': 1, '_id': 0}

    # running query
    cursor = []
    try:
        cursor = allergyGlobal.find(query, projection)
        # cursor = cursor.limit(50)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    print("Finding used terms frequency..")
    # Listing countered terms coming from tweets for storing later the corresponding query in a CSV file
    termsList = []
    countAllTerms = Counter()

    tweetTokenizer = TweetTokenizer()
    punct = list(string.punctuation)
    stopWordsUsed = ['get', 'broke']
    stopwordList = stopwords.words('english') + punct + ['rt', 'via', '…', '...'] + stopWordsUsed

    for doc in cursor:
        tokens = ''
        doc['text'] = doc['text'].encode('ascii', 'ignore')
        # print(doc['text'])
        try:
            tokens = process(text=doc['text'], tokenizer=tweetTokenizer, stopwords=stopwordList)
            # print(tokens)
        except Exception as exceptionTweet:
            print('Error! Not valid term:', exceptionTweet)

        countAllTerms.update(tokens)

    print('Most 10 frequently used terms:')
    print(countAllTerms.most_common(10))

    """
        CATEGORICAL ANALYSIS (BAR-PLOT) PANDAS SECTION
    """
    print('Starting data analysis with Pandas.')
    print('Creating data frame:')
    terms_freq = countAllTerms.most_common(10)
    terms = pd.DataFrame(terms_freq)
    terms.set_index(0, inplace=True)
    print('Data frame:')
    print(terms.head())
    print('Writing CSV file..')
    terms.to_csv('/home/allergy/containers/website/files/termsAllergy.csv')
    print('Writing Terms Categorical Analysis to CSV file completed!')

# function for converting CSV to JSON
def csvToJsonTerms():

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonBarPlotsTerms = []
    with open('/home/allergy/containers/website/files/termsAllergy.csv') as csvfileTerms:
        readCSVTerms = csv.reader(csvfileTerms, delimiter=',')
        next(readCSVTerms)
        for row in readCSVTerms:
            row[1] = int(row[1])
            jsonBarPlotsTerms.append(row)

    # print('New file --> Terms Bar-Plots:')
    # print(jsonBarPlotsTerms)
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/termsAllergy.json', 'w') as file:
        json.dump(jsonBarPlotsTerms, file, indent=4)
    print('Writing Terms Bar Plots to JSON file completed!')



"""MAIN FUNCTION"""
if __name__ == '__main__':

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

    # find the db
    allergydb = connection.allergy

    # find the right collection
    allergyGlobal = allergydb.allergyGlobal

    print("Database connection successful..")
    print()
    print('TIME SERIES DESCRIPTIVE ANALYSIS - ALLERGY RELATED HASHTAGS')
    findHashtagsTimeSeriesAllergy()
    csvToJsonTimeSeriesAllergy()
    print()
    print('CATEGORICAL ANALYSIS - MOST FREQUENT HASHTAGS')
    findMostFrequentHashtags()
    csvToJsonHashtags()
    print()
    print('CATEGORICAL ANALYSIS - MOST FREQUENT MENTIONS')
    findMostFrequentMentions()
    csvToJsonMentions()
    print()
    print('CATEGORICAL ANALYSIS - MOST FREQUENT TERMS')
    findMostFrequentTerms()
    csvToJsonTerms()

    print()
    print()

    # Irritants Analysis
    print('IRRITANTS ANALYSIS')
    print('Starting..')
    print('TIME SERIES DESCRIPTIVE ANALYSIS - DUST HASHTAGS')
    findHashtagsTimeSeriesDust()
    csvToJsonTimeSeriesDust()
    print()
    print('TIME SERIES DESCRIPTIVE ANALYSIS - HUMIDITY HASHTAGS')
    findHashtagsTimeSeriesHumidity()
    csvToJsonTimeSeriesHumidity()

    print('Process completed!')
