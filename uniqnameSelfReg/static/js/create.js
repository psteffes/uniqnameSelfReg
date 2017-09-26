$(document).ready(function(){
  $('#tab_create').addClass('active');
});
$("#id_uniqname").on('input', reset_uniqname_check);
$("#id_suggestion_list").on('click', "a[role='button']", function() {
    $('#id_uniqname').val($(this).html());
    onSuggestionClick();
});
function reset_uniqname_check () {
    $("#id_claim_btn").prop("disabled", true);
    $("#id_check_btn").removeClass("btn-success btn-danger");
    $("#id_check_btn").addClass("btn-blue");
    $("#id_check_btn").html("Check Availability");
    $("#id_check_btn").prop("disabled", false);
}
function onSuggestionClick () {
    reset_uniqname_check();
    checkAvailability();
}
$("#id_check_btn").click(checkAvailability);
function checkAvailability() {
    var uid = $("#id_uniqname").val();
    console.log('uid=' + uid);

    $("#id_check_btn").prop("disabled", true);

    $.ajax({
        type: 'POST',
        url: '/api/find_uniqname/',
        dataType: 'json',
        data: {
            'uid': uid,
        },
        success: function (data) {
            console.log(data);
            if (data.uid) {
                console.log('found ' + data.uid);
                $("#id_claim_btn").prop("disabled", true);
                $("#id_check_btn").removeClass("btn-blue");
                $("#id_check_btn").addClass("btn-danger");
                $("#id_check_btn").html('Not Available <span class="glyphicon glyphicon-remove"</span>');
            }
            else {
                console.log('no match');
                $("#id_check_btn").removeClass("btn-blue");
                $("#id_check_btn").addClass("btn-success");
                $("#id_check_btn").html('Available <span class="glyphicon glyphicon-ok"</span>');
                $("#id_claim_btn").prop("disabled", false);
            }
        },
        error: function () {
            $("#id_check_btn").prop("disabled", false);
            displayBootstrapError('Something happened');
        },
    });
}
function displayBootstrapError(message) {
    container = document.getElementById("alert-container");
    var div = document.createElement("div");
    div.setAttribute('class', 'alert alert-danger alert-dismissable');
    var a = document.createElement("a");
    a.href = "#"
    a.setAttribute('class', 'close');
    a.setAttribute('data-dismiss', 'alert');
    a.setAttribute('aria-label', 'close');
    a.setAttribute('style', 'right: 0px;');
    a.innerHTML = '&times;';
    var t = document.createTextNode(message);
    div.appendChild(a);
    div.appendChild(t);
    container.insertBefore(div, container.childNodes[0]);
}
$('#id_claim_btn').click(function() {
    $('#modal-uid').text('"' + $('#id_uniqname').val() + '"');
});
$('#confirm-delete').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
});
$("#id_suggest_btn").click(function() {
    var name_parts = $("#id_suggest_field").val();
    console.log('name_parts=' + name_parts);
    console.log('name_parts.trim=' + name_parts.trim());
    name_parts = name_parts.split(/\s+/);
    console.log('name_parts=' + name_parts);

    //$("#id_suggest_btn").html("<i id='loginSpinner' class='icon icon-spinner icon-lg animate-pulse'></i>&nbspLoading");
    $("#id_suggest_btn").prop("disabled", true);
      
    $.ajax({
        type: 'POST',
        url: '/api/get_suggestions/',
        traditional: true,
        dataType: 'json',
        data: {
            //'dn': 'ou=people,dc=umich,dc=edu',
            'name_parts': name_parts,
        },
        success: function (data) {
            console.log(data.suggestions);
            if (data.suggestions.length > 1) {
                displaySuggestions(data.suggestions);
            }
            else {
                displayError('Not enough results returned');
            }
        },
        error: function (data) {
            displayError('Unable to get suggestions, please try again');
        },
        complete: function () {
            //$("#id_suggest_btn").html("Suggest");
            $("#id_suggest_btn").prop("disabled", false);
        },
    });
});
function displaySuggestions(suggestions) {
    var suggest_div = document.getElementById("id_suggestion_list");
    while (suggest_div.hasChildNodes()) {
        suggest_div.removeChild(suggest_div.lastChild);
    }
    for (var i=0; i < suggestions.length; i++) {
        console.log(suggestions[i]);
        var t = document.createTextNode("\n\u00A0\u00A0\u00A0\u00A0");
        suggest_div.appendChild(t);
        var a = document.createElement("a");
        a.setAttribute('role', 'button');
        //a.setAttribute('onClick', "document.getElementById('id_uniqname').value=this.innerHTML");
        a.innerHTML = suggestions[i];
        suggest_div.appendChild(a);
    }
}
function displayError(message) {
    //grid = document.getElementById("grid");
    //var div = document.createElement("div");
    //div.setAttribute('class', 'alert alert-danger alert-dismissable');
    //div.innerHTML = message;
    //grid.insertBefore(div, grid.childNodes[0]);

    var suggest_div = document.getElementById("id_suggestion_list");
    while (suggest_div.hasChildNodes()) {
        suggest_div.removeChild(suggest_div.lastChild);
    }
    var span = document.createElement("span");
    span.setAttribute('class', 'text-danger');
    span.innerHTML = message;
    suggest_div.appendChild(span);
}
function createRadioElements2(suggestions) {
    var suggest_div = document.getElementById("id_suggest_div");
    while (suggest_div.hasChildNodes()) {
        suggest_div.removeChild(suggest_div.lastChild);
    }
    for (var i=0; i < suggestions.length; i++) {
        console.log(suggestions[i]);
        var div = document.createElement("div");
        div.setAttribute('class', 'form-group');
        var label = document.createElement("label");
        label.setAttribute('class', 'id-verify-label');
        var input = document.createElement("input");
        input.setAttribute('type', 'radio');
        input.setAttribute('value', suggestions[i]);
        input.setAttribute('name', 'suggestionRadios');
        input.setAttribute('onclick', 'document.getElementById("id_uniqname").value=this.value');
        var t = document.createTextNode("\n" + suggestions[i]);
        label.appendChild(input);
        label.appendChild(t);
        div.appendChild(label);
        suggest_div.appendChild(div);
    }
}
