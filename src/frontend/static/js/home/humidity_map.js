// Init lmap
var leaflet_map_tile = $("#leaflet_map_tile").val();
var humidity_lmap = L.map('humidity_lmap', {scrollWheelZoom: false}).setView([38.1, -96], 4);
var geojson_markets4, geojson_states4;

L.tileLayer(leaflet_map_tile, {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    minZoom: 4,
    maxZoom: 8,
    tileSize: 512,
    zoomOffset: -1
}).addTo(humidity_lmap);
// Zoom control position
humidity_lmap.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(humidity_lmap);
// -------------------

/** Button for hide color guide */
hide_button4(humidity_lmap);
$('#hide_color_guide4').click(function () {

    if ($('#hide_color_guide4').text() == 'Show guide') {
        color_guide_legend4(humidity_lmap);
        $("#hide_color_guide4").text("Hide guide");
    } else if (($('#hide_color_guide4').text() == 'Hide guide')) {
        if (legend4) { legend4.remove() }
        $("#hide_color_guide4").text("Show guide");
    }

});
/** -------------------------- */


/** ---------------------------- DEFAUL LEAFLET MAP---------------------------- */
var d = new Date().getTimezoneOffset();
var utc_offset = -(d/60);

humidity_lmap.spin(true);
fetch('/api/Home/humidity/' + 0 + '/' + utc_offset)
    .then((response) => { return response.json(); })
    .then((marketsData) => {

        geojson_markets4 = L.geoJSON(marketsData.market_data, {
            style: markets_style4
        }).addTo(humidity_lmap); // Add markets to map

        fetch('/api/Home/us_states')
            .then((response) => { return response.json(); })
            .then((statesData) => {
                geojson_states4 = L.geoJson(statesData, {
                    style: states_style4,
                    onEachFeature: onEachFeature4
                }).addTo(humidity_lmap); // Add states to map

                update_basic_legend2(1, humidity_lmap);
                humidity_lmap.spin(false);

            })
            .catch((error) => { console.error('Error:', error); });
    })
    .catch((error) => { console.error('Error:', error); });


/** ------------------------ FORECAST CLICK ------------------------- */
$("#humidity_forecast").click(function () {
    $("#forecast2").hide();
    $("#today2").show();

    humidity_lmap.spin(true);
    fetch('/api/Home/humidity/' + 1 + '/' + utc_offset)
        .then((response) => { return response.json(); })
        .then((marketsData) => {

            if (geojson_markets4) { geojson_markets4.remove(); }

            geojson_markets4 = L.geoJSON(marketsData.market_data, {
                style: markets_style4
            }).addTo(humidity_lmap); // Add markets to map

            fetch('/api/Home/us_states')
                .then((response) => { return response.json(); })
                .then((statesData) => {

                    if (geojson_states4) { geojson_states4.remove(); }

                    geojson_states4 = L.geoJson(statesData, {
                        style: states_style4,
                        onEachFeature: onEachFeature4
                    }).addTo(humidity_lmap); // Add states to map

                    if (time_interval_leg4) { time_interval_leg4.remove(); }
                    update_basic_legend2(2, humidity_lmap);
                    humidity_lmap.spin(false);

                })
                .catch((error) => { console.error('Error:', error); });
        })
        .catch((error) => { console.error('Error:', error); });
});


/** -------------------------- TODAY CLICK -------------------------- */
$("#humidity_today").click(function () {
    $("#today2").hide();
    $("#forecast2").show();

    humidity_lmap.spin(true);
    fetch('/api/Home/humidity/' + 0 + '/' + utc_offset)
        .then((response) => { return response.json(); })
        .then((marketsData) => {

            if (geojson_markets4) { geojson_markets4.remove(); }

            geojson_markets4 = L.geoJSON(marketsData.market_data, {
                style: markets_style4
            }).addTo(humidity_lmap); // Add markets to map

            fetch('/api/Home/us_states')
                .then((response) => { return response.json(); })
                .then((statesData) => {

                    if (geojson_states4) { geojson_states4.remove(); }

                    geojson_states4 = L.geoJson(statesData, {
                        style: states_style4,
                        onEachFeature: onEachFeature4
                    }).addTo(humidity_lmap); // Add states to map

                    if (time_interval_leg4) { time_interval_leg4.remove(); }
                    update_basic_legend2(1, humidity_lmap);
                    humidity_lmap.spin(false);

                })
                .catch((error) => { console.error('Error:', error); });
        })
        .catch((error) => { console.error('Error:', error); });
});


/** ------------------------- TIME INTERVAL ------------------------- */
$('#humidity_time_picker').on('change', function () {
    var minutes = parseInt($('#humidity_time_picker').val());
    $('#humidity_time_picker').val(0);
    // console.log(minutes);

    if (minutes != 0) {

        humidity_lmap.spin(true);
        fetch('/api/Home/humidity/' + minutes + '/' + utc_offset)
            .then((response) => { return response.json(); })
            .then((marketsData) => {

                if (geojson_markets4) { geojson_markets4.remove(); }

                geojson_markets4 = L.geoJSON(marketsData.market_data, {
                    style: markets_style4
                }).addTo(humidity_lmap); // Add markets to map

                fetch('/api/Home/us_states')
                    .then((response) => { return response.json(); })
                    .then((statesData) => {

                        if (geojson_states4) { geojson_states4.remove(); }

                        geojson_states4 = L.geoJson(statesData, {
                            style: states_style4,
                            onEachFeature: onEachFeature4
                        }).addTo(humidity_lmap); // Add states to map

                        if (day_leg2) { day_leg2.remove(); }
                        if (time_interval_leg4) { time_interval_leg4.remove(); }
                        search_legend4(minutes, '', humidity_lmap);
                        humidity_lmap.spin(false);

                    })
                    .catch((error) => { console.error('Error:', error); });
            })
            .catch((error) => { console.error('Error:', error); });
    }
});