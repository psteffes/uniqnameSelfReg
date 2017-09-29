$(document).ready(function(){
  $('#tab_password').addClass('active');
});
$('#id_password, #id_confirm_password').keyup(function() {
    var password1 = $('#id_password').val()
    var password2 = $("#id_confirm_password").val();

    if ( password2.length == 0 ) {
        $("#id_confirm_help").css("visibility","hidden");
    }

    if ( password1.length == 0 ) {
        $("#id_password_help").css("visibility","hidden");
        resetPWDisplay();
        return;
    }

    $.ajax({
        type: 'GET',
        url: '/api/validate_password',
        dataType: 'json',
        data: {
            'uid': $('#uid').text(),
            'password1': password1,
            'password2': password2,
        },
        success: function (data) {
            updateDisplay(data);
        },
    });
});
function resetPWDisplay() {
    $("#min_char").removeClass();
    $("#min_char").addClass("glyphicon glyphicon-chevron-right");
    $("#min_char").css("color","initial");

    $("#meet3").removeClass();
    $("#meet3").addClass("glyphicon glyphicon-chevron-right");
    $("#meet3").css("color","initial");

    $("#lcase").removeClass();
    $("#lcase").addClass("glyphicon glyphicon-chevron-right");
    $("#lcase").css("color","initial");

    $("#ucase").removeClass();
    $("#ucase").addClass("glyphicon glyphicon-chevron-right");
    $("#ucase").css("color","initial");

    $("#digit").removeClass();
    $("#digit").addClass("glyphicon glyphicon-chevron-right");
    $("#digit").css("color","initial");

    $("#punc").removeClass();
    $("#punc").addClass("glyphicon glyphicon-chevron-right");
    $("#punc").css("color","initial");
}
function updateDisplay(resultInfo) {
    var issue = resultInfo.evaluation.issue;

    if (issue) {
        if (issue.contains_id('javax.validation.constraints.Size.message')) {
            $("#min_char").removeClass("glyphicon-ok glyphicon-chevron-right");
            $("#min_char").addClass("glyphicon-remove");
            $("#min_char").css("color","#FF0004");
        } else {
            $("#min_char").removeClass("glyphicon-remove glyphicon-chevron-right");
            $("#min_char").addClass("glyphicon-ok");
            $("#min_char").css("color","#00A41E");
        }

        if (issue.contains_id('validator.rules')) {
            $("#meet3").removeClass("glyphicon-ok glyphicon-chevron-right");
            $("#meet3").addClass("glyphicon-remove");
            $("#meet3").css("color","#FF0004");
        } else {
            $("#meet3").removeClass("glyphicon-remove glyphicon-chevron-right");
            $("#meet3").addClass("glyphicon-ok");
            $("#meet3").css("color","#00A41E");
        }

        if (issue.contains_id('validator.contains.lowercase')) {
            $("#lcase").removeClass("glyphicon-ok");
            $("#lcase").addClass("glyphicon-chevron-right");
            $("#lcase").css("color","initial");
        } else {
            $("#lcase").removeClass("glyphicon-chevron-right");
            $("#lcase").addClass("glyphicon-ok");
            $("#lcase").css("color","#00A41E");
        }

        if (issue.contains_id('validator.contains.uppercase')) {
            $("#ucase").removeClass("glyphicon-ok");
            $("#ucase").addClass("glyphicon-chevron-right");
            $("#ucase").css("color","initial");
        } else {
            $("#ucase").removeClass("glyphicon-chevron-right");
            $("#ucase").addClass("glyphicon-ok");
            $("#ucase").css("color","#00A41E");
        }

        if (issue.contains_id('validator.contains.digit')) {
            $("#digit").removeClass("glyphicon-ok");
            $("#digit").addClass("glyphicon-chevron-right");
            $("#digit").css("color","initial");
        } else {
            $("#digit").removeClass("glyphicon-chevron-right");
            $("#digit").addClass("glyphicon-ok");
            $("#digit").css("color","#00A41E");
        }

        if (issue.contains_id('validator.contains.symbols')) {
            $("#punc").removeClass("glyphicon-ok");
            $("#punc").addClass("glyphicon-chevron-right");
            $("#punc").css("color","initial");
        } else {
            $("#punc").removeClass("glyphicon-chevron-right");
            $("#punc").addClass("glyphicon-ok");
            $("#punc").css("color","#00A41E");
        }

        if (issue.contains_id('validator.contains.ascending.pattern')) {
            $("#id_password_help").html("Password must not contain ascending or descending pattern (abcd, 1234, etc)");
            $("#id_password_help").css("visibility","visible");
        } else if (issue.contains_id('validator.contains.dictionary.word')) {
            $("#id_password_help").html("Password must not be a word or simple phrase");
            $("#id_password_help").css("visibility","visible");
        } else if (issue.contains_id('validator.contains.nameparts.present')) {
            $("#id_password_help").html("Password must not use parts of your name)");
            $("#id_password_help").css("visibility","visible");
        } else {
            $("#id_password_help").css("visibility","hidden");
        }

        if ( $('#id_confirm_password').val().length > 0 && issue.contains_id('validator.matches.error') ) {
            $("#id_confirm_help").css("visibility","visible");
            $("#id_submit_btn").prop("disabled",true);
        } else {
            $("#id_confirm_help").css("visibility","hidden");
        }
    }

    if (resultInfo.evaluation.valid == true ) {
        $("#id_confirm_help").css("visibility","hidden");
        $("#id_submit_btn").prop("disabled",false);
    } else {
        $("#id_submit_btn").prop("disabled",true);
    }
}
Array.prototype.contains_id = function (needle) {
    for (i in this) {
        if (this[i].id == needle) return true;
    }
    return false;
}
