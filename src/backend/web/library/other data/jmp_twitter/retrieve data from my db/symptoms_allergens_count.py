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

"""SYMPTOMS PROCESS"""

# symptoms = ['Sneezing', 'Runny Nose', 'Headache', 'Coughing', 'Shortness of Breath', 'Sore Throat', 'Itchy Eyes',
#                 'Red Eyes', 'Watery Eyes', 'Wheezing', 'Fatigue', 'Nasal Congestion']

with open('/home/allergy/Desktop/allergy-scripts/sna/symptoms.json') as f:
    symptoms = json.load(f)

def symptoms_processing():
    print('Symptoms Names - List:')
    print(symptoms)
    print('Total symptoms to be checked:', len(symptoms))
    print()
    print("Finding tweets with included hashtags from the Database, over the last X days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    dayCounter = datetime.datetime.utcnow() - datetime.timedelta(days=90)


    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonCountTweets = []
    countRegion = 0

    symptomsCount = 0

    symptomsDictionary = {}

    for symptom in symptoms:

        for symptomKey, valueSymptomList in symptom.items():
            print('Key: ' + symptomKey + ' - Value: ' + str(valueSymptomList))

            countAllergyTweets = 0

            for symptomSubName in valueSymptomList:
                print("Checking symptom: " + symptomSubName)

                query = {'$and': [{'mongoDate': {'$gte': dayCounter}}, {'text': re.compile(symptomSubName, re.IGNORECASE)},
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
                            {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)},
                            {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}

                # projection = {'created_at': 1, '_id': 0, 'user.location': 1}
                projection = {'created_at': 1, '_id': 0}

                # running query
                try:
                    cursor = allergyGlobal.find(query, projection)
                    # cursor = cursor.limit(2)

                except Exception as e:
                    print("Unexpected error:", type(e), e)


                # Listing dates coming from tweets for storing later the corresponding query in a CSV file
                # count = 0
                for doc in cursor:
                    # print(doc['created_at'])
                    # datesQuery.append(doc['created_at'])
                    countAllergyTweets += 1
                print()
                print(symptomSubName + " count finished --> Tweets until now: " + str(countAllergyTweets))

        print()
        if countAllergyTweets != 0:

            print("Symptom: " + symptomKey + " --> Total Number: " + str(countAllergyTweets))

            symptomsDictionary = {'name': symptomKey, 'y': countAllergyTweets}

            jsonCountTweets.append(symptomsDictionary)

            symptomsCount += 1
        print()

    print()
    print("Total symptoms scanned: ", symptomsCount)
    print('Symptoms processed Dictionary:')
    print(jsonCountTweets)
    print()
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/symptomsCount.json', 'w') as file:
        json.dump(jsonCountTweets, file, indent=4)
    print('Writing Symptoms Related Tweets JSON file completed!')
    print()

    # starting the percentage converted Dictionary
    jsonCountTweetsDuplicated = jsonCountTweets
    symptomsNumberAll = 0
    print('Adding the tweets countered symptoms:')
    for item in jsonCountTweetsDuplicated:
        # print(item['y'])
        symptomsNumberAll += item['y']

    print('Symptoms countered:', symptomsNumberAll)

    jsonCountTweetsPercentage = []

    for item in jsonCountTweetsDuplicated:
        x = (item['y'] * 100) / symptomsNumberAll
        x = round(x, 2)
        item['y'] = x
        jsonCountTweetsPercentage.append(item)

    print('Count Tweets Percentage:', jsonCountTweetsPercentage)
    print()
    x = 0
    for eachPercentage in jsonCountTweetsPercentage:
        x += eachPercentage['y']
    print('Total countered symptoms affections - validation of 100% --> x variable:', x)

    print()
    print('Writing JSON file percentage..')
    with open('/home/allergy/containers/website/files/symptomsCountPercentage.json', 'w') as file:
        json.dump(jsonCountTweetsPercentage, file, indent=4)
    print('Writing Symptoms Percentage Related Tweets JSON file completed!')

"""ALLERGENS PROCESS"""

allergens = ['Acacia', 'Alder', 'Ash', 'Bald Cypress', 'Beech', 'Birch', 'Cattail', 'Juniper', 'Chenopods',
             'Composites', 'Elm', 'Ephedra', 'Fir', 'Grasses', 'Hackberry', 'Hazelnut', 'Hemp', 'Hickory',
             'Goosefoot', 'Linden', 'Locust', 'Maple', 'Mesquite', 'Mixed Trace', 'Mulberry', 'Bayberry',
             'Nettle', 'Oak', 'Olive', 'Osage Orange', 'Palm', 'Pellitory', 'Amaranth', 'Pine', 'Plantain',
             'Poplar', 'Privet', 'Ragweed', 'Sagebrush', 'Dock', 'SweetGum', 'Sycamore', 'Tree of Heaven',
             'Walnut', 'Willow', 'Mold']

def allergens_processing():
    print('Allergens Names - List:')
    print(allergens)
    print('Total allergrens to be checked:', len(allergens))
    print()
    print("Finding tweets with included hashtags from the Database, over the last X days.")
    print('Querying database and retrieving the data.')
    # computing the datetime now - 7 days ago
    dayCounter = datetime.datetime.utcnow() - datetime.timedelta(days=90)

    print('Starting CSV to JSON conversion.')
    print('Data file processing..')
    jsonCountTweets = []

    allergensCount = 0

    allergensDictionary = {}

    for allergen in allergens:

        countAllergyTweets = 0

        query = {'$and': [{'mongoDate': {'$gte': dayCounter}}, {'text': re.compile(allergen, re.IGNORECASE)},
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
                                   {'user.location': re.compile(r'\bWY\b', re.IGNORECASE)},
                                   {'user.location': re.compile(r'\bWyoming\b', re.IGNORECASE)}]}]}

        projection = {'created_at': 1, '_id': 0}

        # running query
        try:
            cursor = allergyGlobal.find(query, projection)
            # cursor = cursor.limit(2)

        except Exception as e:
            print("Unexpected error:", type(e), e)

        # Listing dates coming from tweets for storing later the corresponding query in a CSV file
        # count = 0
        for doc in cursor:
            # print(doc['created_at'])
            # datesQuery.append(doc['created_at'])
            countAllergyTweets += 1

        if countAllergyTweets != 0:
            print("Allergen: " + allergen + " --> Number: " + str(countAllergyTweets))
            allergensDictionary = {'name': allergen, 'y': countAllergyTweets}
            jsonCountTweets.append(allergensDictionary)
            allergensCount += 1
        print()

    print()
    print("Total allergens scanned: ", allergensCount)
    print('Allergens processed Dictionary:')
    print(jsonCountTweets)
    print()
    print('Writing JSON file..')
    with open('/home/allergy/containers/website/files/allergensCount.json', 'w') as file:
        json.dump(jsonCountTweets, file, indent=4)
    print('Writing Allergens Related Tweets JSON file completed!')
    print()

    # starting the percentage converted Dictionary
    jsonCountTweetsDuplicated = jsonCountTweets
    allergensNumberAll = 0
    for item in jsonCountTweetsDuplicated:
        # print(item['y'])
        allergensNumberAll += item['y']

    print('Allergens countered:', allergensNumberAll)

    jsonCountTweetsPercentage = []

    for item in jsonCountTweetsDuplicated:
        x = (item['y'] * 100) / allergensNumberAll
        x = round(x, 2)
        item['y'] = x
        jsonCountTweetsPercentage.append(item)

    print('Count Tweets Percentage:', jsonCountTweetsPercentage)
    print()
    x = 0
    for eachPercentage in jsonCountTweetsPercentage:
        x += eachPercentage['y']
    print('Total counted allergens affections - validation of 100% --> x variable:', x)
    print()
    print('Writing JSON file percentage..')
    with open('/home/allergy/containers/website/files/allergensCountPercentage.json', 'w') as file:
        json.dump(jsonCountTweetsPercentage, file, indent=4)
    print('Writing Allergens Percentage Related Tweets JSON file completed!')

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
    print('SYMPTOMS RELATED ALLERGY TWEETS')
    symptoms_processing()
    print()
    print()
    print()
    print('ALLERGENS RELATED ALLERGY TWEETS')
    allergens_processing()

    print('Process completed!')
