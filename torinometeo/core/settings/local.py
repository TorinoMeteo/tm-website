'''This module sets the configuration for a local development

'''
from datetime import timedelta

from .common import * # noqa

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE

# MAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CKEDITOR
CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + 'core/src/vendor/Font-Awesome/scss/font-awesome.css',
    STATIC_URL + 'core/src/scss/styles.css',
    STATIC_URL + 'core/src/css/ckeditor.css']

# DEBUG_TOOLBAR
JQUERY_URL = ''

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
}
