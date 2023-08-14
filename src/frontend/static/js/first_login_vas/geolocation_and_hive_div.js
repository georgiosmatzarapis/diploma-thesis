// Hide div
$('#work_school_form').on('change', function () {
    if (this.value == "Yes") {
      $('#work_school_today_hide').show();
    //   console.log('Yes selected')
    } else {
      $('#work_school_today_hide').hide();
    //   console.log('No selected')
    }
  });