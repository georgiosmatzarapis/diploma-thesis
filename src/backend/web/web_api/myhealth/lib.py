from flask import session
from backend.web.database_api import MyhealthManager
from backend.web import lib
from backend import lg
from backend.helpers.constans import VALIDATION_NAMESPACE
from datetime import datetime

LOGGER = lg.get_logger(__name__)


def get_data_for_line_graph():
    """ 
    Returns a list like -> [ [timestamp,symptom], [timestamp,symptom], [timestamp,symptom], ...,[timestamp,symptom] ] 
    1) Timestamps will be values from last year until current date
    2) For each day of submitted vas form, will return  only 5 pairs of datetime and symptoms.
    """

    selected_data = MyhealthManager.get_last_year_dates_from_vas(session.get('email'))

    timestamp_symptoms = []
    final_list = []
    counter = 0

    # store in 'timestamp_symptoms' list with pairs of timestamps, symptoms -> [ [timestamp,symptom], [timestamp,symptom], [timestamp,symptom], ...,[timestamp,symptom] ]
    for x in selected_data:
        timestamp_symptoms.append([x.get('timestamp'), x['VAS Inputs'][0].get('today symptoms')])

    # In this loop, are selected max 5 pairs of datetime and symptoms, for each day of submitted vas form.
    epoch = datetime.utcfromtimestamp(0)
    for i in range(0, len(timestamp_symptoms)):
        
        if i != len(timestamp_symptoms)-1:
            
            if (timestamp_symptoms[i][0].date()) == (timestamp_symptoms[i+1][0].date()):
                counter += 1

                if counter <= 4:
                    date = (timestamp_symptoms[i][0].replace(microsecond=0) - epoch).total_seconds() * 1000.0
                    final_list.append([date, timestamp_symptoms[i][1]])
                else:
                    continue

            else:
                date = (timestamp_symptoms[i][0].replace(microsecond=0) - epoch).total_seconds() * 1000.0
                final_list.append([date, timestamp_symptoms[i][1]])
                counter = 0
            
        else:
            date = (timestamp_symptoms[i][0].replace(microsecond=0) - epoch).total_seconds() * 1000.0
            final_list.append([date, timestamp_symptoms[i][1]])

    return final_list


def get_geolocation_point_pairs(minutes_interval):
    """ Returns user's geolocation for the given argument. """
    
    selected_data = MyhealthManager.get_documents_with_existing_coordinates(session.get('email'), minutes_interval)

    geolocation_pairs_list = []
    for data in selected_data:
        temp_dict = {'geolocation': data.get('location')[0].get('coordinates'), 
                     'symptoms_scale':  data.get('VAS Inputs')[0].get('today symptoms')}
        geolocation_pairs_list.append(temp_dict)

    return geolocation_pairs_list
