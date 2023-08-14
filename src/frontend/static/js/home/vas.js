// COOKIES - [Reminder access location & Reminder complete daily symptoms]

// Check if cookie (reminder to complete daily symptoms) has expired or not exist
if (!get_cookie('complete_vas_reminder')) {
    $('#warningAlert').show();
} else {
    $('#warningAlert').hide();
}

// popovers Initialization
$(function () {
    $('[data-toggle="popover"]').popover()
})


// Submit vas form
$("#id_submit").click(function (event) {

    // try access to geoloaction via html5's method
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(location_access, no_location_access, { enableHighAccuracy: true });
    } else {
        alert("Geolocation is not supported by this browser.");
    }

    // enable loader, disable submit button (while finding location)
    $('#id_submit').attr('disabled', true);
    $("#location_loader").addClass("loader");


    /** Set map and get coordinates */
    function location_access(position) {

        // Enable 'No' button at modal
        $('#fail_location').attr('disabled', false);

        // open location modal
        $(document).ready(function () {
            $("#vas_location").modal();
        });

        // retrieve user's coordinates
        onclick_lat = position.coords.latitude;
        onclick_lng = position.coords.longitude;

        // Map settings
        if (circle) { delete_circle(); }
        if (marker) { delete_marker(); marker = null; }
        vas_map.setCenter({ lat: onclick_lat, lng: onclick_lng });
        vas_map.setZoom(10);
        get_circle(onclick_lat, onclick_lng, vas_map);
        //end

        // disable loader and enable button (when location has found)
        $("#location_loader").removeClass("loader");
        $('#id_submit').attr('disabled', false);
    }

    /** Send data to server without location */
    function no_location_access(error) {

        // Set cookie (reminder to complete daily symptoms)
        set_cookie('complete_vas_reminder', true, 1)

        // Retrieve data from inputs
        var $inputs = $('#vas_form_submition :input');
        var values = {};
        var inputs_list = [];

        $inputs.each(function () {
            values[this.name] = $(this).val();
            inputs_list.push(values[this.name]);
        });

        delete inputs_list[0];
        inputs_list.pop();

        const data = {
            "vas": {
                "vas info": [{ "general_symptoms": parseInt(inputs_list[1]) },
                { "rhinitis": parseInt(inputs_list[2]) },
                { "asthma": parseInt(inputs_list[3]) },
                { "conjunctivitis": parseInt(inputs_list[4]) },
                { "work": inputs_list[5] },
                { "work_symptoms": parseInt(inputs_list[6]) },
                { "lat": 'no lat' },
                { "lng": 'no lng' },
                { "location state": false }
                ]
            }
        };
        //end

        // console.log('[DEBUG]');
        // console.log('Data for server -> ', data);
        // console.log('[END]');

        // Send data to server and get as response suitable messager for user
        fetch('/api/Home/vastool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
            .then((response) => response.json())
            .then((data) => {
                $('#successAlert').show();
                $('#warningAlert').hide();
            })
            .catch((error) => { console.error('Error:', error); });


        // Alert user for probably problems and set cookie
        if (error.code == 1) {
            if (!get_cookie('blocked_location_access_reminder')) { // if COOKIE has expired or no exist (Reminder for access location)
                $(document).ready(function () {
                    $("#cookie_modal").modal();
                });
                set_cookie('blocked_location_access_reminder', true, 3)
            }
        } else if (error.code == 2) {
            alert('Location information is unavailable.');
        } else if (error.code == 3) {
            alert('The request to get user location timed out.');
        } else if (error.code == 4) {
            alert('An unknown error occurred.');
        }

        // Disable loader and enable button
        $("#location_loader").removeClass("loader");
        $('#id_submit').attr('disabled', false);

        // pop up modal in case of high symptoms
        if (parseInt(inputs_list[1]) == 12) {
            $(document).ready(function () {
                $("#high_symptoms_modal").modal();
            });
        }

    }

});

// [MODAL]
$('#success_location').click(function (event) {

    // Set cookie (reminder to complete daily symptoms)
    set_cookie('complete_vas_reminder', true, 1)

    // Retrieve data from inputs
    var $inputs = $('#vas_form_submition :input');
    var values = {};
    var inputs_list = [];

    $inputs.each(function () {
        values[this.name] = $(this).val();
        inputs_list.push(values[this.name]);
    });

    delete inputs_list[0];
    inputs_list.pop();
    
    if (marker) {
        onclick_lat = marker.getPosition().lat();
        onclick_lng = marker.getPosition().lng();
    }

    const data = {
        "vas": {
            "vas info": [{ "general_symptoms": parseInt(inputs_list[1]) },
            { "rhinitis": parseInt(inputs_list[2]) },
            { "asthma": parseInt(inputs_list[3]) },
            { "conjunctivitis": parseInt(inputs_list[4]) },
            { "work": inputs_list[5] },
            { "work_symptoms": parseInt(inputs_list[6]) },
            { "lat": onclick_lat },
            { "lng": onclick_lng },
            { "location state": true }
            ]
        }
    };
    // end

    // console.log('[DEBUG]');
    // console.log('Data for server -> ', data);
    // console.log('onclick data: ' + onclick_lat + ", " + onclick_lng);
    // console.log('[END]');

    // send data to server and get as response suitable messager for user
    fetch('/api/Home/vastool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            $('#successAlert').show();
            $('#warningAlert').hide();
        })
        .catch((error) => { console.error('Error:', error); });

    // pop up modal in case of high symptoms
    if (parseInt(inputs_list[1]) == 12) {
        $(document).ready(function () {
            $("#high_symptoms_modal").modal();
        });
    }

});


$('#fail_location').click(function (event) {

    // Disable 'No' button
    $('#fail_location').attr('disabled', true);

    if (circle) { delete_circle(); }
    if (marker) { delete_marker(); marker = null }
    var myLatlng = new google.maps.LatLng(onclick_lat, onclick_lng);
    // Pin to America
    // var myLatlng = new google.maps.LatLng(38.8, -96);
    // vas_map.setCenter(myLatlng);
    vas_map.setZoom(5);
    vas_map.setZoom(4.3);
    get_marker(myLatlng, vas_map);

});



// Hide div
$('#work_school_form').on('change', function () {
    if (this.value == "Yes") {
        $('#work_school_today_hide').show();
        // console.log('Yes selected')
    } else {
        $('#work_school_today_hide').hide();
        // console.log('No selected')
    }
});