import tweepy, time, json, yaml, os, sys, re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime 
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime


class MyListener(StreamListener):
    """ Custom StreamListener for streaming data. """

    def __init__(self, start_time, time_limit, counter_tweets, states):
        self.start_time = start_time
        self.limit = time_limit
        self.counter_tweets = counter_tweets
        self.states = states
        super(MyListener, self).__init__()

    def on_data(self, data):
        try:
            datajson = 0
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            # Add field MongoDB datetime format
            datajson['mongoDate'] = datetime.strptime(datajson['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

            # Save only tweets for usa's areas
            if datajson.get('user') and datajson.get('user').get('location'):
                for region in STATES:
                    for region_key, region_value_list in region.items():
                        find = False
                        for region_name in region_value_list:
                            if re.search(re.compile(r'\b{0}\b'.format(region_name), re.IGNORECASE), datajson.get('user').get('location')):
                                TWITTER_USA_COL.insert_one(datajson)
                                TWITTER_USA_LIGHT_COL.insert_one({"Date": datetime.utcnow(), "state_code": region_key})
                                self.counter_tweets += 1
                                find = True
                                break
                    if find:
                        break

            if (time.time() - self.start_time) < self.limit: 
                return True
            else:
                print(f"Execution finished at --> [UTC]: {datetime.utcnow()} | [UTC+3]: {datetime.now()}")
                print(f"Number of retrieved tweets: {self.counter_tweets}")
                print("------------------------------\n")
                return False

        except BaseException as e:
            print(f"Error on_data: {e}")
            time.sleep(10)

            if (time.time() - self.start_time) < self.limit: 
                return True
            else:
                print(f"Execution finished at --> [UTC]: {datetime.utcnow()} | [UTC+3]: {datetime.now()}")
                print(f"Number of retrieved tweets: {self.counter_tweets}")
                print("------------------------------\n")
                return False

    def on_error(self, status):
        print(status)
        if status == 420:
            print("Rate limit exceeded.")
            time.sleep(420)

            if (time.time() - self.start_time) < self.limit: 
                return True
            else:
                print(f"Execution finished at --> [UTC]: {datetime.utcnow()} | [UTC+3]: {datetime.now()}")
                print(f"Number of retrieved tweets: {self.counter_tweets}")
                print("------------------------------\n")
                return False
        else:

            if (time.time() - self.start_time) < self.limit: 
                return True
            else:
                print(f"Execution finished at --> [UTC]: {datetime.utcnow()} | [UTC+3]: {datetime.now()}")
                print(f"Number of retrieved tweets: {self.counter_tweets}")
                print("------------------------------\n")
                return False


if __name__ == '__main__':

    start_time = time.time()

    while(True):

        try:
            if (time.time() - start_time) > 20500: 
                break

            def file_path(folder_name, file_name):
                """ Specify file path. """

                file_directory = os.path.dirname(os.path.abspath(__file__))
                parent_directory = os.path.dirname(file_directory)
                file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
                return file_path

            with open(file_path('twitter_api/files','states.json')) as statesFile:
                STATES = json.load(statesFile)

            with open(file_path('twitter_api', 'config.yaml'), encoding='utf-8') as file:
                CONF = yaml.full_load(file)

            def connect_to_mongo(col_name):
                uri = CONF['db']['uri']
                db = CONF['db']['db']
                collection = CONF['db'][col_name]
                client = MongoClient(uri, serverSelectionTimeoutMS=55000, connectTimeoutMS=40000, socketTimeoutMS=30000)
                try:
                    result = client.admin.command("ismaster")
                except ConnectionFailure:
                    print("Server not available")
                    exit('------------------- \n')
                return client[db][collection]

            TWITTER_USA_COL = connect_to_mongo("twitter_usa_collection")
            TWITTER_USA_LIGHT_COL = connect_to_mongo("twitter_usa_light_collection")
            
            print("Initiating db connections finished")

            auth = OAuthHandler(CONF['twitter']['consumer_key'][0], CONF['twitter']['consumer_secret'][0])
            auth.set_access_token(CONF['twitter']['access_token'][0], CONF['twitter']['access_secret'][0])
            api = tweepy.API(auth)

            print("Initiating tweeter connection finished")

            my_listener = MyListener(start_time, 20500, 0, STATES)
            Stream(auth, my_listener).filter(track=[
                '#pollen #allergy',
                '#pollen #spring',
                '#allergy',
                '#allergens',
                '#allergen',
                '#pollen',
                '#allergyseason',
                '#allergic #symptoms',
                '#allergic #symptom',
                '#allergic #disease',
                '#allergic #diseases',
                'pollen allergy grass',
                'pollen allergy grasses',
                'pollen health allergy',
                'allergy pollen symptoms',
                'suffer pollen allergy',
                'pollen allergies',
                'pollen symptoms',
                'allergic pollen',
                'trees allergy',
                'flowers allergy',
                'weeds allergy',
                'molds allergy',
                'pine allergy',
                'allergic symptom',
                'allergic symptoms',
                'allergic disease',
                'allergic diseases',
                'food allergy'
            ])
        except:
            print("Something went wrong!")
