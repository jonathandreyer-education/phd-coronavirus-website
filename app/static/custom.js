(function($){

    function update_numbers(confirmed, deaths, recovered) {
        $('.data-virus').html('Today there are ' + confirmed + ' confirmed, ' + deaths + ' dead and ' + recovered + ' recovered individuals in relation to the current coronavirus (nCov-2019).');
	}

	function update_timestamp(ts) {
        $('.timestamp-virus').html('Last data on ' + ts + '.');
	}

	function draw_chart() {
        // Set the dimensions of the canvas / graph
        var	margin = {top: 30, right: 20, bottom: 30, left: 50},
            width = $("#chartArea").width() - margin.left - margin.right,
            height = $("#chartArea").height() - margin.top - margin.bottom;

        // Parse the date / time
        var	parseDate = d3.time.format("%d/%m/%Y %H:%M:%S").parse;

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
            .y(function(d) { return y(d.value); });
        var	valuelineConfirmed = d3.svg.line()
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.value); });
        var	valuelineRecovered = d3.svg.line()
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.value); });

        // Adds the svg canvas
        d3.select("#chartArea").select("svg").remove();

        var	chart = d3.select("#chartArea")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Get the data
        d3.json("api/timeseries", function(error, datajson) {
            var categories = ['deaths', 'confirmed', 'recovered'];
            var data = {};

            categories.forEach(function (c) {
                var _ = [];
                datajson[c].forEach(function(d) {
                    var _d = {};
                    _d.date = parseDate(d.timestamp);
                    _d.value = +d.value;
                    _.push(_d);
                });
                data[c] = _;
            });

            // Scale the range of the data
            var dates = [];
            categories.forEach(function (c) {
                data[c].forEach(function (d) {
                    dates.push(d.date);
                })
            });
            var values = [];
            categories.forEach(function (c) {
                data[c].forEach(function (d) {
                    values.push(d.value);
                })
            });

            // Scale the range of the data
            x.domain(d3.extent(dates));
            y.domain([ 0, d3.max(values)]);

            // Add the valueline path.
            chart.append("path")
                .attr("class", "line")
                .style("stroke", "green")
                .attr("d", valuelineDeath(data.deaths));
            chart.append("path")
                .attr("class", "line")
                .style("stroke", "blue")
                .attr("d", valuelineConfirmed(data.confirmed));
            chart.append("path")
                .attr("class", "line")
                .style("stroke", "red")
                .attr("d", valuelineRecovered(data.recovered));

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
    }

    window.addEventListener('load', function() {
        update_data();
        draw_chart();

        function update_data() {
            $.ajax({
                url : '/api/latest',
                type : 'GET',
                dataType : 'json',
                success : function(response) {
                    data = response['data'];
                    update_numbers(data['confirmed'], data['deaths'], data['recovered'],);
                    update_timestamp(response['timestamp']);
                    draw_chart();
                    },
                error : function() {
                    console.log('Error to fetch data!');
                }
            });
        }

        setInterval(update_data, intervalRefresh * 1000);
    }, false);

    // chart
    window.addEventListener('resize', function(event){
        draw_chart();
    });

})(jQuery);
