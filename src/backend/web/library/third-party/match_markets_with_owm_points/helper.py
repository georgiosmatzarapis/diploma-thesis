import os, json, pprint
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def file_path(folder_name, file_name):
    """ Specify file path. """
    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path

# polygons_path = file_path('find spots', 'polygons_markets.json')
# with open(polygons_path) as json_file:
#     polygons = json.load(json_file)

# multipolygons_path = file_path('find spots', 'multipolygons_markets.json')
# with open(multipolygons_path) as json_file:
#     multipolygons = json.load(json_file)

# markets_path = file_path('find spots', 'markets_names.json')
# with open(markets_path) as json_file:
#     market_names = json.load(json_file)

# owm_points_path = file_path('find spots', 'us_cities.json')
# with open(owm_points_path) as json_file:
#     owm_points = json.load(json_file)


""" STEP 1: For each market find every owm point which is inside. """

# temp_list = []
# owm_list = []
# final_list = []

# for owm_point in owm_points:
#     point = Point(owm_point.get('coord').get('lat'),
#                   owm_point.get('coord').get('lon'))

#     for data in polygons:
#         polygon = Polygon(data.get('coordinates'))
#         if polygon.contains(point):
#             temp_list.append({"market": data.get('market_code'),
#                               "owm_id": owm_point.get('id')})

#     for multipolygon in multipolygons:
#         for data in multipolygon.get('coordinates'):
#             polygon = Polygon(data)
#             if polygon.contains(point):
#                 temp_list.append({"market": multipolygon.get('market_code'),
#                                   "owm_id": owm_point.get('id')})


# for market_name in market_names:

#     for data in temp_list:
#         if market_name == data.get('market'):
#             owm_list.append(data.get('owm_id'))

#     if owm_list:
#         final_list.append({"market": market_name,
#                            "owm_points": owm_list})
#         owm_list = []
#     else:
#         final_list.append({"market": market_name,
#                            "owm_points": "NO"})
#         owm_list = []

# with open('markets_with_owm_points.json', 'w') as json_file:
#     json.dump(final_list, json_file)



""" STEP2: From these points, hold 6 of them for each market. """

# markets_with_owm_path = file_path('find spots', 'markets_with_owm_points.json')
# with open(markets_with_owm_path) as json_file:
#     markets_info = json.load(json_file)

# for market in markets_info:
#     if len(market.get('owm_points')) > 6:
#         market.update(owm_points = market.get('owm_points')[:6])


# with open('markets_with_owm_points_6.json', 'w') as json_file:
#     json.dump(markets_info, json_file)