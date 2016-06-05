// $('form').submit(function(){
//     //alert($('input[name=year]:checked').val());
  
//     alert($(this).serialize());
  
//     return false;
// });

// function renderChart(timespan) {
//     var chart = timespan;
//     $('#chart').html(chart);
// }

// row 15-24 needs review
// function getTimespan(evt) {
//     console.log("Made it here");
//     var timespan = $(this).val();
//     console.log(timespan);
//     $.get('/data.json/'+ timespan, function (data) {
//         renderChart(data);
//     });
// }

// $('.timespan-button').click(getTimespan);


// This was working...
function alertMe(evt) {
    console.log("Made it here");
    $('#bar-chart').empty();
    var timespan = $(this).val();
    console.log(timespan);
    $.get("/data.json/"+ timespan, function (data) {
        updateGraph(timespan);  //need to clear data before calling updateGraph
    });
    // alert(timespan);
}

$('.timespan-button').click(alertMe);
    

//Making AJAX call to get data



// function refreshGraph