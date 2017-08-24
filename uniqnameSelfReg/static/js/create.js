$("#id_check_btn").click(function () {
    var uid = $(id_uniqname).val();
    console.log('uid=' + uid);

    $.ajax({
        type: 'POST',
        url: '/api/find_uniqname/',
        dataType: 'json',
        data: {
            'uid': uid,
        }
        success: function (data) {
            console.log(data);
        }
    });
});
$("#id_suggest_btn").click(function() {
    var name_parts = $(id_suggest_field).val();
    console.log('name_parts=' + name_parts);
    name_parts = name_parts.split(/\s+/);
    console.log('name_parts=' + name_parts);
      
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
            createRadioElements(data.suggestions)
        },
    });
});
function createRadioElements(suggestions) {
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
