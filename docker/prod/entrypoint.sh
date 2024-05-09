#!/bin/sh

# Wait for the database to be ready
/wait-for-it.sh postgress:5432 --timeout=30 --strict -- echo "Postgres is up"

python manage.py collectstatic --no-input
python manage.py migrate

# Start the server
gunicorn --bind 0:8000 --workers 3 app.config.wsgi:application

exec "$@"
