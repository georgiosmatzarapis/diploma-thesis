var circle, marker;

/** Set circle layer to map. */
function get_circle(lat, lng, my_map) {
    circle = new google.maps.Circle({
        strokeColor: 'purple',
        strokeOpacity: 0.5,
        strokeWeight: 2,
        fillColor: 'purple',
        fillOpacity: 0.35,
        map: my_map,
        center: { lat: lat, lng: lng },
        radius: 1500
    });
}
/** Delete circle layer from map. */
function delete_circle() {
    circle.setMap(null)
}

/** Set marker. */
function get_marker(position, my_map) {
    marker = new google.maps.Marker({
        position: position,
        map: my_map,
        draggable: true,
        animation: google.maps.Animation.DROP
    });
    marker.setMap(my_map);
}
/** Delete marker. */
function delete_marker() {
    marker.setMap(null);
}