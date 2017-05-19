//"use strict";

window.torinometeo = window.torinometeo || {};
torinometeo.realtime = torinometeo.realtime || {};

/**
 * Class to manage the relatime stations jumbotron
 *
 * @param string container_id id attribute of the container
 * @param array id_stations station ids array
 * @param array name_stations station name array
 */
torinometeo.realtime.Jumbotron = function(container_id, id_stations, name_stations, url_stations, options)
{
    var opts = {
        'base_url': '/realtime/jumbotron/station/'
    };

    /* cache object */
    this.$cache = {};
    /* current station index */
    this.$index = -1;
    /* station selection layer status */
    this.$selection_open = false;

    /**
     * Constructor
     */
    this.init = function(container_id, id_stations, name_stations, options) {

        this.$dom = {};
        this.$dom.container = jQuery('#' + container_id);
        this._id_stations = id_stations;
        this._name_stations = name_stations;
        this._url_stations = url_stations;
        this.$last_index = id_stations.length - 1;
        this.options = jQuery.extend({}, opts, options);

        /* LAYOUT */
        this.$dom.title_container = jQuery('<div>', {'class': 'station-title clearfix'}).appendTo(this.$dom.container);
        this.$dom.title = jQuery('<h1>', {'class': ''}).appendTo(this.$dom.title_container);
        this.$dom.title.on('click', jQuery.proxy(this.stationSelection, this));
        this.$dom.geo = jQuery('<p>', {'class': 'geo pull-left'}).appendTo(this.$dom.container);
        this.$dom.date = jQuery('<time>').appendTo(jQuery('<p>', {'class': 'pull-left time'}).appendTo(this.$dom.container));
        this.$dom.detail = jQuery('<p>', {'class': 'pull-left'}).appendTo(this.$dom.container);
        this.$dom.clear = jQuery('<div>', {'class': 'clearfix'}).appendTo(this.$dom.container);
        this.$dom.bookmark = jQuery('<a>', {'class': 'fa fa-bookmark-o'}).appendTo(this.$dom.title_container);
        this.$dom.next_arrow = jQuery('<span>', {'class': 'arrow arrow-next fa fa-angle-double-right hidden'})
            .on('click', jQuery.proxy(this.goNext, this))
            .appendTo(this.$dom.title_container);
        this.$dom.prev_arrow = jQuery('<span>', {'class': 'arrow arrow-prev fa fa-angle-double-left hidden'})
            .on('click', jQuery.proxy(this.goPrev, this))
            .appendTo(this.$dom.title_container);

        // columns
        this.$dom.col1 = jQuery('<div>', {'class': 'col-lg-3 col-md-6 hidden-sm-down'}).appendTo(this.$dom.container);
        this.$dom.col2 = jQuery('<div>', {'class': 'col-lg-4 col-md-6 col-sm-12'}).appendTo(this.$dom.container);
        this.$dom.col3 = jQuery('<div>', {'class': 'col-lg-2 col-md-6 col-sm-6 col-xs-6'}).appendTo(this.$dom.container);
        this.$dom.col4 = jQuery('<div>', {'class': 'col-lg-3 col-md-6 col-sm-6 col-xs-6'}).appendTo(this.$dom.container);

        // image
        this.$dom.station_image = jQuery('<div>', {'class': 'station-img'}).appendTo(this.$dom.col1);

        // GRAPHS
        this.$dom.graph_wrapper = jQuery('<div>', {id: 'rt-graph-wrapper'}).appendTo(this.$dom.col2);
        // labels
        this.$dom.temperature_label = jQuery('<div>', {'class': 'rt-label rt-temperature-label txt-rotate-ao active'}).text('T °C').appendTo(this.$dom.graph_wrapper);
        this.$dom.pressure_label = jQuery('<div>', {'class': 'rt-label rt-pressure-label txt-rotate-ao'}).text('p hPa').appendTo(this.$dom.graph_wrapper);
        this.$dom.relative_humidity_label = jQuery('<div>', {'class': 'rt-label rt-relative-humidity-label txt-rotate-o'}).text('RH %').appendTo(this.$dom.graph_wrapper);
        this.$dom.rain_label = jQuery('<div>', {'class': 'rt-label rt-rain-label txt-rotate-o'}).text('Pr mm').appendTo(this.$dom.graph_wrapper);
        var self = this;
        this.$dom.temperature_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); self.$dom.graph_rail.css('margin-top', '-0px') });
        this.$dom.pressure_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); self.$dom.graph_rail.css('margin-top', '-220px') });
        this.$dom.relative_humidity_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); self.$dom.graph_rail.css('margin-top', '-440px') });
        this.$dom.rain_label.on('click', function() { jQuery('.rt-label').removeClass('active'); jQuery(this).addClass('active'); self.$dom.graph_rail.css('margin-top', '-660px') });
        // graphs
        this.$dom.graph_container = jQuery('<div>', {id: 'rt-graph-container'}).appendTo(this.$dom.graph_wrapper);
        this.$dom.graph_rail = jQuery('<div>', {id: 'rt-graph-rail'}).appendTo(this.$dom.graph_container);
        this.$dom.temperature_graph = jQuery('<div>', {id: 'rt-temperature-graph'}).appendTo(this.$dom.graph_rail);
        this.$dom.pressure_graph = jQuery('<div>', {id: 'rt-pressure-graph'}).appendTo(this.$dom.graph_rail);
        this.$dom.relative_humidity_graph = jQuery('<div>', {id: 'rt-relative_humidity-graph'}).appendTo(this.$dom.graph_rail);
        this.$dom.rain_graph = jQuery('<div>', {id: 'rt-rain-graph'}).appendTo(this.$dom.graph_rail);
        // END GRAPHS

        // realtime data
        this.$dom.rt_data3 = jQuery('<div>', {'class': 'rt-data'}).appendTo(this.$dom.col3);
        this.$dom.rt_data_temperature = jQuery('<div>', {'class': 'rt-data-temperature'}).appendTo(this.$dom.rt_data3);
        this.$dom.rt_data_pressure = jQuery('<div>', {'class': 'rt-data-pressure'}).appendTo(this.$dom.rt_data3);
        this.$dom.rt_data_relative_humidity = jQuery('<div>', {'class': 'rt-data-relative-humidity'}).appendTo(this.$dom.rt_data3);

        this.$dom.rt_data4 = jQuery('<div>', {'class': 'rt-data rt-data2'}).appendTo(this.$dom.col4);
        this.$dom.rt_data_wind = jQuery('<div>', {'class': 'rt-data-wind'}).appendTo(this.$dom.rt_data4);
        this.$dom.rt_data_rain_rate = jQuery('<div>', {'class': 'rt-data-rain'}).appendTo(this.$dom.rt_data4);
        this.$dom.rt_data_rain = jQuery('<div>', {'class': 'rt-data-rain'}).appendTo(this.$dom.rt_data4);

        // end realtime data
        this.$dom.clear = jQuery('<div>', {'class': 'clearfix'}).appendTo(this.$dom.container);

        // spinner
        this.$dom.spinner_overlay = jQuery('<div>', {'class': 'spinner-overlay hidden'}).appendTo(this.$dom.container);
        this.$dom.spinner = jQuery('<div>', {'class': 'spinner hidden'}).appendTo(this.$dom.container);
        // end spinner
    };

    /**
     * Popup to select station
     */
    this.stationSelection = function() {
        if(this.$selection_open) {
            this.$dom.selection_layer.remove();
            this.$selection_open = false;
            return false;
        }
        this.$selection_open = true;
        this.$dom.selection_layer = jQuery('<div>', {'class': 'station-selection-layer'}).appendTo(this.$dom.title);
        var ul = jQuery('<ul>').appendTo(this.$dom.selection_layer);
        for(var i = 0, l = this._id_stations.length; i < l; i++) {
            var id = this._id_stations[i];
            var name = this._name_stations[i];
            var self = this;
            var li = jQuery('<li>').text(name)
                .bind('click', {index: i}, function(evt) {
                    self.loadStation(evt.data.index);
                })
                .appendTo(ul);
        }

    }

    /**
     * Loads the component
     */
    this.load = function() {
        this.loadStation(0);
    };

    /**
     * Loads the next station
     */
    this.goNext = function() {
        this.loadStation(this.$index + 1);
    }

    /**
     * Loads the prev station
     */
    this.goPrev = function() {
        this.loadStation(this.$index - 1);
    }

    /**
     * Loads the given station
     * @param int index
     */
    this.loadStation = function(index) {
        this.showSpinner();
        this.$index = index;
        if(typeof(this.$cache[this.$index]) !== 'undefined') {
            this.renderStation(this.$cache[this.$index]);
        }
        else {
            jQuery.getJSON(this.options.base_url + this._id_stations[this.$index], jQuery.proxy(this.renderStation, this));
        }
    }

    this.renderValue = function(value) {
        if (value === null || value === 'null') {
            return 'ND';
        }
        return value;
    }

    /**
     * Renders the station data
     * @param object data json data
     */
    this.renderStation = function(data) {

        if(typeof(this.$cache[this.$index]) === 'undefined') {
            this.$cache[this.$index] = data;
        }

        // infos and strings
        this.$dom.title.text(data.name);
        var geo_a = [data.nation, data.region];
        if(data.province) geo_a.push(data.province);
        this.$dom.geo.text(geo_a.join(' » '));
        if(data.data_date) {
            this.$dom.date.text(this.formatDate(data.data_date));
        }
        else {
            this.$dom.date.html('<strong>Dati non disponibili</strong>');
        }
        this.$dom.detail.html('<a href="' + this._url_stations[this.$index] + '"><i class="fa fa-plus-circle"></i></a>');
        // bookmarks
        clickNoAuthFn = function () {
            new tm.Modal({ url: '/account/?action=bookmark', title:'Sign In/Up', show_action_btn: false }).open();
        }
        var self = this
        var clickAddFn = function () {
            $.getJSON('/preferiti/aggiungi/stazione/' + data.id, function (data) {
                if (data.status === 'ok') {
                    self.$cache[self.$index]['bookmarked'] = true;
                    self.$dom.bookmark.removeClass('fa-bookmark-o').addClass('fa-bookmark')
                    self.$dom.bookmark.off('click');
                    self.$dom.bookmark.on('click', clickRemoveFn)
                }
            })
        }
        var clickRemoveFn = function () {
            $.getJSON('/preferiti/rimuovi/stazione/' + data.id, function (data) {
                if (data.status === 'ok') {
                    self.$cache[self.$index]['bookmarked'] = false;
                    self.$dom.bookmark.removeClass('fa-bookmark').addClass('fa-bookmark-o')
                    self.$dom.bookmark.off('click');
                    self.$dom.bookmark.on('click', clickAddFn)
                }
            })
        }
        if(data.bookmarked) {
            this.$dom.bookmark.removeClass('fa-bookmark-o').addClass('fa-bookmark').off('click');
            this.$dom.bookmark.on('click', data.authenticated ? clickRemoveFn : clickNoAuthFn)
        }
        else {
            this.$dom.bookmark.removeClass('fa-bookmark').addClass('fa-bookmark-o').off('click');
            this.$dom.bookmark.on('click', data.authenticated ? clickAddFn : clickNoAuthFn)
        }

        // graphs
        this.renderStationGraphs(data);
        // image
        this.$dom.station_image.css({
            'background-image': 'url(' + data.image_url + ')',
            'background-position': 'center center',
            'background-repeat': 'no-repeat',
            'background-size': 'cover'
        });
        // raltime data
        if(data.data) {
            this.$dom.rt_data_temperature.html(
                '<i class="wi wi-thermometer"></i> <span data-heat="' + this.heatClass(data.data.temperature) + '">' + this.renderValue(data.data.temperature) + '</span>' + ' <span>°C</span>');
            this.$dom.rt_data_pressure.html(
                '<i class="wi wi-barometer"></i> ' + '<span data-heat="">' + this.renderValue(data.data.pressure) + '</span>' + ' <span>hPa</span>');
            this.$dom.rt_data_relative_humidity.html(
                '<i class="wi wi-humidity"></i> ' + '<span data-heat="">' + this.renderValue(data.data.relative_humidity) + '</span>' + ' <span>%</span>');
            this.$dom.rt_data_wind.html(
                '<i class="wi wi-windy"></i> ' + '<span data-heat="">' + this.renderValue(data.data.wind_strength) + '</span>' + ' <span>Km/h</span>' + ' ' + '<span data-heat="">' + this.renderValue(data.data.wind_dir_text) + '</span>');
            this.$dom.rt_data_rain_rate.html(
                '<i class="wi wi-raindrops"></i> ' + '<span data-heat="">' + this.renderValue(data.data.rain_rate) + '</span>' + ' <span>mm/h</span>');
            this.$dom.rt_data_rain.html(
                '<i class="wi wi-umbrella"></i> ' + '<span data-heat="">' + this.renderValue(data.data.rain) + '</span>' + ' <span>mm</span>');
        }
        else {
            this.$dom.rt_data_temperature.html('<i class="wi wi-thermometer"></i> ND')
            this.$dom.rt_data_pressure.html('<i class="wi wi-barometer"></i> ND')
            this.$dom.rt_data_relative_humidity.html('<i class="wi wi-humidity"></i> ND')
            this.$dom.rt_data_wind.html('<i class="wi wi-windy"></i> ND')
            this.$dom.rt_data_rain_rate.html('<i class="wi wi-raindrops"></i> ND')
            this.$dom.rt_data_rain.html('<i class="wi wi-umbrella"></i> ND')
        }

        this.$index == 0 ? this.$dom.prev_arrow.addClass('hidden') : this.$dom.prev_arrow.removeClass('hidden');
        this.$index == this.$last_index ? this.$dom.next_arrow.addClass('hidden') : this.$dom.next_arrow.removeClass('hidden');
        this.hideSpinner();
    }

    /**
     * Css class depending upon temperature value
     */
    this.heatClass = function(value) {
        if(value < 0) return 'vcold';
        if(value < 10) return 'cold';
        if(value < 18) return 'warm';
        if(value < 25) return 'hot';
        return 'vhot';
    }

    /**
     * Date formatting
     * @param string date
     * @return formatted date, string
     */
    this.formatDate = function(date) {
        var text_months = {
            1: 'gennaio',
            2: 'febbraio',
            3: 'marzo',
            4: 'aprile',
            5: 'maggio',
            6: 'giugno',
            7: 'luglio',
            8: 'agosto',
            9: 'settembre',
            10: 'ottobre',
            11: 'novembre',
            12: 'dicembre',
        };

        var date_split = date.split(' '),
            date = date_split[0],
            time = date_split[1];
        var date_split = date.split('/'),
            day = date_split[0],
            month = date_split[1];
        var time_split = time.split(':'),
            hour = time_split[0],
            minute = time_split[1];

        return day + ' ' + text_months[parseInt(month)] + ', ore ' + hour + ':' + minute;
    }

    /**
     * Renders station h24 graphs
     */
    this.renderStationGraphs = function(data) {

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
        for(var i = 0, l = data.day_data.temperature.length; i < l; i++) {
            var r_t = data.day_data.temperature[i];
            var r_p = data.day_data.pressure[i];
            var r_rh = data.day_data.relative_humidity[i];
            var r_rr = data.day_data.rain_rate[i];
            var r_r = data.day_data.rain[i];
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
        this.$dom.temperature_graph.highcharts(temperature_conf);

        // pressure
        var pressure_conf = dft_conf;
        // pressure_conf.title.text = 'Pressione';
        pressure_conf.yAxis.title.text = 'Pressione hPa';
        pressure_conf.series = [{ name: 'Pressione', data: pressure_data }];
        this.$dom.pressure_graph.highcharts(pressure_conf);

        // relative_humidity
        var relative_humidity_conf = dft_conf;
        // relative_humidity_conf.title.text = 'RH';
        relative_humidity_conf.yAxis.title.text = 'RH %';
        relative_humidity_conf.series = [{ name: 'RH', data: relative_humidity_data }];
        this.$dom.relative_humidity_graph.highcharts(relative_humidity_conf);

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
        this.$dom.rain_graph.highcharts(rain_conf);
    }

    /**
     * Shows the loading spinner
     */
    this.showSpinner = function() {
        this.$dom.spinner_overlay.removeClass('hidden');
        this.$dom.spinner.removeClass('hidden');
    };

    /**
     * Hides the loading spinner
     */
    this.hideSpinner = function() {
        this.$dom.spinner_overlay.addClass('hidden');
        this.$dom.spinner.addClass('hidden');
    }

    this.init(container_id, id_stations, name_stations, options);
}
