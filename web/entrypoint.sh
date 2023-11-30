#!/bin/sh

echo "Collect static files"
python3 manage.py collectstatic --noinput

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Apply database migrations"
python3 manage.py migrate

exec "$@"