#!/bin/sh

# making migrations
python manage.py makemigrations accounts
python manage.py makemigrations posts

# migrate
python manage.py migrate

# run
exec gunicorn 'app.wsgi:application'