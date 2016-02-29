var Charts = function () {

    return {
        initBarCharts: function (data) {
            var options = {
				series:{
					bars:{
						show: true
					}
				},
				bars:{
					barWidth:0.6
				},
            };
 
            $.plot($("#bar-chart"), data, options);
        },
    };

}();