// Source: http://bl.ocks.org/d3noob/8952219, http://bl.ocks.org/Caged/6476579

// Parse the date / time
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// Notes from https://github.com/d3/d3/wiki/Time-Formatting
// var format = d3.time.format("%Y-%m-%d");
// format.parse("2011-01-01"); // returns a Date
// format(new Date(2011, 0, 1)); // returns a string

// Work on labels for x-axis
var margin ={top:20, right:30, bottom:200, left:60},
    width=814-margin.left - margin.right,
    height=500-margin.top-margin.bottom;

// scale to ordinal because x axis is not numerical
var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.1);


//scale to numerical value by height
var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
              .scale(x)
              .orient("bottom");  //orient bottom because x-axis will appear below the bars

var yAxis = d3.svg.axis()
              .scale(y)
              .orient("left");

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>Volume:</strong> <span style='color:red'>" + d.value + "</span>";
  });


// #chart
// var svg = d3.select("#bar-chart").append("svg")
//     .attr("width", width + margin.left + margin.right) //Set width
//     .attr("height", height + margin.top + margin.bottom)  //Set height
//   .append("g")
//     .attr("transform",
//           "translate(" + margin.left + "," + margin.top + ")");

// svg.call(tip);


// Making an AJAX call to get data from /data.json route
// d3.json("/data.json/" + timespan, renderChart);

function updateGraph(timespan) {
    console.log("Made it to updateGraph");
    d3.json("/data.json/" + timespan, renderChart);

}

// select.empty (jquery)
// select the svg element and empty it 

function type(d) {
  d.value = +d.value;
  return d;
}

// assign variable to a function
function renderChart(error, data) {
    console.log("This is data" + data);
    console.log("This is data 2" + JSON.stringify(data));
    debugger;
    data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.value = +d.value;
    });
  
  var svg = d3.select("#bar-chart").append("svg")
    .attr("width", width + margin.left + margin.right) //Set width
    .attr("height", height + margin.top + margin.bottom)  //Set height
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

  x.domain(data.map(function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) { return d.value; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Volume (shares)");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.date); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); })
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);

}

updateGraph(24);
