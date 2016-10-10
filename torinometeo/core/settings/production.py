'''This module sets the configuration for a local development

'''
from .common import *

import os

DEBUG = False

ALLOWED_HOSTS = ['ws.torinometeo.org',]

SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SESSION_COOKIE_SECURE = True

STATIC_ROOT = '/home/torinometeo/www/torinometeo/static/'
MEDIA_ROOT = '/home/torinometeo/www/torinometeo/media/'
# CKEDITOR
CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + 'core/css/vendor.min.css',
    STATIC_URL + 'core/css/core.min.css',
    STATIC_URL + 'core/src/css/ckeditor.css']

LOGGING['handlers']['file']['filename'] = here('..', '..', '..', '..', os.path.join('logs', 'debug.log'))
