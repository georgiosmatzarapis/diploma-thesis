// Init lmap
var leaflet_map_tile = $("#leaflet_map_tile").val();
var twitter_lmap = L.map('twitter_lmap', {scrollWheelZoom: false}).setView([38.1, -95], 4);
var geojson_states5;

L.tileLayer(leaflet_map_tile, {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    minZoom: 4,
    maxZoom: 8,
    tileSize: 512,
    zoomOffset: -1
}).addTo(twitter_lmap);

// Zoom control position
twitter_lmap.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(twitter_lmap);
// -------------------

/** Button for hide color guide */
hide_button5(twitter_lmap);
$('#hide_color_guide5').click(function () {

    if ($('#hide_color_guide5').text() == 'Show guide') {
        color_guide_legend5(twitter_lmap); // Add color guide on map
        $("#hide_color_guide5").text("Hide guide");
    } else if (($('#hide_color_guide5').text() == 'Hide guide')) {
        if (legend5) { legend5.remove(); }
        $("#hide_color_guide5").text("Show guide");
    }

});
/** -------------------------- */

/** ---------------------------- DEFAUL LEAFLET MAP---------------------------- */
$('#twitter_time_picker').val(0);
var max_state_tweets = [];
var max_tweet = 0;
var color_index = 0;
var color_spaces = [];
var d = new Date().getTimezoneOffset();
var utc_offset = -(d/60);

twitter_lmap.spin(true);
fetch('/api/Home/twitter/' + 0 + '/' + utc_offset)
    .then((response) => { return response.json(); })
    .then((statesData) => {

        // create list with valid tweets of the states
        statesData.features.forEach(element => {
            if (element.properties.tweets != '-') {
                max_state_tweets.push(element.properties.tweets)
            }
        });

        if (max_state_tweets.length != 0) {

            max_tweet = Math.max.apply(null, max_state_tweets)
            color_index = max_tweet / 5

            var s1 = 0;
            var s2 = s1 + color_index;
            var s3 = s2 + 0.1;
            var s4 = s3 + color_index;
            var s5 = s4 + 0.1;
            var s6 = s5 + color_index;
            var s7 = s6 + 0.1;
            var s8 = s7 + color_index;
            var s9 = s8 + 0.1;
            var s10 = s9 + color_index;
            color_spaces.push(Math.round((s1 + Number.EPSILON) * 100) / 100,
                                  Math.round((s2 + Number.EPSILON) * 100) / 100,
                                  Math.round((s3 + Number.EPSILON) * 100) / 100,
                                  Math.round((s4 + Number.EPSILON) * 100) / 100,
                                  Math.round((s5 + Number.EPSILON) * 100) / 100,
                                  Math.round((s6 + Number.EPSILON) * 100) / 100,
                                  Math.round((s7 + Number.EPSILON) * 100) / 100,
                                  Math.round((s8 + Number.EPSILON) * 100) / 100,
                                  Math.round((s9 + Number.EPSILON) * 100) / 100,
                                  Math.round((s10 + Number.EPSILON) * 100) / 100)
        }

        geojson_states5 = L.geoJson(statesData, {
            style: states_style5,
            onEachFeature: onEachFeature5
        }).addTo(twitter_lmap); // Add states to map

        custom_info(twitter_lmap);
        twitter_lmap.spin(false);

    })
    .catch((error) => { console.error('Error:', error); });
/** ---------------------------------------------------------------------------- */


/** ------------------------------ TIME INTERVAL ------------------------------- */
$('#twitter_time_picker').on('change', function () {

    var minutes = parseInt($('#twitter_time_picker').val());
    max_state_tweets = []
    max_tweet = 0
    color_index = 0
    color_spaces = []

    twitter_lmap.spin(true);
    fetch('/api/Home/twitter/' + minutes + '/' + utc_offset)
        .then((response) => { return response.json(); })
        .then((statesData) => {

            // create list with valid tweets of the states
            statesData.features.forEach(element => {
                if (element.properties.tweets != '-') {
                    max_state_tweets.push(element.properties.tweets)
                }
            });

            if (max_state_tweets.length != 0) {

                max_tweet = Math.max.apply(null, max_state_tweets)
                color_index = max_tweet / 5

                var s1 = 0;
                var s2 = s1 + color_index;
                var s3 = s2 + 0.1;
                var s4 = s3 + color_index;
                var s5 = s4 + 0.1;
                var s6 = s5 + color_index;
                var s7 = s6 + 0.1;
                var s8 = s7 + color_index;
                var s9 = s8 + 0.1;
                var s10 = s9 + color_index;
                color_spaces.push(Math.round((s1 + Number.EPSILON) * 100) / 100,
                                  Math.round((s2 + Number.EPSILON) * 100) / 100,
                                  Math.round((s3 + Number.EPSILON) * 100) / 100,
                                  Math.round((s4 + Number.EPSILON) * 100) / 100,
                                  Math.round((s5 + Number.EPSILON) * 100) / 100,
                                  Math.round((s6 + Number.EPSILON) * 100) / 100,
                                  Math.round((s7 + Number.EPSILON) * 100) / 100,
                                  Math.round((s8 + Number.EPSILON) * 100) / 100,
                                  Math.round((s9 + Number.EPSILON) * 100) / 100,
                                  Math.round((s10 + Number.EPSILON) * 100) / 100)
            }

            if (geojson_states5) { geojson_states5.remove(); }

            geojson_states5 = L.geoJson(statesData, {
                style: states_style5,
                onEachFeature: onEachFeature5
            }).addTo(twitter_lmap);

            twitter_lmap.spin(false);

        })
        .catch((error) => { console.error('Error:', error); });

});