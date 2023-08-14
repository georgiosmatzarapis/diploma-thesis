// Check if cookie has expired or not exist
if (!get_cookie("accept_cookie_usage")) {
    $(document).ready(function () {
        $("#accept_cookies").modal();
    });
}

// When clicking on the agree button, create a 1 year
// cookie to remember user's choice and close the banner
$('.acceptcookies').click(function () {
    set_cookie("accept_cookie_usage", true, 365);
});