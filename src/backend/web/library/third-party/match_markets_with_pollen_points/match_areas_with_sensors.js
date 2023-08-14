fetch('/api/Home/sensors_info')
    .then((response) => { return response.json(); })
    .then((sensorsData) => {

        fetch('/api/Home/us_markets')
            .then((response) => { return response.json(); })
            .then((areasData) => {

                area_sensor_matching(sensorsData, areasData);

            })
            .catch((error) => { console.error('Error:', error); });
    })
    .catch((error) => { console.error('Error:', error); });


/** Returns a list that contains, which sensors match in which areas. */
function area_sensor_matching(sensorsData, areasData) {

    var temp_point_array = [];
    var temp_polygon_array = [];
    var final_polygons_array = [];
    var temp_polygon_dict = {};

    var temp_point_array2 = [];
    var temp_polygon_array2 = [];
    var polygons_array2 = [];
    var final_multipolygons_array = [];
    var temp_multipolygon_dict = {};
    areasData.features.forEach(multi_polygon => {

        if (multi_polygon.geometry.type == "Polygon") {

            multi_polygon.geometry.coordinates[0].forEach(polygon_point => {
                temp_point_array.push(polygon_point[1], polygon_point[0]);
                temp_polygon_array.push(temp_point_array);
                temp_point_array = [];
            });

            temp_polygon_dict = {
                "market_code": multi_polygon.properties.market_to_,
                "coordinates": temp_polygon_array
            };
            final_polygons_array.push(temp_polygon_dict); // Array which includes market_name & coordinates for every area which is polygon.
            temp_polygon_dict = {};
            temp_polygon_array = [];

        } else if (multi_polygon.geometry.type == "MultiPolygon") {

            multi_polygon.geometry.coordinates.forEach(polygon => {

                polygon[0].forEach(polygon_point => {
                    temp_point_array2.push(polygon_point[1], polygon_point[0]);
                    temp_polygon_array2.push(temp_point_array2);
                    temp_point_array2 = [];
                });

                polygons_array2.push(temp_polygon_array2);
                temp_polygon_array2 = [];
            });

            temp_multipolygon_dict = {
                "market_code": multi_polygon.properties.market_to_,
                "coordinates": polygons_array2
            };
            final_multipolygons_array.push(temp_multipolygon_dict); // Array which includes market_name & coordinates for every area which is multipolygon.        
            temp_multipolygon_dict = {};
            polygons_array2 = [];
        }

    });

    var temp_polygon1, temp_polygon2;
    var temp_sensor;
    var temp_dict = {};
    var temp_dict2 = {};
    var data_list = [];
    var data_list2 = [];
    var complete_array = [];
    sensorsData.features.forEach(sensor => {
        temp_sensor = L.marker(sensor.geometry.coordinates);

        final_polygons_array.forEach(polygon => {
            temp_polygon1 = L.polygon(polygon.coordinates);

            if (temp_polygon1.contains(temp_sensor.getLatLng())) {
                temp_dict = {
                    "sensor_market": polygon.market_code,
                    "sensor_id": sensor.properties.city_name + ', ' + sensor.properties.state_code
                };
                data_list.push(temp_dict); // Array that contains fields like -> [{sensor_market, sensor_name, sensor_state},{},{},...,{}], for polygon areas
                temp_dict = {};
            }
        });

        final_multipolygons_array.forEach(multipolygon => {

            multipolygon.coordinates.forEach(polygon => {
                temp_polygon2 = L.polygon(polygon);

                if (temp_polygon2.contains(temp_sensor.getLatLng())) {
                    temp_dict2 = {
                        "sensor_market": multipolygon.market_code,
                        "sensor_id": sensor.properties.city_name + ', ' + sensor.properties.state_code
                    };
                    data_list2.push(temp_dict2); // Array that contains fields like -> [{sensor_market, sensor_name, sensor_state},{},{},...,{}], for multipolygon areas
                    temp_dict2 = {};
                }
            });

        });

    });
    complete_array = data_list.concat(data_list2);

    var area_names = [];
    areasData.features.forEach(area => {
        area_names.push(area.properties.market_to_) //Array with all markets names
    });
    console.log(area_names)
    console.log(complete_array);

    var temp_dict3 = {};
    var temp_dict4 = {};
    var temp_sensors = [];
    var final_data = [];
    var final_data2 = [];
    area_names.forEach(market => {

        complete_array.forEach(sensor => {
            if (sensor.sensor_market == market) {
                temp_sensors.push(sensor.sensor_id);
            }
        });
        if (jQuery.isEmptyObject(temp_sensors)) {
            temp_dict4 = {
                "market": market,
                "info": "No sensors for this market"
            }
            final_data2.push(temp_dict4); // Array with markets that have no sensors
        } else {
            temp_dict3 = {
                "market": market,
                "sensors": temp_sensors
            };
            final_data.push(temp_dict3); // Array with markets and its sensors
        }
        temp_dict3 = {};
        temp_dict4 = {};
        temp_sensors = [];

    });
    console.log(final_data);
    console.log(final_data2);
    return final_data;
}