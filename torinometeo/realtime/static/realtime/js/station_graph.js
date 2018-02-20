"use strict";

(function($) {
    window.tm.StationChart = function(render_to, input_from, input_to, redraw_button, api_url, opts) {

        var self = this;

        this.opts = opts;
        this.render_to = $(render_to);
        this.input_from = $(input_from);
        this.input_to = $(input_to);
        this.redraw_button = $(redraw_button);
        this.api_url = api_url;

        $(this.redraw_button).click(function() {
            self.update();
        });

        this.update = function() {
            var from_date = this.input_from.val();
            var to_date = this.input_to.val();
            if (!from_date || !to_date) {
                var alert_div = $('<div />', {
                    'class': 'alert alert-danger text-center'
                }).text('Inserire le date Da A');
                this.redraw_button.parent().after(alert_div);
                setTimeout(function () { alert_div.remove() }, 2000);
            } else {
                var data = this.fetchData( from_date, to_date, this.renderChart );
            }
        };

        this.fetchData = function(from_date, to_date, callback) {
            var url = this.api_url + '?from_date=' + from_date + '&to_date=' + to_date;
            $.getJSON(url, function(data) {
                callback.call(self, data, from_date, to_date);
            });
        };

        this.renderChart = function(data, from_date, to_date) {

            var tmax_color = '#ff0000',
                tmin_color = '#0000ff',
                tmean_color = '#666',
                p_color = '#00ff00',
                r_color = '#0000aa';

            var data_temp_mean = [],
                data_temp_max = [],
                data_temp_min = [],
                data_press_mean = [],
                data_rain = [],
                data_rain_sum = [];
            var indexes = {};

            var rain_sum_partial = 0;
            for (var i = 0, len = data.length; i < len; i++) {
                var record = data[i];
                var utc = moment(record.date).valueOf();
                data_temp_mean.push([utc, parseFloat(record['temperature_mean'])]);
                data_temp_max.push([utc, parseFloat(record['temperature_max'])]);
                data_temp_min.push([utc, parseFloat(record['temperature_min'])]);
                data_press_mean.push([utc, parseFloat(record['pressure_mean'])]);
                data_rain.push([utc, parseInt(record['rain'], 10)]);
                rain_sum_partial = rain_sum_partial + parseInt(record['rain'], 0);
                data_rain_sum.push([utc, rain_sum_partial]);
                indexes[utc] = i;
            }

            this.chart = new Highcharts.Chart({
                time : {
                    timezone: 'Europe/Rome'
                },
                chart: {
                    renderTo: this.render_to.attr('id'),
                    zoomType: 'x',
                    plotBackgroundColor: 'rgba(255, 255, 255, .9)',
                    marginBottom: 80
                },
                title: {
                    text: window.tm.format('Grafico periodo dal {0} al {1}', from_date, to_date)
                },
                subtitle: {
                    text: tm.format('Stazione meteo "{0}"', this.opts.station_name)
                },
                xAxis: {
                    type: 'datetime',
                },
                yAxis: [
                    { // temperature axis
                        /*labels: {
                            format: '{value}°C',
                        },*/
                        title: {
                            text: 'Temperatura (°C)',
                        }
                    },
                    { // pressure axis
                        /*labels: {
                            format: '{value}hPa',
                        },*/
                        title: {
                            text: 'Pressione (hPa)'
                        },
                        opposite: false
                    },
                    { // rain axis
                        /*labels: {
                            format: '{value}mm',
                        },*/
                        title: {
                            text: 'Precipitazioni (mm)'
                        },
                        min: 0,
                        opposite: true
                    },
                    { // rain sum axis
                        /*labels: {
                            format: '{value}mm',
                        },*/
                        title: {
                            text: 'Accumulo (mm)'
                        },
                        min: 0,
                        opposite: true
                    }
                ],
                tooltip: {
                    shared: true,
                    crosshairs: true
                },
                plotOptions: {
                    series: {
                        cursor: 'pointer',
                        marker: { lineWidth: 1, radius: 3 },
                        point: {
                            events: {
                                click: function (e) {
                                    $('#modal-title').text(Highcharts.dateFormat('%A, %b %e, %Y', this.x));

                                    var utc = moment(Highcharts.dateFormat('%Y-%m-%d', this.x)).valueOf();
                                    var text = tm.format(
                                        "<p><table class=\"table table-striped table-hover modal-daydata\"><thead><tr><td></td><td><i class=\"fa fa-arrow-up\"></i> max</td><td><i class=\"fa fa-arrow-down\"></i> min</td><td><i class=\"fa fa-arrows-v\"></i> media</td></tr></thead><tr><td><i class=\"wi wi-2x wi-thermometer\"></i></td><td style=\"color: " + tmax_color + "\">{0} °C</td><td style=\"color: " + tmin_color + "\">{1} °C</td><td style=\"color: " + tmean_color + "\">{2} °C</td></tr><tr><td><i class=\"wi wi-barometer\"></i></td><td>{3} hPa</td><td>{4} hPa</td><td style=\"color: " + p_color + "\">{5} hPa</td></tr><tr><td><i class=\"wi wi-humidity\"></i></td><td>{6} %</td><td>{7} %</td><td>{8} %</td></tr><tr><td><i class=\"wi wi-raindrops\"></i></td><td style=\"color: " + r_color + "\" colspan=\"3\">{9} mm</td></tr></table>",
                                        data[indexes[utc]].temperature_max,
                                        data[indexes[utc]].temperature_min,
                                        data[indexes[utc]].temperature_mean,
                                        data[indexes[utc]].pressure_max,
                                        data[indexes[utc]].pressure_min,
                                        data[indexes[utc]].pressure_mean,
                                        data[indexes[utc]].relative_humidity_max,
                                        data[indexes[utc]].relative_humidity_min,
                                        data[indexes[utc]].relative_humidity_mean,
                                        data[indexes[utc]].rain
                                    );
                                    $('#modal-body').html(text);
                                    $('#graphModal').modal();
                                }
                            }
                        }
                    }
                },
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom',
                    floating: true,
                    borderColor: '#eee',
                    backgroundColor: '#eee',

                },
                series : [{
                    name: 'Temperatura media',
                    type: 'spline',
                    data: data_temp_mean,
                    color: '#666',
                    zIndex: 6,
                    tooltip: {
                        valueSuffix: '°C'
                    }
                }, {
                    name: 'Temperatura massima',
                    type: 'spline',
                    data: data_temp_max,
                    color: '#ff0000',
                    zIndex: 5,
                    tooltip: {
                        valueSuffix: '°C'
                    }
                },{
                    name: 'Temperatura minima',
                    type: 'spline',
                    data: data_temp_min,
                    color: '#0000ff',
                    zIndex: 4,
                    tooltip: {
                        valueSuffix: '°C'
                    }
                },
                {
                    name: 'Pressione media',
                    yAxis: 1,
                    type: 'spline',
                    data: data_press_mean,
                    color: '#00ff00',
                    dashStyle: 'Dash',
                    zIndex: 3,
                    tooltip: {
                        valueSuffix: 'hPa'
                    }
                },
                {
                    name: 'Precipitazioni',
                    yAxis: 2,
                    type: 'column',
                    data: data_rain,
                    color: '#0000aa',
                    zIndex: 1,
                    tooltip: {
                        valueSuffix: 'mm'
                    }
                },
                {
                    name: 'Accumulo',
                    yAxis: 3,
                    type: 'area',
                    data: data_rain_sum,
                    color: '#80ffff',
                    zIndex: 2,
                    tooltip: {
                        valueSuffix: 'mm'
                    }
                }
                ]

            });
        };

        this.update();


    };
})(jQuery)

/*
        chart = new Highcharts.Chart({

            xAxis: [{
                categories: [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, ],
				gridLineWidth: 1,
				lineColor: '#000',
				tickColor: '#000'
            }],
			labels: {
                  items: [{
                  html: 'Temperatura media: <strong>19.1°C</strong> - Pioggia mese: <strong>51.0 mm</strong>',
                  style: {
                  left: '0px',
                  top: '375px',
                  color: '#3E576F'            
                        }
                        }]
                },
            yAxis: [{ // Primary yAxis
                labels: {
                    formatter: function() {
                        return this.value +'°C';
                    },
                    style: {
                        color: '#4572A7'
                    }
                },
                plotLines: [{
					color: 'gray',
					dashStyle: 'solid',
					width: 2,
					value: 0
				}],
				lineColor: '#000',
				lineWidth: 1,
				tickWidth: 1,
				tickColor: '#000',
                title: {
                    text: 'Temperatura',
                    style: {
                        color: '#4572A7'
                    }
                }
            }, { // Secondary yAxis
                title: {
                    text: 'Pioggia',
                    style: {
                        color: '#4572A7'
                    }
                },
                lineColor: '#000',
				lineWidth: 1,
				tickWidth: 1,
				tickColor: '#000',
                labels: {
                    formatter: function() {
                        return this.value +' mm';
                    },
                    style: {
                        color: '#4572A7'
                    }
                },
                opposite: true
            }, { // Tertiary yAxis
                gridLineWidth: 0,
                title: {
                    text: 'Pressione',
                    style: {
                        color: '#AA4643'
                    }
                },
                labels: {
                    formatter: function() {
                        return this.value +' hPa';
                    },
                    style: {
                        color: '#AA4643'
                    }
                },
                opposite: true
            }],
            tooltip: {
                formatter: function() {
                    var unit = {
                        'Pioggia': ' mm',
                        'Temperatura media': '°C',
                        'Temperatura massima': '°C',
                        'Temperatura minima': '°C',
                        'Pressione': ' hPa'
                    }[this.series.name];
    
                    return ''+
                        '<span style="font-size:11px; color:' + this.series.color + '">'+this.series.name+'</span><br>'+ this.x +' Settembre: <strong>'+ this.y + unit + '</strong>';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 70,
                verticalAlign: 'top',
                y: 0,
                floating: true,
                backgroundColor: '#FFFFFF'
            },
			exporting: {
            width: 960
			},
            series: [{
                name: 'Pioggia',
                color: '#00FFFF',
                type: 'column',
                borderWidth: 1,
				borderColor: 'rgb(1, 158, 158)',
                yAxis: 1,
                data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 44.7, 1.5, 0.0, 1.0, 3.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ]
    
            }, {
                name: 'Pressione',
                type: 'spline',
                color: '#AA4643',
                yAxis: 2,
                data: [1013.9, 1011.8, 1012.3, 1013.3, 1012.5, 1018.5, 1020.5, 1021.3, 1018.2, 1017.5, 1020.7, 1022.8, 1017.3, 1009.8, 1011.7, 1011.9, 1010.2, 1015.0, 1018.3, 1017.6, 1016.2, 1010.8, 1007.6, 1015.1, 1015.8, 1018.7, 1023.0, 1027.1, ],
                marker: {
                    enabled: false
                },
                dashStyle: 'shortdot'
    
            }, {
                name: 'Temperatura media',
                color: '#89A54E',
                type: 'spline',
                data: [23.8, 23.7, 20.9, 20.7, 19.3, 19.5, 18.7, 18.5, 19.4, 19.3, 18.0, 19.4, 18.0, 19.4, 19.5, 17.4, 19.1, 20.3, 19.6, 19.9, 18.4, 17.3, 16.6, 17.4, 19.2, 18.1, 17.4, 16.6, ]
            }, {
                name: 'Temperatura massima',
                color: '#FF0000',
                type: 'spline',
                data: [27.3, 30.7, 24.4, 24.4, 24.4, 26.1, 23.9, 23.1, 23.5, 22.6, 19.7, 22.8, 22.3, 23.8, 22.6, 18.7, 22.3, 26.6, 24.6, 26.6, 23.9, 19.8, 20.1, 25.1, 27.6, 22.9, 20.0, 18.3, ]
            }, {
                name: 'Temperatura minima',
                color: '#0000FF',
                type: 'spline',
                data: [20.3, 19.9, 18.6, 15.9, 15.2, 14.2, 13.4, 14.4, 15.6, 16.8, 15.8, 17.2, 15.5, 16.0, 17.2, 16.8, 17.1, 16.3, 14.8, 13.1, 13.2, 14.9, 13.1, 10.5, 11.4, 13.1, 15.4, 15.2, ]
            }]
        });
    });
*/
