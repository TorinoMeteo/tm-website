import requests
import json
from datetime import datetime, date, time

from .factory import parser_factory
from .labels import DATA_LABELS as DL


class DateTimeEncoder(json.JSONEncoder):
    """ Custom serializer for datetime not json serializable objects
    """
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, time):
            return o.strftime('%H:%M')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')

        return json.JSONEncoder.default(self, o)


class Data(dict):
    """ Wraps the python dict object to add convenience methods, i.e. as_json
    """
    def __init__(self, *args, **kwargs):
        """ Just add datetime key, date + time"""
        super(Data, self).__init__(*args, **kwargs)
        try:
            self[DL['DATETIME']] = datetime.combine(self[DL['DATE']], self[DL['TIME']]) # noqa
        except:
            self[DL['DATETIME']] = None

    def as_json(self):
        return json.dumps(self, cls=DateTimeEncoder)


def fetch(url):
    """ Fetches an url content
    """
    response = requests.get(url).text
    return response


def parse(content, type, **kwargs):
    """ Parses the given content base upon type
    """
    klass = parser_factory(type)(**kwargs)
    return Data(klass.parse(content))
