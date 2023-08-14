// Hide div
$('#immunotherapy_form').on('change', function () {
    if (this.value == "Not receiving immunotherapy") {
        $("input[type=date]").val("");
        $('#immunotherapy_start_date_hide').hide();
        // console.log('Not receiving immonotherapy, selected')
    } else {
        $('#immunotherapy_start_date_hide').show();
        // console.log('Other choices selected')
    }
});