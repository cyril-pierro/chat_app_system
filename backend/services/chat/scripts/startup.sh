#!/bin/bash


python manage.py migrate --pythonpath .
gunicorn --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi -b :8083
