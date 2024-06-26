#!/bin/sh

echo 'yes'| python manage.py flush

python manage.py makemigrations accounts
python manage.py makemigrations posts

# Выполняем миграции
python manage.py migrate

# Запускаем сервер
exec gunicorn 'app.wsgi:application'