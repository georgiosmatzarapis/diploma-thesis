var infoWindow, heatmap;

/** Set infoWindow. */
function set_infoWindow(LatLng, message, my_map) {
    infoWindow = new google.maps.InfoWindow;
    infoWindow.setPosition(LatLng);
    infoWindow.setContent(message);
    infoWindow.open(my_map);
}
/** Delete infoWindow. */
function delete_infoWindow() {
    infoWindow.close();
}

/** Set heatmap layer. */
function set_heatmap(heat_data, gradient, radius, dissipating, maxIntensity, my_map) {

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: heat_data,
        gradient: gradient,
        radius: radius,
        opacity: 0.6,
        dissipating: dissipating,
        maxIntensity: maxIntensity
    });
    heatmap.setMap(my_map);
}
/** Delete heatmap layer. */
function delete_heatmap() {
    heatmap.setMap(null);
}

/** Set radius on heatmap. */
function set_heatmap_radius(radius_value) {
    heatmap.set('radius', radius_value);
}
/** Radius specified be zoom level. */
function zoom_changed_event_myallergy(my_map) {
    google.maps.event.addListener(my_map, 'zoom_changed', function () {
        var zoomLevel = my_map.getZoom();
        switch (zoomLevel) {
            case 15:
                set_heatmap_radius(0.0050);
                break;
            case 14:
                set_heatmap_radius(0.0050);
                break;
            case 13:
                set_heatmap_radius(0.0050);
                break;
            case 12:
                set_heatmap_radius(0.0060);
                break;
            case 11:
                set_heatmap_radius(0.0075);
                break;
            case 10:
                set_heatmap_radius(0.0135);
                break;
            case 9:
                set_heatmap_radius(0.025);
                break;
            case 8:
                set_heatmap_radius(0.048);
                break;
            case 7:
                set_heatmap_radius(0.068);
                break;
            case 6:
                set_heatmap_radius(0.15);
                break;
            case 5:
                set_heatmap_radius(0.29);
                break;
            case 4:
                set_heatmap_radius(0.55);
                break;
        }
        // console.log(zoomLevel);
    });
}

/** Returns max intensity for heatmap. */
function heatmap_weight(total_spots, total_weight) {

    var max_intensity;

    if (total_spots <= 10) {

        max_intensity = 12 * total_spots;
        return max_intensity;

    } else if (total_spots > 10) {

        var symptoms_average = total_weight / total_spots;
        var spot_probability = 0.7; // the average probability one person to visit same places into the day
        var common_visited_spots = 2.5; // 2-3 are the common visited spots for one common person into the day

        // Max intensity represents the max heat value in the map. More specific, i set as max the total weights of
        // spots which are gathered in the almost same geolocation.
        max_intensity = ((total_spots * spot_probability) / common_visited_spots) * symptoms_average;
        return max_intensity.toFixed(0);

    }

}