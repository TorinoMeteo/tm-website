"use strict";

window.tm = {};
window.tm.tmp = {};

/**
 * Format string function
 */
window.tm.format = function() {
    var string = Array.prototype.shift.apply(arguments);;
    var args = arguments;
    return string.replace(/{(\d+)}/g, function(match, number) { 
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
        ;
    });
};

tm.sameHeightColumns = function() {
    var columns = [];
    for(var i = 0; i < arguments.length; i++) {
        var arg = arguments[i];
        $(arg).each(function () {
            columns.push($(this).height());
        })
    }
    var min = Math.min.apply(null, columns);
    for(var i = 0; i < arguments.length; i++) {
        var arg = arguments[i];
        $(arg).each(function () {
            $(this).height(min - parseInt($(this).css('margin-top'), 10));
        })
    }
}

/**
 * Renders station h24 graphs
 */
tm.render24Graphs = function(container, data, opts) {

    var height = (typeof opts == 'undefined' || typeof opts.height == 'undefined') ? 220 : opts.height;

    var $dom = {
        container: jQuery(container)
    };
    // GRAPHS
    $dom.graph_wrapper = jQuery('<div>', {id: 'rt-graph-wrapper'}).appendTo($dom.container);
    // labels
    $dom.temperature_label = jQuery('<div>', {'class': 'rt-label rt-temperature-label txt-rotate-ao active'}).text('T °C').appendTo($dom.graph_wrapper);
    $dom.pressure_label = jQuery('<div>', {'class': 'rt-label rt-pressure-label txt-rotate-ao'}).text('p hPa').appendTo($dom.graph_wrapper);
    $dom.relative_humidity_label = jQuery('<div>', {'class': 'rt-label rt-relative-humidity-label txt-rotate-o'}).text('RH %').appendTo($dom.graph_wrapper);
    $dom.rain_label = jQuery('<div>', {'class': 'rt-label rt-rain-label txt-rotate-o'}).text('Pr mm').appendTo($dom.graph_wrapper);
    var self = this;
    $dom.temperature_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); $dom.graph_rail.css('margin-top', '-0px') });
    $dom.pressure_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); $dom.graph_rail.css('margin-top', '-' + height + 'px') });
    $dom.relative_humidity_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); $dom.graph_rail.css('margin-top', '-' + (2 * height) + 'px') });
    $dom.rain_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); $dom.graph_rail.css('margin-top', '-' + (3 * height) + 'px') });
    // graphs
    $dom.graph_container = jQuery('<div>', {id: 'rt-graph-container'}).appendTo($dom.graph_wrapper);
    $dom.graph_rail = jQuery('<div>', {id: 'rt-graph-rail'}).appendTo($dom.graph_container);
    $dom.temperature_graph = jQuery('<div>', {id: 'rt-temperature-graph'}).appendTo($dom.graph_rail);
    $dom.pressure_graph = jQuery('<div>', {id: 'rt-pressure-graph'}).appendTo($dom.graph_rail);
    $dom.relative_humidity_graph = jQuery('<div>', {id: 'rt-relative_humidity-graph'}).appendTo($dom.graph_rail);
    $dom.rain_graph = jQuery('<div>', {id: 'rt-rain-graph'}).appendTo($dom.graph_rail);


    var dft_conf = {
        chart: {
            type: 'spline',
            backgroundColor: {
                linearGradient: [0, 0, 500, 500],
                stops: [
                    [0, 'rgba(255, 255, 255, 0.5)'],
                    [1, '#fff']
                ]
            },
            borderColor: '#fff',
            borderWidth: 1,
            marginBottom:50
        },
        title: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%H:%M'
            }
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        plotOptions: {
            spline: {
                lineWidth: 1,
            },
            marker: {
                enabled: false,
            }
        },
        legend: { enabled: false },
        credits: { enabled: false },
        series: [{
            data: []
        }]
    };

    var temperature_data = [];
    var pressure_data = [];
    var relative_humidity_data = [];
    var rain_rate_data = [];
    var rain_data = [];
    for(var i = 0, l = data.temperature.length; i < l; i++) {
        var r_t = data.temperature[i];
        var r_p = data.pressure[i];
        var r_rh = data.relative_humidity[i];
        var r_rr = data.rain_rate[i];
        var r_r = data.rain[i];
        var date_utc = Date.UTC(r_t.datetime_year, r_t.datetime_month-1, r_t.datetime_day, r_t.datetime_hour, r_t.datetime_minute, r_t.datetime_second);
        temperature_data.push([
            date_utc,
            parseFloat(r_t.value)
        ]);
        pressure_data.push([
            date_utc,
            parseFloat(r_p.value)
        ]);
        relative_humidity_data.push([
            date_utc,
            parseFloat(r_rh.value)
        ]);
        rain_rate_data.push([
            date_utc,
            parseFloat(r_rr.value)
        ]);
        rain_data.push([
            date_utc,
            parseFloat(r_r.value)
        ]);
    }

    // temperature
    var temperature_conf = dft_conf;
    // temperature_conf.title.text = 'Temperatura';
    temperature_conf.yAxis.title.text = 'Temperatura °C';
    temperature_conf.series = [{ name: 'Temperatura', data: temperature_data }];
    $dom.temperature_graph.highcharts(temperature_conf);

    // pressure
    var pressure_conf = dft_conf;
    // pressure_conf.title.text = 'Pressione';
    pressure_conf.yAxis.title.text = 'Pressione hPa';
    pressure_conf.series = [{ name: 'Pressione', data: pressure_data }];
    $dom.pressure_graph.highcharts(pressure_conf);

    // relative_humidity
    var relative_humidity_conf = dft_conf;
    // relative_humidity_conf.title.text = 'RH';
    relative_humidity_conf.yAxis.title.text = 'RH %';
    relative_humidity_conf.series = [{ name: 'RH', data: relative_humidity_data }];
    $dom.relative_humidity_graph.highcharts(relative_humidity_conf);

    // rain
    var rain_conf = {
        chart: {
            defaultSeriesType: 'column',
            backgroundColor: {
                linearGradient: [0, 0, 500, 500],
                stops: [
                    [0, 'rgba(255, 255, 255, 0.5)'],
                    [1, '#fff']
                ]
            },
            borderColor: '#fff',
            borderWidth: 1,
            marginBottom:50
        },
        title: {
            // text: 'Precipitazioni'
            text: ''
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%H:%M'
            }
        },
        yAxis: [
            {
                title: {
                    text: 'Precipitazione oraria (mm)'
                },
                min: 0,
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            {
                title: {
                    text: 'Accumulo precipitazioni (mm)'
                },
                min: 0,
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }],
                opposite: true
            }
        ],
        tooltip: {
            formatter: function() {
                return '<b>'+this.series.name+'</b><br/>'+Highcharts.dateFormat('%e %b %Y, %H:%M', this.x) +
                       ': <b>'+ this.y +'mm</b>';
            }
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: [0, 0, 0, 400],
                    stops: [
                        [0, 'rgb(153,255,0)'],
                        [1, 'rgba(2,0,0,0)']
                    ]
                },
                lineWidth: 1,
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 5
                        }
                    }
                },
                shadow: false,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                }
            }
        },
        legend: { enabled: false },
        credits: { enabled: false },
    };

    rain_conf.series = [{ name: 'prec. oraria', data: rain_rate_data }, { name: 'precip. accumulo', data: rain_data, yAxis: 1, type: 'area' }];
    $dom.rain_graph.highcharts(rain_conf);
}


tm.Modal = function(params) {

    var opts = {
        show_action_btn: false,
        action_btn_label: 'salva',
        action_btn_cb: function () {},
        on_url_loaded: function() {}
    }

    this.init = function(params) {
        this.modal = $('#dynamicModal');
        this.options = $.extend({}, opts, params);
        this.setStyle();
        this.setTitle();
        this.setContent();
        this.setButtons();
    };

    this.setStyle = function() {

        if(typeof this.options.style != 'undefined') {
            this.modal.addClass(this.options.style);
        }

    };

    this.setTitle = function() {

        if(typeof this.options.title != 'undefined') {
            this.modal.find('.modal-title').html(this.options.title);
        }

    };

    this.setContent = function() {
        var self = this;
        if(typeof this.options.url != 'undefined') {
            this.method = 'request';
            $.get(this.options.url, function(response) {
                self.modal.find('.modal-body').html(response);
                self.options.on_url_loaded(self);
            })
        }
        else if(typeof this.options.content != 'undefined') {
            self.modal.find('.modal-body').html(this.options.content);
        }
    };

    this.setButtons = function() {

        var action_btn = this.modal.find('.btn-action').unbind('click');
        if(typeof this.options.show_action_btn != 'undefined' && this.options.show_action_btn ) {
            action_btn.html(this.options.action_btn_label).on('click', this.options.action_btn_cb);
        }
        else {
            this.modal.find('.btn-action').hide();
        }
    };

    this.open = function() {
        this.modal.modal();
    };

    this.init(params);
}


/*
Uncomment this to get an opacity animation for the navbar element when scrolling
(function($) {
    $(window).on('scroll', function() {
        if(window.scrollY > 40) {
            $('.navbar-fixed-top').css('opacity', 0.7);
        }
        else {
            $('.navbar-fixed-top').css('opacity', 1);
        }
    });
    $(window).on('load', function() {
        $('.navbar-fixed-top').on('mouseover', function() { console.log($(this)); $(this).css('opacity', 1); })
        $('.navbar-fixed-top').on('mouseout', function() { $(this).css('opacity', window.scrollY > 40 ? 0.7 : 1); });
    });
})(jQuery);
*/
