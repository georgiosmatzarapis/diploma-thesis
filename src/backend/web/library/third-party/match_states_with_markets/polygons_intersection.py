from shapely.geometry.polygon import Polygon
import pprint, json, os

def file_path(folder_name, file_name):
    """ Specify file path. """
    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path

with open(file_path('match_states_with_markets', 'us_states.json')) as file:
    STATES = json.load(file)

with open(file_path('match_states_with_markets', 'us_markets.json')) as file:
    MARKETS = json.load(file)

states_and_markets = []

# Create list with dict. like {state_code, market}
for state in STATES.get('features'):
    for market in MARKETS.get('features'):

        if state.get('geometry').get('type') == "Polygon" and market.get('geometry').get('type') == "Polygon":
            state_polygon = Polygon(state.get('geometry').get('coordinates')[0])
            market_polygon = Polygon(market.get('geometry').get('coordinates')[0])

            if market_polygon.intersects(state_polygon):
                states_and_markets.append({"state_code": state.get('properties').get('STUSPS'),
                                           "market": market.get('properties').get('market_to_')})


        if state.get('geometry').get('type') == "MultiPolygon" and market.get('geometry').get('type') == "Polygon":

            state_polygon = state.get('geometry').get('coordinates')
            market_polygon = Polygon(market.get('geometry').get('coordinates')[0])

            for polygon in state_polygon:
                st_pol = Polygon(polygon[0])
                if market_polygon.intersects(st_pol):
                    states_and_markets.append({"state_code": state.get('properties').get('STUSPS'),
                                               "market": market.get('properties').get('market_to_')})
                    break


        if state.get('geometry').get('type') == "Polygon" and market.get('geometry').get('type') == "MultiPolygon":

            state_polygon = Polygon(state.get('geometry').get('coordinates')[0])
            market_polygon = market.get('geometry').get('coordinates')

            for polygon in market_polygon:
                mar_pol = Polygon(polygon[0])
                if mar_pol.intersects(state_polygon):
                    states_and_markets.append({"state_code": state.get('properties').get('STUSPS'),
                                               "market": market.get('properties').get('market_to_')})
                    break


        if state.get('geometry').get('type') == "MultiPolygon" and market.get('geometry').get('type') == "MultiPolygon":

            state_polygon = state.get('geometry').get('coordinates')
            market_polygon = market.get('geometry').get('coordinates')

            for polygon1 in state_polygon:
                st_pol = Polygon(polygon1[0])
                find = False
                for polygon2 in market_polygon:
                    mar_pol = Polygon(polygon2[0])

                    if st_pol.intersects(mar_pol):
                        states_and_markets.append({"state_code": state.get('properties').get('STUSPS'),
                                                   "market": market.get('properties').get('market_to_')})
                        find = True
                        break
                if find:
                    break


      
# Create final list with all markets of each state
final_list, temp_markets = [], []

for state in STATES.get('features'):
    for match in states_and_markets:
        if state.get('properties').get('STUSPS') == match.get('state_code'):
            temp_markets.append(match.get('market'))

    if temp_markets:
        final_list.append({
            "state_code": state.get('properties').get('STUSPS'),
            "markets": temp_markets
        })
        temp_markets = []
    else:
        list_2.append(state.get('properties').get('STUSPS'))
