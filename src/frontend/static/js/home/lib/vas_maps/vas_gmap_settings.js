var heatmap2, zoom_listener2, line2;

/** Set heatmap layer. */
function set_heatmap2(heat_data, gradient, radius, dissipating, maxIntensity, my_map) {
    
    heatmap2 = new google.maps.visualization.HeatmapLayer({
        data: heat_data,
        gradient: gradient,
        radius: radius,
        opacity: 0.6,
        dissipating: dissipating,
        maxIntensity: maxIntensity
    });
    heatmap2.setMap(my_map);
}
/** Delete heatmap layer. */
function delete_heatmap2() {
    heatmap2.setMap(null);
}

/** Set zoom listenter. */
function zoom_changed_event_main2(my_map) {
    zoom_listener2 = google.maps.event.addListener(my_map, 'zoom_changed', function () {
        var zoomLevel = my_map.getZoom();
        switch (zoomLevel) {
            case 7:
                heatmap2.set('radius', 0.22);
                break;
            case 6:
                heatmap2.set('radius', 0.37);
                break;
            case 5:
                heatmap2.set('radius', 0.42);
                break;
            case 4:
                heatmap2.set('radius', 0.5);
                break;
        }
        // console.log(zoomLevel);
    });
}
/** Delete zoom listener. */
function delete_zoom_listener2() {
    google.maps.event.removeListener(zoom_listener2);
}

/** Set loader. */
function enable_loader2(my_map) {
    var count = 0;
    var lineSymbol = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        strokeColor: '#5c11e7'
    };

    // Create the polyline and add the symbol to it via the 'icons' property.
    line2 = new google.maps.Polyline({
        path: [{ lat: 39.8, lng: -102 }, { lat: 39.8, lng: -99 }],
        strokeColor: '#1a1919',
        strokeOpacity: 0.9,
        strokeWeight: 17,
        icons: [{
            icon: lineSymbol,
            offset: '100%',
        }],
        map: my_map
    });

    return window.setInterval(function () {
        count = (count + 6) % 200;
        var icons = line2.get('icons');
        icons[0].offset = (count / 2) + '%';
        line2.set('icons', icons);
    }, 20);
}

/** Disable loader. */
function disable_loader2() {
    return line2.setMap(null);
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
                polygon_on_map.setMap(vas_gmap);
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
                    polygon_on_map.setMap(vas_gmap);
                    temp_polygon2 = []

                });
            }
        });
    })
    .catch((error) => { console.error('Error:', error); });