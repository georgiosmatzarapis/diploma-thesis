/** ---------------------------- STYLES ---------------------------- */

// LEGENDS
var legend1, button1, day_leg1, time_interval_leg1;

/** Adds checkbox. */
function hide_button1(my_map) {
    button1 = L.control({ position: 'topleft' });

    button1.onAdd = function (map) {
        var div = L.DomUtil.create('div');

        div.innerHTML = '<button type="button" style="padding: 5px 12px;" class="btn btn-blue-grey btn-sm curved_edge_button" \
                         id="hide_color_guide1">Show guide</button>';

        return div;
    };
    button1.addTo(my_map);
}

/** Adds color guide. */
function color_guide_legend1(my_map) {
    legend1 = L.control({ position: 'bottomleft' });

    legend1.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info_guide1 legend'),
            grades = ["(0-2.4)", "(2.5-4.8)", "(4.9-7.2)", "(7.3-9.6)", "(9.7-12)", ""],
            colors = ["#82CC31", "#A2FF3D", "#FFFF1A", "#FFAF13", "#FF231A", '#A93EAB'],
            labels = ["Low", "Low-Medium", "Medium", "Medium-High", "High", "No data"];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += '<i style="background:' + colors[i] + '"></i> ' + labels[i] + ' ' + grades[i] + "<br>";
        }

        return div;
    };

    return legend1.addTo(my_map);
}

day_leg1 = L.control({ position: 'topright' });
day_leg1.onAdd = function (my_map) {
    this._div = L.DomUtil.create('div', 'info legend');
    this.update();
    return this._div;
};
/** Updates legend about basic time interval. */
function update_basic_legend1(leg_type, my_map) {
    day_leg1.update = function () {
        this._div.innerHTML = (leg_type == 1 ?
            "<h6><strong style='font-weight: bold;'>Today</strong></h6>"
            : "<h6><strong style='font-weight: bold;'>Tomorrow</strong></h6>");
    };

    return day_leg1.addTo(my_map);
}

/** Adds chosen time interval to map. */
function search_legend1(time, text, my_map) {
    var time_display;
    time_interval_leg1 = L.control({ position: 'topright' });

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

    time_interval_leg1.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        if (text == '') {
            div.innerHTML = "<b>Time interval: </b>" + time_display;
            return div;
        } else {
            div.innerHTML = "<b>Time interval: </b>" + time_display + '<br>' + text;
            return div;
        }

    };

    return time_interval_leg1.addTo(my_map);
}


/** Sets colors. */
function getColor1(d) {

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
function markets_style1(feature) {
    return {
        fillColor: getColor1(feature.properties.density),
        fillOpacity: .6,
        weight: 1.5,
        opacity: .5,
        color: getColor1(feature.properties.density),
        stroke: true
    };
}

/** Config style for states. */
function states_style1() {
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
function highlightFeature1(e) {
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
function resetHighlightMarkets1(n) {
    geojson_markets1.resetStyle(n.target);
}

/** Resets highlight state. */
function resetHighlightStates1(n) {
    geojson_states1.resetStyle(n.target);
}

/** Zooms to state. */
function zoomToFeature1(n) {
    sensor_lmap.fitBounds(n.target.getBounds());
}

/** Adds listeners to state layer. */
function onEachFeature1(feature, layer) {
    layer.on({
        mouseover: highlightFeature1,
        mouseout: resetHighlightMarkets1,
        mouseout: resetHighlightStates1,
        click: zoomToFeature1
    });
}
// End Listeners to states