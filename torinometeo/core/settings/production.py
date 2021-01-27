'''This module sets the configuration for a local development

'''
import os
from datetime import timedelta

from celery.schedules import crontab

from .common import * # noqa

DEBUG = False

ALLOWED_HOSTS = ['ws.torinometeo.org', 'torinometeo.org', 'www.torinometeo.org', ] # noqa

HTTPS = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

STATIC_ROOT = '/home/torinometeo/www/torinometeo/static/'
MEDIA_ROOT = '/home/torinometeo/www/torinometeo/media/'
# CKEDITOR
CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + 'core/css/vendor.min.css',
    STATIC_URL + 'core/css/core.min.css',
    STATIC_URL + 'core/src/css/ckeditor.css']

LOGGING['handlers']['file']['filename'] = here('..', '..', '..', '..', os.path.join('logs', 'debug.log')) # noqa
LOGGING['handlers']['celery_logger']['filename'] = here('..', '..', '..', '..', os.path.join('logs', 'celery.log')) # noqa
LOGGING['handlers']['realtime_celery_logger']['filename'] = here('..', '..', '..', '..', os.path.join('logs', 'realtime.log')) # noqa

# CELERY
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_HIJACK_ROOT_LOGGER = False
CELERYBEAT_SCHEDULE = {
    'fetch-realtime-data': {
        'task': 'realtime.tasks.fetch_realtime_data',
        'schedule': timedelta(seconds=300),
        'args': ()
    },
    'clean-realtime-data': {
        'task': 'realtime.tasks.clean_realtime_data',
        'schedule': crontab(hour=0, minute=1, day_of_week=1),  # every monday morning # noqa
        'args': ()
    },
    'store-historic-data': {
        'task': 'realtime.tasks.store_historic_data',
        'schedule': crontab(minute=10, hour=0),  # every day 00:10
        'args': ()
    },
    'fetch-radar-images': {
        'task': 'realtime.tasks.fetch_radar_images',
        'schedule': timedelta(seconds=240),
        'args': ()
    },
    'fetch-weather-forecast': {
        'task': 'realtime.tasks.fetch_weather_forecast',
        'schedule': crontab(minute=0, hour='0,6,12,18'),  # every 6 hours
        'args': ()
    },
    'clean-weather-forecast': {
        'task': 'realtime.tasks.clean_weather_forecast',
        'schedule': crontab(minute=30, hour=0),  # every day 00:30
        'args': ()
    },
    'fetch-airquality-data': {
        'task': 'realtime.tasks.fetch_airquality_data',
        'schedule': timedelta(seconds=500),
        'args': ()
    },
    'clean-airquality-data': {
        'task': 'realtime.tasks.clean_air_quality_data',
        'schedule': crontab(hour=0, minute=10, day_of_week=1),  # every monday morning # noqa
        'args': ()
    },
    'store-airquality-historic-data': {
        'task': 'realtime.tasks.store_air_quality_historic_data',
        'schedule': crontab(minute=20, hour=0),  # every day 00:20
        'args': ()
    },
}
