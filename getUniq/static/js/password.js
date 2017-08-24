/*
$("#id_password").keyup(function(){
    var ucase = new RegExp("[A-Z]+");
    var lcase = new RegExp("[a-z]+");
    var num = new RegExp("[0-9]+");
    
    if($("#id_password").val().length >= 9){
        $("#min_char").removeClass("glyphicon-remove glyphicon-chevron-right");
        $("#min_char").addClass("glyphicon-ok");
        $("#min_char").css("color","#00A41E");
    }else{
        $("#min_char").removeClass("glyphicon-ok glyphicon-chevron-right");
        $("#min_char").addClass("glyphicon-remove");
        $("#min_char").css("color","#FF0004");
    }
    
    if(ucase.test($("#id_password").val())){
        $("#ucase").removeClass("glyphicon-remove");
        $("#ucase").addClass("glyphicon-ok");
        $("#ucase").css("color","#00A41E");
    }else{
        $("#ucase").removeClass("glyphicon-ok");
        $("#ucase").addClass("glyphicon-remove");
        $("#ucase").css("color","#FF0004");
    }
    
    if(lcase.test($("#id_password").val())){
        $("#lcase").removeClass("glyphicon-remove");
        $("#lcase").addClass("glyphicon-ok");
        $("#lcase").css("color","#00A41E");
    }else{
        $("#lcase").removeClass("glyphicon-ok");
        $("#lcase").addClass("glyphicon-remove");
        $("#lcase").css("color","#FF0004");
    }
    
    if(num.test($("#id_password").val())){
        $("#num").removeClass("glyphicon-remove");
        $("#num").addClass("glyphicon-ok");
        $("#num").css("color","#00A41E");
    }else{
        $("#num").removeClass("glyphicon-ok");
        $("#num").addClass("glyphicon-remove");
        $("#num").css("color","#FF0004");
    }
    
    if($("#id_password").val() == $("#id_confirm_password").val()){
        $("#pwmatch").removeClass("glyphicon-remove");
        $("#pwmatch").addClass("glyphicon-ok");
        $("#pwmatch").css("color","#00A41E");
    }else{
        $("#pwmatch").removeClass("glyphicon-ok");
        $("#pwmatch").addClass("glyphicon-remove");
        $("#pwmatch").css("color","#FF0004");
    }
});
*/
$("#id_confirm_password").keyup(function() {
    if($("#id_password").val() == $("#id_confirm_password").val()){
        $("#id_confirm_help").css("visibility","hidden");
        $("#id_submit_btn").prop("disabled",false);
    }else{
        $("#id_confirm_help").css("visibility","visible");
        $("#id_submit_btn").prop("disabled",true);
    }
});
$("#id_password").keyup(function () {
    var password1 = $("#id_password").val();
    var password2 = $("#id_confirm_password").val();
    console.log('pw1=' + password1);
    console.log('pw2=' + password2);

    $.ajax({
        type: 'GET',
        url: '/api/validate_password',
        dataType: 'json',
        data: {
           'password1': password1,
           'password2': password2,
        },
        success: function (data) {
            console.log('data=' + data);
            console.log(data.evaluation);
            console.log(data.evaluation.issue);
            updateDisplay(data);
        },
    });
});
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
            $("#lcase").addClass("glyphicon-menu-right");
            $("#lcase").css("color","initial");
        } else {
            $("#lcase").removeClass("glyphicon-menu-right");
            $("#lcase").addClass("glyphicon-ok");
            $("#lcase").css("color","#00A41E");
        }

        if (issue.contains_id('validator.contains.uppercase')) {
            $("#ucase").removeClass("glyphicon-ok");
            $("#ucase").addClass("glyphicon-triangle-right");
            $("#ucase").css("color","initial");
        } else {
            $("#ucase").removeClass("glyphicon-triangle-right");
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
            $("#id_password_help").html("Password must not be a word or simple phrase)");
            $("#id_password_help").css("visibility","visible");
        } else if (issue.contains_id('validator.contains.nameparts.present')) {
            $("#id_password_help").html("Password must not use parts of your name)");
            $("#id_password_help").css("visibility","visible");
        } else {
            $("#id_password_help").css("visibility","hidden");
        }
/*
        if (issue.contains_id('validator.contains.ascending.pattern')) {
            $("#id_password_help").html("Password must not contain ascending or descending pattern (abcd, 1234, etc)");
            $("#id_password_help").css("visibility","visible");
        } else {
            $("#id_password_help").css("visibility","hidden");
        }

        if (issue.contains_id('validator.contains.dictionary.word')) {
            $("#id_password_help").html("Password must not be a word or simple phrase)");
            $("#id_password_help").css("visibility","visible");
        } else {
            $("#id_password_help").css("visibility","hidden");
        }

        if (issue.contains_id('validator.contains..nameparts.present')) {
            $("#id_password_help").html("Password must not use parts of your name)");
            $("#id_password_help").css("visibility","visible");
        } else {
            $("#id_password_help").css("visibility","hidden");
        }
*/
    }
}
Array.prototype.contains_id = function (needle) {
    for (i in this) {
        if (this[i].id == needle) return true;
    }
    return false;
}
