#!/bin/sh
echo 'Run migration'
python3 manage.py migrate
echo 'Collect Static'
python3 manage.py collectstatic --noinput
exec "$@"
