var Charts = function () {
    return {
        initPieCharts: function (data) {
            $.plot($(".pie_chart"), data, {
				series: {
					pie: {
						show: true,
						radius: 1,
						label: {
							show: true,
							radius: 3 / 4,
							formatter: function (label, series) {
								return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">' + label + '<br/>' + Math.round(series.percent) + '%</div>';
							},
							background: {
								opacity: 0.5,
								color: '#000'
							}
						}
					}
				},
				legend: {
					show: false
				}
			});
        }
    };

}();