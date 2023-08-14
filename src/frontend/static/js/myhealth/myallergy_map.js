var myhealth_map;

/** Initialize map. */
function initMap() {
    var view = { lat: 1, lng: 1 }
    myhealth_map = new google.maps.Map(document.getElementById('myhealth_map'), {
        center: view,
        zoom: 4,
        maxZoom: 15,
        minZoom: 4,
        mapTypeId: 'hybrid'
    });
}


// FETCH - get coordinates for first 3 MONTHS (default)   
fetch('/api/MyHealth/myallergymap/' + 129600)
    .then((response) => {
        return response.json();
    })
    .then((data) => {

        // suitable format the data's structure, etc [{lat: lat_value, lng: lng_value, count: count_value}, {lat: lat_value, lng: lng_value, count: count_value}, ..., {lat: lat_value, lng: lng_value, count: count_value}] 
        var heatMapData = [];
        var total_weight = 0;
        var total_spots = 0;
        data.forEach(element => {
            if (element.symptoms_scale != 0) {
                var temp_obj = {
                    location: new google.maps.LatLng(element.geolocation[0], element.geolocation[1]),
                    weight: element.symptoms_scale
                }
                total_weight += element.symptoms_scale;
                total_spots += 1;
                heatMapData.push(temp_obj)
            }
        });

        // console.log('[DEBUG]');
        // console.log('maxIntensity: ', heatmap_weight(total_spots, total_weight), '|',
        //     'Total spots: ', total_spots, '|',
        //     'Total weight: ', total_weight, '|',
        //     'Gathered data: ', heatMapData);
        // console.log('[END]');

        if (heatMapData.length != 0) {

            myhealth_map.setCenter(heatMapData[0].location);
            myhealth_map.setZoom(9);
            set_infoWindow(heatMapData[0].location, '<b>Your first trace!</b><br>(default: 3 months)', myhealth_map);
            set_heatmap(heatMapData, gradient, 0.025, false, heatmap_weight(total_spots, total_weight), myhealth_map);
            zoom_changed_event_myallergy(myhealth_map); // this function is also used for below on changed events

        } else {

            set_infoWindow({ lat: 1, lng: 1 }, 'No allergy traces found for (default) time interval: <b>3 months</b>.', myhealth_map);

        }

    });


// On change map
$('#time_picker').on('change', function () {
    var string_minutes = $('#time_picker').val();
    $('#time_picker').val(0);
    var minutes = parseInt(string_minutes);

    if (minutes != 0) {

        // FETCH - send to back time interval and get coordinates       
        // TODO ADD LOADER
        fetch('/api/MyHealth/myallergymap/' + minutes)
            .then((response) => {
                return response.json();
            })
            .then((data) => {

                var heatMapData = [];
                var total_weight = 0;
                var total_spots = 0;
                data.forEach(element => {
                    if (element.symptoms_scale != 0) {
                        var temp_obj = {
                            location: new google.maps.LatLng(element.geolocation[0], element.geolocation[1]),
                            weight: element.symptoms_scale
                        }
                        total_weight += element.symptoms_scale;
                        total_spots += 1;
                        heatMapData.push(temp_obj)
                    }
                });

                // console.log('[DEBUG]');
                // console.log('maxIntensity: ', heatmap_weight(total_spots, total_weight), '|',
                //     'Total spots: ', total_spots, '|',
                //     'Total weight: ', total_weight, '|',
                //     'Gathered data: ', heatMapData);
                // console.log('[END]');

                if (heatMapData.length != 0) {

                    if (heatmap) {
                        delete_heatmap();
                    }
                    if (infoWindow) {
                        delete_infoWindow();
                    }

                    myhealth_map.setCenter(heatMapData[0].location);
                    myhealth_map.setZoom(9);
                    set_infoWindow(heatMapData[0].location, '<b>Your first trace!</b><br>(time interval: <b>' + popup_message(minutes) + '</b>)', myhealth_map);
                    set_heatmap(heatMapData, gradient, 0.025, false, heatmap_weight(total_spots, total_weight), myhealth_map);

                } else {

                    if (heatmap) {
                        delete_heatmap();
                    }
                    if (infoWindow) {
                        delete_infoWindow();
                    }

                    myhealth_map.setCenter({ lat: 1, lng: 1 });
                    myhealth_map.setZoom(4);
                    set_infoWindow({ lat: 1, lng: 1 }, 'No allergy traces found for time interval: <b>' + popup_message(minutes) + '</b>.', myhealth_map)
                }

            });

    } else {
        // console.log('\'Select from below\', selected')
    }
});