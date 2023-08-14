""" Match zip codes to points. """

import pgeocode, os.path, yaml, json
import pandas as pd


def zip_codes_list():
    """ Returns a list with all sensor's (cities) zip codes. """

    zip_codes_conf_path = "us_zip_codes.yaml"
    zip_code_counter = 0
    zip_code_list = []

    if not os.path.isfile(zip_codes_conf_path):
        print(f"Config file: {zip_codes_conf_path} not found.")
        exit(1)

    with open(zip_codes_conf_path) as file:
        conf = yaml.full_load(file)

    for key, value in conf.items():
        for data in value:
            for key, value in data.items():
                zip_code_counter += 1
                zip_code_list.append(value)

    return zip_code_list

def match_zip_codes_to_points():
    """ Returns json with sensor's info, including points. """

    zip_codes = zip_codes_list()
    nomi = pgeocode.Nominatim('us') # region to look up
    df = nomi.query_postal_code(zip_codes) # All zip code's points as pandas df
    my_list = df.values.tolist() # Convert df to list

    zip_codes_to_points = []
    for x in my_list:
        temp_dict = {"type": "Feature",
                    "properties": {"city_name": x[2],
                                    "state_code": x[4]},
                    "geometry": {"type": "Point",
                                "coordinates": [x[9], x[10]]}}
        zip_codes_to_points.append(temp_dict)

    return zip_codes_to_points