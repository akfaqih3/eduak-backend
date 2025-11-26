from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS Settings for development
CORS_ALLOW_ALL_ORIGINS = True
