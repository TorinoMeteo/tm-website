# fetch module for TorinoMeteo station data

Module used to fetch and parse station data from external urls.

## Usage

Somewhere in your code:

    from fetch_station_data.shortcuts import fetch_data

    data = fetch_data(
        station.data_url,
        station.data_type.name,
        time_format=station.data_time_format,
        date_format=station.data_date_format,
    )
    json_data = data.as_json()

## Submodules

### shortcuts

**fetch_data(url, type): dict**
- url: string
- type: string

fetches, parses and returns data of format type from url

### core

**Data(dict)**
wrapper of the dictionary data type, which adds some convenient methods:

- **as_json(): json**
  returns dictionary in a json format

**fetch(url): string**
- url: string

Fetches and retreives the url content

**parse(content, type): Data**
- content: string
- type: string
Parses the content of format type and retrieves a Data object

### factory

**parser_factory(type): object**
- type: string
Factory method which returns the appropriate parsing class given the content type

### labels

Defines the labels to be used as exported data keys in one place

### parsers.*

All the parser classes, one file for each content type. Same interface, defined by `abstract.Parser`:

**parse(content): dict**
parses content and returns a dictionary of data

## Development

Clone the repo:

    $ https://github.com/TorinoMeteo/fetch_station_data.git

Create a virtualenv

    $ mkdir .virtualenv
    $ cd .virtualenv
    $ virtualenv --no-site-packages .
    $ source bin/activate
    $ cd ..

Install requirements

    $ pip install -r fetch_station_data/requirements.txt

Create a python file

    $ touch main.py

With the following content:


    from fetch_station_data.shortcuts import fetch_data

    data = fetch_data(
        'http://danielemeteo.altervista.org/wx.txt',
        'txt-wd',
        time_format='%H:%M %p',
        date_format='%d/%m/%y',
    )
    json_data = data.as_json()
    print json_data

You're ready to go

    (.virtualenv)abidibo@abidibo-K56CM:~/Web/www/tests/fetch$ python main.py 
    {"temp": 11.5, "temp_max": 11.5, "temp_min": 1.1, "datetime": "2016-12-10 15:00:00", "time": "15:00", "date": "2016-12-10"}
    (.virtualenv)abidibo@abidibo-K56CM:~/Web/www/tests/fetch$


### How to add a parser

- add the 'type' condition in the `fetch.factory.parser_factory` function
- add a file in the `fetch.parsers` module implementing the `fetch.parsers.abstract.Parser` interface
