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

""" Load necessary files. """
config_path = file_path('pollen_api', 'config.yaml')
zip_codes_path = file_path('pollen_api', 'files/zip_codes.json')
markets_path = file_path('pollen_api', 'files/markets_names.json')
markets_with_sensors_path = file_path('pollen_api', 'files/markets_with_sensors.json')

if not os.path.isfile(config_path):
    print(f"Config file: {config_path} not found.")
    exit()
elif not os.path.isfile(zip_codes_path):
    print(f"Zip codes file: {zip_codes_path} not found.")
    exit()
elif not os.path.isfile(markets_path):
    print(f"Markets's names file: {markets_path} not found.")
    exit()
elif not os.path.isfile(markets_with_sensors_path):
    print(f"Zip codes file: {markets_with_sensors_path} not found.")
    exit()

with open(config_path, encoding="utf-8") as file:
    CONF = yaml.full_load(file)
with open(zip_codes_path) as file:
    ZIP_CODES = json.load(file)
with open(markets_path) as file:
    MARKETS = json.load(file)
with open(markets_with_sensors_path) as file:
    MARKETS_WITH_SENSORS = json.load(file)

def connect_to_sensors_collection():
    uri = CONF['db']['uri']
    db = CONF['db']['db']
    collection = CONF['db']['pollen_sensors_collection']
    client = MongoClient(uri, serverSelectionTimeoutMS=55000, connectTimeoutMS=40000, socketTimeoutMS=30000)
    try:
        result = client.admin.command("ismaster")
    except ConnectionFailure:
        print("Server not available")
        print('------------------- \n')
        exit()
    return client[db][collection]

def connect_to_markets_collection():
    uri = CONF['db']['uri']
    db = CONF['db']['db']
    collection = CONF['db']['pollen_markets_collection']
    client = MongoClient(uri, serverSelectionTimeoutMS=55000, connectTimeoutMS=40000, socketTimeoutMS=30000)
    try:
        result = client.admin.command("ismaster")
    except ConnectionFailure:
        print("Server not available")
        print('------------------- \n')
        exit()
    return client[db][collection]

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
                    if market2.get('zip_code_data')[0].get('periods')[1].get('pollen_index') == None:
                        
                        today_index = market2.get('zip_code_data')[0].get('periods')[0].get('pollen_index') 

                        if (today_index >= 0) and (today_index <= 12):
                            today_pollen_index_sum += today_index
                            today_sensor_counter += 1
                            for trigger in market2.get('zip_code_data')[0].get('periods')[0].get('triggers'):
                                today_triggers.append(trigger.get('Name'))

                    # case of having both today & tomorrow data
                    else:

                        today_index = market2.get('zip_code_data')[0].get('periods')[0].get('pollen_index')
                        tomorrow_index = market2.get('zip_code_data')[0].get('periods')[1].get('pollen_index')

                        if (today_index >= 0) and (today_index <= 12):
                            today_pollen_index_sum += today_index
                            today_sensor_counter += 1
                            for trigger in market2.get('zip_code_data')[0].get('periods')[0].get('triggers'):
                                today_triggers.append(trigger.get('Name'))

                        if (tomorrow_index >= 0) and (tomorrow_index <= 12):
                            tomorrow_pollen_index_sum += tomorrow_index
                            tomorrow_sensor_counter += 1
                            for trigger in market2.get('zip_code_data')[0].get('periods')[1].get('triggers'):
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

def pollen_api_call(query_date, forecast_date):
    """ 
    Implements the insertion of pollen's values in mongodb collections.
    1st collection: Includes values from sensors.
    2nd collection: Process values from sensors and create pollen data about markets.
    """

    SENSORS_COLLECTION = connect_to_sensors_collection()
    MARKETS_COLLECTION = connect_to_markets_collection()

    yaml.warnings({'YAMLLoadWarning': False})

    async def main() -> None:
        """Create the aiohttp session and run."""
        async with ClientSession() as websession:
            await run(websession, query_date, forecast_date)


    async def run(websession, query_date, forecast_date):
        """Run."""

        """ Handle pyiqvia's errors. """
        try:
            start = time.time()
            pollen_data, init_list, sensor_col_data = [], [], []
            empty_document_counter = 0

            for zip_code in ZIP_CODES:

                """ Handle connection errors while defining client. """
                try:
                    client = Client(zip_code, websession)
                except:
                    # [CASE]: First execution
                    if forecast_date == 0:
                        query_date = datetime(datetime.utcnow().year,
                                              datetime.utcnow().month,
                                              datetime.utcnow().day)
                        document = {
                            "Forecast date": query_date + timedelta(hours=4),
                            "error": zip_code,
                            "error_type": 'Error while defining client: ClientError'
                        }
                        SENSORS_COLLECTION.insert_one(document)
                        MARKETS_COLLECTION.insert_one(document)
                        break
                    if query_date > forecast_date:
                        document = {
                            "Forecast date": forecast_date + timedelta(days=1),
                            "error": zip_code,
                            "error_type": 'Error while defining client: ClientError'
                        }
                        SENSORS_COLLECTION.insert_one(document)
                        MARKETS_COLLECTION.insert_one(document)
                        break
                    else:
                        document = {
                            "Forecast date": forecast_date,
                            "error": zip_code,
                            "error_type": 'Error while defining client: ClientError'
                        }
                        SENSORS_COLLECTION.insert_one(document)
                        MARKETS_COLLECTION.insert_one(document)
                        break


                current_values = await client.allergens.current()

                # len: 3, values: Yesterday, Today, Tomorrow, final len: 2
                if (len(current_values.get('Location').get('periods')) == 3 and 
                    current_values.get('Location').get('periods')[0].get('Type') == 'Yesterday' and
                    current_values.get('Location').get('periods')[1].get('Type') == 'Today' and
                    current_values.get('Location').get('periods')[2].get('Type') == 'Tomorrow'):   

                    # city info
                    forecast_date1 = current_values.get('ForecastDate')
                    date_obj = iso8601.parse_date(forecast_date1)
                    date_utc = date_obj.astimezone(pytz.utc)

                    sensor_id = current_values.get('Location').get('DisplayLocation')
                    city = current_values.get('Location').get('City')
                    state = current_values.get('Location').get('State')
                    city_zip_code = current_values.get('Location').get('ZIP')

                    # TODAY VALUES
                    period_type1 = current_values.get('Location').get('periods')[1].get('Type')
                    pollen_index_today = current_values.get('Location').get('periods')[1].get('Index')
                    triggers_today = current_values.get('Location').get('periods')[1].get('Triggers')

                    # TOMORROW VALUES
                    period_type2 = current_values.get('Location').get('periods')[2].get('Type')
                    pollen_index_tomorrow = current_values.get('Location').get('periods')[2].get('Index')
                    triggers_tomorrow = current_values.get('Location').get('periods')[2].get('Triggers')

                    """ Store above info to mongodb. """
                    pollen_data.append({"basic info": {"sensor_id": sensor_id.upper(),
                                                    "city": city,
                                                    "state": state,
                                                    "zip code": city_zip_code
                                                    },
                                        "periods": [{"pollen_index": pollen_index_today,
                                                    "triggers": triggers_today,
                                                    "type": period_type1},
                                                    {"pollen_index": pollen_index_tomorrow,
                                                    "triggers": triggers_tomorrow,
                                                    "type": period_type2}]
                                        })
                    sensor_col_data.append(pollen_data[0])

                # len: 2, values: Today, Tomorrow, final len: 2
                elif (len(current_values.get('Location').get('periods')) == 2 and 
                    current_values.get('Location').get('periods')[0].get('Type') == 'Today' and
                    current_values.get('Location').get('periods')[1].get('Type') == 'Tomorrow'):

                        # city info
                        forecast_date1 = current_values.get('ForecastDate')
                        date_obj = iso8601.parse_date(forecast_date1)
                        date_utc = date_obj.astimezone(pytz.utc)

                        sensor_id = current_values.get('Location').get('DisplayLocation')
                        city = current_values.get('Location').get('City')
                        state = current_values.get('Location').get('State')
                        city_zip_code = current_values.get('Location').get('ZIP')

                        # TODAY VALUES
                        period_type1 = current_values.get('Location').get('periods')[1].get('Type')
                        pollen_index_today = current_values.get('Location').get('periods')[1].get('Index')
                        triggers_today = current_values.get('Location').get('periods')[1].get('Triggers')

                        # TOMORROW VALUES
                        period_type2 = current_values.get('Location').get('periods')[2].get('Type')
                        pollen_index_tomorrow = current_values.get('Location').get('periods')[2].get('Index')
                        triggers_tomorrow = current_values.get('Location').get('periods')[2].get('Triggers')

                        """ Store above info to mongodb. """
                        pollen_data.append({"basic info": {"sensor_id": sensor_id.upper(),
                                                        "city": city,
                                                        "state": state,
                                                        "zip code": city_zip_code
                                                        },
                                            "periods": [{"pollen_index": pollen_index_today,
                                                        "triggers": triggers_today,
                                                        "type": period_type1},
                                                        {"pollen_index": pollen_index_tomorrow,
                                                        "triggers": triggers_tomorrow,
                                                        "type": period_type2}]
                                            })
                        sensor_col_data.append(pollen_data[0])

                # len: 2, values: Yesterday, Today, final len: 1
                elif (len(current_values.get('Location').get('periods')) == 2 and 
                    current_values.get('Location').get('periods')[0].get('Type') == 'Yesterday' and
                    current_values.get('Location').get('periods')[1].get('Type') == 'Today'):   

                    # city info
                    forecast_date1 = current_values.get('ForecastDate')
                    date_obj = iso8601.parse_date(forecast_date1)
                    date_utc = date_obj.astimezone(pytz.utc)

                    sensor_id = current_values.get('Location').get('DisplayLocation')
                    city = current_values.get('Location').get('City')
                    state = current_values.get('Location').get('State')
                    city_zip_code = current_values.get('Location').get('ZIP')

                    # TODAY VALUES
                    period_type1 = current_values.get('Location').get('periods')[1].get('Type')
                    pollen_index_today = current_values.get('Location').get('periods')[1].get('Index')
                    triggers_today = current_values.get('Location').get('periods')[1].get('Triggers')

                    """ Store above info to mongodb. """
                    pollen_data.append({"basic info": {"sensor_id": sensor_id.upper(),
                                                    "city": city,
                                                    "state": state,
                                                    "zip code": city_zip_code
                                                    },
                                        "periods": [{"pollen_index": pollen_index_today,
                                                    "triggers": triggers_today,
                                                    "type": period_type1},
                                                    {"pollen_index": None,
                                                    "triggers": [],
                                                    "type": 'Tomorrow'}]
                                        })
                    sensor_col_data.append(pollen_data[0])

                # len: 1, values: Today, final len: 1
                elif (len(current_values.get('Location').get('periods')) == 1 and 
                    current_values.get('Location').get('periods')[0].get('Type') == 'Today'):
                    
                    # city info
                    forecast_date1 = current_values.get('ForecastDate')
                    date_obj = iso8601.parse_date(forecast_date1)
                    date_utc = date_obj.astimezone(pytz.utc)

                    sensor_id = current_values.get('Location').get('DisplayLocation')
                    city = current_values.get('Location').get('City')
                    state = current_values.get('Location').get('State')
                    city_zip_code = current_values.get('Location').get('ZIP')

                    # TODAY VALUES
                    period_type1 = current_values.get('Location').get('periods')[1].get('Type')
                    pollen_index_today = current_values.get('Location').get('periods')[1].get('Index')
                    triggers_today = current_values.get('Location').get('periods')[1].get('Triggers')

                    """ Store above info to mongodb. """
                    pollen_data.append({"basic info": {"sensor_id": sensor_id.upper(),
                                                    "city": city,
                                                    "state": state,
                                                    "zip code": city_zip_code
                                                    },
                                        "periods": [{"pollen_index": pollen_index_today,
                                                    "triggers": triggers_today,
                                                    "type": period_type1},
                                                    {"pollen_index": None,
                                                    "triggers": [],
                                                    "type": 'Tomorrow'}]
                                        })
                    sensor_col_data.append(pollen_data[0])

                # all other cases
                else:
                    empty_document_counter += 1


                # Markets process: Create list which contains dicts of form {market, zip_code_data}
                if current_values.get('Location').get('DisplayLocation'):
                    for market in MARKETS_WITH_SENSORS:
                        if current_values.get('Location').get('DisplayLocation').upper() in market.get('sensors'):
                            init_list.append({
                                "market": market.get('market'),
                                "zip_code_data": pollen_data 
                            })
                pollen_data = []


                # In case of more than 50 empty documents, insert error document to the db. 
                if empty_document_counter >= 50:
                     # [CASE]: First execution
                    if forecast_date == 0:
                        query_date = datetime(datetime.utcnow().year,
                                              datetime.utcnow().month,
                                              datetime.utcnow().day)
                        document = {
                            "Forecast date": query_date + timedelta(hours=4),
                            "error": 'Null current-periods data'
                        }
                        SENSORS_COLLECTION.insert_one(document)
                        MARKETS_COLLECTION.insert_one(document)
                        break
                    if query_date > forecast_date:
                        document = {
                            "Forecast date": forecast_date + timedelta(days=1),
                            "error": 'Null current-periods data'
                        }
                        SENSORS_COLLECTION.insert_one(document)
                        MARKETS_COLLECTION.insert_one(document)
                        break
                    else:
                        document = {
                            "Forecast date": forecast_date,
                            "error": 'Null current-periods data'
                        }
                        SENSORS_COLLECTION.insert_one(document)
                        MARKETS_COLLECTION.insert_one(document)
                        break

            """ --------------------------- END FOR LOOP --------------------------- """


            if empty_document_counter < 50:
                """ 1. MARKET DATA INSERTION """

                # Insert data to pollen_markets_value collection
                document = {
                    "Forecast date": date_utc,
                    "Sensor data": markets_processing(MARKETS, init_list)
                }
                MARKETS_COLLECTION.insert_one(document)

                """ 2. SENSOR DATA INSERTION """
                
                # check for NOT valid pollen index values
                for sensor in sensor_col_data:

                    today_pollen_index = sensor.get('periods')[0].get('pollen_index')
                    tomorrow_pollen_index = sensor.get('periods')[1].get('pollen_index')
                    
                    if not ((today_pollen_index >= 0) and (today_pollen_index <= 12)):
                        sensor.get('periods')[0].update(pollen_index = None)
                        sensor.get('periods')[0].update(triggers = [])

                    if tomorrow_pollen_index != None:
                        if not ((tomorrow_pollen_index >= 0) and (tomorrow_pollen_index <= 12)):
                            sensor.get('periods')[1].update(pollen_index = None)
                            sensor.get('periods')[1].update(triggers = [])
                            
                # Insert data to pollen_sensors_value collection
                document = {
                    "Forecast date": date_utc,
                    "Sensor data": sensor_col_data
                }
                SENSORS_COLLECTION.insert_one(document)

            # time calc
            end = time.time()
            print(end - start)

        except IQVIAError as err:
             # [CASE]: First execution
            if forecast_date == 0:
                query_date = datetime(datetime.utcnow().year,
                                        datetime.utcnow().month,
                                        datetime.utcnow().day)
                document = {
                    "Forecast date": query_date + timedelta(hours=4),
                    "error": err
                }
                SENSORS_COLLECTION.insert_one(document)
                MARKETS_COLLECTION.insert_one(document)
            if query_date > forecast_date:
                document = {
                    "Forecast date": forecast_date + timedelta(days=1),
                    "error": err
                }
                SENSORS_COLLECTION.insert_one(document)
                MARKETS_COLLECTION.insert_one(document)
            else:
                document = {
                    "Forecast date": forecast_date,
                    "error": err
                }
                SENSORS_COLLECTION.insert_one(document)
                MARKETS_COLLECTION.insert_one(document)
            


    asyncio.get_event_loop().run_until_complete(main())