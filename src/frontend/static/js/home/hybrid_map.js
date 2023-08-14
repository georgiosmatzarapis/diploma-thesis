// Init lmap
var leaflet_map_tile = $("#leaflet_map_tile").val();
var hybrid_lmap2 = L.map('main_lmap4', {scrollWheelZoom: false}).setView([38.1, -96], 4);
var geojson_markets6, geojson_states6;

L.tileLayer(leaflet_map_tile, {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    minZoom: 4,
    maxZoom: 8,
    tileSize: 512,
    zoomOffset: -1
}).addTo(hybrid_lmap2);
hybrid_lmap2.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(hybrid_lmap2);
// -------------------

/** Button for hide color guide */
hide_button6(hybrid_lmap2);
$('#hide_color_guide6').click(function () {

    if ($('#hide_color_guide6').text() == 'Show guide') {
        color_guide_legend6(hybrid_lmap2); // Add color guide on map
        $("#hide_color_guide6").text("Hide guide");
    } else if (($('#hide_color_guide6').text() == 'Hide guide')) {
        if (legend6) { legend6.remove() }
        $("#hide_color_guide6").text("Show guide");
    }

});
/** -------------------------- */


/** ---------------------------- DEFAUL LEAFLET MAP---------------------------- */
var d = new Date().getTimezoneOffset();
var utc_offset = -(d/60);

hybrid_lmap2.spin(true);
fetch('/api/Home/hybrid_map', {
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

        geojson_markets6 = L.geoJSON(marketsData.data, {
            style: markets_style6
        }).addTo(hybrid_lmap2); // Add markets to map

        fetch('/api/Home/us_states')
            .then((response) => { return response.json(); })
            .then((statesData) => {
                geojson_states6 = L.geoJson(statesData, {
                    style: states_style6,
                    onEachFeature: onEachFeature6
                }).addTo(hybrid_lmap2); // Add states to map

                today_legend6(hybrid_lmap2);
                hybrid_lmap2.spin(false);

            })
            .catch((error) => { console.error('Error:', error); });

    })
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */


/** ------------------------ ALLERGY SEARCH ------------------------ */
var selected_time4, selected_allergens4 = [];

// Clear chooce form
$("#clear_chooce4").click(function (event) {
    selected_time4 = 0;
    selected_allergens4 = [];
    $('#time_picker4').prop('selectedIndex', 0);
    $('#time_reminder4').show();
    $('#hybrid_map_allergens input[type=checkbox]').prop('checked', false);
});

// Retrieve time interval
$('#time_picker4').on('change', function () {
    selected_time4 = parseInt($("#time_picker4").val());
    if (selected_time4 == 0) {
        $('#time_reminder4').show();
    } else {
        $('#time_reminder4').hide();
    }
});

// SUBMIT CHOSEN FORM
$("#submit_allergy_search4").click(function (event) {

    // Retrieve allergens
    var allergens4 = $('#hybrid_map_allergens :checkbox:checked').map(function() {
        return $(this).val();
    });
    selected_allergens4 = Object.values(allergens4);
    selected_allergens4.pop(2);
    selected_allergens4.pop(1);

    // console.log(selected_time4, selected_allergens4);
    if (selected_time4) {
        $('#time_alert4').hide();

        /** LEAFLET MAP */
        hybrid_lmap2.spin(true);
        fetch('/api/Home/hybrid_map', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    "request_data": {
                        "time_interval": selected_time4,
                        "utc_offset": utc_offset,
                        "allergens": selected_allergens4,
                        "map_type": "leaflet"
                    }
                }
            ),
        })
            .then((response) => { return response.json(); })
            .then((marketsData) => {

                if (geojson_markets6) { geojson_markets6.remove() }

                geojson_markets6 = L.geoJSON(marketsData.data, {
                    style: markets_style6
                }).addTo(hybrid_lmap2); // Add markets to map

                fetch('/api/Home/us_states')
                    .then((response) => { return response.json(); })
                    .then((statesData) => {

                        if (geojson_states6) { geojson_states6.remove() }

                        geojson_states6 = L.geoJson(statesData, {
                            style: states_style6,
                            onEachFeature: onEachFeature6
                        }).addTo(hybrid_lmap2); // Add states to map                            

                        // Legens controls
                        if (today_leg6) { today_leg6.remove(); }
                        if (time_interval_leg6) { time_interval_leg6.remove(); }

                        if (selected_allergens4 != 0) { // If allergens has been selected

                            if (marketsData.message == 'No areas found for selected allergens.') {
                                search_legend6(selected_time4, marketsData.message, hybrid_lmap2);
                            } else {
                                search_legend6(selected_time4, '', hybrid_lmap2);
                            }
                        } else {
                            search_legend6(selected_time4, '', hybrid_lmap2);
                        }
                        hybrid_lmap2.spin(false);
                        // -------------------------

                        // Clear search form
                        selected_time4 = 0;
                        selected_allergens4 = [];
                        $('#time_picker4').prop('selectedIndex', 0);
                        $('#time_reminder4').show();
                        $('#hybrid_map_allergens input[type=checkbox]').prop('checked', false);

                    })
                    .catch((error) => { console.error('Error:', error); });
            })
            .catch((error) => { console.error('Error:', error); });

    } else {

        selected_time4 = 0;
        selected_allergens4 = [];
        $('#time_picker4').prop('selectedIndex', 0);
        $('#hybrid_map_allergens input[type=checkbox]').prop('checked', false);
        $('#time_reminder4').show();
        $('#time_alert4').show();
    }
});
