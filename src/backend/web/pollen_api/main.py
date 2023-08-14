""" Execution at 7:15 (utc+3) and then every 3 hours. """
from pymongo.errors import ServerSelectionTimeoutError

from datetime import datetime, timedelta
from lib import pollen_api_call, connect_to_sensors_collection, connect_to_markets_collection
# TODO Script which will periodically delete data from db collections
if __name__ == "__main__":

    SENSORS_COLLECTION = connect_to_sensors_collection()
    MARKETS_COLLECTION = connect_to_markets_collection()

    # Retrieve last document from each collection
    try:
        last_sensors_document = list(SENSORS_COLLECTION.find().sort("Forecast date", -1).limit(1))
        last_markets_document = list(MARKETS_COLLECTION.find().sort("Forecast date", -1).limit(1))
    except ServerSelectionTimeoutError as e:
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        print(f'Could not connect to MongoDB: {e}')
        print('------------------- \n')
        exit()

    query_time = datetime.utcnow() - timedelta(hours=4) # 4 hours because i get data about pollen at 04:00:00 (UTC)
    query_date = datetime(query_time.year, query_time.month, query_time.day)

    if len(last_sensors_document) != 0:
        last_document_forecast = last_sensors_document[0].get('Forecast date')
        last_document_date = datetime(last_document_forecast.year, last_document_forecast.month, last_document_forecast.day)


    # First execution
    if len(last_sensors_document) == 0:
        print('First execution.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        pollen_api_call(query_date, 0)
        print('------------------- \n')

    # First execution of the day or just first execution
    elif (query_date > last_document_date):
        print('First call of the day.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        pollen_api_call(query_date, last_document_forecast)
        print('------------------- \n')

    # Executions during the day
    elif query_date == last_document_date:
        print('Call during the day.')

        # if-statement just for debugging reasons. Because of the same behaviour on errors
        # can check both collections
        if last_sensors_document[0].get('error'):

            print('Error')
            print(f'UTC: {datetime.utcnow()}')
            print(f'UTC+3: {datetime.now()}')
            pollen_api_call(query_date, last_document_forecast)
            SENSORS_COLLECTION.delete_one({'_id': last_sensors_document[0].get('_id')})
            MARKETS_COLLECTION.delete_one({'_id': last_markets_document[0].get('_id')})
            print('------------------- \n')

        else:

            print('No error')
            print(f'UTC: {datetime.utcnow()}')
            print(f'UTC+3: {datetime.now()}')
            pollen_api_call(query_date, last_document_forecast)
            SENSORS_COLLECTION.delete_one({'_id': last_sensors_document[0].get('_id')})
            MARKETS_COLLECTION.delete_one({'_id': last_markets_document[0].get('_id')})
            print('------------------- \n')