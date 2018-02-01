$(document).ready(function(){
  $('#tab-recovery').addClass('active');
});
$('#recovery, #confirmrecovery').keyup(function() {
    var recovery1 = $('#recovery').val();
    var recovery2 = $("#confirmrecovery").val();
    if ( recovery2.length == 0 ) {
        $("#confirm-help").css("visibility","hidden");
    }
    if ( recovery1.length == 0 ) {
        $("#recovery-help").css("visibility","hidden");
    }
    if ( recovery1 == recovery2 && recovery1.length > 0) {
        $("#confirm-help").css("visibility","hidden");
        $("#submit-btn").prop("disabled",false);
    } else {
        $("#submit-btn").prop("disabled",true);
    }
});
