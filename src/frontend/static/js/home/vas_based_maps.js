// Init lmap
var leaflet_map_tile = $("#leaflet_map_tile").val();
var vas_lmap = L.map('main_lmap2', {scrollWheelZoom: false}).setView([38.1, -96], 4);
var geojson_markets2, geojson_states2;

L.tileLayer(leaflet_map_tile, {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    minZoom: 4,
    maxZoom: 8,
    tileSize: 512,
    zoomOffset: -1
}).addTo(vas_lmap);
vas_lmap.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(vas_lmap);
// -------------------

/** Button for hide color guide */
hide_button2(vas_lmap);
$('#hide_color_guide2').click(function () {

    if ($('#hide_color_guide2').text() == 'Show guide') {
        color_guide_legend2(vas_lmap); // Add color guide on map
        $("#hide_color_guide2").text("Hide guide");
    } else if (($('#hide_color_guide2').text() == 'Hide guide')) {
        if (legend2) { legend2.remove() }
        $("#hide_color_guide2").text("Show guide");
    }

});
/** -------------------------- */


/** ---------------------------- DEFAUL LEAFLET MAP---------------------------- */
var d = new Date().getTimezoneOffset();
var utc_offset = -(d / 60);

vas_lmap.spin(true);
fetch('/api/Home/vas_maps', {
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
        geojson_markets2 = L.geoJSON(marketsData.data, {
            style: markets_style2
        }).addTo(vas_lmap); // Add markets to map

        fetch('/api/Home/us_states')
            .then((response) => { return response.json(); })
            .then((statesData) => {
                geojson_states2 = L.geoJson(statesData, {
                    style: states_style2,
                    onEachFeature: onEachFeature2
                }).addTo(vas_lmap); // Add states to map

                today_legend2(vas_lmap);
            })
            .catch((error) => { console.error('Error:', error); });

    })
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */


/** ----------------------------- DEFAUL GOOGLE MAP----------------------------- */
fetch('/api/Home/vas_maps', {
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

            set_heatmap2(heat_data, gradient, 0.5, false, 12, vas_gmap);
            if (heat_data.length != 0) { zoom_changed_event_main2(vas_gmap); }
        } else {
            if (heatmap2) { delete_heatmap2() }
        }
        vas_lmap.spin(false);
    }))
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */


/** ------------------------ ALLERGY SEARCH - BOTH MAPS ------------------------ */
var selected_time2, selected_allergens2 = [];

// Clear chooce form
$("#clear_chooce2").click(function (event) {
    selected_time2 = 0;
    selected_allergens2 = [];
    $('#time_picker2').prop('selectedIndex', 0);
    $('#time_reminder2').show();
    $('#mcs_map_allergens input[type=checkbox]').prop('checked', false);
});

// Retrieve time interval
$('#time_picker2').on('change', function () {
    selected_time2 = parseInt($("#time_picker2").val());
    if (selected_time2 == 0) {
        $('#time_reminder2').show();
    } else {
        $('#time_reminder2').hide();
    }
});


// SUBMIT CHOSEN FORM
$("#submit_allergy_search2").click(function (event) {

    // Retrieve allergens
    var allergens2 = $('#mcs_map_allergens :checkbox:checked').map(function () {
        return $(this).val();
    });
    selected_allergens2 = Object.values(allergens2);
    selected_allergens2.pop(2);
    selected_allergens2.pop(1);

    // console.log(selected_time2, selected_allergens2);
    if (selected_time2) {
        $('#time_alert2').hide();

        /** LEAFLET MAP */
        vas_lmap.spin(true);
        fetch('/api/Home/vas_maps', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    "request_data": {
                        "time_interval": selected_time2,
                        "utc_offset": utc_offset,
                        "allergens": selected_allergens2,
                        "map_type": "leaflet"
                    }
                }
            ),
        })
            .then((response) => { return response.json(); })
            .then((marketsData) => {

                if (geojson_markets2) { geojson_markets2.remove() }

                geojson_markets2 = L.geoJSON(marketsData.data, {
                    style: markets_style2
                }).addTo(vas_lmap); // Add markets to map

                fetch('/api/Home/us_states')
                    .then((response) => { return response.json(); })
                    .then((statesData) => {

                        if (geojson_states2) { geojson_states2.remove() }

                        geojson_states2 = L.geoJson(statesData, {
                            style: states_style2,
                            onEachFeature: onEachFeature2
                        }).addTo(vas_lmap); // Add states to map                            

                        // Legens controls
                        if (today_leg2) { today_leg2.remove(); }
                        if (time_interval_leg2) { time_interval_leg2.remove(); }

                        if (selected_allergens2 != 0) { // If allergens has been selected

                            if (marketsData.message == 'No areas found for selected allergens.') {
                                search_legend2(selected_time2, marketsData.message, vas_lmap);
                            } else {
                                search_legend2(selected_time2, '', vas_lmap);
                            }
                        } else {
                            search_legend2(selected_time2, '', vas_lmap);
                        }
                        // -------------------------

                        // Clear search form
                        selected_time2 = 0;
                        selected_allergens2 = [];
                        $('#time_picker2').prop('selectedIndex', 0);
                        $('#time_reminder2').show();
                        $('#mcs_map_allergens input[type=checkbox]').prop('checked', false);

                    })
                    .catch((error) => { console.error('Error:', error); });
            })
            .catch((error) => { console.error('Error:', error); });
        /** ----------------------------------------------------------- */

        /** GOOGLE MAP */
        // enable_loader2(vas_gmap)
        fetch('/api/Home/vas_maps', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    "request_data": {
                        "time_interval": selected_time2,
                        "utc_offset": utc_offset,
                        "allergens": selected_allergens2,
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

                    if (heatmap2) { delete_heatmap2() }
                    set_heatmap2(heat_data, gradient, 0.5, false, 12, vas_gmap);
                    delete_zoom_listener2();
                    if (heat_data.length != 0) { zoom_changed_event_main2(vas_gmap); }
                } else {
                    if (heatmap2) { delete_heatmap2() }
                    delete_zoom_listener2();
                }
                // if (line2) { disable_loader2() }
                vas_lmap.spin(false);

            }))
            .catch((error) => { console.error('Error:', error); });
        /** ----------------------------------------------------------- */

    } else {

        selected_time2 = 0;
        selected_allergens2 = [];
        $('#time_picker2').prop('selectedIndex', 0);
        $('#mcs_map_allergens input[type=checkbox]').prop('checked', false);
        $('#time_reminder2').show();
        $('#time_alert2').show();
    }
});
/** ----------------------------------------------------------- */