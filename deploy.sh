#!/bin/sh

git pull

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn djarzeit.wsgi -w 2 -b 127.0.0.1:8999
