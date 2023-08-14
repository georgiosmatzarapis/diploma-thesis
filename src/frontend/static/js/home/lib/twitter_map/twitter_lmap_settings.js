/** ---------------------------- STYLES ---------------------------- */

// LEGENDS
var legend5, button5, geojson_markets5, geojson_states5, info;

/** Adds checkbox. */
function hide_button5(my_map) {
    button5 = L.control({ position: 'topleft' });

    button5.onAdd = function (map) {
        var div = L.DomUtil.create('div');

        div.innerHTML = '<button type="button" style="padding: 5px 12px;" class="btn btn-blue-grey btn-sm curved_edge_button" \
                         id="hide_color_guide5">Show guide</button>';

        return div;
    };
    button5.addTo(my_map);
}

/** Adds color guide. */
function color_guide_legend5(my_map) {
    legend5 = L.control({ position: 'bottomleft' });

    legend5.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info_guide5 legend'),
            grades = ["min", "", "", "", "max"],
            colors = ["#c7effc", "#70d1f4", "#00a3e0", "#076ca7", "#10405c"],
            labels = ["", "", "", "", ""];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += '<i style="background:' + colors[i] + '"></i> ' + labels[i] + ' ' + grades[i] + "<br>";
        }

        return div;
    };

    return legend5.addTo(my_map);
}

/** Custom info control */
function custom_info(my_map) {
    info = L.control();

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info.update = function (props) {
        this._div.innerHTML = '<h6>Allergy/Allergens Density</h6>' + (props ?
            '<b>' + props.NAME + '</b><br />' + props.tweets + ' tweet(s) </sup>'
            : 'Hover over a state');
    };

    info.addTo(my_map);
}

/** Sets colors. */
function getColor5(d) {
    if (d == '-') {
        return '#fff' // This values means that there is no density for these area
    }else if (d >= color_spaces[0] && d <= color_spaces[1]) {
        return '#c7effc'
    } else if (d >= color_spaces[2] && d <= color_spaces[3]) {
        return '#70d1f4'
    } else if (d >= color_spaces[4] && d <= color_spaces[5]) {
        return '#00a3e0'
    } else if (d >= color_spaces[6] && d <= color_spaces[7]) {
        return '#076ca7'
    } else if (d >= color_spaces[8] && d <= color_spaces[9]) {
        return '#10405c'
    }
}

/** Config style for us markets. */
function states_style5(feature) {
    return {
        fillColor: getColor5(feature.properties.tweets),
        fillOpacity: .6,
        weight: 1.5,
        opacity: .5,
        color: getColor5(feature.properties.tweets),
        dashArray: '3',
        color: "#595959",
        stroke: true
    };
}


/** ---------------------------- LISTENERS ---------------------------- */
/** Highlights state. */
function highlightFeature5(e) {
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
    info.update(layer.feature.properties);
}

/** Resets highlight state. */
function resetHighlightStates5(n) {
    geojson_states5.resetStyle(n.target);
    info.update();
}

/** Zooms to state. */
function zoomToFeature5(n) {
    twitter_lmap.fitBounds(n.target.getBounds());
}

/** Adds listeners to state layer. */
function onEachFeature5(feature, layer) {
    layer.on({
        mouseover: highlightFeature5,
        mouseout: resetHighlightStates5,
        click: zoomToFeature5
    });
}
// End Listeners to states