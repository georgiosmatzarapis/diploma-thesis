""" Module which contains the Config class. """
from datetime import timedelta
from backend.helpers.lib import file_path
import os, yaml


class Config(object):
    """ Configuration class for AllergyMap US-edition. """

    def __init__(self):
        """ Class constructor """
        conf_file_path = file_path('configs','config.yaml')

        if os.path.isfile(conf_file_path):
            config_dict = yaml.safe_load(open(conf_file_path, 'r'))
            # WSGI Application
            self.secret_key = config_dict['app']['secret_key']
            self.mongo_uri = config_dict['app']['mongo_uri']
            self.permanent_session_lifetime = timedelta(minutes=config_dict['app']['permanent_session_lifetime'])
            # Logger
            self.folder = config_dict['logging']['folder']
            self.file = config_dict['logging']['file']
            self.level = config_dict['logging']['level']
            self.format = config_dict['logging']['format']
            self.template_location = config_dict['locations']['template_location']
            self.static_location = config_dict['locations']['static_location']
            # Maps keys
            self.gmaps_api_key = config_dict['google_maps']['api_key']
            self.leaflet_map_tile = config_dict['lealfet_maps']['tile']
            # Maps weights
            self.SENSOR_sensor_vas = config_dict['hybrid_maps']['sensor_vas']['sensor']
            self.VAS_sensor_vas = config_dict['hybrid_maps']['sensor_vas']['vas']

            self.SENSOR_sensor_twitter = config_dict['hybrid_maps']['sensor_twitter']['sensor']
            self.TWITTER_sensor_twitter = config_dict['hybrid_maps']['sensor_twitter']['twitter']

            self.VAS_vas_twitter = config_dict['hybrid_maps']['vas_twitter']['vas']
            self.TWITTER_vas_twitter = config_dict['hybrid_maps']['vas_twitter']['twitter']

            self.SENSOR_all = config_dict['hybrid_maps']['sensor_vas_twitter']['sensor']
            self.VAS_all = config_dict['hybrid_maps']['sensor_vas_twitter']['vas']
            self.TWITTER_all = config_dict['hybrid_maps']['sensor_vas_twitter']['twitter']
            # Twitter config
            self.days_for_normalisation = config_dict['twitter_max_days_retrieved_for_normalisation']
        else:
            print(f"Config file: {conf_file_path} not found.")
            exit(1)

CONFIGURATION = Config()