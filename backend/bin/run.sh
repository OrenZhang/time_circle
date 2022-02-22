#! /bin/sh

python manage.py migrate
uwsgi --ini /usr/src/time-circle/uwsgi.ini --processes $UWSGI_PROCESSES --threads $UWSGI_THREADS -w wsgi.wsgi:application > /dev/null 2>&1
