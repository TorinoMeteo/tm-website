""" Defines Parser Settings
"""

EXTREMES = {
    'TEMP': {
        'MAX': 47.0,
        'MIN': -30.0
    },
    'HUMIDITY': {
        'MAX': 100.0,
        'MIN': 5.0
    },
    'DEW': {
        'MAX': 40.0,
        'MIN': -40.0
    },
    'PRESSURE': {
        'MAX': 1070.0,
        'MIN': 800.0
    },
    'WIND': {
        'MAX': 170.0,
        'MIN': 0.0
    },
    'WIND_DIR': {
        'MAX': 360.0,
        'MIN': 0.0,
        'TEXT': ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'], # noqa
        'TEXT_I': ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSO', 'SO', 'OSO', 'O', 'OOO', 'NO', 'NNO'] # noqa
    },
    'RAIN': {
        'MAX': 250.0,
        'MIN': 0.0
    },
    'RAIN_RATE': {
        'MAX': 400.0,
        'MIN': 0.0
    }
}
