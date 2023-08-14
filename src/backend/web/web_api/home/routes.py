from flask import session, jsonify, json
from flask_restplus import Resource, Namespace

from backend import lg
from backend.helpers.lib import file_path
from backend.helpers.constans import VALIDATION_NAMESPACE
from backend.web.database_api import UserFindManager
from backend.web.lib import check_if_all_settings_exist
from . import lib


LOGGER = lg.get_logger(__name__)
NAMESPACE = Namespace('Home', description='Api namespace representing \'/Home\' page requirements.')

maps_args = NAMESPACE.parser().add_argument('request_data', help='Required data for lmap display.', type=dict, required=True)
sensor_args = NAMESPACE.parser().add_argument('sensors_data', help='Required data for gmap display.', type=dict, required=True)
vas_tool = NAMESPACE.parser().add_argument('vas', help='The updated vas.', type=dict, required=True)


@NAMESPACE.route('/sensor_maps')
class SensorMapsAPI(Resource):

    @NAMESPACE.expect(maps_args)
    def post(self):
        """
        Serves data for pollen sensor maps: 
        Gets required data for maps display.
        Returns geojson which includes all required info about USA markets. 
        """

        returned_args = maps_args.parse_args().get("request_data")

        if returned_args.get("map_type") == "leaflet":
            return lib.PollenSensorMaps(returned_args).leaflet_map()

        elif returned_args.get("map_type") == "google":
            return lib.PollenSensorMaps(returned_args).google_map()


@NAMESPACE.route('/vas_maps')
class VASMapsAPI(Resource):

    @NAMESPACE.expect(maps_args)
    def post(self):
        """
        Serves data for vas maps:
        Gets required data for maps display.
        Returns geojson which includes all required info about USA markets. 
        """

        returned_args = maps_args.parse_args().get("request_data")

        if returned_args.get("map_type") == "leaflet":
            return lib.VASMaps(returned_args).leaflet_map()

        elif returned_args.get("map_type") == "google":
            return lib.VASMaps(returned_args).google_map()


@NAMESPACE.route('/twitter/<int:time_interval>/<int:utc_offset>')
class TwitterUStatesApi(Resource):

    def get(self, time_interval, utc_offset):
        """ Returns geojson which includes us states with twitter data. """

        response = lib.TwitterMap.create_state_geojson(time_interval)
        return response


@NAMESPACE.route('/hybrid_mcs_map')
class HybridMCSMapApi(Resource):

    @NAMESPACE.expect(maps_args)
    def post(self):
        """
        Serves data for hybrid mcs map:
        Gets required data for map display.
        Returns geojson which includes all required info about USA markets. 
        """

        returned_args = maps_args.parse_args().get("request_data")

        response = lib.HybridMCSMap(returned_args).leaflet_map()
        return response


@NAMESPACE.route('/hybrid_map')
class HybridMapApi(Resource):

    @NAMESPACE.expect(maps_args)
    def post(self):
        """
        Serves data for hybrid map:
        Gets required data for map display.
        Returns geojson which includes all required info about USA markets. 
        """

        returned_args = maps_args.parse_args().get("request_data")

        response = lib.HybridMap(returned_args).leaflet_map()
        return response


@NAMESPACE.route('/us_states')
class UStatesApi(Resource):

    def get(self):
        """ Returns geojson which includes us states. """

        us_state_path = file_path("web/web_api/home/map_data", "us_states.json")
        with open(us_state_path) as json_file:
            response = json.load(json_file)
            return jsonify(response)


@NAMESPACE.route('/humidity/<int:time_interval>/<int:utc_offset>')
class HumidityApi(Resource):

    def get(self, time_interval, utc_offset):
        """
        Gets required data for map display. 
        Returns geojson which includes suitable humidity values.
        """

        response = lib.HumidityMaps.color_humidity_map(time_interval)
        return response


@NAMESPACE.route('/humidity_gmap')
class HumidityGmapTestingApi(Resource):

    def get(self):
        """ Returns owm u.s. points with humidity densities. """

        response = lib.HumidityMaps.color_humidity_gmap_testing()
        return response


@NAMESPACE.route('/vastool')
class VasToolApi(Resource):

    @NAMESPACE.expect(vas_tool)
    def post(self):
        """ Gets vas form inputs and insert to mongodb. """

        USER = UserFindManager.find_user('email', session.get('email'))

        if USER and check_if_all_settings_exist():

            list_args = vas_tool.parse_args()['vas']['vas info']
            return lib.HomeVasTool.add_vas_info(list_args, LOGGER)

        else:
            return VALIDATION_NAMESPACE.UNKNOWN_USER