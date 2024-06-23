import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('DJANGO_ENV')
print('env', ENVIRONMENT)

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .dev import *

print('debug', DEBUG)

