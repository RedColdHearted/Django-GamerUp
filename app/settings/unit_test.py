from app.settings.dev import *

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': ':memory:',  # in-memory SQLite
   }
}
