from app.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=5)
