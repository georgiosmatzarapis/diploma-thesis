from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from aiohttp import ClientSession
from pyiqvia import Client
from pyiqvia.errors import IQVIAError
from dateutil.parser import parse
from datetime import datetime, timedelta

import dateutil.parser
import os, yaml, time, asyncio, iso8601, pytz, json, pprint


def file_path(folder_name, file_name):
    """ Specify file path. """

    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path

with open(file_path('pollen_api', 'files/markets_names.json')) as file:
    MARKETS = json.load(file)
with open(file_path('pollen_api', 'files/markets_with_sensors.json')) as file:
    MARKETS_WITH_SENSORS = json.load(file)
with open(file_path('pollen_api', 'test.json')) as file:
    TEST_JSON = json.load(file)

# Markets process: Create list which contains dicts of form {market, zip_code_data}
init_list = []
for market in MARKETS_WITH_SENSORS:
    for sensor in TEST_JSON.get('Sensor data'):
        if sensor.get('basic info').get('sensor_id') in market.get('sensors'):
            init_list.append({
                "market": market.get('market'),
                "zip_code_data": sensor
            })
pollen_data = []

def markets_processing(MARKETS, IQVIA_DATA):
    """ Implementation of the final document which includes data for all USA markets. """

    #[STAGE]: Create list which contains dict about markets's data

    today_pollen_index_sum, tomorrow_pollen_index_sum = 0, 0
    today_sensor_counter, tomorrow_sensor_counter = 0, 0
    today_triggers, tomorrow_triggers, markets_data_list = [], [], []

    for market1 in MARKETS:
        for market2 in IQVIA_DATA:
            if market1 == market2.get('market'):

                if len(market2.get('zip_code_data')) != 0:

                    # case of having only today data
                    if market2.get('zip_code_data').get('periods')[1].get('pollen_index') == None:
                        
                        today_index = market2.get('zip_code_data').get('periods')[0].get('pollen_index') 

                        if (today_index >= 0) and (today_index <= 12):
                            today_pollen_index_sum += today_index
                            today_sensor_counter += 1
                            for trigger in market2.get('zip_code_data').get('periods')[0].get('triggers'):
                                today_triggers.append(trigger.get('Name'))

                    # case of having both today & tomorrow data
                    else:

                        today_index = market2.get('zip_code_data').get('periods')[0].get('pollen_index')
                        tomorrow_index = market2.get('zip_code_data').get('periods')[1].get('pollen_index')

                        if (today_index >= 0) and (today_index <= 12):
                            today_pollen_index_sum += today_index
                            today_sensor_counter += 1
                            for trigger in market2.get('zip_code_data').get('periods')[0].get('triggers'):
                                today_triggers.append(trigger.get('Name'))

                        if (tomorrow_index >= 0) and (tomorrow_index <= 12):
                            tomorrow_pollen_index_sum += tomorrow_index
                            tomorrow_sensor_counter += 1
                            for trigger in market2.get('zip_code_data').get('periods')[1].get('triggers'):
                                tomorrow_triggers.append(trigger.get('Name'))


        # create market document for collection including both today & tomorrow data
        if today_sensor_counter != 0 and tomorrow_sensor_counter != 0:

            markets_data_list.append({
                "market": market1,
                "today": {
                    "pollen_index": round((today_pollen_index_sum/today_sensor_counter), 1),
                    "triggers": list(dict.fromkeys(today_triggers))
                },
                "tomorrow": {
                    "pollen_index": round((tomorrow_pollen_index_sum/tomorrow_sensor_counter), 1),
                    "triggers": list(dict.fromkeys(tomorrow_triggers))
                }
            })
            today_pollen_index_sum, tomorrow_pollen_index_sum = 0, 0
            today_sensor_counter, tomorrow_sensor_counter = 0, 0
            today_triggers, tomorrow_triggers = [], []

        elif today_sensor_counter != 0 and tomorrow_sensor_counter == 0:

            markets_data_list.append({
                "market": market1,
                "today": {
                    "pollen_index": round((today_pollen_index_sum/today_sensor_counter), 1),
                    "triggers": list(dict.fromkeys(today_triggers))
                },
                "tomorrow": {
                    "pollen_index": 100,
                    "triggers": []
                }
            })
            today_pollen_index_sum, today_sensor_counter, today_triggers = 0, 0, []

        elif today_sensor_counter == 0 and tomorrow_sensor_counter != 0:

            markets_data_list.append({
                "market": market1,
                "today": {
                    "pollen_index": 100,
                    "triggers": []
                },
                "tomorrow": {
                    "pollen_index": round((tomorrow_pollen_index_sum/tomorrow_sensor_counter), 1),
                    "triggers": list(dict.fromkeys(tomorrow_triggers))
                }
            })
            tomorrow_pollen_index_sum, tomorrow_sensor_counter, tomorrow_triggers = 0, 0, []

        elif today_sensor_counter == 0 and tomorrow_sensor_counter == 0:

            markets_data_list.append({
                "market": market1,
                "today": {
                    "pollen_index": 100,
                    "triggers": []
                },
                "tomorrow": {
                    "pollen_index": 100,
                    "triggers": []
                }
            })


    return markets_data_list

document = {
    "Forecast date": 1,
    "Sensor data": markets_processing(MARKETS, init_list)
}

with open('data.json', 'w') as outfile:
    json.dump(document, outfile)