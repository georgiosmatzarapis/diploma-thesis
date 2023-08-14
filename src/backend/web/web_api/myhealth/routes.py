from flask import redirect, Response, request, session, Blueprint, jsonify, json
from flask_restplus import Resource, Namespace
from backend import lg
from . import lib
from backend.helpers.constans import VALIDATION_NAMESPACE
from backend.web.database_api import UserFindManager
from backend.web.lib import check_if_all_settings_exist

LOGGER = lg.get_logger(__name__)
NAMESPACE = Namespace('MyHealth', description='Api namespace representing \'/myHealth\' page requirements.')


@NAMESPACE.route('/line_graph')
class MyhealthGraphApi(Resource):

    def get(self):
        """ Returns a list which includes processed data about user's health (timestamp and symptom scale from vas tool). """
        
        USER = UserFindManager.find_user('email', session.get('email'))

        if USER and check_if_all_settings_exist():

            response = lib.get_data_for_line_graph()
            return response

        else:
            return VALIDATION_NAMESPACE.UNKNOWN_USER


@NAMESPACE.route('/myallergymap/<int:time_interval>')
class MyAllergyMapApi(Resource):

    def get(self, time_interval):
        """ Get input (path param) user's selected time in minutes and returns geolocation point pairs. """

        USER = UserFindManager.find_user('email', session.get('email'))

        if USER and check_if_all_settings_exist():

            response = lib.get_geolocation_point_pairs(time_interval)
            return response

        else:
            return VALIDATION_NAMESPACE.UNKNOWN_USER
