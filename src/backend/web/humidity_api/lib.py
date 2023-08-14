from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pyowm import OWM
from pyowm.exceptions import OWMError, api_call_error, api_response_error
from datetime import datetime, timedelta

import os, yaml, pprint, time, json


def file_path(folder_name, file_name):
    """ Specify file path. """
    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path


config_path = file_path('humidity_api', 'config.yaml')

if not os.path.isfile(config_path):
    print(f"Config file: {config_path} not found.")
    exit()

with open(config_path, encoding="utf-8") as file:
    CONF = yaml.full_load(file)


def connect_to_mongodb_collection1():
    """ Connect to 'humidity_api' collection. """

    uri = CONF['db']['uri']
    db = CONF['db']['db']
    collection = CONF['db']['humidity_api_collection']
    client = MongoClient(uri, serverSelectionTimeoutMS=75000, connectTimeoutMS=90000, socketTimeoutMS=90000)
    try:
        result = client.admin.command("ismaster")
    except ConnectionFailure:
        print("Server not available")
        print('------------------- \n')
        exit()
    return client[db][collection]


def connect_to_mongodb_collection2():
    """ Connect to 'today_humidity_api' collection. """

    uri = CONF['db']['uri']
    db = CONF['db']['db']
    collection = CONF['db']['today_humidity_api_collection']
    client = MongoClient(uri, serverSelectionTimeoutMS=85000, connectTimeoutMS=100000, socketTimeoutMS=100000)
    try:
        result = client.admin.command("ismaster")
    except ConnectionFailure:
        print("Server not available")
        print('------------------- \n')
        exit()
    return client[db][collection]


OWM_KEY = OWM(CONF['owm']['api_key'])
TODAY_HUMIDITY_API = connect_to_mongodb_collection2()

def humidity_api_call():
    """ Inserts in mongodb collection humidity data from OpenWeatherMap. """


    if OWM_KEY.is_API_online():

        markets_path = file_path('humidity_api', 'files/markets_with_owm_points.json')
        with open(markets_path, encoding="utf-8") as json_file:
            MARKETS = json.load(json_file)

        cur_humidity, counter_cur_humidity = 0, 0
        temp_for_humidity, temp_counter_for_humidity = 0, 0
        for_humidity, counter_for_humidity = 0, 0
        er_counter, forecast_counter = 0, 0
        id_list, city_data = [], []
        start = time.time()
        """ ------------------------------------------------------------------ """

        utc_now = datetime.utcnow()

        # For the ids of each market, find their average humidity density (current and tomorrow forecast)
        for market in MARKETS:

            for id_ in market.get('owm_points'):

                # calculate CURRENT humidity for each market - ERROR CHECKING
                try:
                    obs = OWM_KEY.weather_at_id(id_).get_weather()

                    if obs.get_humidity() >= 0 and obs.get_humidity() <= 100:
                        cur_humidity += obs.get_humidity()
                        counter_cur_humidity += 1

                except:
                    er_counter += 1
                """ --------------------------------------------------- """


                # calculate average FORECAST humidity for each id (tomorrow) - ERROR CHECKING
                try:
                    f = OWM_KEY.three_hours_forecast_at_id(id_).get_forecast().get_weathers()

                    for weather in f:
                        if weather.get_reference_time('date').date() > datetime.utcnow().date():
                            if weather.get_humidity() >= 0 and weather.get_humidity() <= 100:
                                temp_for_humidity += weather.get_humidity()
                                temp_counter_for_humidity += 1
                            forecast_counter += 1
                            # Find the avr of the first 8 times of forecast api. These are the times of
                            # the day which consider for the tomorrow day.
                            if forecast_counter == 8: break

                    # calculate average forecast humidity for each market
                    if temp_counter_for_humidity != 0:
                        for_humidity += round((temp_for_humidity/temp_counter_for_humidity),0)
                        counter_for_humidity += 1
                        temp_for_humidity, temp_counter_for_humidity = 0, 0

                    forecast_counter = 0

                except:
                    er_counter += 1
                """ --------------------------------------------------- """

            # Handle errors
            if er_counter >= 140:

                print('Error Occured')
                document = {
                    "Forecast date": datetime.utcnow(),
                    "error": 'err'
                }
                TODAY_HUMIDITY_API.insert_one(document)
                break

            else:

                # Create dicts for db
                if counter_cur_humidity != 0 and counter_for_humidity != 0:
                    city_data.append({"market": market.get('market'),
                                      "cur_humidity": round((cur_humidity/counter_cur_humidity),0),
                                      "for_humidity": round((for_humidity/counter_for_humidity),0)})
                    cur_humidity, counter_cur_humidity = 0, 0
                    for_humidity, counter_for_humidity = 0, 0

                elif counter_cur_humidity == 0 and counter_for_humidity != 0:
                    city_data.append({"market": market.get('market'),
                                      "cur_humidity": 120,
                                      "for_humidity": round((for_humidity/counter_for_humidity),0)})
                    cur_humidity, counter_cur_humidity = 0, 0
                    for_humidity, counter_for_humidity = 0, 0

                elif counter_cur_humidity != 0 and counter_for_humidity == 0:
                    city_data.append({"market": market.get('market'),
                                      "cur_humidity": round((cur_humidity/counter_cur_humidity),0),
                                      "for_humidity": 120})
                    cur_humidity, counter_cur_humidity = 0, 0
                    for_humidity, counter_for_humidity = 0, 0

                elif counter_cur_humidity == 0 and counter_for_humidity == 0:
                    city_data.append({"market": market.get('market'),
                                      "cur_humidity": 120,
                                      "for_humidity": 120})
                    cur_humidity, counter_cur_humidity = 0, 0
                    for_humidity, counter_for_humidity = 0, 0
        """ -------------------------- [END OF LOOPx2] -------------------------- """
        
        if er_counter < 140:

            document = {
                "Forecast date": datetime.utcnow(),
                "Markets data": city_data
            }
            TODAY_HUMIDITY_API.insert_one(document)
            end = time.time()
            print(end - start)

    else:

        print('Error Occured: OWM API IS DOWN')
        document = {
            "Forecast date": datetime.utcnow(),
            "error": 'OWM API IS DOWN'
        }
        TODAY_HUMIDITY_API.insert_one(document)