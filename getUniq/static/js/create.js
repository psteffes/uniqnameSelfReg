// Update active tab in progress bar
$(document).ready(function(){
  $('#tab-create').addClass('active');
});
// Reset validity if uniqname field changes
$("#uniqname").on('input', reset_uniqname_check);

$("#suggestion-list").on('click', "a[role='button']", function() {
    $('#uniqname').val($(this).html());    // set uniqname field to clicked suggestion
    onSuggestionClick();
});
// Prevent submit via enter in text input
$("#uniqname").on('keypress', function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
    }
});
function reset_uniqname_check () {
    $("#claim-btn").prop("disabled", true);
    $("#check-btn").removeClass("btn-success btn-danger");
    $("#check-btn").addClass("btn-blue");
    $("#check-btn").html("Check Availability");
    $("#check-btn").prop("disabled", false);
}
function onSuggestionClick () {
    reset_uniqname_check();
    checkAvailability();
}
$("#check-btn").click(checkAvailability);
function checkAvailability() {
    var uid = $("#uniqname").val();

    $("#check-btn").prop("disabled", true);

    $.ajax({
        type: 'POST',
        url: '/api/find_uniqname/',
        dataType: 'json',
        data: {
            'uid': uid,
        },
        success: function (data) {
            if (data.uid) {
                $("#claim-btn").prop("disabled", true);
                $("#check-btn").removeClass("btn-blue");
                $("#check-btn").addClass("btn-danger");
                $("#check-btn").html('Not Available <span class="glyphicon glyphicon-remove"</span>');
            }
            else {
                $("#check-btn").removeClass("btn-blue");
                $("#check-btn").addClass("btn-success");
                $("#check-btn").html('Available <span class="glyphicon glyphicon-ok"</span>');
                $("#claim-btn").prop("disabled", false);
            }
        },
        error: function () {
            $("#check-btn").prop("disabled", false);
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
$('#claim-btn').click(function() {
    $('#modal-uid').text('"' + $('#uniqname').val() + '"');
});
$('#confirm-submit').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
});
$("#suggest-btn").click(function() {
    var name_parts = $("#suggest-field").val();
    name_parts = name_parts.split(/\s+/);

    $("#suggest-btn").prop("disabled", true);
      
    $.ajax({
        type: 'POST',
        url: '/api/get_suggestions/',
        traditional: true,
        dataType: 'json',
        data: {
            'name_parts': name_parts,
        },
        success: function (data) {
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
            $("#suggest-btn").prop("disabled", false);
        },
    });
});
function displaySuggestions(suggestions) {
    var suggest_div = document.getElementById("suggestion-list");
    while (suggest_div.hasChildNodes()) {
        suggest_div.removeChild(suggest_div.lastChild);
    }
    for (var i=0; i < suggestions.length; i++) {
        var t = document.createTextNode("\n\u00A0\u00A0\u00A0\u00A0");
        suggest_div.appendChild(t);
        var a = document.createElement("a");
        a.setAttribute('role', 'button');
        a.innerHTML = suggestions[i];
        suggest_div.appendChild(a);
    }
}
function displayError(message) {
    var suggest_div = document.getElementById("suggestion-list");
    while (suggest_div.hasChildNodes()) {
        suggest_div.removeChild(suggest_div.lastChild);
    }
    var span = document.createElement("span");
    span.setAttribute('class', 'text-danger');
    span.innerHTML = message;
    suggest_div.appendChild(span);
}
