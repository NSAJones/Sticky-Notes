function get_notes(){
    // Get list of notes
    let notes = $("#notes").children();
    var note_data = [];
    let id;
    let text;

    // Process DOM into dict
    $("textarea").each(function(){
        id = $(this).attr("id").split("_")[1];
        id = parseInt(id);
        text = $(this).val();
        note_data.push({
            "id":id,
            "text":text
        })
    })

    let csrftoken = $("[name='csrfmiddlewaretoken']").val()
    console.log(csrftoken)

    // Send POST request to the same url
    let data = {
        "notes":note_data
    }
    let url = window.location.href;

    console.log(note_data)

    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType:    "json",
        beforeSend: function(request){
            request.setRequestHeader("x-CSRFToken", csrftoken)
        }
        
    });
}