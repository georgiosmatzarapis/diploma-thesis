import pymongo, pprint
from datetime import datetime

from lib import TWITTER_USA, geoprocessing_tweets_usa


if __name__ == "__main__":

    try:
        last_document = list(TWITTER_USA.find().sort("Date", -1).limit(1))
        if len(last_document) != 0:
            last_doc_date = last_document[0].get('Date')
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print('\n-------------------')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        print(f'Could not connect to MongoDB: {e}')
        print('-------------------\n')
        exit()

    # First execution
    if len(last_document) == 0:
        print('\n-------------------')
        print('First execution.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        geoprocessing_tweets_usa()
        print('-------------------\n')

    # First execution of the day (middle night execution - utc)
    elif datetime.utcnow().date() > last_doc_date.date():
        print('\n-------------------')
        print('First call of the day.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        geoprocessing_tweets_usa()
        print('------------------- \n')

    # Executions during the day
    elif datetime.utcnow().date() == last_doc_date.date():
        print('\n-------------------')
        print('Call during the day.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        geoprocessing_tweets_usa()
        print('-------------------\n')
