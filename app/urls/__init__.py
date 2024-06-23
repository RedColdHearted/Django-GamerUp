import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('DJANGO_ENV')

if ENVIRONMENT == 'production':
    from app.urls.production import *
else:
    from app.urls.dev import *
