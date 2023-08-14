""" Module which implements app's need including mongodb. """
import dateutil.parser, pprint, json
from flask import session
from datetime import datetime, timedelta

from backend import lg
from backend.helpers.lib import file_path
from backend.helpers.db_config import DB_CONSTANTS
from backend.helpers.constans import VALIDATION_NAMESPACE


LOGGER = lg.get_logger(__name__)

USER = DB_CONSTANTS.user_collection
VAS = DB_CONSTANTS.vas_collection
MARKETS_COLLECTION = DB_CONSTANTS.pollen_markets_collection
SENSORS_COLLECTION = DB_CONSTANTS.pollen_sensors_collection
HUMIDITY_API = DB_CONSTANTS.humidity_api_collection
TODAY_HUMIDITY_API = DB_CONSTANTS.today_humidity_api_collection
HUMIDITY_GMAP = DB_CONSTANTS.humidity_gmap_collection
TWITTER_USA = DB_CONSTANTS.twitter_usa_colletion


class UserInsertManager:
    """ Class with functions related with user's insertions processes. """

    def insert_user(username_value, email_value, password_value, birthday_value, first_name_value, last_name_value):
        """ Implements the insertion of user with her basic info to mongodb, after the registry. """
        return USER.insert({'username': username_value,
                            'email': email_value,
                            'password': password_value,
                            'birthday': datetime.strptime(f'{birthday_value}', "%Y-%m-%d"),
                            'first name': first_name_value,
                            'last name': last_name_value,
                            'registry date': datetime.utcnow()})

    def insert_allergy_data(email_value, gender_value, family_history_value, allergic_rhinitis_value, allergic_asthma_value,
                            allergic_conjunctivitis_value, allergy_frequency_value, allergy_affection_value, immunotherapy_value,
                            immunotherapy_start_date_value, medicine_days_value, medicine_weeks_value):
        """ Implements the insertion of user's allergy data to mongodb. Called while user is logging for the first time and has to complete
            the necessary forms. """
        document_for_update = {'email': email_value}
        return USER.update_one(document_for_update,
                               {'$set': {'Allergy Data': {'gender': gender_value,
                                                          'family history': family_history_value,
                                                          'allergic rhinitis': allergic_rhinitis_value,
                                                          'allergic asthma': allergic_asthma_value,
                                                          'allergic conjunctivitis': allergic_conjunctivitis_value,
                                                          'allergy frequency': allergy_frequency_value,
                                                          'allergy affection': allergy_affection_value,
                                                          'immunotherapy': immunotherapy_value,
                                                          'immunotherapy start date': datetime.strptime(f'{immunotherapy_start_date_value}', "%Y-%m-%d"),
                                                          'medicine days': medicine_days_value,
                                                          'medicine weeks': medicine_weeks_value}}})

    def insert_allergy_data_without_immunotherapy_date(email_value, gender_value, family_history_value, allergic_rhinitis_value, allergic_asthma_value,
                                                       allergic_conjunctivitis_value, allergy_frequency_value, allergy_affection_value, immunotherapy_value,
                                                       immunotherapy_message_value, medicine_days_value, medicine_weeks_value):
        """ Implements the insertion of user's allergy data to mongodb, while user doesnt recieves or didnt filled immunotherapy start date.
            Called while user is logging for the first time and has to complete the necessary forms. """
        document_for_update = {'email': email_value}
        return USER.update_one(document_for_update,
                               {'$set': {'Allergy Data': {'gender': gender_value,
                                                          'family history': family_history_value,
                                                          'allergic rhinitis': allergic_rhinitis_value,
                                                          'allergic asthma': allergic_asthma_value,
                                                          'allergic conjunctivitis': allergic_conjunctivitis_value,
                                                          'allergy frequency': allergy_frequency_value,
                                                          'allergy affection': allergy_affection_value,
                                                          'immunotherapy': immunotherapy_value,
                                                          'immunotherapy start date': immunotherapy_message_value,
                                                          'medicine days': medicine_days_value,
                                                          'medicine weeks': medicine_weeks_value}}})

    def insert_allergy_symptoms(email_value, symptoms_value):
        """ Implements the insertion of user's allergy symptoms to mongodb. Called while user is logging for the first time and has to complete
            the necessary forms. """
        document_for_update = {'email': email_value}
        return USER.update_one(document_for_update,
                               {'$set': {'Allergy Symptoms': {'symptoms': symptoms_value}}})

    def insert_allergens(email_value, allergens):
        """ Implements the insertion of user's allergens to mongodb. Called while user is logging for the first time and has to complete
            the necessary forms. """
        document_for_update = {'email': email_value}
        return USER.update_one(document_for_update,
                               {'$set': {'Allergens': {'allergens': allergens}}})

    def insert_medicines(email_value, allergic_rhinitis_nose_value, allergic_rhinitis_mouth_value, allergic_rhinitis_injection_value,
                         allergic_asthma_mouth_value, allergic_conjunctivitis_drops_value):
        """ Implements the insertion of user's allergy medicines to mongodb. Called while user is logging for the first time and has to complete
        the necessary forms. """
        document_for_update = {'email': email_value}
        return USER.update_one(document_for_update,
                               {'$set': {'Medicines': {'allergic rhinitis - nose': allergic_rhinitis_nose_value,
                                                       'allergic rhinitis - mouth': allergic_rhinitis_mouth_value,
                                                       'allergic rhinitis - injection': allergic_rhinitis_injection_value,
                                                       'allergic asthma - mouth': allergic_asthma_mouth_value,
                                                       'allergic conjunctivitis - drops': allergic_conjunctivitis_drops_value}}})

    def insert_vas(email_value, today_symptoms_value, rhinitis_symptoms_today_value, asthma_symptoms_today_value,
                   conjunctivitis_symptoms_today_value, work_school_today_value, work_affection_value, lat_value, lng_value, timestamp_value):
        """ Implements the insertion of user's vas, geolocation and timestamp to mongodb. """
        return VAS.insert_one({'email': email_value,
                               'VAS Inputs': [{'today symptoms': today_symptoms_value,
                                               'today rhinitis symptoms': rhinitis_symptoms_today_value,
                                               'today asthma symptoms': asthma_symptoms_today_value,
                                               'today conjunctivitis symptoms': conjunctivitis_symptoms_today_value,
                                               'today_work_School': work_school_today_value,
                                               'work_school_affection': work_affection_value}],
                               'location': [{'type': 'Point',
                                             'coordinates': [float(lat_value), float(lng_value)]}],
                               'timestamp': timestamp_value})

    def insert_vas_without_geolocation(email_value, today_symptoms_value, rhinitis_symptoms_today_value, asthma_symptoms_today_value,
                                       conjunctivitis_symptoms_today_value, work_school_today_value, work_affection_value, location_value, timestamp_value):
        """ Implements the insertion of user's vas and timestamp to mongodb. """
        return VAS.insert_one({'email': email_value,
                               'VAS Inputs': [{'today symptoms': today_symptoms_value,
                                               'today rhinitis symptoms': rhinitis_symptoms_today_value,
                                               'today asthma symptoms': asthma_symptoms_today_value,
                                               'today conjunctivitis symptoms': conjunctivitis_symptoms_today_value,
                                               'today_work_School': work_school_today_value,
                                               'work_school_affection': work_affection_value}],
                               'location': location_value,
                               'timestamp': timestamp_value})


class UserUpdateManager:
    """ Class with functions related with user's updates processes. """

    def update_authentication_info(email_value, key, update_value):
        """ Implements the update of user's authentication informations. """
        document_for_update = {'email': email_value}
        new_value = {'$set': {key: update_value}}
        return USER.update_one(document_for_update, new_value)

    def update_allergy_info(email_value, setting_category, update_key, update_value):
        """ Implements the update of user's allergy informations. """
        document_for_update = {'email': email_value}
        updated_value = {
            '$set': {f'{setting_category}.{update_key}': update_value}}

        if update_key == 'immunotherapy start date' and (not isinstance(update_value, str)):
            return USER.update_one(document_for_update, {'$set': {f'{setting_category}.{update_key}': datetime.strptime(f'{update_value}', "%Y-%m-%d")}})

        return USER.update_one(document_for_update, updated_value)

    def delete_medicine_info(email_value, setting_category, update_key):
        """ Implements the deletion of user's medicine(s) information(s). """
        document_for_update = {'email': email_value}
        updated_value = {
            '$set': {f'{setting_category}.{update_key}': 'No medicine'}}

        return USER.update_one(document_for_update, updated_value)


class UserFindManager:
    """ Class with functions related with user's finds and checks processes. """

    def find_user(key, value):
        """ Checks for the existence of a user in mongodb. """
        return USER.find_one({key: value})

    def find_basic_account_info(email_value, key):
        """ Finds and returns basic account info, like username, email, etc. """
        cursor = UserFindManager.find_user('email', email_value)

        if key == 'registry date':
            return cursor.get(key).date()

        return cursor.get(key)

    def find_allergy_info(email_value, allergy_category, allergy_category_subfield):
        """ Finds and returns allergy info (data, allergens, symptoms, medicines). """
        cursor = UserFindManager.find_user('email', email_value)
        search_category = cursor.get(allergy_category)

        if allergy_category_subfield == 'immunotherapy start date':
            if isinstance(search_category.get(allergy_category_subfield), str):
                return search_category.get(allergy_category_subfield)
            else:
                return search_category.get(allergy_category_subfield).date()

        return search_category.get(allergy_category_subfield)

    def check_for_existing_allergy_info(email_value, key):
        """ Checks for the existence of allergy informations. Used for log-in authentication. """
        cursor = UserFindManager.find_user('email', email_value)
        for field in cursor:
            if field == key:
                return True

    def check_for_existing_vas_info(email_value):
        """ Checks for the existence of vas document for specific user. Used for log-in authentication. """
        return VAS.find_one({'email': email_value})


class UserDeleteManager:
    """ Class with functions related with user's account deletion. """

    def delete_user(email_value):
        """ Deletes all user's informations. """

        USER.delete_one({'email': email_value})
        VAS.delete_many({'email': email_value})

    def delete_user_settings(email_value):
        """ Deletes all user's settings (no registration info). Used for 1st login auth. """

        USER.update_one({'email': email_value}, {'$unset': {'Allergy Data': '',
                                                            'Allergy Symptoms': '',
                                                            'Allergens': '',
                                                            'Medicines': ''}})
        VAS.delete_many({'email': email_value})


class MyhealthManager:
    """ Class with functions related with myhealth api implementation. """

    def get_last_year_dates_from_vas(email_value):
        """ Returns dates from last year to today from vas collection """

        query_date = datetime.utcnow() - timedelta(days=365)
        start = datetime(query_date.year, query_date.month, query_date.day)

        return VAS.find({
            'email': email_value,
            'timestamp': {'$gte': start}
        })


    def get_documents_with_existing_coordinates(email_value, user_selected_minutes):
        """ Returns documents with existing coordinates for the requested time interval. """

        query_date = datetime.utcnow() - timedelta(minutes=user_selected_minutes)
        start = datetime(query_date.year, query_date.month, query_date.day, query_date.hour, query_date.minute, query_date.second)

        return VAS.find({
            'email': email_value,
            "location.type": "Point",
            'timestamp': {'$gte': start}
        })


class SensorMapsFindManager:
    """ Class including functions related with pollen api processes. """

    def __init__(self, request_args):
        """ Class constructor. """

        self.request_args = request_args
        self.datetime_query = datetime.utcnow() - timedelta(minutes=self.request_args.get('time_interval'))
        self.date = datetime(self.datetime_query.year, self.datetime_query.month, self.datetime_query.day)

    def find_pollen_data(self):
        """ Retrieves data from "pollen_markets" & "pollen_sensors" collections according to utc time. """

        # Calculate query date
        if self.datetime_query.hour >= 4:
            date_query = self.date + timedelta(hours=4) # TODO add 4 hours bacause i get data from iqvia api at 04:00 utc
        elif self.datetime_query.hour >= 0 and self.datetime_query.hour < 4:
            date_query = self.date - timedelta(days=1) + timedelta(hours=4)

        LOGGER.debug(f"Date query for pollen: {date_query}")

        # Query to suitable collection according the map request
        if self.request_args.get('map_type') == 'leaflet':
            return list(MARKETS_COLLECTION.find({"Forecast date": {"$gte": date_query}}))
        elif self.request_args.get('map_type') == 'google':
            return list(SENSORS_COLLECTION.find({"Forecast date": {"$gte": date_query}}))


class VASMapsFindManager:
    """ Class which implements functions for retrieving data from mongodb about vas maps. """

    def __init__(self, request_args):
        """ Class constructor. """

        self.request_args = request_args
        self.datetime_query = datetime.utcnow() - timedelta(minutes=self.request_args.get('time_interval'))


    def find_vas_data(self):
        """ Retrieves data from 'vas_tool' collection according to the utc time. """

        # Default request
        if self.request_args.get('time_interval') == 0:
            utc = datetime.utcnow()
            date_query = datetime(utc.year, utc.month, utc.day)
            LOGGER.debug(f"Date query for VAS: {date_query}")
            
            return list(VAS.find({"location.type": "Point", "timestamp": {"$gte": date_query}}))

        # Time interval
        else:
            LOGGER.debug(f"Date query for VAS: {self.datetime_query}")
            return list(VAS.find({"location.type": "Point", "timestamp": {"$gte": self.datetime_query}}))


class TwitterFindManager:
    """ Class including functions related with twitter data. """

    def find_twitter_data(time_interval):
        """ Retrieves today twitter data from "twitter_usa" collection. """

        # Default case (today)
        if time_interval == 0:
            utc = datetime.utcnow()
            date_query = datetime(utc.year, utc.month, utc.day)
            LOGGER.debug(f"Date query for Twitter: {date_query}")

            return list(TWITTER_USA.find({"Date": {"$gte": date_query}}))

        # Time interval
        else:
            dt_query = datetime.utcnow() - timedelta(minutes=time_interval)
            LOGGER.debug(f"Date query for Twitter: {dt_query}")

            return list(TWITTER_USA.find({"Date": {"$gte": dt_query}}))


class HumidityFindManager:
    """ Class including functions related with humidity api processes. """


    def find_humidity_data(time_interval):
        """
        Returns from humidity_api collection the necessary documents,
        according to user's requests.
        """

        USER_DATA = {
            "time_interval": time_interval,
            "current_utc": datetime.utcnow(),
            "humidity_date_search": datetime.utcnow() - timedelta(minutes=time_interval)
        }
        LOGGER.debug(f"Date query for humidity: {USER_DATA.get('humidity_date_search')}")
        # TODAY: Take values from last element inserted doc. in 'today_humidity_api' col.
        # TOMORROW: Same
        if USER_DATA.get('time_interval') == 0 or USER_DATA.get('time_interval') == 1:
            most_cur_document = list(TODAY_HUMIDITY_API.find().sort("Forecast date", -1).limit(1))

            # If no existing documents
            if len(most_cur_document) == 0:
                LOGGER.error('No data for today/tomorrow humidity.')
                response = VALIDATION_NAMESPACE.DB_ERROR
                return response

            else:

                # Document with error
                if most_cur_document[0].get('error'):
                    LOGGER.error('Error for today/tomorrow humidity.')
                    response = VALIDATION_NAMESPACE.DB_ERROR
                    return response

                else:

                    # Check if exists document in collection with the same date with today's date.
                    if USER_DATA.get('current_utc').date() == most_cur_document[0].get('Forecast date').date():
                        return most_cur_document
                    else:
                        LOGGER.error('No data for today/tomorrow humidity.')
                        response = VALIDATION_NAMESPACE.DB_ERROR
                        return response

        # TIME INTERVAL
        else:

            # Define start and end date for the time interval which user selected.
            start_date_interval = datetime(USER_DATA.get('current_utc').year,
                                           USER_DATA.get('current_utc').month,
                                           USER_DATA.get('current_utc').day)
            end_date_interval = datetime(USER_DATA.get('humidity_date_search').year,
                                         USER_DATA.get('humidity_date_search').month,
                                         USER_DATA.get('humidity_date_search').day)
            
            LOGGER.debug(f'[ START: {start_date_interval} | END: {end_date_interval} ]')
            """ --------------------------------------------------------------------- """

            # [1ST CASE]: If request considers to the same date, data are retrieved from
            #             'today_humidity_api' collection.
            if start_date_interval == end_date_interval:

                documents = list(TODAY_HUMIDITY_API.find({
                    "Forecast date": {'$gte': USER_DATA.get('humidity_date_search')}
                }))

                # If for the time interval that user requested, there are no data in collection,
                # return most current document or error in case of older date data.
                if len(documents) == 0:
                    LOGGER.info(f'NO DATA FOR TIME INT -> {time_interval}. Return most current.')

                    most_cur_document = list(TODAY_HUMIDITY_API.find().sort("Forecast date", -1).limit(1))

                    # If no existing documents
                    if len(most_cur_document) == 0:
                        LOGGER.error(f'NO DATA FOR TIME INT -> {time_interval}.')
                        response = VALIDATION_NAMESPACE.DB_ERROR
                        return response

                    else:

                        # Document with error
                        if most_cur_document[0].get('error'):
                            LOGGER.error(f'Error for TIME INT -> {time_interval}.')
                            response = VALIDATION_NAMESPACE.DB_ERROR
                            return response

                        else:

                            # Check if exists document in collection with the same date with today's date.
                            if USER_DATA.get('current_utc').date() == most_cur_document[0].get('Forecast date').date():
                                return most_cur_document
                            else:
                                LOGGER.error(f'No data for TIME INT -> {time_interval}.')
                                response = VALIDATION_NAMESPACE.DB_ERROR
                                return response

                # Found the avrg. values of queried documents and return list with
                # dicts of form {market, avr_humidity}.
                else:
                    LOGGER.info(F'DATA FOUND FOR TIME INTERVAL {time_interval} -> {len(documents)}')
                    all_data, temp_document, response = [], [], []
                    humidity, counter_hum, counter_no_error = 0, 0, 0

                    markets_path = file_path('web/humidity_api/files', 'markets_names.json')
                    with open(markets_path, encoding="utf-8") as json_file:
                        MARKETS = json.load(json_file)

                    for obs in documents:
                        if not obs.get('error'):
                            counter_no_error += 1
                            for market in obs.get('Markets data'):
                                if market.get('cur_humidity') != 120:
                                    all_data.append({"market": market.get('market'),
                                                     "humidity": market.get('cur_humidity')})

                    # If all the documents during the requested time interval had errors
                    if counter_no_error == 0:
                        LOGGER.error('Error for today humidity.')
                        response = VALIDATION_NAMESPACE.DB_ERROR
                        return response

                    else:

                        for name in MARKETS:

                            for market in all_data:
                                if name == market.get('market'):
                                    humidity += market.get('humidity')
                                    counter_hum += 1
                                
                            if counter_hum != 0:
                                temp_document.append({"market": name,
                                                      "cur_humidity": round((humidity/counter_hum),0)})
                                humidity, counter_hum = 0, 0
                            else:
                                temp_document.append({"market": name,
                                                      "cur_humidity": 120})
                                humidity, counter_hum = 0, 0

                        response.append({
                            "Markets data": temp_document
                        })
                        return response
                    """ -------------------------------------------------------- """

            # [2ND CASE]: If request considers to more than one date:
            #             1. Create a list (like above) with all documents of current day
            #             2. Do the same for date queried documents from the main collection
            #             3. Find avrg of 1,2 and create list with dicts of form {market, avr_humidity}
            else:
                # 1.
                # Exec query with 'start_date_interval' in order to prevent return past date data
                # in case of not updated values in collection.
                documents1 = list(TODAY_HUMIDITY_API.find({
                    "Forecast date": {"$gte": USER_DATA.get('humidity_date_search')}
                }))

                # For documents about today data, if exist erros, then a counter is increased in order
                # not to be calculated at step 3.
                counter_err_today = 0

                markets_path = file_path('web/humidity_api/files', 'markets_names.json')
                with open(markets_path, encoding="utf-8") as json_file:
                    MARKETS = json.load(json_file)

                if len(documents1) == 0:
                    counter_err_today += 1
                else:
                    all_data1, temp_document1, final_document1 = [], [], []
                    humidity1, counter_hum1, counter_no_error1 = 0, 0, 0

                    for obs in documents1:
                        if not obs.get('error'):
                            counter_no_error1 += 1
                            for market in obs.get('Markets data'):
                                if market.get('cur_humidity') != 120:
                                    all_data1.append({"market": market.get('market'),
                                                     "humidity": market.get('cur_humidity')})

                    # If all the documents during the day had errors
                    if counter_no_error1 == 0:
                        
                        counter_err_today += 1

                    else:

                        for name in MARKETS:

                            for market in all_data1:
                                if name == market.get('market'):
                                    humidity1 += market.get('humidity')
                                    counter_hum1 += 1
                                
                            if counter_hum1 != 0:
                                temp_document1.append({"market": name,
                                                       "cur_humidity": round((humidity1/counter_hum1),0)})
                                humidity1, counter_hum1 = 0, 0
                            else:
                                temp_document1.append({"market": name,
                                                       "cur_humidity": 120})
                                humidity1, counter_hum1 = 0, 0

                        final_document1.append({
                            "Markets data": temp_document1
                        })
                """ -------------------------------------------------------- """

                # 2.
                documents2 = list(HUMIDITY_API.find({
                    "Forecast date": {"$gte": end_date_interval}
                }))
                
                # In case of no documents to 'humidity_api' collection, return today documents
                if len(documents2) == 0:
                    # if there are no errors at today documents
                    if counter_err_today == 0:
                        LOGGER.error('DATA ONLY FROM TODAY\'S VALUES')
                        return final_document1
                    else:
                        LOGGER.error(f'Error for time interval {time_interval}, humidity.')
                        response = VALIDATION_NAMESPACE.DB_ERROR
                        return response
                else:
                    all_data2, temp_document2, final_document2 = [], [], []
                    humidity2, counter_hum2, counter_no_error2 = 0, 0, 0

                    for obs in documents2:
                        if not obs.get('error'):
                            counter_no_error2 += 1
                            for market in obs.get('Markets data'):
                                if market.get('humidity') != 120:
                                    all_data2.append({"market": market.get('market'),
                                                      "humidity": market.get('humidity')})

                    # In case of errors at 'humidity_api' collection, return today documents
                    if counter_no_error2 == 0:
                        
                        # if there are no error at today documents
                        if counter_err_today == 0:
                            LOGGER.error('DATA ONLY FROM TODAY\'S VALUES')
                            return final_document1
                        else:
                            LOGGER.error(f'Error for time interval {time_interval}, humidity.')
                            response = VALIDATION_NAMESPACE.DB_ERROR
                            return response

                    else:

                        for name in MARKETS:

                            for market in all_data2:
                                if name == market.get('market'):
                                    humidity2 += market.get('humidity')
                                    counter_hum2 += 1
                                
                            if counter_hum2 != 0:
                                temp_document2.append({"market": name,
                                                       "cur_humidity": round((humidity2/counter_hum2),0)})
                                humidity2, counter_hum2 = 0, 0
                            else:
                                temp_document2.append({"market": name,
                                                       "cur_humidity": 120})
                                humidity2, counter_hum2 = 0, 0

                        final_document2.append({
                            "Markets data": temp_document2
                        })
                """ -------------------------------------------------------- """

                # 3.

                # 1st case: there are no processable data in 'today_humidity_api' col.,
                #           so return data from the rest days (main collection).
                if counter_err_today != 0:
                    LOGGER.info(f'DATA ONLY FROM MAIN COLLECTION. DAYS RETURNED -> {len(documents2)}')
                    return final_document2

                # 2nd case: i have data from both collections.
                else:
                    temp_document3, response = [], []
                    humidity3, counter_hum3 = 0, 0

                    # Concatenate two lists about today and past humidity values
                    conc_data = final_document1[0].get('Markets data') + final_document2[0].get('Markets data')

                    for name in MARKETS:

                        for market in conc_data:
                            if name == market.get('market') and market.get('cur_humidity') != 120:
                                humidity3 += market.get('cur_humidity')
                                counter_hum3 += 1
                            
                        if counter_hum3 != 0:
                            temp_document3.append({"market": name,
                                                   "cur_humidity": round((humidity3/counter_hum3),0)})
                            humidity3, counter_hum3 = 0, 0
                        else:
                            temp_document3.append({"market": name,
                                                   "cur_humidity": 120})
                            humidity3, counter_hum3 = 0, 0

                    response.append({
                        "Markets data": temp_document3
                    })
                    LOGGER.info(f'DATA ONLY FROM BOTH COLLECTIONS.\
                                  TODAY COL. RETURNED -> {len(documents1)}\
                                  MAIN COLLECTION. RETURNED -> {len(documents2)}')
                    return response


    def find_humidity_gmap_testing():
        """
        Retrieve from the collection this document with all sensor/points
        (19.908) from OpenWeatherMap for U.S. for a fixed past date.
        """
        return list(HUMIDITY_GMAP.find())
