#!/bin/sh

python manage.py makemigrations

# Выполняем миграции
python manage.py migrate

# Запускаем сервер
exec gunicorn 'app.wsgi:application'