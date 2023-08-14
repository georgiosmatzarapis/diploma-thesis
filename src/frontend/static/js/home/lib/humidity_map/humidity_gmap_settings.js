var heatmap4, zoom_listener4;

/** Set heatmap layer. */
function set_heatmap4(heat_data, gradient, radius, dissipating, maxIntensity, my_map) {

    heatmap4 = new google.maps.visualization.HeatmapLayer({
        data: heat_data,
        gradient: gradient,
        radius: radius,
        opacity: 0.6,
        dissipating: dissipating,
        maxIntensity: maxIntensity
    });
    heatmap4.setMap(my_map);
}
/** Delete heatmap layer. */
function delete_heatmap4() {
    heatmap4.setMap(null);
}

/** Set zoom listenter. */
function zoom_changed_event_main4(my_map) {
    zoom_listener4 = google.maps.event.addListener(my_map, 'zoom_changed', function () {
        var zoomLevel = my_map.getZoom();
        switch (zoomLevel) {
            case 7:
                heatmap4.set('radius', 0.22);
                break;
            case 6:
                heatmap4.set('radius', 0.37);
                break;
            case 5:
                heatmap4.set('radius', 0.42);
                break;
            case 4:
                heatmap4.set('radius', 0.5);
                break;
        }
        // console.log(zoomLevel);
    });
}
/** Delete zoom listener. */
function delete_zoom_listener1() {
    google.maps.event.removeListener(zoom_listener4);
}

// Load states
var temp_polygon = [];
var temp_polygon2 = [];
var polygon_on_map;

fetch('api/Home/us_states')
    .then((response) => {
        return response.json();
    })
    .then((states) => {
        states.features.forEach(state => {

            if (state.geometry.type == 'Polygon') {

                state.geometry.coordinates[0].forEach(polygon_point => {
                    temp_polygon.push({ lat: polygon_point[1], lng: polygon_point[0] });
                });

                polygon_on_map = new google.maps.Polygon({
                    paths: temp_polygon,
                    strokeColor: '#000',
                    strokeOpacity: .75,
                    strokeWeight: 1,
                    fillOpacity: 0
                });
                polygon_on_map.setMap(humidity_gmap);
                temp_polygon = []

            } else if (state.geometry.type == 'MultiPolygon') {

                state.geometry.coordinates.forEach(polygon => {

                    polygon[0].forEach(polygon_point => {
                        temp_polygon2.push({ lat: polygon_point[1], lng: polygon_point[0] });
                    });

                    polygon_on_map = new google.maps.Polygon({
                        paths: temp_polygon2,
                        strokeColor: '#000',
                        strokeOpacity: .75,
                        strokeWeight: 1,
                        fillOpacity: 0
                    });
                    polygon_on_map.setMap(humidity_gmap);
                    temp_polygon2 = []

                });
            }
        });
    })
    .catch((error) => { console.error('Error:', error); });