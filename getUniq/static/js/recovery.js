$(document).ready(function(){
  $('#tab-recovery').addClass('active');
});
$('#recovery, #confirmrecovery').keyup(function() {
    var recovery1 = $('#recovery').val();
    var recovery2 = $("#confirmrecovery").val();
    var sms1 = $('#sms').val();
    if ( recovery2.length == 0 ) {
        $("#confirm-help").css("visibility","hidden");
    }
    if ( recovery1.length == 0 ) {
        $("#recovery-help").css("visibility","hidden");
    }
    if ( recovery1 == recovery2 && recovery1.length > 0) {
        $("#confirm-help").css("visibility","hidden");
    } 
});
$('#sms, #confirmsms').keyup(function() {
    var sms1 = $('#sms').val();
    var sms2 = $("#confirmsms").val();
    var recovery1 = $('#recovery').val();
    if ( sms2.length == 0 ) {
        $("#confirmsms-help").css("visibility","hidden");
    }
    if ( sms1.length == 0 ) {
        $("#sms-help").css("visibility","hidden");
    }
    if ( sms1 == sms2 && sms1.length > 0) {
        $("#confirmsms-help").css("visibility","hidden");
});
$("input[type='tel']").each(function(){
  $(this).on("change keyup paste", function (e) {
    var output,
      $this = $(this),
      input = $this.val();

    if(e.keyCode != 8) {
      input = input.replace(/[^0-9]/g, '');
      var area = input.substr(0, 3);
      var pre = input.substr(3, 3);
      var tel = input.substr(6, 4);
      if (area.length == 0) {
        output = ""
      } else if (area.length < 3) {
        output = "(" + area;
      } else if (area.length == 3 && pre.length < 3) {
        output = "(" + area + ")" + " " + pre;
      } else if (area.length == 3 && pre.length == 3) {
        output = "(" + area + ")" + " " + pre + "-" + tel;
      }
      $this.val(output);
    }
  });
});