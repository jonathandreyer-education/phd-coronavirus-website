(function($){

    function update_numbers(confirmed, deaths, recovered) {
        $('.data-virus').html('Currently,<br>there is ' + confirmed + ' confirmed, ' + deaths + ' deaths and ' + recovered + ' recovered.');
	}

	function update_timestamp(ts) {
        $('.timestamp-virus').html('Last data on ' + ts + '.');
	}

    window.addEventListener('load', function() {
        update_data();

        function update_data() {
            $.ajax({
                url : '/api/latest',
                type : 'GET',
                dataType : 'json',
                success : function(response) {
                    data = response['data'];
                    update_numbers(data['confirmed'], data['deaths'], data['recovered'],);
                    update_timestamp(response['timestamp']);
                    },
                error : function() {
                    console.log('Error to fetch data!');
                }
            });
        }

        setInterval(update_data, 5000);
    }, false);

    // chart
    window.addEventListener('resize', function(event){
        console.log('TODO need to redraw chart!');
    });

    // Set the dimensions of the canvas / graph
    var	margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 400 - margin.left - margin.right,
        height = 220 - margin.top - margin.bottom;

    // Parse the date / time
    var	parseDate = d3.time.format("%d-%b-%y").parse;

    // Set the ranges
    var	x = d3.time.scale().range([0, width]);
    var	y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var	xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);

    var	yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    // Define the line
    var	valuelineDeath = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.death); });
    var	valuelineConfirmed = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.confirmed); });
    var	valuelineRecovered = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.recovered); });

    // Adds the svg canvas
    var	chart = d3.select("#chartArea")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Get the data
    d3.csv("static/data.csv", function(error, data) {
        data.forEach(function(d) {
            //date,death,confirmed,recovered
            d.date = parseDate(d.date);
            d.death = +d.death;
            d.confirmed = +d.confirmed;
            d.recovered = +d.recovered;
        });

        var extents = ["death", "confirmed"].map(function(dimensionName) {
            return d3.extent(data, function(d) { return d[dimensionName] });
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([ 0, d3.max(data, function(d) { return Math.max.apply(Math, [d.death, d.confirmed, d.recovered]); })]);

        // Add the valueline path.
        chart.append("path")
            .attr("class", "line")
            .attr("d", valuelineDeath(data));
        chart.append("path")
            .attr("class", "line")
            .attr("d", valuelineConfirmed(data));
        chart.append("path")
            .attr("class", "line")
            .attr("d", valuelineRecovered(data));

        // Add the X Axis
        chart.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        chart.append("g")
            .attr("class", "y axis")
            .call(yAxis);
    });

})(jQuery);
