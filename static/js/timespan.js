
function alertMe(evt) {
    console.log("Made it here");
    $('#bar-chart').empty();
    var timespan = $(this).val();
    console.log(timespan);
    $.get("/data.json/"+ timespan, function (data) {
        updateGraph(timespan);  //need to clear data before calling updateGraph
    });
}

//Making AJAX call to get data

$('.timespan-button').click(alertMe);