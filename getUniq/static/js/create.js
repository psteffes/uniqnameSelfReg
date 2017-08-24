$("#id_uniqname").keyup(checking);
$("a[role='button']").click(checking);
function checking () {
    $("#id_claim_btn").prop("disabled", true);
    $("#id_check_btn").removeClass("btn-success");
    $("#id_check_btn").addClass("btn-blue");
    $("#id_check_btn").prop("disabled", false);
}
$("#id_check_btn").click(function () {
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
            }
            else {
                console.log('no match');
                $("#id_check_btn").removeClass("btn-blue");
                $("#id_check_btn").addClass("btn-success");
                $("#id_claim_btn").prop("disabled", false);
            }
        },
    });
});
$("#id_suggest_btn").click(function() {
    var name_parts = $("#id_suggest_field").val();
    console.log('name_parts=' + name_parts);
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
            displayError('There was an error');
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
        a.setAttribute('onClick', "document.getElementById('id_uniqname').value=this.innerHTML");
        a.innerHTML = suggestions[i];
        suggest_div.appendChild(a);
    }
}
function displayError(message) {
    grid = document.getElementById("grid");
    var div = document.createElement("div");
    div.setAttribute('class', 'alert alert-danger alert-dismissable');
    div.innerHTML = message;
    grid.insertBefore(div, grid.childNodes[0]);

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
