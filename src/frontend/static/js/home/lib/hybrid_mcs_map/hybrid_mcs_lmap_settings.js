/** ---------------------------- STYLES ---------------------------- */

// LEGENDS
var today_leg3, time_interval_leg3, legend3, button3;

/** Adds checkbox. */
function hide_button3(my_map) {
    button3 = L.control({ position: 'topleft' });

    button3.onAdd = function (map) {
        var div = L.DomUtil.create('div');

        div.innerHTML = '<button type="button" style="padding: 5px 12px;" class="btn btn-blue-grey btn-sm curved_edge_button" \
                         id="hide_color_guide3">Show guide</button>';

        return div;
    };
    button3.addTo(my_map);
}

/** Adds color guide. */
function color_guide_legend3(my_map) {
    legend3 = L.control({ position: 'bottomleft' });

    legend3.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info_guide3 legend'),
            grades = ["(0-2.4)", "(2.5-4.8)", "(4.9-7.2)", "(7.3-9.6)", "(9.7-12)", ""],
            colors = ["#82CC31", "#A2FF3D", "#FFFF1A", "#FFAF13", "#FF231A", '#A93EAB'],
            labels = ["Low", "Low-Medium", "Medium", "Medium-High", "High", "No data"];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += '<i style="background:' + colors[i] + '"></i> ' + labels[i] + ' ' + grades[i] + "<br>";
        }

        return div;
    };

    return legend3.addTo(my_map);
}

/** Adds forecast day legend. */
function today_legend3(my_map) {
    today_leg3 = L.control({ position: 'topright' });

    today_leg3.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML = "<h6><strong style='font-weight: bold;'>Today</strong></h6>";
        return div;
    };

    return today_leg3.addTo(my_map);
}

/** Adds chosen time interval to map. */
function search_legend3(time, text, my_map) {
    var time_display;
    time_interval_leg3 = L.control({ position: 'topright' });

    switch (time) {
        case 30:
            time_display = '30 minutes'
            break;
        case 60:
            time_display = '1 hour'
            break;
        case 180:
            time_display = '3 hours'
            break;
        case 720:
            time_display = '12 hours'
            break;
        case 1440:
            time_display = '24 hours'
            break;
        case 4320:
            time_display = '3 days'
            break;
        case 10080:
            time_display = '1 week'
            break;
    }

    time_interval_leg3.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        if (text == '') {
            div.innerHTML = "<b>Time interval: </b>" + time_display;
            return div;
        } else {
            div.innerHTML = "<b>Time interval: </b>" + time_display + '<br>' + text;
            return div;
        }

    };

    return time_interval_leg3.addTo(my_map);
}


/** Sets colors. */
function getColor3(d) {

    if (d >= 0 && d <= 2.4) {
        return '#82CC31'
    } else if (d >= 2.5 && d <= 4.8) {
        return '#A2FF3D'
    } else if (d >= 4.9 && d <= 7.2) {
        return '#FFFF1A'
    } else if (d >= 7.3 && d <= 9.6) {
        return '#FFAF13'
    } else if (d >= 9.7 && d <= 12) {
        return '#FF231A'
    } else if (d == 100) { // This values means that there is no density for these area
        return '#A93EAB'
    }
}

/** Config style for us markets. */
function markets_style3(feature) {
    return {
        fillColor: getColor3(feature.properties.density),
        fillOpacity: .6,
        weight: 1,
        opacity: .5,
        color: getColor3(feature.properties.density),
        stroke: true
    };
}

/** Config style for states. */
function states_style3() {
    return {
        color: "#595959",
        weight: 1.5,
        opacity: .8,
        fillOpacity: 0,
        dashArray: '3',
        stroke: true
    };
}


/** ---------------------------- LISTENERS ---------------------------- */
/** Highlights state. */
function highlightFeature3(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 3,
        opacity: .7,
        dashArray: "",
        stroke: true
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

/** Resets highlight market. */
function resetHighlightMarkets3(n) {
    geojson_markets3.resetStyle(n.target);
}

/** Resets highlight state. */
function resetHighlightStates3(n) {
    geojson_states3.resetStyle(n.target);
}

/** Zooms to state. */
function zoomToFeature3(n) {
    hybrid_lmap.fitBounds(n.target.getBounds());
}

/** Adds listeners to state layer. */
function onEachFeature3(feature, layer) {
    layer.on({
        mouseover: highlightFeature3,
        mouseout: resetHighlightMarkets3,
        mouseout: resetHighlightStates3,
        click: zoomToFeature3
    });
}
// End Listeners to states