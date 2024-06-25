from app.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=999)
