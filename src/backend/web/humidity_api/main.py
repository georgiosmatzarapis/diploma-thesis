from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from datetime import datetime, timedelta
from lib import (file_path, connect_to_mongodb_collection1,
                 connect_to_mongodb_collection2, humidity_api_call)
                 
import json, pprint, pymongo.errors


if __name__ == "__main__":

    HUMIDITY_API = connect_to_mongodb_collection1()
    TODAY_HUMIDITY_API = connect_to_mongodb_collection2()

    utc_now = datetime.utcnow()

    try:
        today_documents = list(TODAY_HUMIDITY_API.find())
        if len(today_documents) != 0:
            doc_date = today_documents[0].get('Forecast date')
    except ServerSelectionTimeoutError as e:
        print('\n-------------------')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        print(f'Could not connect to MongoDB: {e}')
        print('-------------------\n')
        exit()


    # First execution
    if len(today_documents) == 0:
        print('\n-------------------')
        print('First execution.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        humidity_api_call()
        print('-------------------\n')

    # First execution of the day (middle night execution - utc)
    elif (utc_now.date() > doc_date.date()):
        """
        Firstly, make a call to the the humidity_api_call().
        For the first execution of the day, take all the data from the today_humidity_api col.
        and find the humidity avrg of each market for this day. Then insert this document to
        the humidity_api col. using as 'Forecast date' the common date field from the
        today_humidity_api col. and delete documents from today_humidity_api col.
        """
        print('\n-------------------')
        print('First call of the day.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        humidity_api_call()

        all_data, temp_document = [], []
        humidity, counter_hum, counter_no_error = 0, 0, 0

        markets_path = file_path('humidity_api', 'files/markets_names.json')
        with open(markets_path, encoding="utf-8") as json_file:
            MARKETS = json.load(json_file)
            
        for obs in today_documents:
            if not obs.get('error'):
                counter_no_error += 1
                for market in obs.get('Markets data'):
                    if market.get('cur_humidity') != 120:
                        all_data.append({"market": market.get('market'),
                                        "humidity": market.get('cur_humidity')})

        # If all the documents during the day had errors
        if counter_no_error == 0:

            final_document = {
                "Forecast date": datetime(doc_date.year, doc_date.month, doc_date.day),
                "error": 'err'
            }
            # Insert avr document of the date to the main collection for history use
            HUMIDITY_API.insert_one(final_document)
            # Delete all older date documents comparing to the inserted one
            TODAY_HUMIDITY_API.delete_many({'Forecast date': {'$lt': utc_now}})

        else:

            for name in MARKETS:

                for market in all_data:
                    if name == market.get('market'):
                        humidity += market.get('humidity')
                        counter_hum += 1
                    
                if counter_hum != 0:
                    temp_document.append({"market": name,
                                        "humidity": round((humidity/counter_hum),0)})
                    humidity, counter_hum = 0, 0
                else:
                    temp_document.append({"market": name,
                                        "humidity": 120})
                    humidity, counter_hum = 0, 0

            final_document = {
                "Forecast date": datetime(doc_date.year, doc_date.month, doc_date.day),
                "Markets data": temp_document
            }
            # Insert avr document of the date to the main collection for history use
            HUMIDITY_API.insert_one(final_document)
            # Delete all older date documents comparing to the inserted one
            TODAY_HUMIDITY_API.delete_many({'Forecast date': {'$lt': utc_now}})
        """ --------------------------------------------------- """

        print('------------------- \n')

    # Executions during the day
    elif utc_now.date() == doc_date.date():
        print('\n-------------------')
        print('Call during the day.')
        print(f'UTC: {datetime.utcnow()}')
        print(f'UTC+3: {datetime.now()}')
        humidity_api_call()
        print('-------------------\n')