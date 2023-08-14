import os, json, re, yaml
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta


def file_path(folder_name, file_name):
    """ Specify file path. """
    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path

with open(file_path('../twitter_api', 'config.yaml'), encoding='utf-8') as file:
    CONF = yaml.full_load(file)

with open(file_path('files','states.json')) as statesFile:
    STATES = json.load(statesFile)

def connect_to_twitter_global_collection():
    uri = CONF['db']['uri']
    db = CONF['db']['db']
    collection = CONF['db']['twitter_global_collection']
    client = MongoClient(uri, serverSelectionTimeoutMS=55000, connectTimeoutMS=40000, socketTimeoutMS=30000)
    try:
        result = client.admin.command("ismaster")
    except ConnectionFailure:
        print("Server not available")
        print('------------------- \n')
        exit()
    return client[db][collection]

def connect_to_twitter_usa_collection():
    uri = CONF['db']['uri']
    db = CONF['db']['db']
    collection = CONF['db']['twitter_usa_collection']
    client = MongoClient(uri, serverSelectionTimeoutMS=55000, connectTimeoutMS=40000, socketTimeoutMS=30000)
    try:
        result = client.admin.command("ismaster")
    except ConnectionFailure:
        print("Server not available")
        print('------------------- \n')
        exit()
    return client[db][collection]


TWITTER_GLOBAL = connect_to_twitter_global_collection()
TWITTER_USA = connect_to_twitter_usa_collection()

def geoprocessing_tweets_usa():
    """ 
    Retrieves data from "twitter_global" collection and counts the number
    of relative tweets at each state of America. The results are stored
    to the "twitter_usa" collection.
    """

    utc = datetime.utcnow()
    dt_search = datetime(utc.year, utc.month, utc.day)
    temp_list = []

    for region in STATES:

        for region_key, region_list in region.items():
            counter_tweet = 0

            # Loop through the possible location states names for each state
            for region_name in region_list:
                query = {'$and': [{'mongoDate': {'$gte': dt_search}}, {'user.location': re.compile(r'\b{0}\b'.format(region_name), re.IGNORECASE)}]}
                projection = {'created_at': 1, '_id': 0}

                try:
                    cursor = list(TWITTER_GLOBAL.find(query, projection))
                except Exception as e:
                    print("Unexpected error:", type(e), e)

                if len(cursor) != []:
                    for doc in cursor:
                        counter_tweet += 1

            if counter_tweet != 0:
                temp_list.append({'state_code': region_key, 'tweets': counter_tweet})

    document = {
        "Date": utc,
        "States data": temp_list
    }

    TWITTER_USA.insert_one(document)
