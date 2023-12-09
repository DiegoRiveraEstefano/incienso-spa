#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py makemigrations user
python manage.py makemigrations blog
python manage.py makemigrations product
python manage.py makemigrations cart
python manage.py makemigrations order
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
gunicorn config.wsgi -w 4 --worker-class gevent -b 0.0.0.0:8000 --chdir=../incienso-spa/
