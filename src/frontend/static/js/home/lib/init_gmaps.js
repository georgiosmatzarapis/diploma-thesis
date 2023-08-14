var sensor_gmap, mcs_gmap, hybrid_gmap, vas_map, humidity_gmap;

var gradient = [
    "rgba(102, 255, 0, 0)",
    "rgba(102, 255, 0, 1)",
    "rgba(147, 255, 0, 1)",
    "rgba(193, 255, 0, 1)",
    "rgba(238, 255, 0, 1)",
    "rgba(244, 227, 0, 1)",
    "rgba(249, 198, 0, 1)",
    "rgba(255, 170, 0, 1)",
    "rgba(255, 113, 0, 1)",
    "rgba(255, 57, 0, 1)",
    "rgba(255, 0, 0, 1)"
];

/** Initializes the map. */
function initMap() {

    var main_options1 = {
        zoom: 4,
        minZoom: 4,
        maxZoom: 7,
        center: { lat: 38.8, lng: -96 },
        gestureHandling: 'cooperative',
        mapTypeId: 'hybrid'
    }

    var main_options2 = {
        zoom: 4,
        minZoom: 4,
        maxZoom: 7,
        center: { lat: 38.8, lng: -96 },
        gestureHandling: 'cooperative',
        mapTypeId: 'hybrid'
    }

    var main_options4 = {
        zoom: 4,
        minZoom: 4,
        maxZoom: 7,
        center: { lat: 38.8, lng: -96 },
        gestureHandling: 'cooperative',
        mapTypeId: 'hybrid',
        disableDefaultUI: true
    }

    var vas_options = {
        zoom: 1,
        minZoom: 1,
        mapTypeControl: false,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.TOP_LEFT
        },
        gestureHandling: 'cooperative',
        center: { lat: 1, lng: 1 }
    }

    sensor_gmap = new google.maps.Map(document.getElementById("main_gmap1"), main_options1);

    vas_gmap = new google.maps.Map(document.getElementById("main_gmap2"), main_options2);

    vas_map = new google.maps.Map(document.getElementById("mini_gmap"), vas_options);

    // humidity_gmap = new google.maps.Map(document.getElementById("humidity_gmap"), main_options4);
}