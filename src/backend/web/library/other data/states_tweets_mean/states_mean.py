import json, os, pprint, yaml
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def find_states_twitter_mean(mean_for_x_days):
    """ Returns the mean of twitters for each united state. """

    db_docs = list(TWITTER_COLLECTION.find({"Date": {"$gte": datetime.utcnow() - timedelta(days=mean_for_x_days)}}))

    # Find min and max date for the query and then calculate the difference of the days
    dates = []
    for doc in db_docs:
        dates.append(doc.get('Date'))

    min_date, max_date = min(dates), max(dates)
    day_dif = (max_date.date() - min_date.date()).days

    # 1. Specify dates which must be queried throught "usa_points" list
    dates_queries = []
    for day in range(1, day_dif+1):
        dates_queries.append(datetime.utcnow() - timedelta(hours=24*day))

    # 2. Create dicts which contain tweets/states for each day of 'day_dif'
    temp_list, twitter_day_data = [], []
    for date in dates_queries:
        for doc in db_docs:
            if (doc.get('Date') >= date) and (doc.get('Date') <= date + timedelta(days=1)):
                temp_list.append(doc.get('state_code'))

        if temp_list:
            twitter_day_data.append({"Date": date,
                                     "twitter_data": temp_list})
            temp_list = []

    # 3. For each dict. (each date) of the above list, find the tweets count for each state
    tweet_sum, temp_state_and_tweets = 0, []
    for data in twitter_day_data:

        for state in STATES:
            for state_data in data.get('twitter_data'):
                if state == state_data:
                    tweet_sum += 1

            if tweet_sum != 0:
                temp_state_and_tweets.append({"state": state,
                                              "tweets": tweet_sum})
                tweet_sum = 0

    # 4. Find the average of the above list for all states and divide by day_dif.
    tweet_sum, state_and_tweets_mean = 0, []
    for state in STATES:
        for data in temp_state_and_tweets:
            if state == data.get("state"):
                tweet_sum += data.get('tweets')

        if tweet_sum != 0:
            state_and_tweets_mean.append({"state": state,
                                          "tweets": round(tweet_sum/day_dif)})
            tweet_sum = 0

    # 5. Match states's values with markets
    markets_and_tweets = []
    for state in state_and_tweets_mean:
        for pair in STATES_AND_MARKETS:
            if state.get('state') == pair.get('state_code'):
                for market in pair.get('markets'):
                    markets_and_tweets.append({
                        "market": market,
                        "tweets": state.get('tweets')
                    })

    # 6. Find the average of above list (case of duplicated markets, almost ever)
    tweets_sum, market_counter, market_and_tweet_mean = 0, 0, []
    for market1 in MARKETS:
        for market2 in markets_and_tweets:
            if market1 == market2.get('market'):
                tweets_sum += market2.get('tweets')
                market_counter += 1

        if market_counter != 0:
            market_and_tweet_mean.append({
                "market": market1,
                "tweets": round((tweets_sum/market_counter)) 
            })
            tweets_sum, market_counter = 0, 0


if __name__ == "__main__":

    def file_path(folder_name, file_name):
        """ Specify file path. """

        file_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(file_directory)
        file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
        return file_path

    with open(file_path('states_tweets_mean/files','markets_names.json')) as statesFile:
        MARKETS = json.load(statesFile)

    with open(file_path('states_tweets_mean/files','states_codes.json')) as statesFile:
        STATES = json.load(statesFile)

    with open(file_path('states_tweets_mean/files','states_and_markets.json')) as statesFile:
        STATES_AND_MARKETS = json.load(statesFile)

    with open(file_path('states_tweets_mean', 'config.yaml'), encoding='utf-8') as file:
        CONF = yaml.full_load(file)

    def connect_to_twitter_light_col():
        uri = CONF['db']['uri']
        db = CONF['db']['db']
        collection = CONF['db']['twitter_usa_light_collection']
        client = MongoClient(uri, serverSelectionTimeoutMS=55000, connectTimeoutMS=40000, socketTimeoutMS=30000)
        try:
            result = client.admin.command("ismaster")
        except ConnectionFailure:
            print("Server not available")
            exit('------------------- \n')
        return client[db][collection]

    TWITTER_COLLECTION = connect_to_twitter_light_col()

    find_states_twitter_mean(3)