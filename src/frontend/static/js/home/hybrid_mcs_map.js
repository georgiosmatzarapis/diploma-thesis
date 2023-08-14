// Init lmap
var leaflet_map_tile = $("#leaflet_map_tile").val();
var hybrid_lmap = L.map('main_lmap3', {scrollWheelZoom: false}).setView([38.1, -96], 4);
var geojson_markets3, geojson_states3;

L.tileLayer(leaflet_map_tile, {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    minZoom: 4,
    maxZoom: 8,
    tileSize: 512,
    zoomOffset: -1
}).addTo(hybrid_lmap);
hybrid_lmap.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(hybrid_lmap);
// -------------------

/** Button for hide color guide */
hide_button3(hybrid_lmap);
$('#hide_color_guide3').click(function () {

    if ($('#hide_color_guide3').text() == 'Show guide') {
        color_guide_legend3(hybrid_lmap); // Add color guide on map
        $("#hide_color_guide3").text("Hide guide");
    } else if (($('#hide_color_guide3').text() == 'Hide guide')) {
        if (legend3) { legend3.remove() }
        $("#hide_color_guide3").text("Show guide");
    }

});
/** -------------------------- */


/** ---------------------------- DEFAUL LEAFLET MAP---------------------------- */
var d = new Date().getTimezoneOffset();
var utc_offset = -(d/60);

hybrid_lmap.spin(true);
fetch('/api/Home/hybrid_mcs_map', {
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

        geojson_markets3 = L.geoJSON(marketsData.data, {
            style: markets_style3
        }).addTo(hybrid_lmap); // Add markets to map

        fetch('/api/Home/us_states')
            .then((response) => { return response.json(); })
            .then((statesData) => {
                geojson_states3 = L.geoJson(statesData, {
                    style: states_style3,
                    onEachFeature: onEachFeature3
                }).addTo(hybrid_lmap); // Add states to map

                today_legend3(hybrid_lmap);
                hybrid_lmap.spin(false);

            })
            .catch((error) => { console.error('Error:', error); });

    })
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */


/** ------------------------ ALLERGY SEARCH ------------------------ */
var selected_time3, selected_allergens3 = [];

// Clear chooce form
$("#clear_chooce3").click(function (event) {
    selected_time3 = 0;
    selected_allergens3 = [];
    $('#time_picker3').prop('selectedIndex', 0);
    $('#time_reminder3').show();
    $('#hybrid_mcs_map_allergens input[type=checkbox]').prop('checked', false);
});

// Retrieve time interval
$('#time_picker3').on('change', function () {
    selected_time3 = parseInt($("#time_picker3").val());
    if (selected_time3 == 0) {
        $('#time_reminder3').show();
    } else {
        $('#time_reminder3').hide();
    }
});


// SUBMIT CHOSEN FORM
$("#submit_allergy_search3").click(function (event) {

    // Retrieve allergens
    var allergens3 = $('#hybrid_mcs_map_allergens :checkbox:checked').map(function() {
        return $(this).val();
    });
    selected_allergens3 = Object.values(allergens3);
    selected_allergens3.pop(2);
    selected_allergens3.pop(1);

    // console.log(selected_time3, selected_allergens3);
    if (selected_time3) {
        $('#time_alert3').hide();
        
        /** LEAFLET MAP */
        hybrid_lmap.spin(true);
        fetch('/api/Home/hybrid_mcs_map', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    "request_data": {
                        "time_interval": selected_time3,
                        "utc_offset": utc_offset,
                        "allergens": selected_allergens3,
                        "map_type": "leaflet"
                    }
                }
            ),
        })
            .then((response) => { return response.json(); })
            .then((marketsData) => {

                if (geojson_markets3) { geojson_markets3.remove() }

                geojson_markets3 = L.geoJSON(marketsData.data, {
                    style: markets_style3
                }).addTo(hybrid_lmap); // Add markets to map

                fetch('/api/Home/us_states')
                    .then((response) => { return response.json(); })
                    .then((statesData) => {

                        if (geojson_states3) { geojson_states3.remove() }
                        
                        geojson_states3 = L.geoJson(statesData, {
                            style: states_style3,
                            onEachFeature: onEachFeature3
                        }).addTo(hybrid_lmap); // Add states to map                            

                        // Legens controls
                        if (today_leg3) { today_leg3.remove(); }
                        if (time_interval_leg3) { time_interval_leg3.remove(); }

                        if (selected_allergens3 != 0) { // If allergens has been selected

                            if (marketsData.message == 'No areas found for selected allergens.') {
                                search_legend3(selected_time3, marketsData.message, hybrid_lmap);
                            } else {
                                search_legend3(selected_time3, '', hybrid_lmap);
                            }
                        } else {
                            search_legend3(selected_time3, '', hybrid_lmap);
                        }
                        hybrid_lmap.spin(false);
                        // -------------------------

                        // Clear search form
                        selected_time3 = 0;
                        selected_allergens3 = [];
                        $('#time_picker3').prop('selectedIndex', 0);
                        $('#time_reminder3').show();
                        $('#hybrid_mcs_map_allergens input[type=checkbox]').prop('checked', false);

                    })
                    .catch((error) => { console.error('Error:', error); });
            })
            .catch((error) => { console.error('Error:', error); });

    } else {

        selected_time3 = 0;
        selected_allergens3 = [];
        $('#time_picker3').prop('selectedIndex', 0);
        $('#hybrid_mcs_map_allergens input[type=checkbox]').prop('checked', false);
        $('#time_reminder3').show();
        $('#time_alert3').show();
    }
});
