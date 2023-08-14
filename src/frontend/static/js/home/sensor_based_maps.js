// Init lmap
var leaflet_map_tile = $("#leaflet_map_tile").val();
var sensor_lmap = L.map('main_lmap1', { scrollWheelZoom: false }).setView([38.1, -96], 4);
var geojson_markets1, geojson_states1;

L.tileLayer(leaflet_map_tile, {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    minZoom: 4,
    maxZoom: 8,
    tileSize: 512,
    zoomOffset: -1
}).addTo(sensor_lmap);

// Zoom control position
sensor_lmap.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(sensor_lmap);
// -------------------

// TODO Add to all leaflet maps ineraction about showing the exact value of each market

/** Button for hide color guide */
hide_button1(sensor_lmap);
$('#hide_color_guide1').click(function () {

    if ($('#hide_color_guide1').text() == 'Show guide') {
        color_guide_legend1(sensor_lmap); // Add color guide on map
        $("#hide_color_guide1").text("Hide guide");
    } else if (($('#hide_color_guide1').text() == 'Hide guide')) {
        if (legend1) { legend1.remove(); }
        $("#hide_color_guide1").text("Show guide");
    }

});
/** -------------------------- */

/** ---------------------------- DEFAUL LEAFLET MAP---------------------------- */
var d = new Date().getTimezoneOffset();
var utc_offset = -(d/60);

sensor_lmap.spin(true);
fetch('/api/Home/sensor_maps', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(
        {
            "request_data": {
                "time_interval": 0,
                "utc_offset": utc_offset,
                "allergens": [],
                "map_type": "leaflet"
            }
        }
    ),
})
    .then((response) => { return response.json(); })
    .then((marketsData) => {

        geojson_markets1 = L.geoJSON(marketsData.data, {
            style: markets_style1
        }).addTo(sensor_lmap); // Add markets to map

        fetch('/api/Home/us_states')
            .then((response) => { return response.json(); })
            .then((statesData) => {
                geojson_states1 = L.geoJson(statesData, {
                    style: states_style1,
                    onEachFeature: onEachFeature1
                }).addTo(sensor_lmap); // Add states to map

                update_basic_legend1(1, sensor_lmap);

            })
            .catch((error) => { console.error('Error:', error); });
    })
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */

/** ----------------------------- DEFAUL GOOGLE MAP----------------------------- */
fetch('/api/Home/sensor_maps', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(
        {
            "request_data": {
                "time_interval": 0,
                "utc_offset": utc_offset,
                "allergens": [],
                "map_type": "google"
            }
        }
    ),
})
    .then((response) => { return response.json(); })
    .then((data => {
        if (data != false) {
            heat_data = [];
            data.features.forEach(sensor => {
                if ("weight" in sensor.properties) {
                    heat_data.push({
                        location: new google.maps.LatLng(sensor.geometry.coordinates[0], sensor.geometry.coordinates[1]),
                        weight: sensor.properties.weight
                    });
                }
            });

            set_heatmap1(heat_data, gradient, 0.5, false, 12, sensor_gmap);
            if (heat_data.length != 0) { zoom_changed_event_main1(sensor_gmap); }
        } else {
            if (heatmap1) { delete_heatmap1(); }
        }
        sensor_lmap.spin(false);

    }))
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */


/** ------------------------ FORECAST CLICK - BOTH MAPS ------------------------ */
$("#forecast_button").click(function () {
    $("#forecast").hide();
    $("#today").show();
    $('#time_alert1').hide();

    /** LEAFLET MAP */
    sensor_lmap.spin(true);
    fetch('/api/Home/sensor_maps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                "request_data": {
                    "time_interval": 1,
                    "utc_offset": utc_offset,
                    "allergens": [],
                    "map_type": "leaflet"
                }
            }
        ),
    })
        .then((response) => { return response.json(); })
        .then((marketsData) => {

            if (geojson_markets1) { geojson_markets1.remove() }

            geojson_markets1 = L.geoJSON(marketsData.data, {
                style: markets_style1
            }).addTo(sensor_lmap); // Add markets to map

            fetch('/api/Home/us_states')
                .then((response) => { return response.json(); })
                .then((statesData) => {

                    if (geojson_states1) { geojson_states1.remove() }

                    geojson_states1 = L.geoJson(statesData, {
                        style: states_style1,
                        onEachFeature: onEachFeature1
                    }).addTo(sensor_lmap); // Add states to map

                    if (time_interval_leg1) { time_interval_leg1.remove(); }
                    update_basic_legend1(2, sensor_lmap);

                })
                .catch((error) => { console.error('Error:', error); });
        })
        .catch((error) => { console.error('Error:', error); });
    /** -------------------------------------------------------- */


    /** GOOGLE MAP */
    // enable_loader1(sensor_gmap)
    fetch('/api/Home/sensor_maps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                "request_data": {
                    "time_interval": 1,
                    "utc_offset": utc_offset,
                    "allergens": [],
                    "map_type": "google"
                }
            }
        ),
    })
        .then((response) => { return response.json(); })
        .then((data => {
            if (data != false) {
                heat_data = [];
                data.features.forEach(sensor => {
                    if ("weight" in sensor.properties) {
                        heat_data.push({
                            location: new google.maps.LatLng(sensor.geometry.coordinates[0], sensor.geometry.coordinates[1]),
                            weight: sensor.properties.weight
                        });
                    }
                });

                if (heatmap1) { delete_heatmap1() }
                set_heatmap1(heat_data, gradient, 0.5, false, 12, sensor_gmap);
                delete_zoom_listener1();
                zoom_changed_event_main1(sensor_gmap);
            } else {
                if (heatmap1) { delete_heatmap1() }
                delete_zoom_listener1();
            }
            // if (line1) {disable_loader1()}
            sensor_lmap.spin(false);

        }))
        .catch((error) => { console.error('Error:', error); });
    /** -------------------------------------------------------------------- */
});


/** -------------------------- TODAY CLICK - BOTH MAPS -------------------------- */
$("#today_button").click(function () {
    $("#forecast").show();
    $("#today").hide();
    $('#time_alert1').hide();

    /** LEAFLET MAP */
    sensor_lmap.spin(true);
    fetch('/api/Home/sensor_maps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                "request_data": {
                    "time_interval": 0,
                    "utc_offset": utc_offset,
                    "allergens": [],
                    "map_type": "leaflet"
                }
            }
        ),
    })
        .then((response) => { return response.json(); })
        .then((marketsData) => {

            if (geojson_markets1) { geojson_markets1.remove() }

            geojson_markets1 = L.geoJSON(marketsData.data, {
                style: markets_style1
            }).addTo(sensor_lmap); // Add markets to map

            fetch('/api/Home/us_states')
                .then((response) => { return response.json(); })
                .then((statesData) => {

                    if (geojson_states1) { geojson_states1.remove() }

                    geojson_states1 = L.geoJson(statesData, {
                        style: states_style1,
                        onEachFeature: onEachFeature1
                    }).addTo(sensor_lmap); // Add states to map

                    if (time_interval_leg1) { time_interval_leg1.remove(); }
                    update_basic_legend1(1, sensor_lmap);

                })
                .catch((error) => { console.error('Error:', error); });
        })
        .catch((error) => { console.error('Error:', error); });
    /** -------------------------------------------------------- */


    /** GOOGLE MAP */
    // enable_loader1(sensor_gmap)
    fetch('/api/Home/sensor_maps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                "request_data": {
                    "time_interval": 0,
                    "utc_offset": utc_offset,
                    "allergens": [],
                    "map_type": "google"
                }
            }
        ),
    })
        .then((response) => { return response.json(); })
        .then((data => {
            if (data != false) {
                heat_data = [];
                data.features.forEach(sensor => {
                    if ("weight" in sensor.properties) {
                        heat_data.push({
                            location: new google.maps.LatLng(sensor.geometry.coordinates[0], sensor.geometry.coordinates[1]),
                            weight: sensor.properties.weight
                        });
                    }
                });
                // console.log('[DEBUG]');
                // console.log('Gathered data: ', heat_data);
                // console.log('[END]');

                if (heatmap1) { delete_heatmap1() }
                set_heatmap1(heat_data, gradient, 0.5, false, 12, sensor_gmap);
                delete_zoom_listener1();
                zoom_changed_event_main1(sensor_gmap);
            } else {
                if (heatmap1) { delete_heatmap1() }
                delete_zoom_listener1();
            }
            // if (line1) {disable_loader1()}
            sensor_lmap.spin(false);

        }))
        .catch((error) => { console.error('Error:', error); });
    /** -------------------------------------------------------------------- */
});


/** ------------------------ ALLERGY SEARCH - BOTH MAPS ------------------------ */
var selected_time1, selected_allergens1 = [];

// Clear chooce form
$("#clear_chooce1").click(function (event) {
    selected_time1 = 0;
    selected_allergens1 = [];
    $('#time_picker1').prop('selectedIndex', 0);
    $('#time_reminder1').show();
    $('#sensor_map_allergens input[type=checkbox]').prop('checked', false);
});

// Retrieve time interval
$('#time_picker1').on('change', function () {
    selected_time1 = parseInt($("#time_picker1").val());
    if (selected_time1 == 0) {
        $('#time_reminder1').show();
    } else {
        $('#time_reminder1').hide();
    }
});


// SUBMIT CHOSEN FORM
$("#submit_allergy_search1").click(function (event) {

    // Retrieve allergens
    var allergens1 = $('#sensor_map_allergens :checkbox:checked').map(function() {
        return $(this).val();
    });
    selected_allergens1 = Object.values(allergens1);
    selected_allergens1.pop(2);
    selected_allergens1.pop(1);

    // console.log(selected_time1, selected_allergens1);
    if (selected_time1) {
        $('#time_alert1').hide();

        /** LEAFLET MAP */
        sensor_lmap.spin(true);
        fetch('/api/Home/sensor_maps', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    "request_data": {
                        "time_interval": selected_time1,
                        "utc_offset": utc_offset,
                        "allergens": selected_allergens1,
                        "map_type": "leaflet"
                    }
                }
            ),
        })
            .then((response) => { return response.json(); })
            .then((marketsData) => {

                if (geojson_markets1) { geojson_markets1.remove() }

                geojson_markets1 = L.geoJSON(marketsData.data, {
                    style: markets_style1
                }).addTo(sensor_lmap); // Add markets to map

                fetch('/api/Home/us_states')
                    .then((response) => { return response.json(); })
                    .then((statesData) => {

                        if (geojson_states1) { geojson_states1.remove() }

                        geojson_states1 = L.geoJson(statesData, {
                            style: states_style1,
                            onEachFeature: onEachFeature1
                        }).addTo(sensor_lmap); // Add states to map                            

                        // Legends controls
                        if (day_leg1) { day_leg1.remove(); }
                        if (time_interval_leg1) { time_interval_leg1.remove(); }

                        if (selected_allergens1 != 0) { // If allergens have been selected

                            if (marketsData.message == 'No areas found for selected allergens.') {
                                search_legend1(selected_time1, marketsData.message, sensor_lmap);
                            } else {
                                search_legend1(selected_time1, '', sensor_lmap);
                            }
                        } else {
                            search_legend1(selected_time1, '', sensor_lmap);
                        }
                        // -------------------------

                        // Clear search form
                        selected_time1 = 0;
                        selected_allergens1 = [];
                        $('#time_picker1').prop('selectedIndex', 0);
                        $('#time_reminder1').show();
                        $('#sensor_map_allergens input[type=checkbox]').prop('checked', false);

                    })
                    .catch((error) => { console.error('Error:', error); });
            })
            .catch((error) => { console.error('Error:', error); });
        /** ----------------------------------------------------------- */

        /** GOOGLE MAP */
        // enable_loader1(sensor_gmap)
        fetch('/api/Home/sensor_maps', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    "request_data": {
                        "time_interval": selected_time1,
                        "utc_offset": utc_offset,
                        "allergens": selected_allergens1,
                        "map_type": "google"
                    }
                }
            ),
        })
            .then((response) => { return response.json(); })
            .then((data => {
                if (data != false) {
                    heat_data = [];
                    data.features.forEach(sensor => {
                        if ("weight" in sensor.properties) {
                            heat_data.push({
                                location: new google.maps.LatLng(sensor.geometry.coordinates[0], sensor.geometry.coordinates[1]),
                                weight: sensor.properties.weight
                            });
                        }
                    });

                    if (heatmap1) { delete_heatmap1() }
                    set_heatmap1(heat_data, gradient, 0.5, false, 12, sensor_gmap);
                    delete_zoom_listener1();
                    zoom_changed_event_main1(sensor_gmap);
                } else {
                    if (heatmap1) { delete_heatmap1() }
                    delete_zoom_listener1();
                }
                // if (line1) {disable_loader1()}
                sensor_lmap.spin(false);

            }))
            .catch((error) => { console.error('Error:', error); });
        /** ----------------------------------------------------------- */

    } else {

        selected_time1 = 0;
        selected_allergens1 = [];
        $('#time_picker1').prop('selectedIndex', 0);
        $('#sensor_map_allergens input[type=checkbox]').prop('checked', false);
        $('#time_reminder1').show();
        $('#time_alert1').show();
    }
});
/** ----------------------------------------------------------- */