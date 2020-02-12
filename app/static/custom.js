(function($){

    function update_numbers(confirmed, deaths, recovered) {
        $('.data-virus').html('Currently,<br>there is ' + confirmed + ' confirmed, ' + deaths + ' deaths and ' + recovered + 'recovered.');
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
                complete: function() {
                    setInterval(update_data, 5000);
                }
            });

        }
    }, false);
})(jQuery);
