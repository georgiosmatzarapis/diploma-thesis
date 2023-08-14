/** ---------------------------- STYLES ---------------------------- */

// LEGENDS
var legend4, button4, day_leg2, time_interval_leg4, geojson_markets4, geojson_states4;

/** Adds checkbox. */
function hide_button4(my_map) {
    button4 = L.control({ position: 'topleft' });

    button4.onAdd = function (map) {
        var div = L.DomUtil.create('div');

        div.innerHTML = '<button type="button" style="padding: 5px 12px;" class="btn btn-blue-grey btn-sm curved_edge_button" \
                         id="hide_color_guide4">Show guide</button>';

        return div;
    };
    button4.addTo(my_map);
}

/** Adds color guide. */
function color_guide_legend4(my_map) {
    legend4 = L.control({ position: 'bottomleft' });

    legend4.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info_guide4 legend'),
            grades = ["(0-19)&#37;", "(20-39)&#37;", "(40-59)&#37;", "(60-79)&#37;", "(80-100)&#37;", ""],
            colors = ["#acf3ef", "#64d6cc", "#0d9b8c", "#007987", "#03395e", '#000'],
            labels = ["Low", "Low-Medium", "Medium", "Medium-High", "High", "No data"];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += '<i style="background:' + colors[i] + '"></i> ' + labels[i] + ' ' + grades[i] + "<br>";
        }

        return div;
    };

    return legend4.addTo(my_map);
}

day_leg2 = L.control({ position: 'topright' });
day_leg2.onAdd = function (my_map) {
    this._div = L.DomUtil.create('div', 'info legend');
    this.update();
    return this._div;
};
/** Updates legend about basic time interval. */
function update_basic_legend2(leg_type, my_map) {
    day_leg2.update = function () {
        this._div.innerHTML = (leg_type == 1 ?
            "<h6><strong style='font-weight: bold;'>Today</strong></h6>"
            : "<h6><strong style='font-weight: bold;'>Tomorrow</strong></h6>");
    };

    return day_leg2.addTo(my_map);
}

/** Adds chosen time interval to map. */
function search_legend4(time, text, my_map) {
    var time_display;
    time_interval_leg4 = L.control({ position: 'topright' });

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

    time_interval_leg4.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        if (text == '') {
            div.innerHTML = "<b>Time interval: </b>" + time_display;
            return div;
        } else {
            div.innerHTML = "<b>Time interval: </b>" + time_display + '<br>' + text;
            return div;
        }

    };

    return time_interval_leg4.addTo(my_map);
}


/** Sets colors. */
function getColor4(d) {

    if (d >= 0 && d <= 19) {
        return '#acf3ef'
    } else if (d >= 20 && d <= 39) {
        return '#64d6cc'
    } else if (d >= 40 && d <= 59) {
        return '#0d9b8c'
    } else if (d >= 60 && d <= 79) {
        return '#007987'
    } else if (d >= 80 && d <= 100) {
        return '#03395e'
    } else if (d == 120) { // This values means that there is no density for these area
        return '#000'
    }
}

/** Config style for us markets. */
function markets_style4(feature) {
    return {
        fillColor: getColor4(feature.properties.density),
        fillOpacity: .6,
        weight: 1,
        opacity: .5,
        color: getColor4(feature.properties.density),
        stroke: true
    };
}

/** Config style for states. */
function states_style4() {
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
function highlightFeature4(e) {
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
function resetHighlightMarkets4(n) {
    geojson_markets4.resetStyle(n.target);
}

/** Resets highlight state. */
function resetHighlightStates4(n) {
    geojson_states4.resetStyle(n.target);
}

/** Zooms to state. */
function zoomToFeature4(n) {
    humidity_lmap.fitBounds(n.target.getBounds());
}

/** Adds listeners to state layer. */
function onEachFeature4(feature, layer) {
    layer.on({
        mouseover: highlightFeature4,
        mouseout: resetHighlightMarkets4,
        mouseout: resetHighlightStates4,
        click: zoomToFeature4
    });
}
// End Listeners to states