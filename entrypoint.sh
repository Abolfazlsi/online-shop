#!/bin/bash
set -e


python manage.py migrate


python manage.py collectstatic --noinput


exec gunicorn --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-3}" core.wsgi:application