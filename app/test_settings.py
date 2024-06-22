from .settings import *

DEBUG = True

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': ':memory:',  # in-memory SQLite
   }
}
