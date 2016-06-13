function updateGraph2(timespan) {
    console.log("Made it to updateGraph2");
    // Get the data
    d3.json("/scatterdata.json/" + timespan, renderChart2);
  }

// assign variable to a function
function renderChart2(error, data) {
    console.log("This is data" + data);
    console.log("This is data 2" + JSON.stringify(data));
    // change string (from JSON) into number and datetime format
    data.forEach(function(d) {
        d.datetime = parseDate(d.datetime);
        d.sentiment = +d.sentiment;
        console.log(d.datetime);
    });
    
     // Set the ranges
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    // Define the line
    var valueline = d3.svg.line()
        .x(function(d) { return x(d.datetime); })
        .y(function(d) { return y(d.sentiment); });
        
    // Adds the svg canvas
    var svg = d3.select("#scatter")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    
    // add the tooltip area to the webpage
    // var tooltip = d3.select("#scatter").append("div")
    //   .attr("class", "tooltip")
    //   .style("opacity", 0);

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.datetime; }));
    y.domain([0, d3.max(data, function(d) { return d.sentiment; })]);

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));

    // Add the scatterplot
    svg.selectAll("dot")
        .data(data)
      .enter().append("circle")
        .attr("r", 3.5)
        .attr("cx", function(d) { return x(d.datetime); })
        .attr("cy", function(d) { return y(d.sentiment); });

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

}

updateGraph2(24);
