""" Module which contains constants about db. """
from backend import mongo
from backend.helpers.lib import file_path
from datetime import timedelta
import os
import json
import yaml


class DbConstants(object):
    """  Class for AllergyMap database. """

    def __init__(self):
        """ Class constructor """
        conf_file_path = file_path('configs','config.yaml')

        if os.path.isfile(conf_file_path):
            config_dict = yaml.safe_load(open(conf_file_path, 'r'))
            self.user_collection = mongo.db[config_dict['db']['user_collection']]
            self.vas_collection = mongo.db[config_dict['db']['vas_collection']]
            self.pollen_sensors_collection = mongo.db[config_dict['db']['pollen_sensors_collection']]
            self.pollen_markets_collection = mongo.db[config_dict['db']['pollen_markets_collection']]
            self.humidity_api_collection = mongo.db[config_dict['db']['humidity_api_collection']]
            self.today_humidity_api_collection = mongo.db[config_dict['db']['today_humidity_api_collection']]
            self.humidity_gmap_collection = mongo.db[config_dict['db']['humidity_gmap_collection']]
            self.twitter_usa_colletion = mongo.db[config_dict['db']['twitter_usa_colletion']]
        else:
            print(f"Config file: {conf_file_path} not found.")
            exit(1)

DB_CONSTANTS = DbConstants()