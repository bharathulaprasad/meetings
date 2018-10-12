#!/bin/sh

python manage.py makemigrations && \
python manage.py migrate && \
exec gunicorn meetings.wsgi:application --bind 0.0.0.0:8000 --workers 3
