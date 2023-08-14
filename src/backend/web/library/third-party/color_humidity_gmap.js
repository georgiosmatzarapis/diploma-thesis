/** Coloring of google map (heatmap) with all (19.908) points from OpenWeatherMap */

var currentDate4 = new Date;
utc_offset4 = (-currentDate4.getTimezoneOffset()); // Retrieve user's utc offset

fetch('/api/Home/humidity_gmap')
    .then((response) => { return response.json(); })
    .then((data => {
        heat_data = [];
        data.forEach(point => {
            heat_data.push({
                location: new google.maps.LatLng(point.point[0], point.point[1]),
                weight: point.weight
            });
        });
        // console.log('[DEBUG]');
        // console.log('Gathered data: ', heat_data);
        // console.log('[END]');

        set_heatmap4(heat_data, gradient, 3.3, true, 100, humidity_gmap);
        // zoom_changed_event_main4(humidity_gmap);

    }))
    .catch((error) => { console.error('Error:', error); });