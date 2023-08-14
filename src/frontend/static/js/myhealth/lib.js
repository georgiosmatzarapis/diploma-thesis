/** Returns message according to time interval selected. */
function popup_message(time_interval) {

    if (time_interval == 30) {
        return popup_msg = '30 minutes';
    } else if (time_interval == 60) {
        return popup_msg = '1 hour';
    } else if (time_interval == 180) {
        return popup_msg = '3 hours';
    } else if (time_interval == 720) {
        return popup_msg = '12 hours';
    } else if (time_interval == 1440) {
        return popup_msg = '24 hours';
    } else if (time_interval == 4320) {
        return popup_msg = '3 days';
    } else if (time_interval == 10080) {
        return popup_msg = '1 week';
    } else if (time_interval == 43200) {
        return popup_msg = '1 month';
    } else if (time_interval == 129600) {
        return popup_msg = '3 months';
    } else if (time_interval == 259200) {
        return popup_msg = '6 months';
    } else if (time_interval == 518400) {
        return popup_msg = '1 year';
    }
}

var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
]