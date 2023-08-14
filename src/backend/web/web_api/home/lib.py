from flask import session
from datetime import datetime, timedelta
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pprint, json

from backend import lg
from backend.helpers.main_config import CONFIGURATION
from backend.helpers.db_config import DB_CONSTANTS
from backend.helpers.constans import VALIDATION_NAMESPACE
from backend.helpers.lib import file_path
from backend.web.database_api import (UserInsertManager, SensorMapsFindManager, 
                                      HumidityFindManager, TwitterFindManager,
                                      VASMapsFindManager)


LOGGER = lg.get_logger(__name__)
MAP_DATA_FILE = "web/web_api/home/map_data"
FILES = {
    "markets with sensors": "markets_with_sensors.json",
    "markets names": "markets_names.json",
    "us markets": "us_markets.json",
    "states": "us_states.json",
    "sensor points": "sensors_info.json",
    "polygons": "polygons_markets.json",
    "multipolygons": "multipolygons_markets.json",
    "states codes": "states_codes.json",
    "states and markets": "states_and_markets.json"
}


class PollenSensorMaps:
    """
    Class which contains methods about the coloring of leaflet and
    google maps using sensor data.
    """

    def __init__(self, request_args):
        self.request_args = request_args


    @staticmethod
    def error_leaflet_response(geojson, allergens_state):
        """ Returns response when an error occurs. """

        if allergens_state == 0:
            message = None
        elif allergens_state == 1:
            message = 'No areas found for selected allergens.'

        for market in geojson.get('features'):
            market.get('properties').update(density = 100)

        return {
            "data": geojson,
            "message": message
        }


    def leaflet_map(self):
        """ Returns geojson with USA markets including pollen density. """

        with open(file_path(MAP_DATA_FILE, FILES.get('us markets'))) as file:
            MARKETS_GEOJSON = json.load(file)

        retrieved_document = SensorMapsFindManager(self.request_args).find_pollen_data()

        # [CASE]: Document not found from mongodb
        if len(retrieved_document) == 0:
            return PollenSensorMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

        # [CASE]: Today, Tomorrow & Time Tnterval which considers the same day
        elif len(retrieved_document) == 1:

            # [CASE]: Document with error
            if retrieved_document[0].get('error'):
                return PollenSensorMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

            # [CASE]: NO ALLERGENS -> Today || Tomorrow || Time Interval for same day
            if len(self.request_args.get('allergens')) == 0:

                valid_markets = []

                for market1 in MARKETS_GEOJSON.get('features'):
                    for market2 in retrieved_document[0].get('Sensor data'):

                        if market1.get('properties').get('market_to_') == market2.get('market'):

                            # [CASE]: Tomorrow
                            if self.request_args.get('time_interval') == 1:
                                if market2.get('tomorrow').get('pollen_index') != 100:
                                    market1.get('properties').update(density = market2.get('tomorrow').get('pollen_index'))
                                    valid_markets.append(market1.get('properties').get('market_to_'))
                            # [CASE]: Today || Time Interval
                            else:
                                if market2.get('today').get('pollen_index') != 100:
                                    market1.get('properties').update(density = market2.get('today').get('pollen_index'))
                                    valid_markets.append(market1.get('properties').get('market_to_'))

                # Give density = 100 for these markets with no data.
                for market in MARKETS_GEOJSON.get('features'):
                    if not market.get('properties').get('market_to_') in valid_markets:
                        market.get('properties').update(density = 100)

                return {
                    "data": MARKETS_GEOJSON,
                    "message": None
                }

            # [CASE]: WITH ALLERGENS -> TIME INTERVAL for same day
            else:

                user_selected_allergens = self.request_args.get('allergens')
                markets_with_allergens, valid_markets = [], []

                # Check which markets include allergens that users has selected
                for market in retrieved_document[0].get('Sensor data'):
                    for allergen in market.get('today').get('triggers'):
                        if allergen in user_selected_allergens:
                            markets_with_allergens.append({
                                "market": market.get('market'),
                                "pollen_index": market.get('today').get('pollen_index') 
                            })
                            break

                # [CASE]: No allergens match to the markets
                if len(markets_with_allergens) == 0:
                    return PollenSensorMaps.error_leaflet_response(MARKETS_GEOJSON, 1)

                # [CASE]: Allergens match to markets
                else:
                    # Create geojson for these markets
                    for market1 in MARKETS_GEOJSON.get('features'):
                        for market2 in markets_with_allergens:
                            if market1.get('properties').get('market_to_') == market2.get('market'):
                                if market2.get('pollen_index') != 100:
                                    market1.get('properties').update(density = market2.get('pollen_index'))
                                    valid_markets.append(market1.get('properties').get('market_to_'))

                    # Give density = 100 for these markets with no data.
                    for market in MARKETS_GEOJSON.get('features'):
                        if not market.get('properties').get('market_to_') in valid_markets:
                            market.get('properties').update(density = 100)

                    return {
                        "data": MARKETS_GEOJSON,
                        "message": None
                    }

        # [CASE]: Time Tnterval > 1 Day
        elif len(retrieved_document) > 1:

            docs_without_error = []

            # Create list with all markets of each retrieved document
            for document in retrieved_document:
                if not document.get('error'):
                    for market in document.get('Sensor data'):
                        docs_without_error.append(market)

            # [CASE]: All retrieved documents contain errors
            if len(docs_without_error) == 0:
                return PollenSensorMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

            # [CASE]: At least one document without error
            else:

                with open(file_path(MAP_DATA_FILE, FILES.get('markets names'))) as file:
                    MARKETS_NAMES = json.load(file)

                # [CASE]: NO ALLERGENS
                if len(self.request_args.get('allergens')) == 0:

                    pollen_index_sum, market_counter, final_list, valid_markets = 0, 0, [], []

                    # Find the average pollen_index for markets
                    for market1 in MARKETS_NAMES:
                        for market2 in docs_without_error:

                            if market1 == market2.get('market'):
                                if market2.get('today').get('pollen_index') != 100:
                                    pollen_index_sum += market2.get('today').get('pollen_index')
                                    market_counter += 1

                        if market_counter != 0:
                            final_list.append({
                                "market": market1,
                                "pollen_index": round((pollen_index_sum/market_counter),1)
                            })
                            pollen_index_sum, market_counter = 0, 0

                    # Create geojson for these markets
                    for market1 in MARKETS_GEOJSON.get('features'):
                        for market2 in final_list:
                            if market1.get('properties').get('market_to_') == market2.get('market'):
                                market1.get('properties').update(density = market2.get('pollen_index'))
                                valid_markets.append(market1.get('properties').get('market_to_'))

                    # Give density = 100 for these markets with no data.
                    for market in MARKETS_GEOJSON.get('features'):
                        if not market.get('properties').get('market_to_') in valid_markets:
                            market.get('properties').update(density = 100)

                    return {
                        "data": MARKETS_GEOJSON,
                        "message": None
                    }

                # [CASE]: ALLERGENS
                else:

                    user_selected_allergens = self.request_args.get('allergens')
                    markets_with_allergens = []

                    # Check which markets contain user's allergens
                    for market in docs_without_error:
                        for allergen in market.get('today').get('triggers'):
                            if allergen in user_selected_allergens:
                                markets_with_allergens.append({
                                    "market": market.get('market'),
                                    "pollen_index": market.get('today').get('pollen_index') 
                                })
                                break

                    # [CASE]: No allergens matches to markets
                    if len(markets_with_allergens) == 0:
                        return PollenSensorMaps.error_leaflet_response(MARKETS_GEOJSON, 1)

                    # [CASE]: Matches with markets and allergens found
                    else:
                        pollen_index_sum, market_counter, final_list, valid_markets = 0, 0, [], []

                        # Find the average pollen_index for markets
                        for market1 in MARKETS_NAMES:
                            for market2 in markets_with_allergens:

                                if market1 == market2.get('market'):
                                    if market2.get('pollen_index') != 100:
                                        pollen_index_sum += market2.get('pollen_index')
                                        market_counter += 1

                            if market_counter != 0:
                                final_list.append({
                                    "market": market1,
                                    "pollen_index": round((pollen_index_sum/market_counter),1)
                                })
                                pollen_index_sum, market_counter = 0, 0

                        # Create geojson for these markets
                        for market1 in MARKETS_GEOJSON.get('features'):
                            for market2 in final_list:
                                if market1.get('properties').get('market_to_') == market2.get('market'):
                                    market1.get('properties').update(density = market2.get('pollen_index'))
                                    valid_markets.append(market1.get('properties').get('market_to_'))

                        # Give density = 100 for these markets with no data.
                        for market in MARKETS_GEOJSON.get('features'):
                            if not market.get('properties').get('market_to_') in valid_markets:
                                market.get('properties').update(density = 100)

                        return {
                            "data": MARKETS_GEOJSON,
                            "message": None
                        }


    def google_map(self):
        """ Returns geojson with pollen sensors. """

        with open(file_path(MAP_DATA_FILE, FILES.get('sensor points'))) as file:
            SENSORS_GEOJSON = json.load(file)
        
        retrieved_document = SensorMapsFindManager(self.request_args).find_pollen_data()

        # [CASE]: Document not found from mongodb
        if len(retrieved_document) == 0:
            return False

        # [CASE]: Today, Tomorrow & Time Tnterval which considers the same day
        elif len(retrieved_document) == 1:

            # [CASE]: Document with error
            if retrieved_document[0].get('error'):
                return False

            # [CASE]: NO ALLERGENS -> Today || Tomorrow || Time Interval for same day
            if len(self.request_args.get('allergens')) == 0:

                for sensor1 in SENSORS_GEOJSON.get('features'):
                    sensor_point_city = sensor1.get('properties').get('city_name')
                    sensor_point_state = sensor1.get('properties').get('state_code')
                    sensor_point_id = f'{sensor_point_city}, {sensor_point_state}'

                    for sensor2 in retrieved_document[0].get('Sensor data'):
                        if sensor_point_id == sensor2.get('basic info').get('sensor_id'):

                            # [CASE]: Tomorrow
                            if self.request_args.get('time_interval') == 1:
                                if sensor2.get('periods')[1].get('pollen_index') != None:
                                    sensor1.get('properties').update(weight = sensor2.get('periods')[1].get('pollen_index'))
                            # [CASE]: Today || Time Interval
                            else:
                                if sensor2.get('periods')[0].get('pollen_index') != None:
                                    sensor1.get('properties').update(weight = sensor2.get('periods')[0].get('pollen_index'))

                return SENSORS_GEOJSON

            # [CASE]: Allergens match to sensors
            else:

                user_selected_allergens = self.request_args.get('allergens')
                sensors_with_allergens = []

                # Check which sensors include allergens that users has selected
                for sensor in retrieved_document[0].get('Sensor data'):
                    for allergen in sensor.get('periods')[0].get('triggers'):
                        if allergen.get('Name') in user_selected_allergens:
                            sensors_with_allergens.append({
                                "sensor_id": sensor.get('basic info').get('sensor_id'),
                                "pollen_index": sensor.get('periods')[0].get('pollen_index')
                            })
                            break

                # [CASE]: No allergens match to sensors
                if len(sensors_with_allergens) == 0:
                    return False

                # [CASE]: Allergens match to sensors
                else:

                    # Create geojson for these sensors
                    for sensor1 in SENSORS_GEOJSON.get('features'):
                        sensor_point_city = sensor1.get('properties').get('city_name')
                        sensor_point_state = sensor1.get('properties').get('state_code')
                        sensor_point_id = f'{sensor_point_city}, {sensor_point_state}'

                        for sensor2 in sensors_with_allergens:
                            if sensor_point_id == sensor2.get('sensor_id'):
                                if sensor2.get('pollen_index') != None:
                                    sensor1.get('properties').update(weight = sensor2.get('pollen_index'))

                    return SENSORS_GEOJSON

        # [CASE]: Time Tnterval > 1 Day
        elif len(retrieved_document) > 1:

            docs_without_error = []

            # Create list with all sensors of each retrieved document
            for document in retrieved_document:
                if not document.get('error'):
                    for sensor in document.get('Sensor data'):
                        docs_without_error.append(sensor)

            # [CASE]: All retrieved documents contain errors
            if len(docs_without_error) == 0:
                return False

            # [CASE]: At least one document without error
            else:

                # [CASE]: NO ALLERGENS
                if len(self.request_args.get('allergens')) == 0:

                    pollen_index_sum, sensor_counter, final_list = 0, 0, []

                    # Find the average pollen_index for sensors
                    for sensor1 in SENSORS_GEOJSON.get('features'):
                        sensor_point_city = sensor1.get('properties').get('city_name')
                        sensor_point_state = sensor1.get('properties').get('state_code')
                        sensor_point_id = f'{sensor_point_city}, {sensor_point_state}'

                        for sensor2 in docs_without_error:

                            if sensor_point_id == sensor2.get('basic info').get('sensor_id'):
                                if sensor2.get('periods')[0].get('pollen_index') != None:
                                    pollen_index_sum += sensor2.get('periods')[0].get('pollen_index')
                                    sensor_counter += 1

                        if sensor_counter != 0:
                            final_list.append({
                                "sensor_id": sensor_point_id,
                                "pollen_index": round((pollen_index_sum/sensor_counter),1)
                            })
                            pollen_index_sum, sensor_counter = 0, 0

                    # Create geojson for these sensors
                    for sensor1 in SENSORS_GEOJSON.get('features'):
                        sensor_point_city = sensor1.get('properties').get('city_name')
                        sensor_point_state = sensor1.get('properties').get('state_code')
                        sensor_point_id = f'{sensor_point_city}, {sensor_point_state}'

                        for sensor2 in final_list:
                            if sensor_point_id == sensor2.get('sensor_id'):
                                sensor1.get('properties').update(weight = sensor2.get('pollen_index'))

                    return SENSORS_GEOJSON

                # [CASE]: ALLERGENS
                else:
                    user_selected_allergens = self.request_args.get('allergens')
                    sensors_with_allergens = []

                    # Check which sensors contain selected allergens
                    for sensor in docs_without_error:
                        for allergen in sensor.get('periods')[0].get('triggers'):
                            if allergen.get('Name') in user_selected_allergens:
                                sensors_with_allergens.append({
                                    "sensor_id": sensor.get('basic info').get('sensor_id'),
                                    "pollen_index": sensor.get('periods')[0].get('pollen_index') 
                                })
                                break

                    # [CASE]: No allergens matches to sensors
                    if len(sensors_with_allergens) == 0:
                        return False

                    # [CASE]: Matches with sensors and allergens found
                    else:

                        pollen_index_sum, sensor_counter, final_list = 0, 0, []

                        # Find the average pollen_index for sensors
                        for sensor1 in SENSORS_GEOJSON.get('features'):
                            sensor_point_city = sensor1.get('properties').get('city_name')
                            sensor_point_state = sensor1.get('properties').get('state_code')
                            sensor_point_id = f'{sensor_point_city}, {sensor_point_state}'

                            for sensor2 in sensors_with_allergens:

                                if sensor_point_id == sensor2.get('sensor_id'):
                                    if sensor2.get('pollen_index') != None:
                                        pollen_index_sum += sensor2.get('pollen_index')
                                        sensor_counter += 1

                            if sensor_counter != 0:
                                final_list.append({
                                    "sensor_id": sensor_point_id,
                                    "pollen_index": round((pollen_index_sum/sensor_counter),1)
                                })
                                pollen_index_sum, sensor_counter = 0, 0

                        # Create geojson for these sensors
                        for sensor1 in SENSORS_GEOJSON.get('features'):
                            sensor_point_city = sensor1.get('properties').get('city_name')
                            sensor_point_state = sensor1.get('properties').get('state_code')
                            sensor_point_id = f'{sensor_point_city}, {sensor_point_state}'

                            for sensor2 in final_list:
                                if sensor_point_id == sensor2.get('sensor_id'):
                                    sensor1.get('properties').update(weight = sensor2.get('pollen_index'))

                        return SENSORS_GEOJSON


class VASMaps:
    """ 
    Class which contains methods about the coloring of leaflet and
    google maps using VAS data. 
    """

    def __init__(self, request_args):
        self.request_args = request_args


    @staticmethod
    def error_leaflet_response(geojson, allergens_state):
        """ Returns response when an error occurs. """

        if allergens_state == 0:
            message = None
        elif allergens_state == 1:
            message = 'No areas found for selected allergens.'

        for market in geojson.get('features'):
            market.get('properties').update(density = 100)

        return {
            "data": geojson,
            "message": message
        }


    @staticmethod
    def check_existence_of_usa_points(scale_and_point):
        """ 
        Check if users's points are inside USA's markets and then create
        list with dicts of form {date, market, scale}. 
        """

        market_and_scale = []

        with open(file_path(MAP_DATA_FILE, FILES.get('polygons'))) as json_file:
            POLYGONS = json.load(json_file)
        with open(file_path(MAP_DATA_FILE, FILES.get('multipolygons'))) as json_file:
            MULTIPOLYGONS = json.load(json_file)

        for pair in scale_and_point:
            point = Point(pair.get('point').get('lat'), pair.get('point').get('lng'))

            for data in POLYGONS:
                polygon = Polygon(data.get('coordinates'))
                if polygon.contains(point):
                    market_and_scale.append({
                        "date": pair.get('date'),
                        "coordinates": {
                            "lat": pair.get('point').get('lat'),
                            "lng": pair.get('point').get('lng')
                        },
                        "market": data.get('market_code'),
                        "symptom_scale": pair.get('scale')
                    })

            for multipolygon in MULTIPOLYGONS:
                for data in multipolygon.get('coordinates'):
                    polygon = Polygon(data)
                    if polygon.contains(point):
                        market_and_scale.append({
                            "date": pair.get('date'),
                            "coordinates": {
                                "lat": pair.get('point').get('lat'),
                                "lng": pair.get('point').get('lng')
                            },
                            "market": multipolygon.get('market_code'),
                            "symptom_scale": pair.get('scale')
                        })

        # Check if users's vas coords are not inside us markets
        if market_and_scale:
            return market_and_scale
        else:
            return False


    @staticmethod
    def markets_and_vas_scale(time_interval, day_dif, dt_query, MARKETS, usa_points):
        """ Returns the average (if needed) of user's symptoms scale for each usa market. """

        # [CASE]: Req. which depends data for the (max) range of 24 hours.
        if ((time_interval == 0) or (day_dif == 0) or 
            ((day_dif == 1) and (dt_query.hour - datetime.utcnow().hour >=0))):
            
            market_counter, scale_sum, market_and_scale = 0, 0, []
            for market_name in MARKETS:
                for pair in usa_points:
                    if market_name == pair.get('market'):
                        scale_sum += pair.get('symptom_scale')
                        market_counter += 1

                if market_counter != 0:
                    market_and_scale.append({"market": market_name,
                                            "scale": round((scale_sum/market_counter), 1)})
                    scale_sum, market_counter = 0, 0

            return market_and_scale

        # [CASE]: Req. which dependes data from more than one day
        elif day_dif > 1:
            
            # 1. Specify dates which must be queried throught "usa_points" list
            dates_queries = []
            for day in range(1, day_dif+1):
                dates_queries.append(datetime.utcnow() - timedelta(hours=24*day))

            # 2. Create dicts which contains user's points for each day of the time interval
            temp_list, market_day_data = [], []
            for date in dates_queries:
                for point in usa_points:
                    if (point.get('date') >= date) and (point.get('date') <= date + timedelta(days=1)):
                        temp_list.append(point)

                if temp_list:
                    market_day_data.append({"Date": date,
                                            "markets_info": temp_list})
                    temp_list = []                        

            # 3. For each dict. (each date) of the above list, find the market's values
            market_counter, scale_sum, temp_market_and_scale = 0, 0, []
            for data in market_day_data:

                for market_name in MARKETS:
                    for market_data in data.get('markets_info'):
                        if market_name == market_data.get('market'):
                            scale_sum += market_data.get('symptom_scale')
                            market_counter += 1

                    if market_counter != 0:
                        temp_market_and_scale.append({"market": market_name,
                                                    "symptom_scale": round((scale_sum/market_counter), 1)})
                        scale_sum, market_counter = 0, 0

            # 4. Find the average of the above list for all markets and divide by day_dif.
            scale_sum, market_counter, market_and_scale = 0, 0, []
            for market_name in MARKETS:
                for pair in temp_market_and_scale:
                    if market_name == pair.get('market'):
                        scale_sum += pair.get('symptom_scale')
                        market_counter += 1

                if market_counter != 0:
                    market_and_scale.append({"market": market_name,
                                             "scale": round(scale_sum/day_dif, 1)})
                    scale_sum, market_counter = 0, 0

            return market_and_scale
        

    def leaflet_map(self):
        """ Returns geojson with USA markets including vas data. """

        with open(file_path(MAP_DATA_FILE, FILES.get('us markets'))) as file:
            MARKETS_GEOJSON = json.load(file)

        vas_documents = VASMapsFindManager(self.request_args).find_vas_data()

        # [CASE]: Document not found from mongodb
        if len(vas_documents) == 0:
            return VASMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

        # [CASE]: Documents found for the request
        else:
            scale_and_point = []

            for document in vas_documents:
                scale_and_point.append({
                    "date": document.get('timestamp'),
                    "scale": document.get('VAS Inputs')[0].get('today symptoms'),
                    "point": {"lat": document.get('location')[0].get('coordinates')[0],
                              "lng": document.get('location')[0].get('coordinates')[1]}
                })

            # Check of the existence of the points at USA
            usa_points = VASMaps.check_existence_of_usa_points(scale_and_point)

            # [CASE]: NO user's points at USA
            if usa_points == False:
                return VASMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

            # [CASE]: User's points found at USA
            else:
                with open(file_path(MAP_DATA_FILE, FILES.get('markets names'))) as json_file:
                    MARKETS = json.load(json_file)

                dt_query = datetime.utcnow() - timedelta(minutes=self.request_args.get('time_interval'))
                start_date_interval = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
                end_date_interval = datetime(dt_query.year, dt_query.month, dt_query.day)
                day_dif = (start_date_interval.date() - end_date_interval.date()).days

                # [CASE]: NO ALLERGENS
                if len(self.request_args.get('allergens')) == 0:

                    market_and_scale = VASMaps.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    # Create geojson with markets data
                    valid_markets = []
                    for market1 in MARKETS_GEOJSON.get('features'):
                        for market2 in market_and_scale:
                            if market1.get('properties').get('market_to_') == market2.get('market'):
                                market1.get('properties').update(density = market2.get('scale'))
                                valid_markets.append(market1.get('properties').get('market_to_'))

                    for market in MARKETS_GEOJSON.get('features'):
                        if not market.get('properties').get('market_to_') in valid_markets:
                            market.get('properties').update(density = 100)

                    return {
                        "data": MARKETS_GEOJSON,
                        "message": None
                    }

                # [CASE]: ALLERGENS
                else:
                    # Retrieve pollen sensors markets data for requested time interval.
                    retrieved_document = SensorMapsFindManager(self.request_args).find_pollen_data()
                    docs_without_error = []

                    # Create list with all markets of each retrieved document
                    for document in retrieved_document:
                        if not document.get('error'):
                            docs_without_error.append(document)

                    # [CASE]: All retrieved documents contain errors
                    if len(docs_without_error) == 0:
                        return VASMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

                    # [CASE]: At least one document without error
                    else:
                        # 1. Check which markets contain users's selected allergens
                        user_selected_allergens, markets_with_allergens = self.request_args.get('allergens'), []

                        for document in docs_without_error:
                            for market in document.get('Sensor data'):
                                for allergen in market.get('today').get('triggers'):
                                    if allergen in user_selected_allergens:
                                        markets_with_allergens.append({
                                            "date": document.get('Forecast date'),
                                            "market": market.get('market')
                                        })
                                        break

                        # [CASE]: NO allergens match to markets
                        if len(markets_with_allergens) == 0:
                            return VASMaps.error_leaflet_response(MARKETS_GEOJSON, 1)

                        # [CASE]: Allergens match to markets
                        else:
                            # 1. Check if exist dates for which users were on markets with selected allergens
                            markets_with_users, valid_markets = [], []

                            for vas_data in usa_points:
                                vas_date = datetime(vas_data.get('date').year,
                                                    vas_data.get('date').month,
                                                    vas_data.get('date').day) + timedelta(hours=4) # TODO 4 because i get pollen data at 4 utc
                                for market in markets_with_allergens:
                                    if (vas_date == market.get('date')) and (vas_data.get('market') == market.get('market')):
                                        markets_with_users.append(vas_data)

                            # [CASE]: NO USERS at markets for these dates
                            if len(markets_with_users) == 0:
                                return VASMaps.error_leaflet_response(MARKETS_GEOJSON, 0)

                            # [CASE]: USERS found
                            else:

                                market_and_scale = VASMaps.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, markets_with_users)

                                # Create geojson with markets data
                                valid_markets = []
                                for market1 in MARKETS_GEOJSON.get('features'):
                                    for market2 in market_and_scale:
                                        if market1.get('properties').get('market_to_') == market2.get('market'):
                                            market1.get('properties').update(density = market2.get('scale'))
                                            valid_markets.append(market1.get('properties').get('market_to_'))

                                for market in MARKETS_GEOJSON.get('features'):
                                    if not market.get('properties').get('market_to_') in valid_markets:
                                        market.get('properties').update(density = 100)

                                return {
                                    "data": MARKETS_GEOJSON,
                                    "message": None
                                }


    def google_map(self):
        """ Returns geojson with USA sensors including vas data. """

        vas_documents = VASMapsFindManager(self.request_args).find_vas_data()

        # [CASE]: Document not found from mongodb
        if len(vas_documents) == 0:
            return False

        # [CASE]: Documents found for the request
        else:
            scale_and_point = []

            for document in vas_documents:
                scale_and_point.append({
                    "date": document.get('timestamp'),
                    "scale": document.get('VAS Inputs')[0].get('today symptoms'),
                    "point": {"lat": document.get('location')[0].get('coordinates')[0],
                              "lng": document.get('location')[0].get('coordinates')[1]}
                })

            # Check of the existence of user's points at USA
            usa_points = VASMaps.check_existence_of_usa_points(scale_and_point)

            # [CASE]: NO user's points at USA
            if usa_points == False:
                return False

            # [CASE]: User's points found at USA
            else:

                # [CASE]: ALLERGENS
                if len(self.request_args.get('allergens')) == 0:

                    sensors_features = []
                    # Create geojson with sensor points
                    for point in usa_points:
                        sensors_features.append({
                            "type": "Feature",
                            "properties": {
                                "weight": point.get('symptom_scale'),
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [
                                    point.get('coordinates').get('lat'),
                                    point.get('coordinates').get('lng')
                                ]
                            }})

                    return {
                        "type": "FeatureCollection",
                        "features": sensors_features
                    }
                
                # [CASE]: ALLERGENS
                else:
                    # Retrieve markets data for requested time interval.
                    retrieved_document = SensorMapsFindManager(self.request_args).find_pollen_data()
                    docs_without_error = []

                    # Create list with all markets of each retrieved document
                    for document in retrieved_document:
                        if not document.get('error'):
                            docs_without_error.append(document)

                    # [CASE]: All retrieved documents contain errors
                    if len(docs_without_error) == 0:
                        return False

                    # [CASE]: At least one document without error
                    else:
                        # 1. Check which sensors contain users's selected allergens
                        user_selected_allergens, sensors_with_allergens = self.request_args.get('allergens'), []

                        for document in docs_without_error:
                            for sensor in document.get('Sensor data'):
                                for allergen in sensor.get('periods')[0].get('triggers'):
                                    if allergen.get('Name') in user_selected_allergens:
                                        sensors_with_allergens.append({
                                            "date": document.get('Forecast date'),
                                            "sensor": sensor.get('basic info').get('sensor_id')
                                        })
                                        break

                        # [CASE]: NO allergens match to markets
                        if len(sensors_with_allergens) == 0:
                            return False

                        # [CASE]: Allergens match to markets
                        else:
                            # 1. Update above list with the markets at which sensors are included
                            with open(file_path(MAP_DATA_FILE, FILES.get('markets with sensors'))) as file:
                                MARKETS_AND_SENSORS = json.load(file)

                            for market in MARKETS_AND_SENSORS:
                                for sensor in sensors_with_allergens:
                                    if sensor.get('sensor') in market.get('sensors'):
                                        sensor.update(market = market.get('market'))

                            # 2. Find out if exist dates for which users were on markets with selected allergens
                            sensors_with_users, valid_markets = [], []

                            for vas_data in usa_points:
                                vas_date = datetime(vas_data.get('date').year,
                                                    vas_data.get('date').month,
                                                    vas_data.get('date').day) + timedelta(hours=4) # TODO 4 because i get pollen data at 4 utc

                                for sensor in sensors_with_allergens:
                                    if (vas_date == sensor.get('date')) and (vas_data.get('market') == sensor.get('market')):
                                        sensors_with_users.append({"coordinates": [
                                                                       vas_data.get('coordinates').get('lat'),
                                                                       vas_data.get('coordinates').get('lng')
                                                                   ],
                                                                   "symptom_scale": vas_data.get('symptom_scale')
                                                                })
                                        break

                            # [CASE]: NO USERS at markets for these dates
                            if len(sensors_with_users) == 0:
                                return False

                            # [CASE]: USERS found
                            else:
                                # 1. Create geojson using users's coordinates
                                sensors_features = []

                                for point in sensors_with_users:
                                    sensors_features.append({
                                        "type": "Feature",
                                        "properties": {
                                            "weight": point.get('symptom_scale'),
                                        },
                                        "geometry": {
                                            "type": "Point",
                                            "coordinates": [
                                                point.get('coordinates')[0],
                                                point.get('coordinates')[1]
                                            ]
                                        }})

                                return {
                                    "type": "FeatureCollection",
                                    "features": sensors_features
                                }

            
class TwitterMap:
    """ 
    Class which contains method about the coloring of leaflet twitter map. 
    """

    def create_state_geojson(time_interval):
        """ Returns geojson data with usa info about the number of tweets for each of them. """

        twitter_data = TwitterFindManager.find_twitter_data(time_interval)

        with open(file_path(MAP_DATA_FILE, FILES.get('states'))) as file:
            STATES_GEOJSON = json.load(file)

        # [CASE]: NULL mongodb response
        if len(twitter_data) == 0:
            for state1 in STATES_GEOJSON.get('features'):
                state1.get('properties').update(tweets = '-')
            return STATES_GEOJSON

        else:
            with open(file_path(MAP_DATA_FILE, FILES.get('states codes'))) as file:
                STATES_CODES = json.load(file)

            dt_query = datetime.utcnow() - timedelta(minutes=time_interval)
            start_date_interval = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
            end_date_interval = datetime(dt_query.year, dt_query.month, dt_query.day)
            day_dif = (start_date_interval.date() - end_date_interval.date()).days

            tweets, states_tweets, states_with_tweets = 0, [], []

            for state_code in STATES_CODES:
                for doc in twitter_data:
                    if state_code == doc.get('state_code'):
                        tweets += 1

                if tweets != 0:
                    if day_dif == 0:
                        states_tweets.append({"state_code": state_code,
                                              "tweets": tweets})
                    else:
                        states_tweets.append({"state_code": state_code,
                                              "tweets": round((tweets/day_dif))})
                    tweets = 0

            # Create geojson with above data
            for state1 in STATES_GEOJSON.get('features'):
                for state2 in states_tweets:
                    if state1.get('properties').get('STUSPS') == state2.get('state_code'):
                        state1.get('properties').update(tweets = state2.get('tweets'))
                        states_with_tweets.append(state1.get('properties').get('STUSPS'))                        

            for state1 in STATES_GEOJSON.get('features'):
                if not state1.get('properties').get('STUSPS') in states_with_tweets:
                    state1.get('properties').update(tweets = '-')

            return STATES_GEOJSON


class HybridMCSMap:
    """ 
    Class which contains methods about the coloring of leaflet map
    using VAS and twitter data. 
    """

    def __init__(self, request_args):
        self.request_args = request_args

    @staticmethod
    def error_leaflet_response(geojson, allergens_state):
        """ Returns response when an error occurs. """

        if allergens_state == 0:
            message = None
        elif allergens_state == 1:
            message = 'No areas found for selected allergens.'

        for market in geojson.get('features'):
            market.get('properties').update(density = 100)

        return {
            "data": geojson,
            "message": message
        }


    @staticmethod
    def check_existence_of_usa_points(scale_and_point):
        """ 
        Check if users's points are inside USA's markets and then create
        list with dicts of form {date, market, scale}. 
        """

        market_and_scale = []

        with open(file_path(MAP_DATA_FILE, FILES.get('polygons'))) as json_file:
            POLYGONS = json.load(json_file)
        with open(file_path(MAP_DATA_FILE, FILES.get('multipolygons'))) as json_file:
            MULTIPOLYGONS = json.load(json_file)

        for pair in scale_and_point:
            point = Point(pair.get('point').get('lat'), pair.get('point').get('lng'))

            for data in POLYGONS:
                polygon = Polygon(data.get('coordinates'))
                if polygon.contains(point):
                    market_and_scale.append({
                        "date": pair.get('date'),
                        "coordinates": {
                            "lat": pair.get('point').get('lat'),
                            "lng": pair.get('point').get('lng')
                        },
                        "market": data.get('market_code'),
                        "symptom_scale": pair.get('scale')
                    })

            for multipolygon in MULTIPOLYGONS:
                for data in multipolygon.get('coordinates'):
                    polygon = Polygon(data)
                    if polygon.contains(point):
                        market_and_scale.append({
                            "date": pair.get('date'),
                            "coordinates": {
                                "lat": pair.get('point').get('lat'),
                                "lng": pair.get('point').get('lng')
                            },
                            "market": multipolygon.get('market_code'),
                            "symptom_scale": pair.get('scale')
                        })

        # Check if users's vas coords are not inside us markets
        if market_and_scale:
            return market_and_scale
        else:
            return False


    @staticmethod
    def markets_and_vas_scale(time_interval, day_dif, dt_query, MARKETS, usa_points):
        """ Returns the average (if needed) of user's symptoms scale for each usa market. """

        # [CASE]: Req. which depends data for the (max) range of 24 hours.
        if ((time_interval == 0) or (day_dif == 0) or 
            ((day_dif == 1) and (dt_query.hour - datetime.utcnow().hour >=0))):
            
            market_counter, scale_sum, market_and_scale = 0, 0, []
            for market_name in MARKETS:
                for pair in usa_points:
                    if market_name == pair.get('market'):
                        scale_sum += pair.get('symptom_scale')
                        market_counter += 1

                if market_counter != 0:
                    market_and_scale.append({"market": market_name,
                                            "scale": round((scale_sum/market_counter), 1)})
                    scale_sum, market_counter = 0, 0

            return market_and_scale

        # [CASE]: Req. which dependes data from more than one day
        elif day_dif > 1:
            
            # 1. Specify dates which must be queried throught "usa_points" list
            dates_queries = []
            for day in range(1, day_dif+1):
                dates_queries.append(datetime.utcnow() - timedelta(hours=24*day))

            # 2. Create dicts which contains user's points for each day of the time interval
            temp_list, market_day_data = [], []
            for date in dates_queries:
                for point in usa_points:
                    if (point.get('date') >= date) and (point.get('date') <= date + timedelta(days=1)):
                        temp_list.append(point)

                if temp_list:
                    market_day_data.append({"Date": date,
                                            "markets_info": temp_list})
                    temp_list = []                        

            # 3. For each dict. (each date) of the above list, find the market's values
            market_counter, scale_sum, temp_market_and_scale = 0, 0, []
            for data in market_day_data:

                for market_name in MARKETS:
                    for market_data in data.get('markets_info'):
                        if market_name == market_data.get('market'):
                            scale_sum += market_data.get('symptom_scale')
                            market_counter += 1

                    if market_counter != 0:
                        temp_market_and_scale.append({"market": market_name,
                                                    "symptom_scale": round((scale_sum/market_counter), 1)})
                        scale_sum, market_counter = 0, 0

            # 4. Find the average of the above list for all markets and divide by day_dif.
            scale_sum, market_counter, market_and_scale = 0, 0, []
            for market_name in MARKETS:
                for pair in temp_market_and_scale:
                    if market_name == pair.get('market'):
                        scale_sum += pair.get('symptom_scale')
                        market_counter += 1

                if market_counter != 0:
                    market_and_scale.append({"market": market_name,
                                            "scale": round(scale_sum/day_dif, 1)})
                    scale_sum, market_counter = 0, 0

            return market_and_scale


    @staticmethod
    def markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, allergens):
        """ For each market, returns the number of tweets. """

        # [CASE]: SELECTED ALLERGENS FROM THE USER
        if allergens:

            # 1. Append markets with same state code.
            states_and_markets, markets = [], []
            for state_code1 in STATES_CODES:
                for state_code2 in twitter_data:
                    if state_code1 == state_code2.get('state_code'):
                        for market in state_code2.get('markets'):
                            markets.append(market)

                if len(markets) != 0:
                    states_and_markets.append({"state_code": state_code1,
                                               "markets": markets})
                    markets = []

            # 2. Find the average market value for each state of the above list
            tweets, temp_twitter_market_and_scale = 0, []
            for data in states_and_markets:

                for market1 in MARKETS:
                    for market2 in data.get('markets'):
                        if market1 == market2:
                            tweets += 1

                    if tweets != 0:
                        if day_dif == 0:
                            temp_twitter_market_and_scale.append({"market": market1,
                                                                  "tweets": tweets})
                        else:
                            temp_twitter_market_and_scale.append({"market": market1,
                                                                  "tweets": round(tweets/day_dif)})
                        tweets = 0

        else:
            # 1. Find the average of tweets for each state.
            #    List with dict of form {state_code, tweets}.
            tweets, states_and_tweets, states_with_tweets = 0, [], []

            for state_code in STATES_CODES:
                for doc in twitter_data:
                    if state_code == doc.get('state_code'):
                        tweets += 1

                if tweets != 0:
                    if day_dif == 0:
                        states_and_tweets.append({"state_code": state_code,
                                                  "tweets": tweets})
                    else:
                        states_and_tweets.append({"state_code": state_code,
                                                  "tweets": round((tweets/day_dif))})
                    tweets = 0

            # 2. Create list with dicts of form {market, tweets}
            temp_twitter_market_and_scale = []
            for state in states_and_tweets:
                for pair in STATES_AND_MARKETS:
                    if state.get('state_code') == pair.get('state_code'):
                        for market in pair.get('markets'):
                            temp_twitter_market_and_scale.append({
                                "market": market,
                                "tweets": state.get('tweets')
                            })

        # 3. Find the average of above list (case of duplicated markets, almost ever)
        tweets_sum, market_counter, market_and_tweets_scale = 0, 0, []
        for market1 in MARKETS:
            for market2 in temp_twitter_market_and_scale:
                if market1 == market2.get('market'):
                    tweets_sum += market2.get('tweets')
                    market_counter += 1

            if market_counter != 0:
                market_and_tweets_scale.append({
                    "market": market1,
                    "tweets": round((tweets_sum/market_counter)) 
                })
                tweets_sum, market_counter = 0, 0

        # 4. Convert one range to another (0-12)
        """ Methodology """
        # OldRange = (OldMax - OldMin)
        # NewRange = (NewMax - NewMin)
        # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        MARKETS_MAX_TWEETS = HybridMCSMap.calculate_max_tweets_value(STATES_CODES, STATES_AND_MARKETS, MARKETS)
        new_range = 12
        new_ranged_markets_and_tweets = []

        for data in market_and_tweets_scale:
            for max_ in MARKETS_MAX_TWEETS:
                if data.get('market') == max_.get('market'):

                    old_range = max_.get('tweets')  
                    old_value = data.get('tweets')

                    if old_range == 0:
                        new_value = 0
                    else:
                        new_value = (old_value * new_range) / old_range

                    # Case of not desired result
                    if new_value > 12:
                        new_value = 12

                    new_ranged_markets_and_tweets.append({"market": data.get("market"),
                                                          "scale":  round(new_value,1),
                                                          "old_max": old_range,
                                                          "old_scale": data.get('tweets')})

        return new_ranged_markets_and_tweets


    @staticmethod
    def calculate_max_tweets_value(STATES_CODES, STATES_AND_MARKETS, MARKETS):
        """ 
        Returns max value of twitter for each market of USA (time interval: x days).
        'x': A config which will try to be αs representative as possible.
        """

        # Days which will be retrieved from twitter collection in order to find the max value from these days.
        days = CONFIGURATION.days_for_normalisation
        db_docs = list(DB_CONSTANTS.twitter_usa_colletion.find({"Date": {"$gte": datetime.utcnow() - timedelta(days=days)}}))
        
        # 1. Find min and max date for the query and then calculate the difference of the days
        dates = []
        for doc in db_docs:
            dates.append(doc.get('Date'))

        min_date, max_date = min(dates), max(dates)
        day_dif = (max_date.date() - min_date.date()).days

        # 2. Specify dates which must be queried throught "usa_points" list
        dates_queries = []
        for day in range(1, day_dif+1):
            dates_queries.append(datetime.utcnow() - timedelta(hours=24*day))

        # 3. Create dicts which contain tweets/states for each day of the query.
        temp_list, twitter_day_data = [], []
        for date in dates_queries:
            for doc in db_docs:
                if (doc.get('Date') >= date) and (doc.get('Date') <= date + timedelta(days=1)):
                    temp_list.append(doc.get('state_code'))

            if temp_list:
                twitter_day_data.append({"Date": date,
                                        "twitter_data": temp_list})
                temp_list = []

        # 4. For each dict. (each day) of the above list, find the tweets count for each state.
        tweet_sum, states_and_tweets = 0, []
        for data in twitter_day_data:

            for state in STATES_CODES:
                for state_data in data.get('twitter_data'):
                    if state == state_data:
                        tweet_sum += 1

                if tweet_sum != 0:
                    states_and_tweets.append({"state": state,
                                              "tweets": tweet_sum})
                    tweet_sum = 0

        # 5. Create list with all the tweets values for each state.
        # List of dicts like {state, tweets:[x,x,x,]}.
        tweets, states_and_tweets2 = [], []
        for state1 in STATES_CODES:
            for state2 in states_and_tweets:
                if state1 == state2.get('state'):
                    tweets.append(state2.get('tweets'))

            if len(tweets) != 0:
                states_and_tweets2.append({"state": state1,
                                           "tweets": tweets})
                tweets = []

        # 6. Find max tweets for each state
        # List of dicts like {state, max_tweet_value}
        states_and_tweets3 = []
        for state in states_and_tweets2:
            states_and_tweets3.append({"state": state.get('state'),
                                       "tweets": max(state.get('tweets'))})

        # 7. Match states's twitter values to markets
        markets_and_tweets = []
        for state in states_and_tweets3:
            for pair in STATES_AND_MARKETS:
                if state.get('state') == pair.get('state_code'):
                    for market in pair.get('markets'):
                        markets_and_tweets.append({"market": market,
                                                   "tweets": state.get('tweets')})

        # 8. Find the average of above list (case of duplicated markets, almost ever)
        tweets_sum, market_counter, market_and_tweet_mean = 0, 0, []
        for market1 in MARKETS:
            for market2 in markets_and_tweets:
                if market1 == market2.get('market'):
                    tweets_sum += market2.get('tweets')
                    market_counter += 1

            if market_counter != 0:
                market_and_tweet_mean.append({"market": market1,
                                              "tweets": round((tweets_sum/market_counter))})
                tweets_sum, market_counter = 0, 0

        return market_and_tweet_mean


    @staticmethod
    def hybrid_mcs_calculation(MARKETS_GEOJSON, market_and_vas_scale, market_and_tweets_scale):
        """ Returns market's hybrid values (vas & twitter). """

        vas_weight = CONFIGURATION.VAS_vas_twitter
        twitter_weight = CONFIGURATION.TWITTER_vas_twitter

        # 1. Find the common markets between vas & twitter and calculate hybrid value
        hybrid_markets, final_markets_values = [], []
        for vas_market in market_and_vas_scale:
            for twitter_market in market_and_tweets_scale:
                if vas_market.get('market') == twitter_market.get('market'):

                    HYBRID_VALUE = vas_market.get('scale')*vas_weight + twitter_market.get('scale')*twitter_weight

                    final_markets_values.append({
                        "market": vas_market.get('market'),
                        "scale": round(HYBRID_VALUE, 1)
                    })
                    hybrid_markets.append(vas_market.get('market'))

        # 2. Add to the final list the rest markets of each vas & twitter list
        for vas_market in market_and_vas_scale:
            if not vas_market.get('market') in hybrid_markets:
                final_markets_values.append(vas_market)

        for twitter_market in market_and_tweets_scale:
            if not twitter_market.get('market') in hybrid_markets:
                final_markets_values.append(twitter_market)

        return HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, final_markets_values)


    @staticmethod
    def general_market_coloring(MARKETS_GEOJSON, market_and_scale):
        """ Returns market's values for input. Vas or Twitter. """

        valid_markets = []
        for market1 in MARKETS_GEOJSON.get('features'):
            for market2 in market_and_scale:

                if market1.get('properties').get('market_to_') == market2.get('market'):
                    market1.get('properties').update(density = market2.get('scale'))
                    valid_markets.append(market1.get('properties').get('market_to_'))

        for market in MARKETS_GEOJSON.get('features'):
            if not market.get('properties').get('market_to_') in valid_markets:
                market.get('properties').update(density = 100)

        return MARKETS_GEOJSON


    def leaflet_map(self):
        """ Returns geojson with USA markets including hybrid m.c.s. density. """

        with open(file_path(MAP_DATA_FILE, FILES.get('us markets'))) as file:
            MARKETS_GEOJSON = json.load(file)

        # Retrieve data from mongodb
        vas_data, VAS = VASMapsFindManager(self.request_args).find_vas_data(), True
        twitter_data, TWITTER = TwitterFindManager.find_twitter_data(self.request_args.get('time_interval')), True

        """ Check the existence of vas and twitter data """
        if len(vas_data) == 0:
            VAS = False
        else:
            scale_and_point = []
            for document in vas_data:
                scale_and_point.append({
                    "date": document.get('timestamp'),
                    "scale": document.get('VAS Inputs')[0].get('today symptoms'),
                    "point": {"lat": document.get('location')[0].get('coordinates')[0],
                            "lng": document.get('location')[0].get('coordinates')[1]}
                })

            # Check of the existence of the points at USA
            usa_points = HybridMCSMap.check_existence_of_usa_points(scale_and_point)

            # [CASE]: NO user's points at USA
            if usa_points == False:
                VAS = False

        if len(twitter_data) == 0:
            TWITTER = False


        # [CASE]: Null response from mongodb for both vas and twitter
        if (not VAS) and (not TWITTER):
            return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

        # [CASE]: At least one element exists
        else:
            """ Necessary data """
            with open(file_path(MAP_DATA_FILE, FILES.get('markets names'))) as json_file:
                MARKETS = json.load(json_file)
            with open(file_path(MAP_DATA_FILE, FILES.get('states and markets'))) as json_file:
                STATES_AND_MARKETS = json.load(json_file)
            with open(file_path(MAP_DATA_FILE, FILES.get('states codes'))) as file:
                STATES_CODES = json.load(file)

            dt_query = datetime.utcnow() - timedelta(minutes=self.request_args.get('time_interval'))
            start_date_interval = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
            end_date_interval = datetime(dt_query.year, dt_query.month, dt_query.day)
            day_dif = (start_date_interval.date() - end_date_interval.date()).days

            if VAS and TWITTER:

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ ----------- VAS ----------- """
                    market_and_vas_scale = HybridMCSMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    """ --------- TWITTER --------- """
                    market_and_tweets_scale = HybridMCSMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, False)

                    return {
                        "data": HybridMCSMap.hybrid_mcs_calculation(MARKETS_GEOJSON, market_and_vas_scale, market_and_tweets_scale),
                        "message": None
                    }
                    
                # [CASE]: ALLERGENS SELECTED
                else:
                    # Retrieve pollen sensors markets data for requested time interval.
                    sensor_docs = SensorMapsFindManager(self.request_args).find_pollen_data()

                    # Create list with all markets of each retrieved document
                    docs_without_error = []
                    for document in sensor_docs:
                        if not document.get('error'):
                            docs_without_error.append(document)

                    # [CASE]: All retrieved sensor documents contain errors
                    if len(docs_without_error) == 0:
                        return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

                    # [CASE]: At least one sensor document without error
                    else:
                        # 1. Check which markets contain users's selected allergens
                        user_selected_allergens, markets_with_allergens = self.request_args.get('allergens'), []

                        for document in docs_without_error:
                            for market in document.get('Sensor data'):
                                for allergen in market.get('today').get('triggers'):
                                    if allergen in user_selected_allergens:
                                        markets_with_allergens.append({
                                            "date": document.get('Forecast date'),
                                            "market": market.get('market')
                                        })
                                        break

                        # [CASE]: NO allergens match to markets
                        if len(markets_with_allergens) == 0:
                            return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                        # [CASE]: Allergens match to markets
                        else:
                            # 1i. VAS: Check if exist dates for which users were on markets with selected allergens
                            vas_markets_with_users = []
                            for vas_data in usa_points:
                                vas_date = datetime(vas_data.get('date').year,
                                                    vas_data.get('date').month,
                                                    vas_data.get('date').day) + timedelta(hours=4) # TODO 4 because i get pollen data at 4 utc
                                for market in markets_with_allergens:
                                    if (vas_date == market.get('date')) and (vas_data.get('market') == market.get('market')):
                                        vas_markets_with_users.append(vas_data)

                            # 1ii. Twitter: Check if exist dates for which users were on markets with selected allergens
                            state_markets, temp_markets, twitter_markets_with_users = [], [], []
                            for data in twitter_data:
                                # Find the markets of each state
                                for state in STATES_AND_MARKETS:
                                    if data.get('state_code') == state.get('state_code'):
                                        for market in state.get('markets'):
                                            state_markets.append(market)
                                # Define Date | TODO 4 because i get pollen data at 4 utc
                                twitter_date = datetime(data.get('Date').year, data.get('Date').month, data.get('Date').day) + timedelta(hours=4)

                                # Check which of these markets are contained to the markets with allergens
                                for market1 in markets_with_allergens:
                                    if twitter_date == market1.get('date'):
                                        for market2 in state_markets:
                                            if market2 == market1.get('market'):
                                                temp_markets.append(market2)

                                if len(temp_markets) != 0:
                                    twitter_markets_with_users.append({"state_code": data.get('state_code'),
                                                                       "markets": temp_markets})
                                    temp_markets = []
                                state_markets = []

                            # [CASE]: NO USERS at markets for these dates
                            if len(vas_markets_with_users) == 0 and len(twitter_markets_with_users) == 0:
                                return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

                            # [CASE]: USERS found
                            else:
                                
                                if len(vas_markets_with_users) != 0 and len(twitter_markets_with_users) != 0:
                                    """ ----------- VAS ----------- """
                                    market_and_vas_scale = HybridMCSMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, vas_markets_with_users)

                                    """ --------- TWITTER --------- """
                                    market_and_tweets_scale = HybridMCSMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_markets_with_users, day_dif, True)

                                    return {
                                        "data": HybridMCSMap.hybrid_mcs_calculation(MARKETS_GEOJSON, market_and_vas_scale, market_and_tweets_scale),
                                        "message": None
                                    }

                                elif len(vas_markets_with_users) != 0 and len(twitter_markets_with_users) == 0:
                                    """ ----------- VAS ----------- """
                                    market_and_vas_scale = HybridMCSMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, vas_markets_with_users)

                                    return {
                                        "data": HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, market_and_vas_scale),
                                        "message": None
                                    }

                                elif len(vas_markets_with_users) == 0 and len(twitter_markets_with_users) != 0:
                                    """ --------- TWITTER --------- """
                                    market_and_tweets_scale = HybridMCSMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_markets_with_users, day_dif, True)

                                    return {
                                        "data": HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, market_and_tweets_scale),
                                        "message": None
                                    }

            elif VAS and (not TWITTER):

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    market_and_vas_scale = HybridMCSMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    return {
                        "data": HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, market_and_vas_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:
                    # Retrieve pollen sensors markets data for requested time interval.
                    sensor_docs = SensorMapsFindManager(self.request_args).find_pollen_data()

                    # Create list with all markets of each retrieved document
                    docs_without_error = []
                    for document in sensor_docs:
                        if not document.get('error'):
                            docs_without_error.append(document)

                    # [CASE]: All retrieved sensor documents contain errors
                    if len(docs_without_error) == 0:
                        return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

                    # [CASE]: At least one sensor document without error
                    else:
                        # 1. Check which markets contain users's selected allergens
                        user_selected_allergens, markets_with_allergens = self.request_args.get('allergens'), []

                        for document in docs_without_error:
                            for market in document.get('Sensor data'):
                                for allergen in market.get('today').get('triggers'):
                                    if allergen in user_selected_allergens:
                                        markets_with_allergens.append({
                                            "date": document.get('Forecast date'),
                                            "market": market.get('market')
                                        })
                                        break

                        # [CASE]: NO allergens match to markets
                        if len(markets_with_allergens) == 0:
                            return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                        # [CASE]: Allergens match to markets
                        else:
                            # 1i. VAS: Check if exist dates for which users were on markets with selected allergens
                            vas_markets_with_users = []
                            for vas_data in usa_points:
                                vas_date = datetime(vas_data.get('date').year,
                                                    vas_data.get('date').month,
                                                    vas_data.get('date').day) + timedelta(hours=4) # TODO 4 because i get pollen data at 4 utc
                                for market in markets_with_allergens:
                                    if (vas_date == market.get('date')) and (vas_data.get('market') == market.get('market')):
                                        vas_markets_with_users.append(vas_data)
                            
                            # [CASE]: NO USERS at markets for these dates
                            if len(vas_markets_with_users) == 0:
                                return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

                            # [CASE]: USERS found
                            else:

                                market_and_vas_scale = HybridMCSMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, vas_markets_with_users)

                                return {
                                    "data": HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, market_and_vas_scale),
                                    "message": None
                                }

            elif (not VAS) and TWITTER:

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:
                    
                    market_and_tweets_scale = HybridMCSMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, False)

                    return {
                        "data": HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, market_and_tweets_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:
                    # Retrieve pollen sensors markets data for requested time interval.
                    sensor_docs = SensorMapsFindManager(self.request_args).find_pollen_data()

                    # Create list with all markets of each retrieved document
                    docs_without_error = []
                    for document in sensor_docs:
                        if not document.get('error'):
                            docs_without_error.append(document)

                    # [CASE]: All retrieved sensor documents contain errors
                    if len(docs_without_error) == 0:
                        return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

                    # [CASE]: At least one sensor document without error
                    else:
                        # 1. Check which markets contain users's selected allergens
                        user_selected_allergens, markets_with_allergens = self.request_args.get('allergens'), []

                        for document in docs_without_error:
                            for market in document.get('Sensor data'):
                                for allergen in market.get('today').get('triggers'):
                                    if allergen in user_selected_allergens:
                                        markets_with_allergens.append({
                                            "date": document.get('Forecast date'),
                                            "market": market.get('market')
                                        })
                                        break

                        # [CASE]: NO allergens match to markets
                        if len(markets_with_allergens) == 0:
                            return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                        # [CASE]: Allergens match to markets
                        else:
                            # 1ii. Twitter: Check if exist dates for which users were on markets with selected allergens
                            state_markets, temp_markets, twitter_markets_with_users = [], [], []
                            for data in twitter_data:
                                # Find the markets of each state
                                for state in STATES_AND_MARKETS:
                                    if data.get('state_code') == state.get('state_code'):
                                        for market in state.get('markets'):
                                            state_markets.append(market)
                                # Define Date | TODO 4 because i get pollen data at 4 utc
                                twitter_date = datetime(data.get('Date').year, data.get('Date').month, data.get('Date').day) + timedelta(hours=4)

                                for market1 in markets_with_allergens:
                                    if twitter_date == market1.get('date'):
                                        for market2 in state_markets:
                                            if market2 == market1.get('market'):
                                                temp_markets.append(market2)

                                if len(temp_markets) != 0:
                                    twitter_markets_with_users.append({"state_code": data.get('state_code'),
                                                                       "markets": temp_markets})
                                    temp_markets = []
                                state_markets = []
                            
                            # [CASE]: NO USERS at markets for these dates
                            if len(twitter_markets_with_users) == 0:
                                return HybridMCSMap.error_leaflet_response(MARKETS_GEOJSON, 0)

                            # [CASE]: USERS found
                            else:
                                market_and_tweets_scale = HybridMCSMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_markets_with_users, day_dif, True)

                                return {
                                    "data": HybridMCSMap.general_market_coloring(MARKETS_GEOJSON, market_and_tweets_scale),
                                    "message": None
                                }


class HybridMap(HybridMCSMap):
    """ 
    Class which contains methods about the coloring of leaflet map
    using VAS, twitter and pollen sensor data. 
    """

    def __init__(self, request_args):
        """ Class constructor. """
        super().__init__(request_args)


    @staticmethod
    def market_and_sensor_scale(MARKETS, pollen_data, allergens_case):
        """ For each market returns the average from sensor values. """

        pollen_index_sum, market_counter, market_and_sensor_scale = 0, 0, []

        for market1 in MARKETS:
            for market2 in pollen_data:

                if market1 == market2.get('market'):

                    if allergens_case:
                        if market2.get('scale') != 100:
                            pollen_index_sum += market2.get('scale')
                            market_counter += 1
                    else:
                        if market2.get('today').get('pollen_index') != 100:
                            pollen_index_sum += market2.get('today').get('pollen_index')
                            market_counter += 1

            if market_counter != 0:
                market_and_sensor_scale.append({
                    "market": market1,
                    "scale": round((pollen_index_sum/market_counter),1)
                })
                pollen_index_sum, market_counter = 0, 0

        return market_and_sensor_scale


    @staticmethod
    def hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, market_and_vas_scale, market_and_tweets_scale):
        """ 
        Returns hybrid calculated value for usa markets.
        Inputs: Sensors, VAS, Twitter.
        """

        # Inputs weights
        w_SENSOR_sensor_vas = CONFIGURATION.SENSOR_sensor_vas
        w_VAS_sensor_vas = CONFIGURATION.VAS_sensor_vas
        w_SENSOR_sensor_twitter = CONFIGURATION.SENSOR_sensor_twitter
        w_TWITTER_sensor_twitter = CONFIGURATION.TWITTER_sensor_twitter
        w_VAS_vas_twitter = CONFIGURATION.VAS_vas_twitter
        w_TWITTER_vas_twitter = CONFIGURATION.TWITTER_vas_twitter
        w_SENSOR_all = CONFIGURATION.SENSOR_all
        w_VAS_all = CONFIGURATION.VAS_all
        w_TWITTER_all = CONFIGURATION.TWITTER_all

        # 1. Create common list which will contains the trhee inputs
        if market_and_sensor_scale:
            for data in market_and_sensor_scale:
                data["type"] = "sensor"
        
        if market_and_vas_scale:
            for data in market_and_vas_scale:
                data["type"] = "vas"

        if market_and_tweets_scale:
            for data in market_and_tweets_scale:
                data["type"] = "twitter"

        all_markets = []
        all_markets = market_and_sensor_scale + market_and_vas_scale + market_and_tweets_scale

        # 2. Find the combinations of the same markets and calculate the respective hybrid value
        market_counter, temp_markets, final_markets_values = 0, [], []

        for market1 in MARKETS:
            for market2 in all_markets:

                if market1 == market2.get('market'):
                    temp_markets.append(market2)
                    market_counter += 1

            if market_counter != 0:

                # 1 input
                if market_counter == 1:
                    final_markets_values.append({"market": temp_markets[0].get('market'),
                                                 "scale": temp_markets[0].get('scale')})

                # 2 inputs
                elif market_counter == 2:

                    if temp_markets[0].get("type") == "sensor" and temp_markets[1].get("type") == "vas":

                        HYBRID = temp_markets[0].get("scale")*w_SENSOR_sensor_vas + temp_markets[1].get("scale")*w_VAS_sensor_vas
                        final_markets_values.append({"market": market1, "scale": round(HYBRID,1)})

                    elif temp_markets[1].get("type") == "sensor" and temp_markets[0].get("type") == "vas":

                        HYBRID = temp_markets[1].get("scale")*w_SENSOR_sensor_vas + temp_markets[0].get("scale")*w_VAS_sensor_vas
                        final_markets_values.append({"market": market1, "scale": round(HYBRID,1)})

                    elif temp_markets[0].get("type") == "sensor" and temp_markets[1].get("type") == "twitter":

                        HYBRID = temp_markets[0].get("scale")*w_SENSOR_sensor_twitter + temp_markets[1].get("scale")*w_TWITTER_sensor_twitter
                        final_markets_values.append({"market": market1, "scale": round(HYBRID,1)})

                    elif temp_markets[1].get("type") == "sensor" and temp_markets[0].get("type") == "twitter":

                        HYBRID = temp_markets[1].get("scale")*w_SENSOR_sensor_twitter + temp_markets[0].get("scale")*w_TWITTER_sensor_twitter
                        final_markets_values.append({"market": market1, "scale": round(HYBRID,1)})

                    elif temp_markets[0].get("type") == "twitter" and temp_markets[1].get("type") == "vas":

                        HYBRID = temp_markets[0].get("scale")*w_TWITTER_vas_twitter + temp_markets[1].get("scale")*w_VAS_vas_twitter
                        final_markets_values.append({"market": market1, "scale": round(HYBRID,1)})

                    elif temp_markets[1].get("type") == "twitter" and temp_markets[0].get("type") == "vas":

                        HYBRID = temp_markets[1].get("scale")*w_TWITTER_vas_twitter + temp_markets[0].get("scale")*w_VAS_vas_twitter
                        final_markets_values.append({"market": market1,"scale": round(HYBRID,1)})

                # 3 inputs
                elif market_counter == 3:
                    for data in temp_markets:
                        if data.get("type") == "sensor":
                            sensor_scale = data.get("scale")
                        elif data.get("type") == "vas":
                            vas_scale = data.get("scale")
                        elif data.get("type") == "twitter":
                            twitter_scale = data.get("scale")

                    HYBRID = sensor_scale*w_SENSOR_all + vas_scale*w_VAS_all + twitter_scale*w_TWITTER_all

                    final_markets_values.append({"market": market1,
                                                 "scale": round(HYBRID,1)})

                market_counter, temp_markets = 0, []

        return HybridMap.general_market_coloring(MARKETS_GEOJSON, final_markets_values)


    @staticmethod
    def check_existence_of_markets_on_selected_allergens(user_selected_allergens, valid_pollen_docs):
        """ Returns markets which contain user's selected allergens. Or False, if not. """

        markets_with_allergens = []
        for document in valid_pollen_docs:
            for market in document.get('Sensor data'):
                for allergen in market.get('today').get('triggers'):
                    if allergen in user_selected_allergens:
                        markets_with_allergens.append({
                            "market": market.get('market'),
                            "scale": market.get('today').get('pollen_index'),
                            "date": document.get('Forecast date'),
                        })
                        break

        # [CASE]: No allergens matches to markets
        if len(markets_with_allergens) == 0:
            return False
        else:
            return markets_with_allergens


    @staticmethod
    def check_vas_existence_on_allergens_markets(usa_points, markets_with_allergens):
        """ VAS: Check if exist dates for which users were on markets with selected allergens. """

        vas_markets_with_users = []
        for vas_data in usa_points:
            vas_date = datetime(vas_data.get('date').year,
                                vas_data.get('date').month,
                                vas_data.get('date').day) + timedelta(hours=4) # TODO 4 because i get pollen data at 4 utc
            for market in markets_with_allergens:
                if (vas_date == market.get('date')) and (vas_data.get('market') == market.get('market')):
                    vas_markets_with_users.append(vas_data)

        if len(vas_markets_with_users) == 0:
            return False
        else:
            return vas_markets_with_users


    @staticmethod
    def check_twitter_existence_on_allergens_markets(STATES_AND_MARKETS, twitter_data, markets_with_allergens):
        """ Twitter: Check if exist dates for which users were on markets with selected allergens. """

        state_markets, temp_markets, twitter_markets_with_users = [], [], []

        for data in twitter_data:
            # Find the markets of each state
            for state in STATES_AND_MARKETS:
                if data.get('state_code') == state.get('state_code'):
                    for market in state.get('markets'):
                        state_markets.append(market)
            # Define Date | TODO 4 because i get pollen data at 4 utc
            twitter_date = datetime(data.get('Date').year, data.get('Date').month, data.get('Date').day) + timedelta(hours=4)

            # Check which of these markets are contained to the markets with allergens
            for market1 in markets_with_allergens:
                if twitter_date == market1.get('date'):
                    for market2 in state_markets:
                        if market2 == market1.get('market'):
                            temp_markets.append(market2)

            if len(temp_markets) != 0:
                twitter_markets_with_users.append({"state_code": data.get('state_code'),
                                                    "markets": temp_markets})
                temp_markets = []
            state_markets = []

        if len(twitter_markets_with_users) == 0:
            return False
        else:
            return twitter_markets_with_users


    def leaflet_map(self):
        """ Returns geojson with USA markets including hybrid density. """

        with open(file_path(MAP_DATA_FILE, FILES.get('us markets'))) as file:
            MARKETS_GEOJSON = json.load(file)

        # Retrieve necessary data from mongodb
        pollen_data, POLLEN = SensorMapsFindManager(self.request_args).find_pollen_data(), True
        vas_data, VAS = VASMapsFindManager(self.request_args).find_vas_data(), True
        twitter_data, TWITTER = TwitterFindManager.find_twitter_data(self.request_args.get('time_interval')), True

        """ Check the existence of above retrieved data """

        # Pollen
        if len(pollen_data) == 0:
            POLLEN = False
        else:
            # Create list with all markets of each retrieved document
            valid_pollen_docs, valid_pollen_markets = [], []
            for document in pollen_data:
                if not document.get('error'):
                    # list with documents (all markets of each day)
                    valid_pollen_docs.append(document)
                    # list with markets
                    for market in document.get('Sensor data'):
                        valid_pollen_markets.append(market)

            # [CASE]: All retrieved documents contain errors
            if len(valid_pollen_markets) == 0:
                POLLEN = False

        # Vas
        if len(vas_data) == 0:
            VAS = False
        else:
            scale_and_point = []
            for document in vas_data:
                scale_and_point.append({
                    "date": document.get('timestamp'),
                    "scale": document.get('VAS Inputs')[0].get('today symptoms'),
                    "point": {"lat": document.get('location')[0].get('coordinates')[0],
                              "lng": document.get('location')[0].get('coordinates')[1]}
                })

            # Check of the existence of the points at USA
            usa_points = HybridMCSMap.check_existence_of_usa_points(scale_and_point)

            # [CASE]: NO user's points at USA
            if usa_points == False:
                VAS = False

        # Twitter
        if len(twitter_data) == 0:
            TWITTER = False

        # [CASE]: Null response from mongodb for all retrieved data
        if (not POLLEN) and (not VAS) and (not TWITTER):
            return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 0)

        # [CASE]: At least one element exists
        else:

            """ Necessary data """
            with open(file_path(MAP_DATA_FILE, FILES.get('markets names'))) as json_file:
                MARKETS = json.load(json_file)
            with open(file_path(MAP_DATA_FILE, FILES.get('states and markets'))) as json_file:
                STATES_AND_MARKETS = json.load(json_file)
            with open(file_path(MAP_DATA_FILE, FILES.get('states codes'))) as file:
                STATES_CODES = json.load(file)

            dt_query = datetime.utcnow() - timedelta(minutes=self.request_args.get('time_interval'))
            start_date_interval = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
            end_date_interval = datetime(dt_query.year, dt_query.month, dt_query.day)
            day_dif = (start_date_interval.date() - end_date_interval.date()).days
            """ -------------- """

            if POLLEN and VAS and TWITTER:

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ --------- POLLEN --------- """
                    market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, valid_pollen_markets, False)
                    
                    """ ----------- VAS ----------- """
                    market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    """ --------- TWITTER --------- """
                    market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, False)

                    """ HYBRID CALCULATION """
                    return {
                        "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, market_and_vas_scale, market_and_tweets_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:

                    # Check if exist markets which contain user's selected allergens
                    markets_with_allergens = HybridMap.check_existence_of_markets_on_selected_allergens(self.request_args.get('allergens'), valid_pollen_docs)

                    # [CASE]: No alllergens matches to markets
                    if not markets_with_allergens:
                        return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                    # [CASE]: Allergens match to markets
                    else:

                        """ --------- POLLEN: Find the average sensor value for each of the above markets. --------- """
                        market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, markets_with_allergens, True)

                        """ ----------- VAS: Find markets - which match with 'markets_with_allergens' list -  for which users have submitted symptoms. ----------- """
                        vas_markets_with_users = HybridMap.check_vas_existence_on_allergens_markets(usa_points, markets_with_allergens)

                        """ --------- TWITTER: Find markets - which match with 'markets_with_allergens' list -  for which users have posted tweets. --------- """
                        twitter_markets_with_users = HybridMap.check_twitter_existence_on_allergens_markets(STATES_AND_MARKETS, twitter_data, markets_with_allergens)

                        # [CASE]: NO USERS at markets for these dates, so return only sensor/pollen data.
                        if (not vas_markets_with_users) and (not twitter_markets_with_users):

                            return {
                                "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_sensor_scale),
                                "message": None
                            }

                        # [CASE]: USERS found
                        else:
                            
                            if vas_markets_with_users and twitter_markets_with_users:

                                """ ----------- VAS ----------- """
                                market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, vas_markets_with_users)

                                """ --------- TWITTER --------- """
                                market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_markets_with_users, day_dif, True)

                                return {
                                    "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, market_and_vas_scale, market_and_tweets_scale),
                                    "message": None
                                }

                            elif vas_markets_with_users and (not twitter_markets_with_users):

                                """ ----------- VAS ----------- """
                                market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, vas_markets_with_users)

                                return {
                                    "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, market_and_vas_scale, []),
                                    "message": None
                                }

                            elif (not vas_markets_with_users) and twitter_markets_with_users:

                                """ --------- TWITTER --------- """
                                market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_markets_with_users, day_dif, True)

                                return {
                                    "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, [], market_and_tweets_scale),
                                    "message": None
                                }

            elif POLLEN and (not VAS) and TWITTER:

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ --------- POLLEN --------- """
                    market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, valid_pollen_markets, False)

                    """ --------- TWITTER --------- """
                    market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, False)

                    """ HYBRID CALCULATION """
                    return {
                        "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, [], market_and_tweets_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:

                    # Check if exist markets which contain user's selected allergens
                    markets_with_allergens = HybridMap.check_existence_of_markets_on_selected_allergens(self.request_args.get('allergens'), valid_pollen_docs)

                    # [CASE]: No alllergens matches to markets
                    if not markets_with_allergens:
                        return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                    # [CASE]: Allergens match to markets
                    else:

                        """ --------- POLLEN: Find the average sensor value for each of the above markets. --------- """
                        market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, markets_with_allergens, True)

                        """ --------- TWITTER: Find markets - which match with 'markets_with_allergens' list -  for which users have posted tweets. --------- """
                        twitter_markets_with_users = HybridMap.check_twitter_existence_on_allergens_markets(STATES_AND_MARKETS, twitter_data, markets_with_allergens)

                        # [CASE]: NO USERS at markets for these dates, so return only sensor/pollen data.
                        if not twitter_markets_with_users:

                            return {
                                "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_sensor_scale),
                                "message": None
                            }

                        # [CASE]: USERS found
                        else:

                            """ --------- TWITTER --------- """
                            market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_markets_with_users, day_dif, True)

                            return {
                                "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, [], market_and_tweets_scale),
                                "message": None
                            }

            elif POLLEN and VAS and (not TWITTER):

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ --------- POLLEN --------- """
                    market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, valid_pollen_markets, False)

                    """ ----------- VAS ----------- """
                    market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    """ HYBRID CALCULATION """
                    return {
                        "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, market_and_vas_scale, []),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:

                    # Check if exist markets which contain user's selected allergens
                    markets_with_allergens = HybridMap.check_existence_of_markets_on_selected_allergens(self.request_args.get('allergens'), valid_pollen_docs)

                    # [CASE]: No alllergens matches to markets
                    if not markets_with_allergens:
                        return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                    # [CASE]: Allergens match to markets
                    else:

                        """ --------- POLLEN: Find the average sensor value for each of the above markets. --------- """
                        market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, markets_with_allergens, True)

                        """ ----------- VAS: Find markets - which match with 'markets_with_allergens' list -  for which users have submitted symptoms. ----------- """
                        vas_markets_with_users = HybridMap.check_vas_existence_on_allergens_markets(usa_points, markets_with_allergens)

                        # [CASE]: NO USERS at markets for these dates, so return only sensor/pollen data.
                        if not vas_markets_with_users:

                            return {
                                "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_sensor_scale),
                                "message": None
                            }

                        # [CASE]: USERS found
                        else:

                            """ ----------- VAS ----------- """
                            market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, vas_markets_with_users)

                            return {
                                "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, market_and_sensor_scale, market_and_vas_scale, []),
                                "message": None
                            }

            elif POLLEN and (not VAS) and (not TWITTER):

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ --------- POLLEN --------- """
                    market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, valid_pollen_markets, False)

                    """ POLLEN CALCULATION """
                    return {
                        "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_sensor_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:

                    # Check if exist markets which contain user's selected allergens
                    markets_with_allergens = HybridMap.check_existence_of_markets_on_selected_allergens(self.request_args.get('allergens'), valid_pollen_docs)

                    # [CASE]: No alllergens matches to markets
                    if not markets_with_allergens:
                        return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 1)

                    # [CASE]: Allergens match to markets
                    else:

                        """ --------- POLLEN: Find the average sensor value for each of the above markets. --------- """
                        market_and_sensor_scale = HybridMap.market_and_sensor_scale(MARKETS, markets_with_allergens, True)

                        return {
                                "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_sensor_scale),
                                "message": None
                            }

            elif (not POLLEN) and VAS and TWITTER:

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ ----------- VAS ----------- """
                    market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    """ --------- TWITTER --------- """
                    market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, False)

                    """ HYBRID CALCULATION """
                    return {
                        "data": HybridMap.hybrid_calculation(MARKETS, MARKETS_GEOJSON, [], market_and_vas_scale, market_and_tweets_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:

                    return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 0)

            elif (not POLLEN) and VAS and (not TWITTER):

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ ----------- VAS ----------- """
                    market_and_vas_scale = HybridMap.markets_and_vas_scale(self.request_args.get('time_interval'), day_dif, dt_query, MARKETS, usa_points)

                    """ VAS CALCULATION """
                    return {
                        "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_vas_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:

                    return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 0) 

            elif (not POLLEN) and (not VAS) and TWITTER:

                # [CASE]: NO allergens selected
                if len(self.request_args.get('allergens')) == 0:

                    """ --------- TWITTER --------- """
                    market_and_tweets_scale = HybridMap.markets_and_tweets_scale(STATES_CODES, STATES_AND_MARKETS, MARKETS, twitter_data, day_dif, False)

                    """ TWITTER CALCULATION """
                    return {
                        "data": HybridMap.general_market_coloring(MARKETS_GEOJSON, market_and_tweets_scale),
                        "message": None
                    }

                # [CASE]: ALLERGENS SELECTED
                else:
                    
                    return HybridMap.error_leaflet_response(MARKETS_GEOJSON, 0)


class HumidityMaps:
    """
    Class which contains functions for the implementetion of user's requests about humidity
    maps at home page.
    """

    def color_humidity_map(time_interval):
        """ 
        Returns geojson including complete info about markets and also their densities.
        """

        db_hum_data = HumidityFindManager.find_humidity_data(time_interval)

        """ ------------------- [CASE]: ERROR -------------------- """
        if isinstance(db_hum_data, str):

            us_markets_path = file_path(MAP_DATA_FILE, FILES.get('us markets'))
            with open(us_markets_path) as json_file:
                us_markets = json.load(json_file)

            # Add for each market debug value for density
            for market in us_markets.get('features'):
                market.get('properties').update(density=120)

            resp = {
                "market_data": us_markets
            }
            return resp
            """ ------------------------------------------------------ """

        else:

            us_markets_path = file_path(MAP_DATA_FILE, FILES.get('us markets'))
            with open(us_markets_path) as json_file:
                us_markets_including_density = json.load(json_file)

            # TODAY
            if time_interval == 0:
                for market1 in db_hum_data[0].get('Markets data'):
                    for market2 in us_markets_including_density.get('features'):
                        if market1.get('market') == market2.get('properties').get('market_to_'):
                            market2.get('properties').update(density = market1.get('cur_humidity'))
                        
                resp = {"market_data": us_markets_including_density}
                return resp

            # TOMORROW
            elif time_interval == 1:
                for market1 in db_hum_data[0].get('Markets data'):
                    for market2 in us_markets_including_density.get('features'):
                        if market1.get('market') == market2.get('properties').get('market_to_'):
                            market2.get('properties').update(density = market1.get('for_humidity'))

                resp = {"market_data": us_markets_including_density}
                return resp

            # TIME INTERVAL
            else:
                for market1 in db_hum_data[0].get('Markets data'):
                    for market2 in us_markets_including_density.get('features'):
                        if market1.get('market') == market2.get('properties').get('market_to_'):
                            market2.get('properties').update(density = market1.get('cur_humidity'))
                        
                resp = {"market_data": us_markets_including_density}
                return resp
            """ --------------------------------------------------------------------------- """


    def color_humidity_gmap_testing():
        """ 
        Returns list with all owm points for u.s. with their densities.
        """

        db_hum_data = HumidityFindManager.find_humidity_gmap_testing()

        points = []
        for data in db_hum_data[0].get('Sensor data'):
            points.append({'point': [data.get('location').get('coordinates')[0], data.get('location').get('coordinates')[1]],
                           'weight': data.get('humidity')})

        return points


class HomeVasTool:
    """
    Class which contains function for the process & insertion of user's vas input to mongodb.
    """

    def add_vas_info(list_args, LOGGER): 
        """ Adds vas information to mongodb. """

        general_symptoms_today = list_args[0].get('general_symptoms')
        rhinitis_symptoms_today = list_args[1].get('rhinitis')
        asthma_symptoms_today = list_args[2].get('asthma')
        conjunctivitis_symptoms_today = list_args[3].get('conjunctivitis')
        work_state = list_args[4].get('work')
        work_symptoms = list_args[5].get('work_symptoms')
        latitude = list_args[6].get('lat')
        longtitude = list_args[7].get('lng')
        location_state = list_args[8].get('location state')

        LOGGER.debug(f'VAS INPUTS: {general_symptoms_today}, {rhinitis_symptoms_today}, {asthma_symptoms_today}, {conjunctivitis_symptoms_today}, {work_state}, {work_symptoms}, {latitude}, {longtitude}, {location_state}, {datetime.utcnow()}')

        user_time = datetime.utcnow()
        no_work = 'No work/school today'
        no_location = 'No location given'

        if work_state == 'Yes' and location_state == True:
            UserInsertManager.insert_vas(session.get('email'), general_symptoms_today, rhinitis_symptoms_today, asthma_symptoms_today,
                                    conjunctivitis_symptoms_today, work_state, work_symptoms, latitude, longtitude, user_time)

        elif work_state == 'No' and location_state == False:
            UserInsertManager.insert_vas_without_geolocation(session.get('email'), general_symptoms_today, rhinitis_symptoms_today, asthma_symptoms_today,
                                    conjunctivitis_symptoms_today, work_state, no_work, no_location, user_time)

        elif work_state == 'No' and location_state == True:
            UserInsertManager.insert_vas(session.get('email'), general_symptoms_today, rhinitis_symptoms_today, asthma_symptoms_today,
                                    conjunctivitis_symptoms_today, work_state, no_work, latitude, longtitude, user_time)

        elif work_state == 'Yes' and location_state == False:
            UserInsertManager.insert_vas_without_geolocation(session.get('email'), general_symptoms_today, rhinitis_symptoms_today, asthma_symptoms_today,
                                    conjunctivitis_symptoms_today, work_state, work_symptoms, no_location, user_time)

        resp = 'Success'
        return resp
